# Security & Governance Architecture

```text
Identity / Principal
        |
        v
Request Context
        |
        v
Policy Engine
   |       |
   |       +--> Risk Classification
   +----------> Authorization
        |
        v
Approval Gate (when required)
        |
        v
MCP Tool Gateway
        |
        v
Vault / RAG / Draft Store
        |
        v
Audit Event
```

## Design rules

1. Deny by default.
2. Tool authorization is explicit per role.
3. Risk is attached to the tool, not inferred from natural-language intent alone.
4. Approval IDs are required for change proposals.
5. Direct execution tooling is disabled in the baseline.
6. Audit events record decisions without storing raw secrets.
