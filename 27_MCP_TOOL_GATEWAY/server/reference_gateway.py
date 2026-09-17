#!/usr/bin/env python3
"""Local, read-only MCP-shaped reference gateway for the Obsidian Vault."""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any

TOOLS = {
    "search_notes": {"access": "read"},
    "read_note": {"access": "read"},
    "list_related_notes": {"access": "read"},
    "retrieve_runbook": {"access": "read"},
}
MAX_RESULTS = 20
MAX_NOTE_BYTES = 100_000
MAX_QUERY = 500


def req_id() -> str:
    return f"req-{uuid.uuid4().hex[:12]}"


def rel_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def safe_note_path(root: Path, note_id: str) -> Path:
    if not note_id or "\x00" in note_id:
        raise ValueError("invalid_note_id")
    p = (root / note_id).resolve()
    if p != root and root not in p.parents:
        raise ValueError("path_escape")
    if p.suffix != ".md":
        raise ValueError("not_markdown")
    if not p.is_file():
        raise FileNotFoundError("note_not_found")
    if p.stat().st_size > MAX_NOTE_BYTES:
        raise ValueError("note_too_large")
    return p


def note_title(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else fallback


def notes(root: Path):
    for p in root.rglob("*.md"):
        if any(part in {".git", ".obsidian"} for part in p.parts):
            continue
        yield p


def search_notes(root: Path, query: str, limit: int) -> dict[str, Any]:
    if len(query) > MAX_QUERY:
        raise ValueError("query_too_long")
    terms = [t.lower() for t in query.split() if t.strip()]
    hits = []
    for p in notes(root):
        text = p.read_text(encoding="utf-8", errors="replace")
        low = text.lower()
        title_guess = note_title(text, p.stem).lower()
        path_low = rel_path(p, root).lower()
        score = (sum(title_guess.count(t) for t in terms) * 8) + (sum(path_low.count(t) for t in terms) * 3) + sum(low.count(t) for t in terms)
        if terms and score == 0:
            continue
        title = note_title(text, p.stem)
        snippet = " ".join(text.strip().split())[:280]
        hits.append((score, rel_path(p, root), title, snippet))
    hits.sort(key=lambda x: (-x[0], x[1]))
    truncated = len(hits) > min(limit, MAX_RESULTS)
    results = [
        {"note_id": path, "path": path, "title": title, "snippet": snippet, "provenance": path}
        for _, path, title, snippet in hits[: min(limit, MAX_RESULTS)]
    ]
    return {"results": results, "truncated": truncated}


def read_note(root: Path, note_id: str) -> dict[str, Any]:
    p = safe_note_path(root, note_id)
    text = p.read_text(encoding="utf-8", errors="replace")
    return {
        "note_id": rel_path(p, root),
        "title": note_title(text, p.stem),
        "content": text,
        "provenance": [rel_path(p, root)],
    }


def links(text: str) -> list[str]:
    return sorted(set(re.findall(r"\[\[([^\]|#]+)", text)))


def resolve_link(root: Path, source: Path, target: str) -> Path | None:
    candidates = [
        root / f"{target}.md",
        source.parent / f"{target}.md",
        root / target,
    ]
    for c in candidates:
        try:
            p = c.resolve()
            if p.is_file() and p.suffix == ".md" and (p == root or root in p.parents):
                return p
        except OSError:
            pass
    for p in notes(root):
        if p.stem == Path(target).stem:
            return p
    return None


def list_related_notes(root: Path, note_id: str, depth: int) -> dict[str, Any]:
    if not 1 <= depth <= 2:
        raise ValueError("invalid_depth")
    start = safe_note_path(root, note_id)
    seen = {rel_path(start, root)}
    frontier = [start]
    related = []
    for _ in range(depth):
        nxt = []
        for src in frontier:
            text = src.read_text(encoding="utf-8", errors="replace")
            for target in links(text):
                p = resolve_link(root, src, target)
                if not p:
                    continue
                rp = rel_path(p, root)
                if rp in seen:
                    continue
                seen.add(rp)
                related.append({"note_id": rp, "title": note_title(p.read_text(encoding="utf-8", errors="replace"), p.stem), "provenance": rp})
                nxt.append(p)
        frontier = nxt
    return {"results": related[:20], "truncated": len(related) > 20}


def retrieve_runbook(root: Path, problem: str, technology: str | None, limit: int) -> dict[str, Any]:
    query = " ".join(x for x in [problem, technology or ""] if x).lower()
    terms = [t for t in query.split() if t]
    hits = []
    for p in notes(root):
        rp = rel_path(p, root)
        text = p.read_text(encoding="utf-8", errors="replace")
        if "17_RUNBOOKS" not in rp and "type: runbook" not in text.lower():
            continue
        low = (rp + " " + text).lower()
        score = sum(low.count(t) for t in terms)
        if score:
            hits.append((score, rp, note_title(text, p.stem)))
    hits.sort(key=lambda x: (-x[0], x[1]))
    truncated = len(hits) > min(limit, 10)
    return {"results": [{"note_id": rp, "title": title, "provenance": [rp]} for _, rp, title in hits[: min(limit, 10)]], "truncated": truncated}


def error_response(request_id: str, code: str, status: str = "error") -> dict[str, Any]:
    return {"request_id": request_id, "status": status, "error_code": code, "provenance": []}


def dispatch(root: Path, method: str, params: dict[str, Any]) -> dict[str, Any]:
    rid = req_id()
    if method == "tools/list":
        return {"request_id": rid, "status": "ok", "tools": [{"name": n, "access": m["access"]} for n, m in sorted(TOOLS.items())]}
    if method != "tools/call":
        return error_response(rid, "method_not_supported")
    name = params.get("name")
    args = params.get("arguments", {})
    if name not in TOOLS:
        return error_response(rid, "tool_not_allowed", "denied")
    try:
        if name == "search_notes":
            out = search_notes(root, str(args.get("query", "")), int(args.get("limit", 10)))
        elif name == "read_note":
            out = read_note(root, str(args.get("note_id", "")))
        elif name == "list_related_notes":
            out = list_related_notes(root, str(args.get("note_id", "")), int(args.get("depth", 1)))
        elif name == "retrieve_runbook":
            out = retrieve_runbook(root, str(args.get("problem", "")), args.get("technology"), int(args.get("limit", 5)))
        else:
            return error_response(rid, "tool_not_allowed", "denied")
        out.update({"request_id": rid, "status": "ok"})
        return out
    except FileNotFoundError as exc:
        return error_response(rid, str(exc) or "not_found")
    except PermissionError:
        return error_response(rid, "permission_denied", "denied")
    except (ValueError, TypeError) as exc:
        return error_response(rid, str(exc) or "invalid_arguments", "denied")
    except Exception:
        return error_response(rid, "internal_error")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--stdio", action="store_true")
    args = parser.parse_args()
    root = args.vault.resolve()
    if not root.is_dir():
        print(json.dumps({"status": "error", "error_code": "vault_not_found"}), flush=True)
        return 2
    if not args.stdio:
        parser.error("--stdio is required for the reference transport")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            result = dispatch(root, msg.get("method", ""), msg.get("params", {}) or {})
            response = {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        except Exception:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": "internal error"}}
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
