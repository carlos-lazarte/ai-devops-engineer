---
type: reference
domain: ai
technology: mcp
status: active
tags:
  - mcp
  - federation
  - adapter
---

# MCP Server Adapter Contract

An adapter maps a registered logical server to a concrete MCP client/server implementation.

## Required behaviors

1. Preserve `correlation_id`.
2. Carry tenant and environment context.
3. Reject unregistered capabilities.
4. Never expose secrets to the Vault.
5. Return structured errors.
6. Emit an audit event for authorization decisions.

## Network/authentication

Transport security, endpoint authentication and certificate validation are deployment-specific and must not be inferred from this reference contract.
