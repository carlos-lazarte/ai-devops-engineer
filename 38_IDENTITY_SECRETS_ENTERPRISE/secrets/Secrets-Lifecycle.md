# Secrets Lifecycle

```text
Create
  ↓
Store in secret manager
  ↓
Reference by identifier
  ↓
Retrieve just-in-time
  ↓
Use in memory
  ↓
Zeroize where practical
  ↓
Rotate
  ↓
Revoke
```

## Rules

- Never commit secret values to Git.
- Never place secrets in Markdown notes.
- Never send secret values to Claude unless an explicit, reviewed integration requires it; the default is redaction.
- Avoid writing secrets to logs, traces, metrics or audit events.
- Prefer short TTLs and automatic rotation.
