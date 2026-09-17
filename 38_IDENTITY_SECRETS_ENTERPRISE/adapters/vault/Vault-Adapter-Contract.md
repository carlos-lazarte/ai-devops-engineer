# Secrets Manager Adapter Contract

Reference interface for a Vault/secret-manager adapter:

```text
resolve(secret_ref) -> opaque in-memory value
renew(secret_ref)  -> refreshed value
revoke(secret_ref) -> confirmation without secret material
```

The adapter must:

- authenticate using workload identity where available;
- enforce namespace/path policy;
- reject unapproved references;
- never log returned secret values;
- return structured errors without echoing secrets.
