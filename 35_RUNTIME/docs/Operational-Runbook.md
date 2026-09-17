---
type: runbook
domain: ai
technology: runtime
status: active
risk: medium
---

# Runbook — AI DevOps Runtime

## Start

```bash
cd 35_RUNTIME
. .venv/bin/activate
python -m app.server --vault .. --host 127.0.0.1 --port 8080
```

## Validate

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/ready
```

## Dry-run an incident

```bash
curl -s http://127.0.0.1:8080/incident/analyze \\
  -H 'content-type: application/json' \\
  -d '{"incident_id":"K8S-NOTREADY-001","mode":"dry-run"}'
```

## Shutdown

Use the process supervisor or stop the container.

## Failure handling

- If health fails, verify process status and Vault path.
- If incident lookup fails, verify the scenario ID exists under `26_OPERATIONAL_AGENT_LAB/scenarios/`.
- If Claude mode returns `anthropic_api_key_missing`, verify the environment without printing the secret.
- If audit writes fail, inspect filesystem permissions for the configured audit directory.
