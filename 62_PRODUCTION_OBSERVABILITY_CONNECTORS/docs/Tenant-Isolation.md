# Tenant and Environment Isolation

The connector layer treats `tenant_id` and `environment` as explicit data-plane boundaries. They are not inferred from arbitrary labels.

Rules:

1. Every telemetry submission must identify a tenant and environment.
2. Prometheus credentials/URLs must be scoped to the same approved environment.
3. Kubernetes credentials should be namespace/cluster scoped as narrowly as possible.
4. Connector health must not disclose secrets.
5. Incident correlation must preserve the tenant/environment boundary.
6. Cross-tenant access is a policy/security failure even when the underlying telemetry endpoint would technically allow it.
