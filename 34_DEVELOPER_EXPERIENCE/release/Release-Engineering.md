# Release Engineering

## Release inputs

- Git commit / tag
- Vault content
- Validation results
- Test results
- RAG evaluation results when applicable

## Release gates

```text
validate → test → rag-check → release-check → package
```

## Release artifact rules

The package must not contain:

- `.git/`
- Python cache directories
- generated temporary files
- local environment files such as `.env`
- secrets or credentials
- local RAG indexes unless explicitly requested for the distribution

## Verification

After packaging, inspect the archive and verify that the expected root directory and essential files are present.
