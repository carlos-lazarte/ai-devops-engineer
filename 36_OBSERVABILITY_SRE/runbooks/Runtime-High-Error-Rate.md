# Runbook — Runtime High Error Rate

## Trigger

5xx request rate exceeds the configured alert threshold.

## Evidence

- Grafana request and error-rate panels
- Runtime logs
- Audit log
- Recent release/change records

## Decision path

```text
5xx spike
  |
  +-- one route only -> inspect route-specific dependency or input handling
  |
  +-- all routes -> inspect process health, Vault access, configuration, resources
  |
  +-- Claude mode only -> inspect provider configuration/latency/errors
```

Do not infer a root cause from the metric alone. Validate with logs and request evidence.
