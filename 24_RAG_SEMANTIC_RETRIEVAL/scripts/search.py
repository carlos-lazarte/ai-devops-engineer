#!/usr/bin/env python3
"""Minimal semantic search client for the prototype index."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install sentence-transformers before running this script.") from exc


def load_chunks(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default="all-MiniLM-L6-v2")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--technology")
    args = parser.parse_args()

    rows = load_chunks(args.index / "chunks.jsonl")
    vectors = np.load(args.index / "vectors.npy")
    model = SentenceTransformer(args.model)
    q = model.encode([args.query], normalize_embeddings=True)[0].astype(np.float32)
    scores = vectors @ q

    allowed = np.ones(len(rows), dtype=bool)
    for i, row in enumerate(rows):
        if args.technology and row.get("metadata", {}).get("technology") != args.technology:
            allowed[i] = False

    candidates = np.where(allowed)[0]
    ranked = candidates[np.argsort(scores[candidates])[::-1][:args.top_k]]

    results = []
    for idx in ranked:
        row = rows[int(idx)].copy()
        row["score"] = float(scores[int(idx)])
        results.append(row)

    print(json.dumps({"query": args.query, "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
