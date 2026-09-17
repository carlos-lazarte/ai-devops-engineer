# Secret Handling & Redaction

Never place API keys, passwords, access tokens, private keys or production credentials inside the Vault.

Before storing or sending evidence to an LLM:

1. detect known sensitive fields;
2. redact values while preserving field names and structural context;
3. log metadata about redaction, not the secret itself;
4. keep the original secret in an approved secret-management system.

Example:

```text
Authorization: Bearer <REDACTED>
password: <REDACTED>
api_key: <REDACTED>
```
