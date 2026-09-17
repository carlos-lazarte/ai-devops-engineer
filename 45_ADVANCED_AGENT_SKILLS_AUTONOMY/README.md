# v2.3.0 — Advanced Agent Skills & DevOps Autonomy

This layer turns general agent capability into bounded, testable DevOps skills. Each skill has explicit inputs, allowed tools, evidence requirements, output schema, safety policy, and an evaluation suite.

## Design principle

Autonomy is earned per skill and per operation. A skill does not inherit permissions from another skill, and a model suggestion is never an authorization decision.

```text
Task
 ↓
Skill Router
 ↓
Skill Contract
 ↓
Evidence Gate
 ↓
Policy / Risk Check
 ↓
Plan
 ↓
Human Approval (when required)
 ↓
Execution Adapter (simulation in v2.3.0)
 ↓
Verification
 ↓
Evaluation / Audit
```

## Scope

The v2.3.0 reference implementation is local and simulation-only. It does not provide shell, SSH, Kubernetes mutation, cloud mutation, or production execution.

See:

- [[docs/Agent-Skills-Architecture]]
- [[docs/Autonomy-Model]]
- [[docs/Skill-Authoring-Guide]]
- [[docs/DevOps-Skills-Catalog]]
