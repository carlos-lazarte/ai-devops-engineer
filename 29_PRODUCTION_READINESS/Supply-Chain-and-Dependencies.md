---
type: checklist
domain: security
status: active
---
# Supply Chain and Dependencies

## Release controls

- Pin or constrain runtime dependencies appropriately for the deployment model.
- Review dependency upgrades.
- Run the test suite against a clean environment.
- Keep build artifacts and caches out of the Vault release archive.
- Record dependency versions for reproducibility.

## AI provider SDKs

Treat SDK changes as operational changes because request/response behavior, authentication, or error semantics can change.
