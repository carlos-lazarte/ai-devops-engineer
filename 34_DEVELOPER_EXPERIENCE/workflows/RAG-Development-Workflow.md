# RAG Development Workflow

RAG-related changes must be evaluated as retrieval changes, not only as text changes.

```text
Content change
   ↓
Metadata/chunking review
   ↓
Rebuild index
   ↓
Run evaluation set
   ↓
Inspect failed queries
   ↓
Approve or revise
```

The evaluation set in `24_RAG_SEMANTIC_RETRIEVAL/evaluation/evaluation-set.yaml` is the baseline for regression checks.
