---
type: knowledge
domain: ai
topic: chunking
difficulty: intermediate
status: active
tags:
  - ai
  - rag
  - chunking
---

# Chunking Strategy

## Objective

Create retrieval units that are semantically coherent, small enough for retrieval, and large enough to preserve operational meaning.

## Default strategy

Prefer structure-aware chunks rather than arbitrary character windows.

Primary boundaries:

1. H1/H2/H3 headings
2. fenced code blocks
3. tables
4. paragraphs
5. list blocks

## Recommended hierarchy

```text
Note
  |
  +-- Heading
        |
        +-- Section
              |
              +-- Content block(s)
```

A chunk should normally contain:

```text
note title
section heading
relevant content
```

## Avoid

- splitting shell commands away from the explanation they support
- splitting a diagnosis away from the evidence that justifies it
- mixing unrelated headings into one chunk
- creating one giant chunk for an entire note

## Stable identifiers

Use a deterministic id such as:

```text
sha256(source_path + heading + ordinal)
```

This makes index updates easier to reconcile.

## Metadata to preserve

```yaml
type:
domain:
technology:
version:
difficulty:
status:
source_path:
heading:
chunk_id:
```

## Operational documents

For runbooks and troubleshooting notes, prefer chunks that preserve the complete local procedure step, diagnostic evidence, or decision branch.

## Quality test

Given a query, a human should be able to identify why the chunk was returned without needing the entire Vault.
