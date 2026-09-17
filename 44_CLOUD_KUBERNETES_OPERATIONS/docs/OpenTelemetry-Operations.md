---
type: architecture
domain: observability
technology: opentelemetry
status: active
tags:
  - opentelemetry
  - tracing
  - observability
---

# OpenTelemetry Operations

Use OpenTelemetry to standardize telemetry generation and export across services.

## Recommended signals

- traces for request path and cross-service latency
- metrics for service and dependency health
- logs with correlation identifiers

## Collector pattern

```text
Application
    |
    +--> OTLP --> Collector --> backend
```

Keep telemetry transport separate from authorization to production change tools. Telemetry should not become an implicit write path.
