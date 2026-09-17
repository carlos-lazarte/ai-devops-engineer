---
type: checklist
domain: security
status: active
---
# Security Baseline

## Identity and access

- Use least-privilege identities for Vault, retrieval, MCP, and Claude access.
- Separate developer, test, and production credentials.
- Prefer short-lived credentials where the provider supports them.
- Require explicit approval for any operation that can alter infrastructure.

## Secrets

- Never commit API keys, tokens, private keys, passwords, or kubeconfigs.
- Supply credentials through environment variables or a managed secret store.
- Redact secrets before writing evidence into the Vault.

## Tool security

- Default deny unknown tools.
- Validate tool arguments against schemas.
- Reject path traversal and unrestricted filesystem access.
- Keep read-only retrieval separate from write or execution capabilities.

## AI security

- Treat retrieved documents as untrusted input.
- Do not let document text redefine system policy.
- Preserve provenance for material claims.
- Require human validation for operational actions.

## Release security

- Review dependency changes.
- Keep generated caches out of releases.
- Review the release tree before packaging.
