---
type: architecture
domain: ai
technology: multi-agent
level: advanced
status: active
tags:
  - agents
  - orchestration
  - delegation
---

# Multi-Agent Orchestration Model

## Agent roles

- **DevOps Agent** — infrastructure, runtime and deployment diagnostics.
- **Cloud Agent** — cloud resource and IAM context analysis.
- **Security Agent** — policy, exposure and control analysis.
- **SRE Agent** — reliability, SLO and incident coordination.

## Delegation rule

Delegation must be explicit in the task envelope.

```text
Task
  -> Router
  -> Agent A
       -> Agent B (optional, explicit)
  -> Aggregator
  -> Human review
```

The router must not create recursive delegation without a bounded hop limit.

## Recommended limits

- Maximum delegation depth: 2.
- Maximum agents per task: 4.
- Maximum tool calls: environment-specific and policy-controlled.
- Critical operations: disabled unless explicitly implemented and approved.
