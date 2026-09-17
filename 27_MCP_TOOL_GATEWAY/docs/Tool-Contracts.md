---
type: reference
domain: ai
technology: mcp
status: active
---

# Tool Contracts

The v0.8.0 gateway exposes five read-only tools.

## `search_notes`

Purpose: search Markdown notes by keyword or simple metadata filters.

Input:

```yaml
query: string
limit: integer 1..20
prefix: optional string
```

Output:

```yaml
status: ok|error
request_id: string
results:
  - note_id: string
    path: string
    title: string
    snippet: string
    provenance: string
truncated: boolean
```

## `read_note`

Input:

```yaml
note_id: string
```

Returns canonical path, title, metadata summary, content, and provenance.

## `list_related_notes`

Input:

```yaml
note_id: string
depth: integer 1..2
```

The reference server follows Obsidian wikilinks in Markdown. Depth is deliberately bounded.

## `retrieve_runbook`

Input:

```yaml
problem: string
technology: optional string
limit: integer 1..10
```

The reference implementation uses keyword matching over notes with `type: runbook` or the `17_RUNBOOKS` path.

## `get_context_packet`

Input:

```yaml
packet_id: string
```

In v0.8.0 the reference server resolves only local YAML/JSON packet fixtures under an explicitly allowed context directory.

## Common response rules

Every successful response includes:

- `request_id`
- `status`
- bounded output
- provenance

Every failure uses a stable error code and avoids exposing sensitive local paths beyond the configured Vault-relative path.
