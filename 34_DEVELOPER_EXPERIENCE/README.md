---
type: reference
domain: developer-experience
status: active
---
# Developer Experience & Distribution

This section defines the reproducible workflow for maintaining, validating, indexing and releasing the AI DevOps Engineer Vault.

## Goals

- Make local development deterministic.
- Keep content changes reviewable through Git.
- Run the same validation locally and in CI.
- Build RAG indexes from the Vault in a reproducible way.
- Produce a clean release artifact without caches, secrets or development-only files.

## Main commands

```bash
make bootstrap
make validate
make test
make rag-index
make release-check
make package
```
