#!/usr/bin/env python3
"""Minimal local-first RAG index builder for Markdown files.

Prototype only. It stores an SQLite metadata table and vectors in NumPy.
An embedding provider can later be replaced without changing the note format.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install sentence-transformers before running this script.") from exc


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sqlite_text(value: object) -> str | None:
    """Convert frontmatter values to SQLite TEXT-compatible values.

    Frontmatter fields may be scalars or YAML-style lists. SQLite's Python
    adapter accepts scalar primitives, but not list/dict objects directly.
    Complex values are stored as JSON text to preserve their structure.
    """
    if value is None:
        return None
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 4:]
    metadata: dict[str, object] = {}
    current_list = None
    for line in raw.splitlines():
        if line.startswith("  - ") and current_list:
            metadata.setdefault(current_list, []).append(line[4:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip().strip('"')
        if value == "":
            metadata[key] = []
            current_list = key
        else:
            metadata[key] = value
            current_list = None
    return metadata, body.lstrip()


def chunks_for_note(path: Path, text: str, max_chars: int, overlap: int) -> Iterable[dict]:
    metadata, body = parse_frontmatter(text)
    title = path.stem
    headings = list(re.finditer(r"(?m)^#{1,3} .+$", body))
    sections = []
    if not headings:
        sections = [("", body)]
    else:
        for i, match in enumerate(headings):
            heading = match.group(0).lstrip("# ").strip()
            start = match.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
            sections.append((heading, body[start:end].strip()))

    ordinal = 0
    for heading, section in sections:
        if not section:
            continue
        prefix = f"# {title}\n## {heading}\n" if heading else f"# {title}\n"
        text_block = prefix + section
        if len(text_block) <= max_chars:
            payloads = [text_block]
        else:
            payloads = []
            step = max(1, max_chars - overlap)
            for start in range(0, len(text_block), step):
                piece = text_block[start:start + max_chars]
                if piece:
                    payloads.append(piece)
        for piece in payloads:
            ordinal += 1
            yield {
                "chunk_id": sha256(f"{path.as_posix()}|{heading}|{ordinal}"),
                "source_path": path.as_posix(),
                "title": title,
                "heading": heading,
                "content": piece,
                "metadata": metadata,
                "ordinal": ordinal,
            }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--model", default="all-MiniLM-L6-v2")
    parser.add_argument("--max-chars", type=int, default=3500)
    parser.add_argument("--overlap", type=int, default=350)
    args = parser.parse_args()

    args.index.mkdir(parents=True, exist_ok=True)
    db_path = args.index / "metadata.sqlite3"
    vectors_path = args.index / "vectors.npy"
    chunks_path = args.index / "chunks.jsonl"

    model = SentenceTransformer(args.model)
    rows = []
    vectors = []

    for path in sorted(args.vault.rglob("*.md")):
        if "/.obsidian/" in path.as_posix():
            continue
        text = path.read_text(encoding="utf-8")
        for chunk in chunks_for_note(path.relative_to(args.vault), text, args.max_chars, args.overlap):
            rows.append(chunk)

    if not rows:
        raise SystemExit("No Markdown notes found.")

    embeddings = model.encode([row["content"] for row in rows], normalize_embeddings=True)
    vectors = np.asarray(embeddings, dtype=np.float32)
    np.save(vectors_path, vectors)

    with chunks_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS chunks")
        conn.execute(
            """CREATE TABLE chunks (
                rowid INTEGER PRIMARY KEY,
                chunk_id TEXT UNIQUE,
                source_path TEXT,
                heading TEXT,
                ordinal INTEGER,
                type TEXT,
                domain TEXT,
                technology TEXT,
                status TEXT
            )"""
        )
        for idx, row in enumerate(rows):
            md = row["metadata"]
            conn.execute(
                "INSERT INTO chunks(rowid,chunk_id,source_path,heading,ordinal,type,domain,technology,status) VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    idx,
                    row["chunk_id"],
                    row["source_path"],
                    row["heading"],
                    row["ordinal"],
                    sqlite_text(md.get("type")),
                    sqlite_text(md.get("domain")),
                    sqlite_text(md.get("technology")),
                    sqlite_text(md.get("status")),
                ),
            )
        conn.commit()

    manifest = {
        "embedding_model": args.model,
        "chunk_count": len(rows),
        "vault": str(args.vault),
    }
    (args.index / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
