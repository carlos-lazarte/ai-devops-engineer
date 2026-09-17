#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from v310_service.registry import ConnectorRegistry  # noqa: E402

p = argparse.ArgumentParser(description="AI DevOps Engineer v3.10 connector control CLI")
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("list")
sub.add_parser("health")
args = p.parse_args()
reg = ConnectorRegistry()
if args.cmd == "list":
    print(json.dumps({"status":"ok", "connectors": reg.metadata()}, indent=2))
else:
    print(json.dumps(reg.health(), indent=2))
