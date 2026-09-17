# Adaptive Routing Policy

The optimizer uses a constrained objective.

Reference utility:

```text
utility = quality_weight * quality
        - latency_weight * normalized_latency
        - cost_weight * normalized_cost
        + reliability_weight * reliability
```

The actual implementation uses deterministic profile and history values.

## Guardrails

- critical tasks require the configured critical quality tier
- no route may bypass policy
- historical data may affect ranking, not authorization
- stale or insufficient telemetry falls back to static routing
- production execution remains disabled

## Exploration

v3.2.0 does not perform autonomous exploratory traffic to external providers. It uses supplied historical telemetry only.
