# Local Development Workflow

```text
Clone
  ↓
Bootstrap
  ↓
Edit Vault
  ↓
Validate
  ↓
Test
  ↓
Rebuild RAG index (when applicable)
  ↓
Review diff
  ↓
Release check
  ↓
Package
```

## Principles

- Local commands should mirror CI commands.
- Generated indexes belong outside release source content unless explicitly versioned.
- A release is reproducible from a clean Git checkout.
- Any tool that can modify operational content should default to dry-run behavior.
