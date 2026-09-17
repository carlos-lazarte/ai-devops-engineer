---
type: troubleshooting
domain: ai
topic: federation
status: active
tags:
  - mcp
  - troubleshooting
  - distributed-systems
---

# Federation Failure Modes

## Unknown agent

Return a denial; do not guess another agent.

## Disabled MCP server

Return a denial or degraded result depending on task requirements.

## Cross-tenant delegation

Reject the request.

## Context mismatch

Reject or quarantine the task when tenant/environment changes unexpectedly.

## Partial multi-agent result

Return a structured partial result with the missing delegation explicitly recorded.
