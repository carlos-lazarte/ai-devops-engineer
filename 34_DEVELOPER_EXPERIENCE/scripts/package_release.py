#!/usr/bin/env python3
"""Build a clean distribution archive from a Vault checkout."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

EXCLUDED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache"}
EXCLUDED_NAMES = {".env"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True
    # Runtime data is generated state. Keep a checked-in .gitkeep only.
    if "runtime-data" in path.parts and path.name != ".gitkeep":
        return True
    if path.name in EXCLUDED_NAMES:
        return True
    if path.suffix in EXCLUDED_SUFFIXES:
        return True
    return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = ap.parse_args()

    root = args.root.resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")

    outdir = args.output_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    archive = outdir / f"AI-DevOps-Engineer-Vault-v{version}.zip"

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / f"AI-DevOps-Engineer-Vault-v{version}"
        for path in root.rglob("*"):
            rel = path.relative_to(root)
            excluded_output = outdir.is_relative_to(root) and rel.parts[:1] == (outdir.relative_to(root).parts[0],)
            if should_skip(rel) or excluded_output:
                continue
            target = staging / rel
            if path.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)

        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in staging.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(staging.parent).as_posix())

    sha = archive.with_suffix(archive.suffix + ".sha256")
    sha.write_text(f"{sha256(archive)}  {archive.name}\n", encoding="utf-8")
    print(f"created: {archive}")
    print(f"sha256: {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
