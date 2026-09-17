# RAG Prototype Scripts

These scripts are a reference implementation, not a production service.

## Intended workflow

```text
python build_index.py --vault ./Vault --index ./_rag/index
python search.py --index ./_rag/index --query "Kubernetes node NotReady"
```

The example uses a local embedding model and a simple persistent vector store abstraction.

Before production use, add:

- secret management
- access control
- index versioning
- structured logging
- test coverage
- retrieval evaluation
- rebuild/rollback procedure
