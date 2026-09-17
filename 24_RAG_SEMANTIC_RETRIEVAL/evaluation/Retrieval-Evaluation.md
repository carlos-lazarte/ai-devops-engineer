---
type: knowledge
domain: ai
topic: retrieval-evaluation
difficulty: intermediate
status: active
tags:
  - ai
  - rag
  - evaluation
---

# Retrieval Evaluation

A RAG system should be evaluated independently from the LLM that consumes its output.

## Evaluation set

Maintain a small, versioned set of representative DevOps questions.

Each test case should contain:

```yaml
id:
query:
expected_sources:
optional_metadata_filters:
notes:
```

## Core metrics

### Recall@K

Did the relevant source appear in the first K retrieved items?

### Precision@K

How many of the retrieved items were relevant?

### MRR

How early does the first relevant result appear?

### Context utilization

Does the final context contain the evidence actually needed to answer the question?

## Manual review criteria

For each query, inspect:

- relevance
- provenance
- duplication
- missing evidence
- metadata correctness
- whether operational risk content was surfaced

## Baseline

Start with deterministic keyword search as a baseline. Semantic retrieval should demonstrate measurable improvement on the evaluation set before it becomes the default.

## Regression rule

When changing:

- chunking
- embedding model
- metadata filters
- vector index
- reranking

rerun the evaluation set.
