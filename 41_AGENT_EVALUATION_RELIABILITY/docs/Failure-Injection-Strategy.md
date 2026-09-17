---
type: procedure
domain: ai-devops
status: active
tags:
  - reliability
  - fault-injection
---
# Failure Injection Strategy

The lab injects failures at component boundaries rather than against real infrastructure.

Scenarios:

- model timeout
- model malformed output
- retriever unavailable
- memory store unavailable
- MCP partial failure
- duplicate request
- stale memory
- cross-tenant query attempt

The expected outcome must be explicit: fail closed, return partial status with missing dependencies, or surface an actionable error without fabricating success.
