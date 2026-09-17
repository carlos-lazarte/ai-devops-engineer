# Secret Redaction Standard

Sensitive values must be replaced before material is placed into:

- Claude prompts
- Context packets
- audit logs
- metrics labels
- exception messages
- Git commits

Examples:

```text
Authorization: Bearer <REDACTED>
AWS_SECRET_ACCESS_KEY=<REDACTED>
password=<REDACTED>
private_key=<REDACTED>
```

Redaction must be applied as early as practical and re-applied at trust boundaries.
