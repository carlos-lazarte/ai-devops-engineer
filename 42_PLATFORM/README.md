---
type: architecture
domain: platform
status: active
---

# v2.0.0 Platform Layer

`42_PLATFORM` is the stable integration boundary for the Production AI DevOps Platform. It defines service responsibilities, API contracts, deployment profiles, compatibility, configuration and conformance checks.

## Stable interfaces

- HTTP API: `api/v1`
- Service configuration: `config/platform.yaml`
- Runtime response contract: `api/v1/runtime-openapi.yaml`
- Conformance: `conformance/`

## Design rule

The platform must remain modular: the Obsidian Vault is a knowledge artifact, while runtime services are replaceable implementations behind explicit contracts.
