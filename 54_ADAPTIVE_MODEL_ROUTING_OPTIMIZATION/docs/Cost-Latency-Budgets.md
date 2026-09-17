# Cost and Latency Budgets

Routing constraints can specify:

```text
max_cost_per_1k_tokens
max_latency_ms
```

These are eligibility constraints.

A candidate outside either limit is excluded before utility ranking.

Provider billing and measured latency must be collected from the target environment; registry estimates are only reference data.
