from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "35_RUNTIME"))
sys.path.insert(0, str(ROOT / "61_REAL_TELEMETRY_EVENT_INGESTION"))

from app.store import IncidentStore
from service.ingest import TelemetryIngestionService


def main():
    p = argparse.ArgumentParser(description="AI DevOps v3.9 telemetry ingestion CLI")
    p.add_argument("--db", default="runtime-data/telemetryctl.db")
    sub = p.add_subparsers(dest="cmd", required=True)
    ing = sub.add_parser("event")
    ing.add_argument("--file", required=True)
    args = p.parse_args()
    store = IncidentStore(sqlite_path=args.db)
    svc = TelemetryIngestionService(store)
    if args.cmd == "event":
        payload = json.loads(Path(args.file).read_text())
        print(json.dumps(svc.ingest_event(payload), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
