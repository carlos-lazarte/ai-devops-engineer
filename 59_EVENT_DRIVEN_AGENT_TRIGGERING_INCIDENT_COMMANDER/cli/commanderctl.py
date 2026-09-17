#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from commander.orchestrator import trigger_to_commander

def main():
    p=argparse.ArgumentParser(description="v3.7 event-driven incident commander reference CLI")
    sub=p.add_subparsers(dest="cmd", required=True)
    r=sub.add_parser("run")
    r.add_argument("--input", required=True)
    r.add_argument("--pretty", action="store_true")
    args=p.parse_args()
    if args.cmd == "run":
        incident=json.loads(Path(args.input).read_text())
        out=trigger_to_commander(incident)
        print(json.dumps(out, indent=2 if args.pretty else None, sort_keys=True))

if __name__ == "__main__": main()
