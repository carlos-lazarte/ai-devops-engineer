# Runbook — Runtime Unavailable

## Trigger

`RuntimeDown` alert or failed health checks.

## Evidence

```bash
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8080/ready

docker compose ps

docker compose logs --tail=200 ai-devops-runtime
```

## Checks

1. Container/process state.
2. Port binding.
3. Vault mount readability.
4. Recent configuration changes.
5. Resource pressure on the host.

## Recovery

Restart only after capturing evidence and confirming the change is understood.

## Verification

Confirm `/health`, `/ready`, and `/metrics` return successfully and that the Prometheus target is `UP`.
