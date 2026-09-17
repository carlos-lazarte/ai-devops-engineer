---
type: security
domain: ai
status: active
---

# Tool Call Validation

Every tool request should pass validation before execution.

## Checks

```text
Schema validation
     ↓
Authorization
     ↓
Scope validation
     ↓
Path / resource allow-list
     ↓
Size / rate limits
     ↓
Redaction policy
     ↓
Execution
```

## Reject

- unknown tool
- unknown argument
- invalid path
- path traversal
- excessive result size
- missing required approval
- attempts to bypass policy
