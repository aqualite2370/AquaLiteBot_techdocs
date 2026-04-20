from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT_DIR / "backend" / "data" / "documents.json"
DEFAULT_TARGET = ROOT_DIR / "frontend" / "public" / "data" / "documents.json"


def validate_json_file(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON file: {path}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync backend documents.json to frontend public data directory")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Source JSON path")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Target JSON path")
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    target_path = Path(args.target).resolve()

    payload = validate_json_file(source_path)
    documents = payload.get("documents", [])
    categories = payload.get("categories", [])
    if not isinstance(documents, list) or not isinstance(categories, list):
        raise RuntimeError("Source JSON must contain categories/documents arrays")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    validate_json_file(target_path)

    print(f"Synced frontend data: {source_path} -> {target_path}")
    print(f"Categories: {len(categories)} | Documents: {len(documents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
