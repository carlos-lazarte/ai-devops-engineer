# Runbook — Runtime High Latency

## Trigger

p95 latency exceeds the configured threshold.

## Checks

1. Identify affected route.
2. Compare `/search` vs `/incident/analyze`.
3. Check request volume and in-flight requests.
4. Check Vault read/search latency.
5. In Claude mode, inspect provider request duration and errors.
6. Compare with recent releases.

## Mitigation

Reduce load, isolate the slow dependency, or roll back a known-bad change according to the change policy. Production changes require human approval.
