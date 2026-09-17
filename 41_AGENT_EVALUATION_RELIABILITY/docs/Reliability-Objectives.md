---
type: reference
domain: sre
status: active
tags:
  - sre
  - reliability
  - slo
---
# Reliability Objectives

These are engineering targets for the local/runtime evaluation layer, not a promise for every production deployment.

| Objective | Target |
|---|---:|
| health/ready availability | >= 99.9% |
| evaluation harness deterministic pass rate | 100% |
| critical safety tests | 100% pass |
| malformed model response containment | 100% |
| audit event emission on deny | 100% |
| duplicate request determinism | 100% within the test contract |

## Error budget principle

A regression in a critical safety invariant consumes the entire release budget and blocks promotion until resolved.
