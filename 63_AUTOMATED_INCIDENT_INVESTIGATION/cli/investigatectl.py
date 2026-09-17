from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "35_RUNTIME"))

from app.store import IncidentStore  # noqa: E402
from investigation.engine import AutomatedIncidentInvestigator  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="AI DevOps Engineer v3.11 automated incident investigation")
    ap.add_argument("incident_id")
    ap.add_argument("--vault", type=Path, default=ROOT)
    ap.add_argument("--db", default="")
    ap.add_argument("--mode", choices=["dry-run", "claude"], default="dry-run")
    ap.add_argument("--no-connectors", action="store_true")
    args = ap.parse_args()
    store = IncidentStore(args.db or None)
    investigator = AutomatedIncidentInvestigator(args.vault, store)
    result = investigator.investigate(args.incident_id, args.mode, not args.no_connectors)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
