# Planner Safety Boundaries

The planner is an advisory control component.

## Prohibited inference
The planner must not infer:
- successful execution from a proposed action
- approval from historical memory
- authorization from Skill membership
- production access from environment metadata alone
- evidence from an unsupported hypothesis

## Required invariants
```text
plan_only is the default
execution requires policy
high-risk actions require explicit approval
critical execution remains disabled
```

## Failure behavior
Missing evidence → identify the gap.
Unavailable tool → report unavailable capability.
Policy denial → exclude the operation and explain the denial.
Ambiguous task → return clarification requirements instead of inventing assumptions.
