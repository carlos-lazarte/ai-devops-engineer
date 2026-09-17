---
type: architecture
domain: ai
task: context-intelligence
status: active
tags:
  - context
  - rag
  - knowledge-graph
---
# Context Intelligence Architecture

Context Intelligence combines graph proximity, lexical relevance, note metadata and Skill candidates before constructing a model context packet.

```text
Task
 ↓
Intent signals
 ↓
Graph retrieval + lexical retrieval
 ↓
Neighbor expansion
 ↓
Skill discovery
 ↓
Policy / compatibility checks
 ↓
Deduplication + provenance
 ↓
Context budget
 ↓
Claude / LLM
```

## Design rule

Retrieval determines what is relevant; policy determines what is allowed. Memory can improve context but cannot grant authorization.

## Context classes

- `knowledge`: durable, curated material.
- `procedure`: actionable operational instructions.
- `evidence`: incident-specific facts or observations.
- `memory`: historical state, decisions or episodes.
- `skill`: capability definition, not permission.

## Explainability

Each selected context item should include a reason such as direct lexical match, graph neighbor, shared technology, shared incident or Skill match.
