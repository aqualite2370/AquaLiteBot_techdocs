from __future__ import annotations

import json
import re
from pathlib import Path


DATA_PATH = Path("backend/data/documents.json")
BACKUP_PATH = Path("backend/data/documents.pre_rewrite_backup.json")


NOISE_LINES = {
    "如图",
    "如下图",
    "如下图示例",
    "见下图",
    "如下",
    "！",
    "!",
    "--",
    "---",
    "----",
    "+++++++++++++++++++++++++++",
    "+++++++++++++++",
}

NOTE_KEYWORDS = [
    "注意",
    "仅限",
    "建议",
    "无法",
    "失效",
    "风控",
    "私聊",
    "安全",
    "概率",
    "随机",
    "解散",
    "弃用",
    "公告",
    "权限",
]

COMMAND_HINTS = [
    "发送",
    "输入",
    "键入",
    "触发方式",
    "命令",
    "指令",
    "用法",
    "使用方法",
    "前缀",
]


def normalize_spaces(text: str) -> str:
    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_md_prefix(line: str) -> str:
    text = line.strip()
    text = re.sub(r"^#{1,6}\s*", "", text)
    text = re.sub(r"^[-*+]\s+", "", text)
    text = re.sub(r"^\d+\.\s+", "", text)
    text = re.sub(r"^>\s*", "", text)
    text = text.replace("**", "").replace("`", "")
    text = text.replace("“", '"').replace("”", '"')
    return normalize_spaces(text)


def normalize_sentence(text: str) -> str:
    text = strip_md_prefix(text)
    text = text.strip("，,；; ")
    if not text:
        return ""
    if re.search(r"[\u4e00-\u9fff]", text) and text[-1] not in "。！？":
        text += "。"
    return text


def is_image_line(line: str) -> bool:
    return bool(re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", line.strip()))


def is_link_only(line: str) -> bool:
    return bool(re.match(r"^https?://\S+$", strip_md_prefix(line), flags=re.I))


def extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s)]+", text)


def looks_like_separator(text: str) -> bool:
    if text in NOISE_LINES:
        return True
    return bool(re.fullmatch(r"[#\-_=*~\s]{3,}", text))


def has_slash_command(text: str) -> bool:
    return bool(re.search(r"(^|[\s(（])/[A-Za-z][\w-]*", text))


def looks_like_command(line: str) -> bool:
    text = strip_md_prefix(line)
    if not text:
        return False
    if text.startswith("!["):
        return False
    if re.match(r"^https?://", text, flags=re.I):
        return False
    if has_slash_command(text):
        return True
    if re.match(r"^(er\S+|jm\[[^\]]+\]|bili\[[^\]]+\]|code\s+\S+)", text, flags=re.I):
        return True
    if any(k in text for k in COMMAND_HINTS) and re.search(r"[/A-Za-z0-9\[\]#@]", text):
        return True
    if "点歌" in text and "/" in text:
        return True
    if "解析" in text and ("/" in text or "bili" in text.lower()):
        return True
    return False


def split_by_feature(text: str) -> tuple[str, str]:
    for sep in [" 以", " 即可", " 可", " 来", " 用于", " 并"]:
        idx = text.find(sep)
        if idx > 0:
            left = text[:idx].strip(" ：:")
            right = text[idx + len(sep) :].strip(" ：:")
            if left and right and (has_slash_command(left) or any(k in left for k in COMMAND_HINTS)):
                return left, right

    verb_match = re.match(
        r"^(.{1,80}?)(创建|删除|查看|获取|推送|绑定|查询|下载|解析|参与|签到|点歌|随机|运行|制作|搜索|返回|合成|抽奖|禁言)(.+)$",
        text,
    )
    if verb_match:
        cmd = verb_match.group(1).strip()
        feat = f"{verb_match.group(2)}{verb_match.group(3).strip()}"
        if cmd:
            return cmd, feat

    return text, ""


def parse_command_feature(line: str, fallback_feature: str) -> tuple[str, str]:
    text = strip_md_prefix(line)
    text = re.sub(r'^"|"$', "", text).strip()

    m = re.match(r"^(发送|输入|键入|触发方式|使用方法|用法|指令(?:如下)?|命令(?:如下)?)[：:]?\s*(.+)$", text)
    body = m.group(2).strip() if m else text

    body = re.sub(r"^如[:：]\s*", "", body)
    body = re.sub(r"^例[:：]\s*", "", body)
    body = body.strip()

    cmd, feat = split_by_feature(body)
    cmd = normalize_spaces(re.sub(r"\s*(以|来|即可|并)$", "", cmd))
    feat = normalize_sentence(feat) if feat else ""
    feat = normalize_sentence(re.sub(r"^(以|来|用于|可)\s*", "", feat)) if feat else ""

    if "均可作为命令前缀触发" in text:
        feat = "支持以下前缀触发同一功能。"
        cmd = normalize_spaces(text.replace("均可作为命令前缀触发", "").strip(" ：:"))

    if not feat:
        feat = fallback_feature or "执行对应功能。"

    if cmd:
        return feat, cmd
    return "", ""


def dedup_keep_order(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        key = item.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def rewrite_content(title: str, content: str) -> str:
    lines = [ln.rstrip() for ln in str(content or "").replace("\r\n", "\n").split("\n")]

    desc: list[str] = []
    notes: list[str] = []
    links: list[str] = []
    images: list[str] = []
    commands: list[tuple[str, str]] = []

    last_desc = ""

    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue

        if is_image_line(stripped):
            images.append(stripped)
            continue

        clean = strip_md_prefix(stripped)
        if not clean:
            continue
        if clean == title:
            continue
        if looks_like_separator(clean):
            continue

        extracted_urls = extract_urls(clean)
        if is_link_only(clean):
            links.append(clean)
            continue

        if looks_like_command(clean):
            feat, cmd = parse_command_feature(clean, last_desc)
            if cmd:
                commands.append((feat, cmd))
            continue

        if extracted_urls:
            for url in extracted_urls:
                links.append(url)
            clean = re.sub(r"https?://[^\s)]+", "", clean).strip(" ：:，,")
            if not clean:
                continue

        sentence = normalize_sentence(clean)
        if not sentence:
            continue

        if any(k in sentence for k in NOTE_KEYWORDS):
            notes.append(sentence)
        else:
            desc.append(sentence)
            last_desc = sentence

    desc = dedup_keep_order(desc)
    notes = dedup_keep_order(notes)
    links = dedup_keep_order(links)

    normalized_commands: list[tuple[str, str]] = []
    seen_cmd: set[tuple[str, str]] = set()
    for feat, cmd in commands:
        cmd = normalize_spaces(cmd)
        feat = normalize_sentence(feat) or "执行对应功能。"
        key = (feat, cmd)
        if not cmd or key in seen_cmd:
            continue
        seen_cmd.add(key)
        normalized_commands.append((feat, cmd))

    parts: list[str] = [f"# {title}", "", "## 描述"]

    if desc:
        parts.extend([f"- {item}" for item in desc])
    else:
        parts.append("- 请参考下方使用说明与示例内容。")

    if normalized_commands:
        parts.extend(["", "## 使用", "```"])
        for idx, (feat, cmd) in enumerate(normalized_commands, start=1):
            parts.append(f"[{idx}]")
            parts.append(f"功能说明: {feat}")
            parts.append(f"触发命令: {cmd}")
            parts.append("")
        if parts[-1] == "":
            parts.pop()
        parts.append("```")

    if notes:
        parts.extend(["", "## 注意"])
        parts.extend([f"- {item}" for item in notes])

    if links:
        parts.extend(["", "## 参考链接"])
        parts.extend([f"- {url}" for url in links])

    if images:
        parts.extend(["", "## 示例", ""])
        for img in images:
            parts.append(img)
            parts.append("")
        if parts[-1] == "":
            parts.pop()

    return "\n".join(parts).strip() + "\n"


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    if not BACKUP_PATH.exists():
        BACKUP_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    rewritten = 0
    for doc in payload.get("documents", []):
        old = doc.get("content", "")
        new = rewrite_content(doc.get("title", "未命名文档"), old)
        if new != old:
            doc["content"] = new
            rewritten += 1

    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"rewritten_docs={rewritten}")
    print(f"backup={BACKUP_PATH}")


if __name__ == "__main__":
    main()
