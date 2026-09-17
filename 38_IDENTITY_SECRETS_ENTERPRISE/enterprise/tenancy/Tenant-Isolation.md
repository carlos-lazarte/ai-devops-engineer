# Tenant Isolation

Tenant identity must be an explicit part of the request context.

```yaml
request_context:
  tenant_id: acme
  environment: prod
  principal: user-123
```

Every retrieval, audit event and tool authorization decision should preserve tenant and environment scope.

## Isolation rules

- Do not allow caller-provided tenant changes after authentication.
- Do not retrieve knowledge across tenant boundaries unless the policy explicitly allows a shared/public scope.
- Partition indexes and audit records by tenant when multi-tenancy is enabled.
