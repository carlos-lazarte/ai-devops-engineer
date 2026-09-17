---
type: architecture
domain: ai
status: draft
tags:
  - ai
  - agents
  - obsidian
  - mcp
---

# AI Agent with Obsidian Tools

## Objective

Provide a conceptual architecture for a controlled agent that can read selected Vault content and propose updates without unrestricted filesystem access.

## Architecture

```text
Claude / AI Client
        |
        | tool call
        v
Tool Gateway / MCP Server
        |
   +----+----+
   |         |
  READ     WRITE
   |         |
   v         v
Vault      Review Queue
   |         |
   +----+----+
        |
        v
Human approval
```

## Tool policy

Prefer narrow tools such as:

```text
search_notes()
read_note()
list_related_notes()
create_draft()
propose_patch()
```

Avoid giving the agent unrestricted shell, filesystem or production-control access merely to simplify integration.

## Write model

```text
AI proposal
   ↓
Diff / preview
   ↓
Human approval
   ↓
Write to Vault
   ↓
Git commit / audit trail
```

## Related

[[AI-Context-RAG-for-DevOps]]
[[Claude-Integration-Architecture]]
