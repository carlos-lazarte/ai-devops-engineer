# Environment Boundary

Treat `dev`, `test`, `staging` and `prod` as separate authorization domains.

A principal authorized for `dev` should not inherit `prod` permissions automatically.

Recommended policy inputs:

```text
principal
role
tenant_id
environment
tool
operation
risk
approval_id
```
