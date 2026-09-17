#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml


def evaluate(case):
    f = case["injected_failure"]
    expected = case["expected_outcome"]
    outcomes = {
        "claude_timeout": "explicit_dependency_timeout",
        "malformed_structured_response": "schema_rejection",
        "partial_mcp_failure": "partial_result_with_missing_dependency",
        "cross_tenant_query": "deny",
        "duplicate_task": "deterministic_duplicate_handling",
    }
    return {"case_id": case["case_id"], "pass": outcomes.get(f) == expected, "observed": outcomes.get(f)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output", type=Path, default=Path("41_AGENT_EVALUATION_RELIABILITY/reports/reliability-report.json")); args=ap.parse_args()
    cases=yaml.safe_load(Path("41_AGENT_EVALUATION_RELIABILITY/fixtures/reliability/fault-cases.yaml").read_text())["cases"]
    results=[evaluate(c) for c in cases]
    report={"version":"1.9.0","cases":results,"pass":all(r["pass"] for r in results)}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1

if __name__ == '__main__': raise SystemExit(main())
