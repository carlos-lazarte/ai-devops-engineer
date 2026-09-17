---
type: architecture
domain: security
status: active
---
# Threat Model

## Assets

- Knowledge contained in the Vault.
- Operational evidence.
- AI provider credentials.
- MCP tool permissions.
- Proposed operational changes.
- Audit records.

## Trust boundaries

```text
User
  |
  v
Claude / LLM
  |
  v
MCP Gateway
  |
  +--> Policy Engine
  |
  +--> Retrieval
  |
  v
Obsidian Vault
```

## Primary threats

| Threat | Control |
|---|---|
| Secret leakage | Redaction + secret-handling policy |
| Prompt injection in documents | Treat documents as data; policy remains authoritative |
| Unauthorized tool use | Default-deny registry + schema validation |
| Path traversal | Canonical path validation |
| Hallucinated diagnosis | Fact/observation/hypothesis separation |
| Unsafe change execution | Human approval gate |
| Data loss | Backup and restore procedure |
| Supply-chain compromise | Dependency review and release validation |

## Residual risk

Production risk remains environment-specific. Cloud accounts, Kubernetes clusters, secret managers, network controls, and external AI providers require their own threat assessment.
