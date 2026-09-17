---
type: architecture
domain: platform
status: active
---

# Deployment Profiles

## Local

Single-host Docker Compose for development, demos and controlled evaluation.

## Hardened Enterprise

Reference requirements before production use:

- TLS at the ingress boundary
- OIDC/OAuth2 identity integration
- secret manager integration with rotation
- network segmentation and egress controls
- non-root runtime where supported by the target image
- pinned container image digests
- centralized logs, metrics and traces
- backup and restore tests
- policy and audit retention controls
- disaster recovery validation

This document defines requirements; it does not claim that the reference package satisfies them automatically.
