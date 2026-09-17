# Adaptive Planning Workflow

```text
User Task
  ↓
Normalize Task
  ↓
Decompose Goal
  ↓
Build Investigation Questions
  ↓
Seed Knowledge Graph
  ↓
Expand Relevant Nodes
  ↓
Retrieve Evidence
  ↓
Discover Skills
  ↓
Resolve Dependencies
  ↓
Select Tools
  ↓
Policy Check
  ↓
Build Plan
```

## Example: Kubernetes NodeNotReady
The planner should determine that it needs to investigate:
- node conditions
- kubelet health
- recent changes
- network state
- related runbooks
- historical incidents

The plan must distinguish:
- known evidence
- required evidence
- hypotheses
- proposed diagnostics
- approval-gated actions
