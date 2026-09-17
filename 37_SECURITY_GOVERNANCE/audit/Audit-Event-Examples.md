# Audit Event Examples

```json
{
  "event": "authorization_decision",
  "request_id": "REQ-004",
  "principal": "alice",
  "role": "operator",
  "tool": "propose_change",
  "decision": "allow",
  "risk": "high",
  "approval_id": "APR-004",
  "policy_version": "1.0"
}
```

Do not include raw passwords, access tokens, private keys, or complete secret-bearing payloads.
