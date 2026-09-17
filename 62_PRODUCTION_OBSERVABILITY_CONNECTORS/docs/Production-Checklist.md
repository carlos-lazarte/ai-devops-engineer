# Production Checklist

- [ ] Explicit telemetry tenants and environments.
- [ ] Dedicated read-only credentials.
- [ ] TLS certificate validation enabled.
- [ ] Egress allow-list in network policy.
- [ ] Request timeout configured.
- [ ] Response-size limit configured.
- [ ] Retry count bounded.
- [ ] Rate limiting configured.
- [ ] Connector health exposed to monitoring.
- [ ] Secrets injected by the deployment platform, not stored in Git.
- [ ] Audit provenance retained.
- [ ] Human approval required for remediation.
- [ ] Production execution remains disabled until a separate change-control phase.
