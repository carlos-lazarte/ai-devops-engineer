# Claude Integration

`dry-run` is the recommended local path because it is deterministic and does not require an external provider.

`claude` calls the existing Claude client with an evidence-bounded prompt. The prompt explicitly forbids invented telemetry and execution claims.

The model response is persisted under `agent` for auditability. Model output is advisory and never becomes an authorization decision.
