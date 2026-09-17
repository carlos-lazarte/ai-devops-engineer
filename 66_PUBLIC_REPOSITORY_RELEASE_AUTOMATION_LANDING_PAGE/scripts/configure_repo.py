#!/usr/bin/env python3
"""Replace the landing-page repository placeholder with an actual GitHub repo URL."""
from __future__ import annotations

import argparse
from pathlib import Path
import re

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="GitHub repository in OWNER/REPO form")
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args()
    if not re.fullmatch(r"[^/\s]+/[^/\s]+", args.repo):
        raise SystemExit("repo must be OWNER/REPO")
    cfg = args.root.resolve()/"66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/site/config.js"
    text = cfg.read_text(encoding="utf-8")
    text = text.replace("https://github.com/OWNER/REPO", f"https://github.com/{args.repo}")
    cfg.write_text(text, encoding="utf-8")
    print(f"configured: {cfg}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
