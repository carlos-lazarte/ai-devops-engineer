# Runtime SLOs

The following objectives are a baseline for the AI DevOps Runtime. Tune them to the real service contract before adopting them as production commitments.

| SLI | Target | Window | Notes |
|---|---:|---|---|
| Availability of `/health` | 99.9% | 30d | HTTP 2xx responses |
| `/search` success rate | 99.0% | 30d | Excludes client-side 4xx |
| `/incident/analyze` success rate | 99.0% | 30d | Excludes client-side 4xx |
| `/search` p95 latency | < 1.0s | 30d | Baseline; measure before committing |
| `/incident/analyze` p95 latency | < 10s dry-run | 30d | Claude mode depends on provider latency |

## Error-budget model

For a 30-day window:

- 99.9% availability leaves 0.1% unavailability budget.
- 99.0% endpoint success leaves 1.0% failed-request budget.

Use burn-rate alerts rather than treating a single spike as an SLO violation.
