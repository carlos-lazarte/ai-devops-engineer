---
type: architecture
domain: ai
technology: mcp
status: draft
---

# MCP Tooling Model

## Purpose

Define a minimal tool surface suitable for exposing the Vault to an MCP-capable AI client such as Claude.

MCP is treated as a tool interoperability layer. It does not by itself determine authorization, safe execution, or business policy.

## Initial read-only tools

```text
search_notes(query, filters, top_k)
read_note(note_id)
list_related_notes(note_id, depth)
retrieve_runbook(problem, technology)
get_context_packet(packet_id)
```

## Draft tools

```text
create_draft(note_type, title, content, metadata)
propose_patch(note_id, patch)
```

Draft tools must never commit directly to the canonical Vault without a separate review step.

## Response requirements

Every tool response should include:

- tool name
- request ID
- result status
- provenance
- source note IDs where applicable
- truncation indicator where applicable
- warnings / policy decisions

## Security boundary

```text
Claude
  ↓
MCP Client
  ↓
MCP Server / Tool Gateway
  ↓
Policy Engine
  ↓
Vault / Retrieval Services
```

The model should not receive direct unrestricted filesystem access.
