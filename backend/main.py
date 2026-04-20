# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="技术文档 API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DocSection(BaseModel):
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    order: int


class DocCategory(BaseModel):
    id: str
    name: str
    icon: str
    description: str


DATA_FILE = Path(__file__).resolve().parent / "data" / "documents.json"
ALLOWED_IMAGE_HOSTS = {"note.youdao.com", "cdn.note.youdao.com"}

DEFAULT_CATEGORIES = [
    {"id": "vue", "name": "Vue.js", "icon": "ri-vuejs-line", "description": "渐进式前端框架"},
    {"id": "fastapi", "name": "FastAPI", "icon": "ri-flashlight-line", "description": "现代 Python Web 框架"},
]

DEFAULT_DOCUMENTS = [
    {
        "id": "vue-intro",
        "title": "Vue 3 核心概念",
        "content": "# Vue 3 核心概念\n\n这是默认文档。导入真实文档后会被替换。",
        "category": "vue",
        "tags": ["默认"],
        "order": 1,
    },
    {
        "id": "fastapi-intro",
        "title": "FastAPI 快速入门",
        "content": "# FastAPI 快速入门\n\n这是默认文档。导入真实文档后会被替换。",
        "category": "fastapi",
        "tags": ["默认"],
        "order": 2,
    },
]


def load_documents() -> tuple[list[dict], list[dict]]:
    if not DATA_FILE.exists():
        return DEFAULT_CATEGORIES, DEFAULT_DOCUMENTS

    try:
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return DEFAULT_CATEGORIES, DEFAULT_DOCUMENTS

    categories = payload.get("categories", [])
    documents = payload.get("documents", [])
    if not isinstance(categories, list) or not isinstance(documents, list):
        return DEFAULT_CATEGORIES, DEFAULT_DOCUMENTS

    return categories, documents


_DATA_LOCK = Lock()
_CATEGORIES: list[dict] = []
_DOCUMENTS: list[dict] = []
_DATA_MTIME_NS: int | None = None


def get_live_documents(force_reload: bool = False) -> tuple[list[dict], list[dict]]:
    global _CATEGORIES, _DOCUMENTS, _DATA_MTIME_NS

    try:
        current_mtime = DATA_FILE.stat().st_mtime_ns
    except OSError:
        current_mtime = None

    with _DATA_LOCK:
        should_reload = force_reload or not _CATEGORIES or not _DOCUMENTS or current_mtime != _DATA_MTIME_NS
        if should_reload:
            categories, documents = load_documents()
            _CATEGORIES = categories
            _DOCUMENTS = documents
            _DATA_MTIME_NS = current_mtime

        return _CATEGORIES, _DOCUMENTS


get_live_documents(force_reload=True)


@app.get("/")
async def root():
    return {
        "message": "技术文档 API",
        "version": app.version,
        "data_file": str(DATA_FILE),
        "endpoints": {
            "categories": "/api/categories",
            "documents": "/api/documents",
            "document": "/api/documents/{doc_id}",
            "search": "/api/search?q={query}",
        },
    }


@app.get("/api/categories", response_model=List[DocCategory])
async def get_categories():
    categories, _ = get_live_documents()
    return categories


@app.get("/api/documents")
async def get_documents(category: Optional[str] = None):
    _, documents = get_live_documents()
    if category:
        return [doc for doc in documents if doc.get("category") == category]
    return documents


@app.get("/api/documents/{doc_id}")
async def get_document(doc_id: str):
    _, documents = get_live_documents()
    doc = next((doc for doc in documents if doc.get("id") == doc_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="文档未找到")
    return doc


@app.get("/api/search")
async def search_documents(q: str):
    if not q:
        return []

    _, documents = get_live_documents()
    q_lower = q.lower()
    results = []
    for doc in documents:
        title = str(doc.get("title", "")).lower()
        content = str(doc.get("content", "")).lower()
        tags = [str(tag).lower() for tag in doc.get("tags", [])]
        if q_lower in title or q_lower in content or any(q_lower in tag for tag in tags):
            results.append(doc)

    return results


@app.get("/api/image-proxy")
async def image_proxy(url: str = Query(..., description="Remote image url")):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise HTTPException(status_code=400, detail="Unsupported URL scheme")
    if parsed.hostname not in ALLOWED_IMAGE_HOSTS:
        raise HTTPException(status_code=400, detail="Host is not allowed")

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=25) as resp:
            content_type = resp.headers.get("Content-Type", "application/octet-stream")
            body = resp.read()
    except (HTTPError, URLError) as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch image: {exc}") from exc

    if not content_type.startswith("image/"):
        raise HTTPException(status_code=502, detail=f"Upstream is not an image: {content_type}")

    return Response(
        content=body,
        media_type=content_type.split(";")[0],
        headers={"Cache-Control": "public, max-age=86400"},
    )


if __name__ == "__main__":
    print("启动 FastAPI 服务...")
    print("API 文档: http://localhost:8000/docs")
    print("ReDoc 文档: http://localhost:8000/redoc")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
