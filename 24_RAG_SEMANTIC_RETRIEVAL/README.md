# RAG & Semantic Retrieval

This module defines the semantic retrieval layer for the AI DevOps Engineer Vault.

## Goal

Turn the Markdown Vault into a searchable knowledge source that can supply relevant, traceable context to an LLM.

## Pipeline

```text
Obsidian Markdown
      |
      v
Parse + Normalize
      |
      v
Chunking
      |
      v
Metadata extraction
      |
      v
Embeddings
      |
      v
Vector index
      |
      v
Semantic retrieval
      |
      v
Metadata filtering + reranking
      |
      v
Context assembly
      |
      v
Claude / LLM
```

## Design principles

1. Retrieval is not generation.
2. Every retrieved chunk keeps source provenance.
3. Metadata filters narrow the search space before generation.
4. Retrieval quality must be measured with a small evaluation set.
5. The LLM receives evidence and source paths, not anonymous text blobs.
6. The prototype should be replaceable: embeddings, vector store and model are implementation details.

## v0.5.0 scope

- Local-first reference architecture.
- Markdown chunking strategy.
- Metadata-aware retrieval.
- Context packet assembly.
- Evaluation dataset and metrics.
- Minimal Python prototype.

See [[RAG-Architecture]], [[Chunking-Strategy]], [[Retrieval-Evaluation]], and [[Context-Assembly]].
