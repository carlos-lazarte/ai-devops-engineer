---
type: example
domain: ai
technology: mcp
status: prototype
---

# MCP Read-Only Reference Server

This document describes a future implementation target, not a production server.

## Minimal interface

```text
search_notes
read_note
list_related_notes
retrieve_runbook
```

## Implementation shape

```text
MCP request
    ↓
Input validation
    ↓
Authorization
    ↓
Retriever
    ↓
Provenance enrichment
    ↓
Response contract
```

## Acceptance criteria

- No unrestricted filesystem access.
- Deterministic path allow-list.
- Bounded result size.
- Provenance on every retrieved note.
- Explicit error responses.
