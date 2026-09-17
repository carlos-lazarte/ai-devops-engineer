---
type: architecture
domain: ai
technology: mcp
status: draft
---

# MCP Server Boundary

## Boundary

The MCP server is a controlled gateway, not a generic shell proxy.

```text
Claude
  |
  | MCP
  v
Tool Gateway
  |
  +--> Policy Engine
  |
  +--> Retriever
  |
  +--> Vault Service
  |
  +--> Audit Log
```

## Initial scope

Read-only retrieval plus draft creation.

## Out of scope

- arbitrary command execution
- unrestricted network requests
- secret management
- direct production changes

## Audit data

At minimum:

- timestamp
- request ID
- principal / session identifier
- tool
- normalized arguments
- decision
- result status
- source references
