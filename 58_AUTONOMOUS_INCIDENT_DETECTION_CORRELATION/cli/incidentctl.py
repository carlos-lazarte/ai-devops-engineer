from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from correlator.service import build_incident_candidates


def main() -> int:
    p = argparse.ArgumentParser(description='v3.6 Autonomous Incident Detection reference CLI')
    p.add_argument('command', choices=['correlate'])
    p.add_argument('--input', required=True, help='JSON array of raw events')
    p.add_argument('--pretty', action='store_true')
    args = p.parse_args()
    events = json.loads(Path(args.input).read_text())
    result = build_incident_candidates(events)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
