---
type: architecture
domain: ai
technology: rag
difficulty: intermediate
status: active
tags:
  - ai
  - rag
  - retrieval
  - obsidian
---

# RAG Architecture for the AI DevOps Engineer Vault

## Objective

Provide an architecture that retrieves relevant Vault knowledge and packages it into a traceable context for an LLM.

## Components

### 1. Source layer

The authoritative source is the Obsidian Markdown Vault.

### 2. Ingestion layer

Responsible for:

- discovering `.md` files
- reading frontmatter
- normalizing Markdown
- extracting headings
- generating stable chunk identifiers
- preserving source paths

### 3. Embedding layer

Each chunk is transformed into a vector representation. The implementation must record the embedding model used so an index can be rebuilt deterministically.

### 4. Vector index

Stores:

- vector
- chunk text
- chunk id
- source path
- heading
- metadata

### 5. Retrieval layer

A query is transformed into an embedding and matched against indexed chunks.

Recommended retrieval flow:

```text
query
  |
  +--> metadata filters
  |
  v
vector search
  |
  v
candidate set
  |
  v
optional reranking
  |
  v
Top-K evidence
```

### 6. Context assembly

Retrieved chunks are converted into a Context Packet compatible with [[AI-DevOps-Context-Protocol]].

## Provenance requirement

Every retrieved chunk must contain:

```text
source_path
chunk_id
heading
retrieval_score
content
```

Never strip provenance before sending context to an LLM.

## Security boundary

The retrieval service should not expose the complete filesystem to the model. The model receives only the selected context.

## Replacement principle

The system should allow these components to be replaced independently:

```text
Markdown parser
Embedding model
Vector store
Reranker
LLM
```

## Related

- [[AI-DevOps-Context-Protocol]]
- [[Context-Assembly]]
- [[Metadata-Filters]]
- [[Retrieval-Evaluation]]
