---
type: reference
domain: ai
status: active
---

# search_notes Tool Specification

## Input

- `query`: required string
- `filters`: optional metadata filters
- `top_k`: integer, bounded by server policy

## Output

A ranked collection of note references with excerpts, metadata, and provenance.

## Server-side controls

- Limit maximum `top_k`.
- Enforce path allow-list.
- Apply metadata filters server-side.
- Redact configured sensitive content.
- Record request ID.
