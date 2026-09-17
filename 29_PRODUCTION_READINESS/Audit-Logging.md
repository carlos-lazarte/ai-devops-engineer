---
type: reference
domain: security
status: active
---
# Audit Logging

Every material agent/tool interaction should be represented by an append-only audit event in the runtime system.

## Minimum fields

```yaml
id: "event-id"
timestamp: "RFC3339"
actor: "user-or-service"
request_type: "agent-task"
tool: "search_notes"
arguments_digest: "sha256:..."
resource: "relative/path"
result: "allowed|denied|error|success"
approval: "not-required|required|approved|rejected"
correlation_id: "..."
```

## Data minimization

Do not store raw secrets or unnecessary sensitive payloads. Prefer hashes/digests for arguments when the original value is not needed for auditability.
