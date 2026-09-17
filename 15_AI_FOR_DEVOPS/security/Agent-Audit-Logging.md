---
type: security
domain: ai
status: active
---

# Agent Audit Logging

Record enough information to reconstruct material agent activity without storing secrets unnecessarily.

## Log fields

- timestamp
- request_id
- session_id
- actor
- task_id
- tool
- argument hash or normalized safe arguments
- policy decision
- approval reference
- result status
- provenance references
- error code

## Do not log

- passwords
- private keys
- bearer tokens
- session cookies
- unredacted secrets
