---
type: workflow
domain: ai
topic: rag
difficulty: intermediate
status: active
tags:
  - ai
  - rag
---

# RAG Quickstart

## What this adds

v0.5.0 adds a reference semantic retrieval layer so the Vault can provide targeted context to an LLM.

## Start here

1. Read [[RAG-Architecture]].
2. Read [[Chunking-Strategy]].
3. Review [[Retrieval-Evaluation]].
4. Inspect [[Context-Assembly]].
5. Run the prototype scripts from `24_RAG_SEMANTIC_RETRIEVAL/scripts/`.

## Prototype

```bash
python build_index.py --vault /path/to/Vault --index /path/to/_rag/index
python search.py --index /path/to/_rag/index --query "Kubernetes node NotReady"
```

The prototype is deliberately local-first and provider-neutral. It is not a production service.

## Success criterion

Before integrating an LLM, semantic retrieval should consistently return the correct Troubleshooting and Runbook notes for the evaluation set.
