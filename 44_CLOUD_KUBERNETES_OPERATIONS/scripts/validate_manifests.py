#!/usr/bin/env python3
"""Static validation for reference cloud/Kubernetes operation manifests."""
from __future__ import annotations
import sys
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"PyYAML is required: {exc}")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIRS = [ROOT / "kubernetes", ROOT / "observability", ROOT / "gitops", ROOT / "backup", ROOT / "security"]
FORBIDDEN = ("BEGIN PRIVATE KEY", "sk-", "AKIA")

def main() -> int:
    errors=[]
    count=0
    for base in MANIFEST_DIRS:
        if not base.exists(): continue
        for path in base.rglob("*.yaml"):
            count += 1
            text=path.read_text(encoding="utf-8")
            if any(token in text for token in FORBIDDEN):
                errors.append(f"possible secret material: {path.relative_to(ROOT)}")
            try:
                docs=list(yaml.safe_load_all(text))
            except Exception as exc:
                errors.append(f"invalid YAML {path.relative_to(ROOT)}: {exc}")
                continue
            for idx, doc in enumerate(docs):
                if doc is None: continue
                if not isinstance(doc, dict):
                    errors.append(f"non-object document: {path.relative_to(ROOT)}#{idx}")
                elif not all(k in doc for k in ("apiVersion", "kind")):
                    errors.append(f"missing apiVersion/kind: {path.relative_to(ROOT)}#{idx}")
    if errors:
        print("manifest validation: FAIL")
        for e in errors: print(f"- {e}")
        return 1
    print(f"manifest validation: PASS ({count} YAML files)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
