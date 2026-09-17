# Threat Scenarios

| Scenario | Baseline control |
|---|---|
| Prompt injection asks agent to ignore policy | policy engine remains authoritative |
| Unauthorized tool call | deny by default |
| Path traversal | MCP/Vault path validation |
| Credential leakage | redaction + external secrets management |
| Privilege escalation | role/risk checks |
| Unapproved production change | approval gate + execution disabled |
| Audit tampering | external append-only audit target recommended for production |
