---
type: schema
domain: ai
technology: mcp
status: active
---

# Audit Event Schema

A reference audit event may contain:

```yaml
schema_version: "1.0"
timestamp: "2026-09-16T00:00:00Z"
request_id: "req-..."
session_id: "sess-..."
actor: "mcp-client"
tool: "search_notes"
decision: allowed|denied
result_status: ok|error
safe_arguments:
  query: "kubernetes node notready"
  limit: 5
provenance:
  - "05_KUBERNETES/..."
error_code: null
```

Do not persist secrets, authentication headers, private keys, session cookies, or raw credentials.
