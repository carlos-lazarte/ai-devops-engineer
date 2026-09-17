# Closed-Loop Agent Execution & Verification

v2.8.0 adds a bounded closed-loop execution layer.

The reference executor is simulation-only and requires explicit approval.
Production execution is disabled.

```text
Plan → Approval → Execute → Observe → Verify → Close / Replan
```
