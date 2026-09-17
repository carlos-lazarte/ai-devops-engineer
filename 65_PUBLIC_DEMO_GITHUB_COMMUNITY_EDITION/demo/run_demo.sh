#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUNTIME_DIR="$ROOT/35_RUNTIME"
PORT="${AIOPS_DEMO_PORT:-18080}"
DEMO_TMP="$(mktemp -d "${TMPDIR:-/tmp}/aiops-community-demo.XXXXXX")"
LOG_FILE="$DEMO_TMP/runtime.log"
PID=""

cleanup() {
  if [[ -n "${PID}" ]] && kill -0 "${PID}" 2>/dev/null; then
    kill "${PID}" 2>/dev/null || true
    wait "${PID}" 2>/dev/null || true
  fi
  rm -rf "$DEMO_TMP"
}
trap cleanup EXIT INT TERM

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 is required" >&2; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "ERROR: curl is required" >&2; exit 1; }

PYTHON_BIN="${AIOPS_DEMO_PYTHON:-python3}"
VENV="$ROOT/.venv-community-demo"
if ! "$PYTHON_BIN" -c 'import prometheus_client, yaml' >/dev/null 2>&1; then
  if [[ ! -x "$VENV/bin/python" ]]; then
    python3 -m venv "$VENV"
    "$VENV/bin/python" -m pip install -r "$ROOT/65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/demo/requirements.txt"
  fi
  PYTHON_BIN="$VENV/bin/python"
fi

export PYTHONPATH="$RUNTIME_DIR:${PYTHONPATH:-}"
export ANTHROPIC_API_KEY=""
export PROMETHEUS_URL="http://127.0.0.1:9090"
export INVESTIGATION_LOCAL_LINUX="false"

if ! "$PYTHON_BIN" - "$PORT" <<'PYPORT' >/dev/null 2>&1
import socket, sys
s = socket.socket(); s.bind(("127.0.0.1", int(sys.argv[1]))); s.close()
PYPORT
then
  PORT="$($PYTHON_BIN - <<'PYFREE'
import socket
s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()
PYFREE
)"
  echo "Requested demo port is busy; using $PORT"
fi

cd "$DEMO_TMP"
"$PYTHON_BIN" "$RUNTIME_DIR/product_server.py" --vault "$ROOT" --host 127.0.0.1 --port "$PORT" >"$LOG_FILE" 2>&1 &
PID=$!

for _ in $(seq 1 80); do
  if curl -fsS "http://127.0.0.1:${PORT}/api/v1/product" >/dev/null 2>&1; then break; fi
  sleep 0.25
done

curl -fsS -X POST "http://127.0.0.1:${PORT}/api/v1/demo/seed" | "$PYTHON_BIN" -m json.tool

STAMP="$(date +%s)"
cat <<JSON | curl -fsS -X POST "http://127.0.0.1:${PORT}/api/v1/telemetry/events" -H 'content-type: application/json' -d @- | "$PYTHON_BIN" -m json.tool
{"events":[
  {"event_id":"public-cpu-${STAMP}","timestamp":${STAMP},"tenant_id":"demo-tenant","environment":"lab","component":"node-01","metric_family":"cpu","condition":"high","severity_hint":"high","value":95,"source":"public-demo"},
  {"event_id":"public-memory-${STAMP}","timestamp":$((STAMP+5)),"tenant_id":"demo-tenant","environment":"lab","component":"node-01","metric_family":"memory","condition":"high","severity_hint":"high","value":92,"source":"public-demo"}
]}
JSON

INCIDENT_ID="$(curl -fsS "http://127.0.0.1:${PORT}/api/v1/incidents?tenant_id=demo-tenant" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["results"][0]["incident_id"])')"

echo "=== Running deterministic investigation for ${INCIDENT_ID} ==="
curl -fsS -X POST "http://127.0.0.1:${PORT}/api/v1/incidents/${INCIDENT_ID}/investigate" -H 'content-type: application/json' -d '{"mode":"dry-run","include_connectors":false}' | "$PYTHON_BIN" -m json.tool

echo "=== Dashboard summary ==="
curl -fsS "http://127.0.0.1:${PORT}/api/v1/dashboard/summary?tenant_id=demo-tenant" | "$PYTHON_BIN" -m json.tool

echo
echo "Demo complete. The dashboard was available at http://127.0.0.1:${PORT}/ during the run."
echo "Runtime log: ${LOG_FILE}"
