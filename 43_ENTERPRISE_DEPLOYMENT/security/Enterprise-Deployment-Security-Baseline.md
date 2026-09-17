---
type: security_policy
domain: security
difficulty: advanced
status: active
tags:
  - kubernetes
  - security
  - enterprise
---
# Enterprise Deployment Security Baseline

## Required controls

- Run as non-root.
- Read-only root filesystem where the runtime supports it.
- `allowPrivilegeEscalation: false`.
- Drop Linux capabilities unless a documented exception exists.
- Seccomp profile `RuntimeDefault`.
- Disable ServiceAccount token automount unless required.
- Isolate the namespace using NetworkPolicy where the CNI supports it.
- Keep image references immutable by digest for controlled releases.
- Keep API credentials outside the Vault and Git repository.
- Apply least privilege to ServiceAccounts and workload identities.

## Network rule

The baseline assumes ingress is allowed only from an approved gateway/ingress path and egress is limited to explicitly required destinations. The exact CIDRs and namespace selectors must be set for the target cluster.
