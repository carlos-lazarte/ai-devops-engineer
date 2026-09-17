---
type: policy
domain: platform
status: active
---

# Compatibility Policy

## API

- `/api/v1/*` is the stable integration surface for v2.x.
- Additive response fields are allowed when clients are expected to ignore unknown fields.
- Removing or changing field semantics requires a new API version.

## Runtime

- Existing unversioned routes are retained as compatibility aliases in v2.0.0.
- New consumers should migrate to versioned routes.

## Contracts

Schema and tool contracts are versioned independently from implementation details.
