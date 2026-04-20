#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

BASE_URL = "https://note.youdao.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CodexImporter/1.0"
ROOT_CATEGORY_ID = "root"

ICON_RULES = [
    (("音游", "舞萌", "phigros", "arcaea", "osu"), "ri-music-2-line"),
    (("娱乐", "杂项", "表情", "抽奖"), "ri-gamepad-line"),
    (("实用", "工具", "计算", "解析"), "ri-tools-line"),
    (("指令", "必读", "说明"), "ri-book-open-line"),
    (("相关", "过去", "信息"), "ri-information-line"),
]
FALLBACK_ICONS = [
    "ri-folder-3-line",
    "ri-folder-open-line",
    "ri-book-2-line",
    "ri-file-list-3-line",
    "ri-stack-line",
]


def decode_response_bytes(raw: bytes, declared_charset: str | None = None) -> str:
    candidates = [declared_charset, "utf-8", "utf-8-sig", "gb18030"]
    seen: set[str] = set()
    for charset in candidates:
        if not charset:
            continue
        key = charset.lower()
        if key in seen:
            continue
        seen.add(key)
        try:
            return raw.decode(charset)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def request_json(url: str, retries: int = 3, timeout: int = 30) -> Any:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                declared_charset = resp.headers.get_content_charset()
            body = decode_response_bytes(raw, declared_charset)
            return json.loads(body)
        except (OSError, ValueError, json.JSONDecodeError, HTTPError, URLError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(0.55 * attempt)
    raise RuntimeError(f"Failed to fetch JSON after {retries} attempts: {url}") from last_error


def parse_share_key(value: str) -> str:
    if re.fullmatch(r"[0-9a-fA-F]{32}", value):
        return value.lower()

    parsed = urlparse(value)
    query = parse_qs(parsed.query)
    share_id = query.get("id", [""])[0]
    if re.fullmatch(r"[0-9a-fA-F]{32}", share_id):
        return share_id.lower()
    raise ValueError("Unable to parse share key from input. Provide full share URL or 32-char id.")


def normalize_title(raw_title: str) -> str:
    title = (raw_title or "").strip()
    if title.lower().endswith(".note"):
        title = title[:-5]
    return title.strip() or "Untitled"


def choose_icon(category_name: str, index: int) -> str:
    lower_name = category_name.lower()
    for keywords, icon in ICON_RULES:
        if any(keyword.lower() in lower_name for keyword in keywords):
            return icon
    return FALLBACK_ICONS[index % len(FALLBACK_ICONS)]


def fetch_tree(share_key: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    folder_map: dict[str, dict[str, Any]] = {}
    notes: list[dict[str, Any]] = []
    queue: list[str | None] = [None]
    visited: set[str] = set()

    while queue:
        folder_id = queue.pop(0)
        if folder_id:
            if folder_id in visited:
                continue
            visited.add(folder_id)
            url = f"{BASE_URL}/yws/public/notebook/{share_key}/subdir/{folder_id}"
        else:
            url = f"{BASE_URL}/yws/public/notebook/{share_key}"

        payload = request_json(url)
        items = payload[2] if isinstance(payload, list) and len(payload) >= 3 else []

        for item in items:
            if not isinstance(item, dict):
                continue
            path = str(item.get("p", "")).strip("/")
            entry_id = path.split("/")[-1] if path else ""
            if not entry_id:
                continue

            domain = int(item.get("domain", 0))
            title = str(item.get("tl", ""))
            if domain == 1:
                folder_map[entry_id] = {
                    "id": entry_id,
                    "name": normalize_title(title),
                    "parent_id": folder_id,
                }
                queue.append(entry_id)
                continue

            notes.append(
                {
                    "id": entry_id,
                    "title": normalize_title(title),
                    "parent_folder_id": folder_id,
                    "path": "/" + path,
                    "created_at": int(item.get("ct", 0) or 0),
                    "updated_at": int(item.get("mt", 0) or 0),
                    "size": int(item.get("sz", 0) or 0),
                }
            )

    return folder_map, notes


def format_segment_text(segment: dict[str, Any]) -> str:
    text = str(segment.get("8", ""))
    marks = segment.get("9") or []
    mark_types = set()
    for mark in marks:
        if isinstance(mark, dict):
            mark_type = mark.get("2")
            if isinstance(mark_type, str):
                mark_types.add(mark_type)

    if "b" in mark_types and text.strip():
        return f"**{text}**"
    return text


def block_text(block: dict[str, Any]) -> str:
    parts: list[str] = []
    for span in block.get("5", []):
        if not isinstance(span, dict):
            continue

        segments = span.get("7")
        if isinstance(segments, list):
            for segment in segments:
                if isinstance(segment, dict):
                    parts.append(format_segment_text(segment))
            continue

        if "8" in span:
            parts.append(str(span.get("8", "")))

    return "".join(parts).replace("\r\n", "\n").replace("\r", "\n")


def markdown_from_note(note_title: str, note_content_json: str) -> str:
    if not note_content_json:
        return f"# {note_title}\n"

    try:
        parsed = json.loads(note_content_json)
    except json.JSONDecodeError:
        plain = note_content_json.strip()
        return f"# {note_title}\n\n{plain}\n" if plain else f"# {note_title}\n"

    blocks = parsed.get("5", [])
    output_lines: list[str] = []

    for block in blocks:
        if not isinstance(block, dict):
            continue

        block_type = str(block.get("6", "p") or "p")
        attrs = block.get("4") if isinstance(block.get("4"), dict) else {}
        text = block_text(block).strip("\n")

        if block_type == "h":
            if not text.strip():
                continue
            level = str(attrs.get("l", "h2"))
            depth = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}.get(level, 2)
            output_lines.append(f"{'#' * depth} {text.strip()}")
            output_lines.append("")
            continue

        if block_type == "im":
            image_url = str(attrs.get("u", "")).strip()
            if image_url:
                if image_url.startswith("http://"):
                    image_url = "https://" + image_url[len("http://") :]
                output_lines.append(f"![image]({image_url})")
                output_lines.append("")
            continue

        if block_type == "l":
            if not text.strip():
                continue
            ordered = str(attrs.get("lt", "")).lower() == "ordered"
            prefix = "1. " if ordered else "- "
            for line in text.splitlines():
                line = line.strip()
                if line:
                    output_lines.append(prefix + line)
            output_lines.append("")
            continue

        if not text.strip():
            output_lines.append("")
            continue

        for line in text.splitlines():
            output_lines.append(line.rstrip())
        output_lines.append("")

    markdown = "\n".join(output_lines)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    if not markdown:
        return f"# {note_title}\n"
    if not markdown.startswith("#"):
        return f"# {note_title}\n\n{markdown}\n"
    return markdown + "\n"


def fetch_note_body(share_key: str, note_id: str, unlogin_id: str) -> str:
    url = (
        f"{BASE_URL}/yws/api/note/{share_key}/{note_id}"
        f"?sev=j1&editorType=1&editorVersion=new-json-editor&unloginId={unlogin_id}"
    )
    payload = request_json(url)
    if isinstance(payload, dict):
        return str(payload.get("content", "") or "")
    return ""


def epoch_to_iso(epoch_seconds: int) -> str:
    if epoch_seconds <= 0:
        return ""
    return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).isoformat()


def build_payload(share_key: str, source_url: str) -> dict[str, Any]:
    folder_map, notes = fetch_tree(share_key)
    unlogin_id = uuid.uuid4().hex

    used_category_ids: set[str] = set()
    documents: list[dict[str, Any]] = []

    for note in sorted(notes, key=lambda item: (-item["updated_at"], item["title"].lower(), item["id"])):
        folder_id = note["parent_folder_id"] if note["parent_folder_id"] in folder_map else ROOT_CATEGORY_ID
        used_category_ids.add(folder_id)

        raw_content = fetch_note_body(share_key, note["id"], unlogin_id)
        markdown = markdown_from_note(note["title"], raw_content)
        category_name = folder_map[folder_id]["name"] if folder_id in folder_map else "根目录"

        documents.append(
            {
                "id": note["id"],
                "title": note["title"],
                "content": markdown,
                "category": folder_id,
                "tags": [category_name, "有道迁移"],
                "order": len(documents) + 1,
                "source": {
                    "path": note["path"],
                    "created_at": epoch_to_iso(note["created_at"]),
                    "updated_at": epoch_to_iso(note["updated_at"]),
                    "size": note["size"],
                },
            }
        )

    categories: list[dict[str, Any]] = []
    ordered_category_ids: list[str] = []
    if ROOT_CATEGORY_ID in used_category_ids:
        ordered_category_ids.append(ROOT_CATEGORY_ID)
    ordered_category_ids.extend(
        sorted([cid for cid in used_category_ids if cid != ROOT_CATEGORY_ID], key=lambda cid: folder_map[cid]["name"])
    )

    for index, category_id in enumerate(ordered_category_ids):
        if category_id == ROOT_CATEGORY_ID:
            name = "根目录"
            description = "有道云笔记根目录下的文档"
        else:
            name = folder_map[category_id]["name"]
            description = f"有道云笔记文件夹：{name}"

        categories.append(
            {
                "id": category_id,
                "name": name,
                "icon": choose_icon(name, index),
                "description": description,
            }
        )

    return {
        "source": {
            "provider": "youdao-share",
            "share_key": share_key,
            "share_url": source_url,
            "migrated_at": datetime.now(timezone.utc).isoformat(),
        },
        "categories": categories,
        "documents": documents,
    }


def load_existing_doc_count(output_path: Path) -> int:
    if not output_path.exists():
        return 0
    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    docs = payload.get("documents", [])
    return len(docs) if isinstance(docs, list) else 0


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    categories = payload.get("categories")
    documents = payload.get("documents")

    if not isinstance(categories, list):
        return ["payload.categories is not a list"]
    if not isinstance(documents, list):
        return ["payload.documents is not a list"]
    if not categories:
        errors.append("categories is empty")
    if not documents:
        errors.append("documents is empty")

    cat_ids: set[str] = set()
    for idx, category in enumerate(categories):
        if not isinstance(category, dict):
            errors.append(f"category[{idx}] is not an object")
            continue
        cid = str(category.get("id", "")).strip()
        name = str(category.get("name", "")).strip()
        if not cid:
            errors.append(f"category[{idx}] has empty id")
        if cid in cat_ids:
            errors.append(f"duplicate category id: {cid}")
        cat_ids.add(cid)
        if not name:
            errors.append(f"category[{idx}] has empty name")

    doc_ids: set[str] = set()
    for idx, doc in enumerate(documents):
        if not isinstance(doc, dict):
            errors.append(f"document[{idx}] is not an object")
            continue
        did = str(doc.get("id", "")).strip()
        title = str(doc.get("title", "")).strip()
        content = str(doc.get("content", ""))
        category = str(doc.get("category", "")).strip()
        if not did:
            errors.append(f"document[{idx}] has empty id")
        if did in doc_ids:
            errors.append(f"duplicate document id: {did}")
        doc_ids.add(did)
        if not title:
            errors.append(f"document[{idx}] has empty title")
        if not content.strip():
            errors.append(f"document[{idx}] has empty content")
        if category and cat_ids and category not in cat_ids:
            errors.append(f"document[{idx}] points to unknown category: {category}")
        if "\x00" in content:
            errors.append(f"document[{idx}] contains NUL byte")

    return errors


def write_json_atomic(output_path: Path, payload: dict[str, Any], backup_enabled: bool = True) -> Path | None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    backup_path: Path | None = None

    if backup_enabled and output_path.exists():
        backup_dir = output_path.parent / "_sync_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{output_path.stem}.{stamp}{output_path.suffix}"
        backup_path.write_bytes(output_path.read_bytes())

    temp_path = output_path.with_suffix(f"{output_path.suffix}.tmp")
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    temp_path.write_text(serialized, encoding="utf-8")
    temp_path.replace(output_path)
    return backup_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a Youdao share notebook into backend/data/documents.json")
    parser.add_argument("source", help="Youdao share URL or share id")
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[1] / "data" / "documents.json"),
        help="Output JSON path",
    )
    parser.add_argument("--min-docs", type=int, default=1, help="Minimum imported document count required to write")
    parser.add_argument(
        "--min-ratio",
        type=float,
        default=0.35,
        help="Required ratio vs existing docs (ignored when existing file missing). Range 0-1",
    )
    parser.add_argument("--no-backup", action="store_true", help="Disable timestamp backup before overwrite")
    parser.add_argument("--force", action="store_true", help="Write output even if sanity checks fail")
    args = parser.parse_args()

    share_key = parse_share_key(args.source)
    output_path = Path(args.output).resolve()
    existing_docs = load_existing_doc_count(output_path)
    payload = build_payload(share_key, args.source)

    validation_errors = validate_payload(payload)
    imported_docs = len(payload.get("documents", []))
    imported_categories = len(payload.get("categories", []))
    dynamic_min_docs = max(args.min_docs, int(existing_docs * max(0.0, min(args.min_ratio, 1.0))))
    count_guard_ok = imported_docs >= dynamic_min_docs

    if (validation_errors or not count_guard_ok) and not args.force:
        details = []
        if validation_errors:
            details.append("validation failed: " + "; ".join(validation_errors[:8]))
        if not count_guard_ok:
            details.append(
                f"doc count guard failed: imported={imported_docs}, required>={dynamic_min_docs}, existing={existing_docs}"
            )
        raise RuntimeError(" | ".join(details))

    backup_path = write_json_atomic(output_path, payload, backup_enabled=not args.no_backup)

    try:
        json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Output file verification failed: {output_path}") from exc

    print(f"Imported {imported_docs} notes into {output_path}")
    print(f"Categories: {imported_categories}")
    print(f"Existing docs before sync: {existing_docs}")
    print(f"Doc count guard threshold: {dynamic_min_docs}")
    if backup_path:
        print(f"Backup saved: {backup_path}")
    if validation_errors:
        print(f"Validation warnings (forced write): {'; '.join(validation_errors[:8])}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Import canceled.", file=sys.stderr)
        raise SystemExit(130)
