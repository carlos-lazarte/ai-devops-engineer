# Incident Simulation Methodology

Each simulation has:

1. Initial state
2. Fault injection
3. Expected telemetry changes
4. Investigation objectives
5. Allowed tools
6. Expected verification
7. Ground-truth outcome

## Scenario lifecycle

```text
Baseline
  ↓
Inject Fault
  ↓
Observe Symptoms
  ↓
Agent Investigation
  ↓
Plan
  ↓
Approved Simulation Action
  ↓
Observe
  ↓
Verify
  ↓
Close / Replan
```

The ground truth is hidden from the agent during a normal evaluation run.

## Purpose

This permits repeatable evaluation of:
- retrieval
- planning
- diagnosis
- tool selection
- action safety
- verification
- replanning
