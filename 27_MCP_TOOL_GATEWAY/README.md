---
type: architecture
domain: ai
technology: mcp
status: prototype
---

# 27 — MCP Tool Gateway

This module defines a local-first, read-only MCP-style tool gateway for the Vault.

## Goal

Provide a narrow interface between an AI client and the Obsidian knowledge base without granting unrestricted filesystem, shell, network, or production access.

## Scope of v0.8.0

- Tool discovery metadata.
- JSON request/response contracts.
- Read-only Vault search and note retrieval.
- Related-note traversal.
- Runbook retrieval.
- Deterministic policy checks.
- Safe path allow-listing.
- Audit records without secrets.
- Local reference server for protocol experimentation.
- Test fixtures and negative security cases.

## Explicitly out of scope

- Arbitrary shell execution.
- Production infrastructure access.
- Secrets retrieval.
- Automatic writes to the canonical Vault.
- Deployment automation.
- Internet access from the gateway.

## Start here

1. [[docs/MCP-Tool-Gateway-Architecture]]
2. [[docs/Tool-Contracts]]
3. [[security/MCP-Request-Policy]]
4. [[server/Reference-Gateway-Quickstart]]
5. [[examples/Example-Tool-Session]]
