# Tenant Budgeting

Budgets are isolated by tenant and environment.

Example:

```text
tenant-a / lab
tenant-a / prod
tenant-b / lab
```

Usage in one scope must not be counted as authorization for another scope.

Budget inheritance is explicit and auditable; implicit cross-tenant inheritance is forbidden.
