---
type: architecture
domain: ai
task: knowledge-graph
status: active
tags:
  - knowledge-graph
  - rag
  - context
---
# Knowledge Graph Architecture

The Knowledge Graph layer models the Vault as a graph of notes, concepts, operational procedures, evidence references and Skills.

## Goals

- Connect related knowledge without replacing Markdown as the source of truth.
- Make context selection explainable.
- Distinguish permanent knowledge from runtime evidence and agent memory.
- Feed the RAG/context layer with graph-aware candidates.

## Graph sources

1. Markdown wikilinks: `[[Target Note]]`.
2. Frontmatter metadata: `type`, `domain`, `technology`, `tags`.
3. Skill registry metadata under `47_KNOWLEDGE_SKILL_MARKETPLACE_INTELLIGENCE/`.

## Node classes

- `knowledge` — concepts and technology notes.
- `procedure` / `runbook` — operational knowledge.
- `incident` / `evidence` — runtime material.
- `workflow` / `architecture` — system relationships.
- `skill` — reusable agent capability.

## Edge semantics

The baseline parser produces explicit edges for wikilinks. Metadata-derived relationships are represented as attributes, not invented edges, unless the source explicitly declares them.

## Source of truth

The Vault remains authoritative. The graph is a derived index and can be regenerated at any time.
