#!/usr/bin/env python3
"""Validate the structural integrity of an Obsidian AI DevOps Vault."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_ROOT_FILES = {"README.md", "CHANGELOG.md", "LICENSE.md"}
FORBIDDEN_NAMES = {".pytest_cache", "__pycache__"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
]
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"Vault root does not exist: {root}"]

    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            errors.append(f"missing root file: {name}")

    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(part in FORBIDDEN_NAMES for part in rel.parts):
            continue
        if not p.is_file() or p.suffix != ".md":
            continue

        text = p.read_text(encoding="utf-8")
        # Content notes are expected to carry metadata; README/legal/changelog are exempt.
        exempt = p.name in {"README.md", "CHANGELOG.md", "LICENSE.md"}
        if not exempt and text.startswith("---\n"):
            match = FRONTMATTER_RE.match(text)
            if not match:
                errors.append(f"invalid YAML frontmatter delimiters: {rel}")
            elif not re.search(r"^type:\s*\S+", match.group(1), re.MULTILINE):
                errors.append(f"missing type property: {rel}")

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret material in: {rel}")
                break

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", type=Path)
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print("Vault validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Vault validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
