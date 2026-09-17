---
type: reference
domain: ai
status: active
---

# Tool Response Contract

## Required envelope

```json
{
  "request_id": "string",
  "tool": "string",
  "status": "ok|denied|error|partial",
  "data": {},
  "provenance": [],
  "warnings": [],
  "truncated": false
}
```

## Provenance object

```json
{
  "source_id": "string",
  "path": "string",
  "section": "string|null"
}
```

## Principles

- Responses are machine-readable.
- Errors are explicit.
- Partial data is marked as partial.
- Provenance is preserved whenever content originates from the Vault.
