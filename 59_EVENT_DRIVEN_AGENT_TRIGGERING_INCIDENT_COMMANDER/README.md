# v3.7.0 — Event-Driven Agent Triggering & Human-in-the-Loop Incident Commander

This module extends v3.6 Incident Candidates into a bounded, event-driven control loop.
A candidate can produce an **Agent Trigger Request**, open an **Incident Commander Session**, request human approval for bounded actions, and hand approved investigation work to the existing Planner boundary.

## Core flow

```text
Incident Candidate
      ↓
Trigger Eligibility
      ↓
Agent Trigger Request
      ↓
Policy / Identity / Budget checks
      ↓
Incident Commander Session
      ↓
Evidence Pack + Hypotheses
      ↓
Human Review / Approval
      ↓
Planner Handoff
      ↓
Plan-only / Verification boundary
```

The reference implementation is deterministic, local and simulation-only. Triggering an agent never grants authorization. Production execution remains disabled.
