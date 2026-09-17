#!/usr/bin/env sh
set -eu
exec python product_server.py --vault "${VAULT_ROOT:-/vault}" --host "${RUNTIME_HOST:-0.0.0.0}" --port "${RUNTIME_PORT:-8080}"
