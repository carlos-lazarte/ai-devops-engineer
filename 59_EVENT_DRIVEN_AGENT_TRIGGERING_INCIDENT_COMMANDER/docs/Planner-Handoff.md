# Planner Handoff

The commander can hand a structured investigation request to the existing planning layer.

```text
Incident Candidate
 → Commander Evidence Pack
 → Investigation Objective
 → Constraints
 → Skill Recommendation
 → Planner Request
```

The handoff carries the candidate's provenance and policy decision but does not mutate authorization state. The planner output is a plan artifact. Execution requires separate policy and approval controls.
