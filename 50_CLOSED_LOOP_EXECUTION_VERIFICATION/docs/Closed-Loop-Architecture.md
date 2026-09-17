---
type: architecture
domain: ai-devops
status: active
version: "2.8.0"
tags:
  - closed-loop
  - execution
  - verification
  - agent
  - sre
---
# Closed-Loop Agent Execution & Verification

## Purpose

Connect a bounded execution plan to controlled execution, observation, verification, and replanning.

## Control loop

```text
PLAN
 ↓
POLICY CHECK
 ↓
APPROVAL
 ↓
EXECUTE
 ↓
OBSERVE
 ↓
VERIFY
 ↓
  ├── VERIFIED → CLOSE
  ├── FAILED   → REPLAN
  └── UNKNOWN  → COLLECT MORE EVIDENCE
```

## Core principles

- Execution is performed only through registered tools.
- The agent does not gain permissions from its plan.
- Approval is explicit and scoped to a task/action.
- Every executed action produces an audit event.
- Verification is mandatory before declaring success.
- Failed verification never becomes a successful outcome through inference.
- Production execution remains disabled in the reference implementation.

## Reference execution modes

```text
plan_only
simulate
approved_execution
```

The reference implementation supports only `simulate` as an actual executor.
