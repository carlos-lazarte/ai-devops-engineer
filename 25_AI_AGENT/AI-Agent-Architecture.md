---
type: architecture
domain: ai
topic: agent
status: draft
---

# AI Agent Architecture

## Goal

Define a controlled AI agent that can retrieve knowledge from the Obsidian Vault, inspect structured evidence, generate drafts, and propose changes without obtaining unrestricted write or execution access.

## Core flow

```text
User Request
    ↓
Intent / Scope
    ↓
Policy Check
    ↓
Tool Selection
    ↓
Read-only Retrieval
    ↓
Context Assembly
    ↓
Claude / LLM Reasoning
    ↓
Structured Result
    ↓
Human Approval (when required)
    ↓
Draft / Proposed Action
```

## Design principles

1. Read before write.
2. Least privilege.
3. Explicit provenance for retrieved evidence.
4. No destructive action without an approval gate.
5. Tool arguments are validated before execution.
6. The model cannot silently convert uncertainty into fact.
7. Every material action is auditable.

## Agent capabilities

- Search notes semantically or by metadata.
- Read relevant notes.
- Retrieve runbooks and troubleshooting procedures.
- Assemble Context Packets.
- Draft new notes.
- Propose patches to notes.
- Produce structured incident analysis.

## Explicitly disabled by default

- Shell execution on production systems.
- Arbitrary filesystem writes.
- Secret retrieval.
- Credential discovery.
- Destructive infrastructure actions.
- Automatic deployment.

## Related

[[AI-DevOps-Context-Protocol]]
[[Claude-Integration-Architecture]]
[[AI-Structured-Response-Contract]]
[[MCP-Tooling-Model]]
[[Agent-Permissions-Policy]]
