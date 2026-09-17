---
type: architecture
domain: ai
technology: runtime
status: active
---

# Deployment Model

## Local

Use the Python runtime directly for development and demos.

## Containerized

Use `docker compose up --build` for a reproducible local stack. The container runs with the Vault mounted read-only.

## Enterprise hardening still required

A target production environment must separately validate:

- identity and authentication;
- TLS termination and certificate rotation;
- secret storage and rotation;
- resource limits and concurrency;
- network policy and egress restrictions;
- centralized logs and metrics;
- backup / restore;
- dependency pinning and image scanning;
- data retention and privacy requirements.

The runtime intentionally does not claim those properties are solved by the reference package alone.
