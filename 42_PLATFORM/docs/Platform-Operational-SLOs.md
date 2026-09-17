---
type: knowledge
domain: sre
status: active
---

# Platform Operational SLOs

Reference objectives for a production implementation:

| Indicator | Reference objective |
|---|---:|
| API availability | >= 99.9% |
| API p95 latency (read requests) | <= 500 ms |
| Successful policy evaluation | >= 99.99% |
| Audit write success | >= 99.99% |
| E2E incident analysis success | >= 99.0% excluding upstream model failures |

These are engineering objectives, not guarantees of the reference implementation.
