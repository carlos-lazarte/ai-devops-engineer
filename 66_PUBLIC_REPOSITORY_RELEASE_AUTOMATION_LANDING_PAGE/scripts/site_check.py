#!/usr/bin/env python3
"""Small static-site sanity checks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/"site"

def main() -> int:
    required = [SITE/"index.html", SITE/"styles.css", SITE/"config.js"]
    for p in required:
        if not p.exists():
            print(f"MISSING: {p}")
            return 1
    html = (SITE/"index.html").read_text(encoding="utf-8")
    for needle in ["AI DevOps Engineer", "Community Edition", "Observe", "Investigate", "Human approval"]:
        if needle not in html:
            print(f"MISSING PAGE TEXT: {needle}")
            return 1
    print("SITE CHECK: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
