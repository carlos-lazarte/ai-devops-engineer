# Dependency Resolution

Skills can declare other Skills as dependencies. Resolution is deterministic and fails closed.

Rules:

1. A dependency must exist in the registry.
2. The dependency version constraint must be satisfied.
3. Dependency cycles are rejected.
4. Every resolved dependency is policy-checked independently.
5. The final plan preserves a deterministic topological order.

Example:

```text
incident-coordination
        ↓
observability-diagnosis
        ↓
kubernetes-troubleshooting
```

A resolved dependency never inherits the permissions of the requesting Skill.
