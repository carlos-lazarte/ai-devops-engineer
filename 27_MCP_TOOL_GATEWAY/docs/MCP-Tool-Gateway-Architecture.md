---
type: architecture
domain: ai
technology: mcp
difficulty: advanced
status: active
tags:
  - ai
  - mcp
  - agents
  - security
---

# MCP Tool Gateway Architecture

## Objective

Create a controlled boundary between an MCP-capable AI client and the Obsidian Vault.

## Reference flow

```text
Claude / MCP Client
        |
        v
   MCP Transport
        |
        v
  Request Validator
        |
        v
   Policy Engine
        |
        +------> Audit Logger
        |
        v
     Tool Router
        |
   +----+----+----------------+
   |         |                |
   v         v                v
Search      Read         Relationships
Notes      Note             / Runbooks
   |         |                |
   +---------+----------------+
             |
             v
        Vault Service
             |
             v
      Obsidian Markdown
```

## Security boundary

The gateway must operate with an explicit Vault root and a canonical-path allow-list. The model never receives direct filesystem primitives such as arbitrary `open`, `exec`, or unrestricted path traversal.

## Trust model

The LLM is treated as an untrusted caller. User intent and tool arguments are validated independently of the model's natural-language explanation.

## Design principles

- Default deny.
- Read before write.
- Least privilege.
- Bounded inputs and outputs.
- Provenance for every retrieved artifact.
- Deterministic rejection of invalid paths.
- Audit material tool calls.
- No secrets in logs or tool responses.
- Human approval remains required for any future mutation capability.

## Future extension

The same gateway can later expose a vector retriever or an approved draft service, but each new capability must add its own contract, policy, tests, and audit semantics.
