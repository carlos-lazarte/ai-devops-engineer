# Contributing

## Workflow

1. Create a topic branch.
2. Change content or tooling.
3. Run `make validate` and `make test`.
4. For RAG-impacting changes, run `make rag-index` and `make rag-check`.
5. Review the generated diff.
6. Open a pull request.

## Content rules

- Use the correct note type and metadata contract.
- Prefer one operational concept per note.
- Link related notes with real semantic relationships.
- Separate facts, observations, hypotheses and proposed actions.
- Do not commit secrets, credentials, tokens or production data.
- Do not silently change an existing runbook's operational meaning.

## Commit guidance

Use small, focused commits. A content-only change and a tooling change should normally be separate commits when practical.
