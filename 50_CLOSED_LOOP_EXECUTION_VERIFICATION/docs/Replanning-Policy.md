# Replanning Policy

A failed or ambiguous verification may trigger replanning.

```text
Execution
   ↓
Verification
   ↓
FAILED / UNKNOWN
   ↓
Evidence update
   ↓
Replanner
   ↓
New plan
```

Replanning must retain the original task correlation ID and must not silently broaden permissions.

Any new high-risk action requires a fresh policy evaluation and, where required, a fresh approval.
