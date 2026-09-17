#!/usr/bin/env python3
"""Minimal local Skill marketplace lifecycle helper.

This tool is intentionally offline and non-executing: it validates metadata and
prints lifecycle decisions. It does not install arbitrary code or execute tools.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED = {
    "skill_id:", "name:", "version:", "platform_api:",
    "contract_version:", "risk:", "autonomy_level:",
}

def validate(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    lines = {line.split(":", 1)[0] + ":" for line in text.splitlines() if ":" in line and not line.startswith(" ")}
    missing = sorted(REQUIRED - lines)
    if missing:
        print("INVALID: missing", ", ".join(missing))
        return 2
    version = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("version:")), "")
    if not SEMVER.match(version):
        print("INVALID: version must use semver")
        return 2
    print("VALID:", path)
    return 0

def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("manifest", type=Path)
    l = sub.add_parser("lifecycle")
    l.add_argument("state", choices=["draft","candidate","verified","published","installed","deprecated","retired"])
    args = ap.parse_args()
    if args.cmd == "validate":
        return validate(args.manifest)
    print(f"state={args.state}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
