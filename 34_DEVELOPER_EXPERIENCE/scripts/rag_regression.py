#!/usr/bin/env python3
"""Minimal RAG regression harness using the local index/search scripts."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import yaml


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--index", type=Path, default=Path(".rag-index"))
    args = ap.parse_args()
    root = args.root.resolve()
    eval_file = root / "24_RAG_SEMANTIC_RETRIEVAL/evaluation/evaluation-set.yaml"
    data = yaml.safe_load(eval_file.read_text(encoding="utf-8")) or {}
    cases = data if isinstance(data, list) else data.get("queries", data.get("cases", []))
    if not cases:
        print("No evaluation cases found", file=sys.stderr)
        return 2
    search = root / "24_RAG_SEMANTIC_RETRIEVAL/scripts/search.py"
    failures = []
    for case in cases:
        query = case.get("query", "")
        expected = [str(x) for x in case.get("expected_sources", case.get("expected_notes", case.get("expected", [])))]
        proc = subprocess.run(
            [sys.executable, str(search), "--index", str(args.index), "--query", query],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            failures.append({"query": query, "reason": proc.stderr.strip()})
            continue
        payload = json.loads(proc.stdout)
        hits = payload.get("results", []) if isinstance(payload, dict) else payload
        hit_paths = {str(h.get("source_path", h.get("path", ""))) for h in hits if isinstance(h, dict)}
        if expected and not any(any(Path(e).as_posix() == Path(h).as_posix() or Path(e).name == Path(h).name for h in hit_paths) for e in expected):
            failures.append({"query": query, "expected": expected, "hits": sorted(hit_paths)})
    print(f"evaluated={len(cases)} failures={len(failures)}")
    if failures:
        for item in failures:
            print(json.dumps(item, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
