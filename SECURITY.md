# Security Policy

## Scope

Security issues include authentication bypasses, tenant-isolation failures, unintended infrastructure mutation, credential leakage, unsafe connector behavior and vulnerabilities that could cause unauthorized execution.

## Responsible disclosure

Do not publish credentials, production data or exploit instructions in a public issue. Use the repository's private security reporting mechanism when available, or contact the maintainers privately through the project owner.

## Security boundary

The Community Edition reference runtime keeps production execution disabled. Connectors are read-only by default, and the approval boundary remains separate from model output.
