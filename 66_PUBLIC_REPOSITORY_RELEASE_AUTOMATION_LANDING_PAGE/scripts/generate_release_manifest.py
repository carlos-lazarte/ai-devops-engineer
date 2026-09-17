#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

EXCLUDED_DIRS={'.git','.venv','__pycache__','.pytest_cache','.mypy_cache','dist','runtime-data'}
EXCLUDED_NAMES={'.env'}
EXCLUDED_SUFFIXES={'.pyc','.pyo'}

def skip(rel: Path)->bool:
    if any(part in EXCLUDED_DIRS for part in rel.parts): return True
    if rel.name in EXCLUDED_NAMES or rel.suffix in EXCLUDED_SUFFIXES: return True
    return False

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path('.')); args=ap.parse_args()
    root=args.root.resolve(); version=(root/'VERSION').read_text().strip()
    entries={}
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(root)
        if skip(rel) or rel.as_posix() == 'release-manifest.json': continue
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        entries[rel.as_posix()]=h
    md=sum(1 for k in entries if k.lower().endswith('.md'))
    data={
        'title':'AI DevOps Engineer Vault',
        'version':version,
        'edition':'Community Edition',
        'feature':'Public Repository, Release Automation & Product Landing Page',
        'file_count':len(entries),
        'markdown_count':md,
        'sha256':entries,
        'release_excludes':sorted(EXCLUDED_DIRS | EXCLUDED_NAMES | EXCLUDED_SUFFIXES),
    }
    (root/'release-manifest.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f"manifest: {len(entries)} files / {md} markdown")
    return 0
if __name__=='__main__': raise SystemExit(main())
