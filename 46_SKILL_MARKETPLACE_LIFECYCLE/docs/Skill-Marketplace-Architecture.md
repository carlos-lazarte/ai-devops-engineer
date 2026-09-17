# Skill Marketplace & Lifecycle Architecture

Version: v2.4.0

## Purpose
Define how DevOps Skills are packaged, published, discovered, installed, upgraded, deprecated, and retired without weakening the platform's security or evaluation controls.

## Lifecycle

```text
Author
  ↓
Develop
  ↓
Validate contract
  ↓
Run skill tests
  ↓
Run evaluation set
  ↓
Package
  ↓
Sign artifact
  ↓
Publish to registry
  ↓
Compatibility check
  ↓
Install
  ↓
Operate / Observe
  ↓
Upgrade or Deprecate
  ↓
Retire
```

## Design principles

1. A Skill is independently versioned.
2. The platform remains the final policy authority.
3. Installing a Skill never grants permissions by itself.
4. Dependencies and capabilities are explicit.
5. Every release must be reproducible and auditable.
6. Evaluation evidence travels with the artifact.

## Trust boundaries

```text
Marketplace Registry
        │
        │ signed artifact
        ▼
Local Trust Verification
        │
        ▼
Compatibility Gate
        │
        ▼
Policy Engine
        │
        ▼
Skill Runtime
```

The registry is a distribution source, not an authorization source.
