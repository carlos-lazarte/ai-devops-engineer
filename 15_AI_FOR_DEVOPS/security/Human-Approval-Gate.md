---
type: security
domain: ai
status: active
---

# Human Approval Gate

## Principle

AI-generated operational changes are proposals until a human reviews and approves them.

## Approval record

```yaml
approval_id: APR-YYYYMMDD-NNN
proposal_id: PROP-YYYYMMDD-NNN
reviewer: <human>
decision: approved|rejected|changes_requested
approved_scope:
  - exact operation
  - exact target
  - exact parameters
timestamp: <ISO-8601>
```

The approval applies only to the declared scope. A materially different action requires a new approval.
