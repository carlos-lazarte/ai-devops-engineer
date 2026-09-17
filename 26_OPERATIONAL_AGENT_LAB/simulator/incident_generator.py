#!/usr/bin/env python3
"""Generate deterministic DevOps incident fixtures for the Operational Agent Lab.

Safety: this script only creates local text/JSON files. It never connects to
Kubernetes, SSH, cloud APIs, or production systems.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCENARIOS: dict[str, dict[str, Any]] = {
    "K8S-NOTREADY-001": {
        "title": "Kubernetes Node NotReady",
        "domain": "kubernetes",
        "expected_failure_domain": "network-path-or-policy",
        "fixtures": [
            "node-description.txt",
            "kubelet.log",
            "network-observation.txt",
            "change-record.txt",
        ],
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a safe local incident fixture")
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    scenario = SCENARIOS[args.scenario]
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "scenario_id": args.scenario,
        "title": scenario["title"],
        "domain": scenario["domain"],
        "fixture_files": scenario["fixtures"],
        "simulation_only": True,
        "expected_failure_domain_for_evaluation": scenario["expected_failure_domain"],
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generated simulated scenario {args.scenario} at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
