---
type: policy
domain: ai
difficulty: advanced
status: active
tags:
  - autonomy
  - risk
  - governance
---
# Autonomy Model

Autonomy is defined by operation class, not by the agent identity alone.

| Level | Meaning | Example | Baseline |
|---|---|---|---|
| L0 | Observe | retrieve notes, collect evidence | Allowed |
| L1 | Analyze | classify incident, form hypotheses | Allowed |
| L2 | Draft | generate runbook steps or change plan | Allowed with validation |
| L3 | Recommend | propose bounded change | Human approval required |
| L4 | Execute | perform mutation | Disabled in v2.3.0 |

## Rules

- L4 is disabled by default.
- A skill cannot self-escalate its autonomy level.
- Approval is bound to a specific task, tenant, environment and proposed action.
- Historical memory never grants permission.
- Verification is mandatory after any simulated execution.
