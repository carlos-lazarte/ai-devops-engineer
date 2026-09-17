#!/usr/bin/env bash
set -euo pipefail

PYTHON="${PYTHON:-python3}"

command -v "$PYTHON" >/dev/null 2>&1 || {
  echo "ERROR: python3 is required" >&2
  exit 1
}

"$PYTHON" -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r 24_RAG_SEMANTIC_RETRIEVAL/scripts/requirements.txt pytest pyyaml

echo "Environment ready. Activate with: . .venv/bin/activate"
