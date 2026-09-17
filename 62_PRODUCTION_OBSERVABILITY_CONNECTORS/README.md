---
type: runtime
version: 3.10.0
domain: observability
status: active
---

# v3.10.0 — Production Observability Connectors

This release turns v3.9 telemetry ingestion into a production-shaped connector boundary. The goal is not to grant the agent direct infrastructure control; it is to provide bounded, observable, retry-aware, read-only data acquisition from approved telemetry systems.

## Connectors

```text
Prometheus  ──read-only──┐
Kubernetes  ──read-only──┤
Linux/proc  ──read-only──┤──> Connector Boundary ──> v3.9 Ingestion
OTel HTTP   ──receiver────┘
```

### Prometheus
- PromQL query API, read-only.
- Optional bearer token from environment.
- Response-size limits.
- Query-size limits.
- Retry with bounded exponential backoff.
- Process-local rate limiting.
- Health check.

### OpenTelemetry Collector
A reference collector configuration is provided in `otel/config.yaml`. The collector is the preferred place for protocol fan-in, batching and memory limiting. The runtime accepts the bounded JSON metrics subset defined in v3.9.

### Kubernetes
- Read-only API access.
- Bearer token / ServiceAccount token support.
- Optional CA bundle.
- Bounded response size.
- Namespace validation.
- No `exec`, `port-forward`, or mutation operation is implemented.
- Health check through `/version`.

### Linux
- Local read-only `/proc` and `/sys` access.
- CPU and memory snapshots.
- No command execution and no remote shell.

## Security model

```text
Credential → Connector
             ↓
         Read-only data
             ↓
     Tenant + Environment
             ↓
       v3.9 ingestion
             ↓
       Correlation
             ↓
      Incident Candidate
```

Connectors do not grant agent authorization. Remediation remains subject to the existing Policy / Identity / Approval / Verification chain.

## Environment

Start from `fixtures/connector-environment.example.env`. In production, load credentials from a secret manager or orchestrator secret store rather than committing them to Git.

## CLI

```bash
python3 62_PRODUCTION_OBSERVABILITY_CONNECTORS/cli/connectorctl.py list
python3 62_PRODUCTION_OBSERVABILITY_CONNECTORS/cli/connectorctl.py health
```
