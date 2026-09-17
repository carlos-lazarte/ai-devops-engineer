# Capacity Planning Methodology

Plan capacity separately for:

- tokens
- model requests
- tool calls
- context size
- concurrency
- latency budget
- estimated spend

Use historical observations and explicit scenarios.

## Planning horizons

```text
short term  → operational headroom
medium term → budget / quota planning
long term   → architecture / capacity changes
```

Reference forecasts in this release are deterministic and synthetic.
