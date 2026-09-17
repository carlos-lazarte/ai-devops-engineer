---
type: guide
domain: ai
technology: runtime
status: active
---

# Runtime Quickstart

The executable runtime lives in `35_RUNTIME/`.

## Local

```bash
cd 35_RUNTIME
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m app.server --vault ..
```

## Docker Compose

From the Vault root:

```bash
docker compose up --build
```

The Vault is mounted read-only into the container.

## End-to-end dry run

```bash
curl -s http://127.0.0.1:8080/incident/analyze \\
  -H 'content-type: application/json' \\
  -d '{"incident_id":"K8S-NOTREADY-001","mode":"dry-run"}'
```

No external AI call is required for dry-run mode.
