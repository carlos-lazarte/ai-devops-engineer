---
type: knowledge
domain: ai
topic: retrieval-filters
difficulty: intermediate
status: active
tags:
  - ai
  - rag
  - metadata
---

# Metadata Filters

Semantic similarity alone is not enough for operational retrieval.

## Filter examples

```yaml
domain: kubernetes
type: troubleshooting
status: active
```

or:

```yaml
technology: terraform
type: runbook
risk: high
```

## Recommended order

```text
User query
   |
   v
Explicit constraints
   |
   v
Metadata filtering
   |
   v
Semantic retrieval
   |
   v
Optional reranking
```

## Why filters matter

A query such as:

> Kubernetes node is NotReady

should prefer active Kubernetes troubleshooting and runbook notes over unrelated historical incident notes.

## Do not over-filter

If metadata coverage is incomplete, hard filters can eliminate useful evidence. Treat filters as constraints only when the user or workflow provides enough information.
