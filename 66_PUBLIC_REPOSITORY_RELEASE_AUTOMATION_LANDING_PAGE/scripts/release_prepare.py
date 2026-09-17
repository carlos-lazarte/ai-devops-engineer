#!/usr/bin/env python3
"""Validate and prepare a public release without publishing it."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import subprocess
import sys

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")

REQUIRED = [
    "README.md", "LICENSE", "NOTICE", "VERSION", "COMMUNITY.md",
    "SECURITY.md", "SUPPORT.md", "GOVERNANCE.md", "ROADMAP.md",
    ".github/workflows/release.yml",
    ".github/workflows/pages.yml",
    ".github/workflows/publish-container.yml",
    "66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/site/index.html",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args()
    root = args.root.resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.match(version):
        print(f"invalid VERSION: {version}")
        return 2
    missing = [p for p in REQUIRED if not (root/p).exists()]
    if missing:
        for p in missing: print(f"MISSING: {p}")
        return 1
    checks = [
        ("public-check", ["bash", "65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/scripts/public-check.sh"]),
        ("python-compile", [sys.executable, "-m", "compileall", "-q", "66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE"]),
    ]
    for name, cmd in checks:
        print(f"== {name} ==")
        proc = subprocess.run(cmd, cwd=root)
        if proc.returncode != 0:
            return proc.returncode
    print(f"RELEASE PREPARE: PASS ({version})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
