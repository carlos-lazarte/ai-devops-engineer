# Identity, Secrets & Enterprise Integration

Version: 1.6.0

This layer defines the enterprise boundary for the AI DevOps runtime. It keeps identity, credentials, tenancy and audit concerns outside the Obsidian knowledge base and exposes only short-lived, least-privileged capabilities to the runtime.

## Core principles

- Obsidian contains knowledge, never operational credentials.
- Human and workload identity are authenticated before authorization.
- Long-lived secrets are avoided in application configuration.
- Short-lived credentials are preferred for runtime access.
- Tenant and environment boundaries are explicit policy inputs.
- Secret values are never copied into model context, logs or prompts.
- The policy engine remains the final authorization point.
- Enterprise adapters are interfaces and reference implementations, not claims of production deployment.

## Components

- `identity/` — principal, claims and OIDC/JWT validation model.
- `secrets/` — secret lifecycle, references, rotation and redaction.
- `enterprise/oidc/` — OIDC integration contract.
- `enterprise/tenancy/` — tenant/environment isolation model.
- `policies/` — enterprise policy rules and decision inputs.
- `schemas/` — machine-readable contracts.
- `adapters/` — reference adapters for Vault and Kubernetes-style secret references.
- `tests/` — local policy and redaction tests.

## Non-goals

This release does not implement a specific identity provider, deploy a secret manager, or grant production infrastructure access.
