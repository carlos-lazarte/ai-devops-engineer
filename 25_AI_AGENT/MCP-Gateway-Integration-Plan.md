---
type: architecture
domain: ai
technology: mcp
status: active
---

# MCP Gateway Integration Plan

## Current state

`27_MCP_TOOL_GATEWAY/` is the reference implementation boundary.

## Integration sequence

```text
1. Tool contract
       ↓
2. Policy rule
       ↓
3. Reference implementation
       ↓
4. Unit / negative tests
       ↓
5. MCP SDK interoperability test
       ↓
6. Claude client test
       ↓
7. Optional draft tools
       ↓
8. Independent approval service
```

## Non-goals

A successful local test does not imply production authorization or operational safety.

## Related

[[27_MCP_TOOL_GATEWAY/docs/MCP-Tool-Gateway-Architecture]]
[[Agent-Permissions-Policy]]
[[MCP-Tooling-Model]]
[[Human-Approval-Gate]]
