# Production Connector Architecture

The connector layer is a controlled acquisition boundary between infrastructure systems and the AI DevOps runtime.

```text
                External Systems
        ┌───────────┬───────────┬───────────┐
        │           │           │           │
    Prometheus     OTel      Kubernetes   Linux
        │           │           │           │
        └───────────┴───────────┴───────────┘
                         ↓
                 Connector Registry
                         ↓
              Validation / Rate Limit
                         ↓
                 Retry / Timeout
                         ↓
                  Read-only data
                         ↓
               v3.9 Telemetry API
                         ↓
            Correlation / Incident Engine
```

The connector layer does not execute remediation commands. It can only acquire telemetry or submit telemetry to the existing ingestion boundary.
