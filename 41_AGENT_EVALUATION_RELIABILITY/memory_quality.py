#!/usr/bin/env python3
"""Quality checks over synthetic memory records."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "40_AGENT_MEMORY_STATE"))
from store.memory_store import MemoryStore


def run(db: Path) -> dict:
    store = MemoryStore(db)
    a = store.add(memory_class="episodic", tenant_id="t1", environment="lab", content="Node not ready", correlation_id="c1", incident_id="i1", source_refs=["e1"], provenance={"source":"lab"})
    b = store.add(memory_class="episodic", tenant_id="t2", environment="lab", content="Other tenant", correlation_id="c2", incident_id="i2", source_refs=["e2"], provenance={"source":"lab"})
    same = bool(store.get(a.memory_id, tenant_id="t1", environment="lab"))
    cross = store.get(a.memory_id, tenant_id="t2", environment="lab") is not None
    promoted = store.promote(a.memory_id, tenant_id="t1", environment="lab", reviewer="reviewer-1")
    checks = {
        "same_tenant_retrieval": same,
        "cross_tenant_isolation": not cross,
        "promotion_requires_review": promoted.status == "verified" and promoted.reviewed_by == "reviewer-1",
        "provenance_present": bool(promoted.source_refs) and bool(promoted.provenance),
    }
    passed = all(checks.values())
    return {"checks": checks, "pass": passed}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, default=Path(".evaluation-memory.db"))
    args = ap.parse_args()
    if args.db.exists():
        args.db.unlink()
    result = run(args.db)
    print(json.dumps(result, indent=2))
    if args.db.exists(): args.db.unlink()
    return 0 if result["pass"] else 1

if __name__ == "__main__": raise SystemExit(main())
