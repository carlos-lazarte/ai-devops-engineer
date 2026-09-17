---
type: reference
domain: ai
status: active
tags:
  - ai
  - evidence
  - quality
---
# Evidence Quality Matrix

| Evidence | Typical quality | Main limitation |
|---|---|---|
| Direct command output | Very high | Can be incomplete or collected after the event |
| Application/system logs | High | Logging may be missing, rotated or misleading |
| Metrics | High | Aggregation can hide short events |
| Traces | High | Sampling and instrumentation can limit coverage |
| Vendor documentation | High | Version mismatch can invalidate details |
| Internal runbook | Medium/High | May be stale |
| Human recollection | Variable | Memory and timing bias |
| AI model prior knowledge | Variable | May be stale or incorrect |

## Rule

When a recommendation depends on a specific system state, prefer current target-system evidence over generic knowledge.

## Evidence mapping pattern

```text
Claim
  ↓
Evidence source
  ↓
Timestamp / version
  ↓
Reasoning
  ↓
Validation step
```
