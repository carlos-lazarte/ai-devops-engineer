---
type: runbook
domain: operations
status: active
---
# Backup and Restore

## Objective

Recover the Vault, configuration, evaluation fixtures, and required automation from a known-good version.

## Backup scope

Include:

- Markdown knowledge.
- YAML/JSON schemas.
- Python tooling.
- CI configuration.
- Release metadata.

Exclude:

- API credentials.
- Temporary caches.
- Python bytecode.
- Local vector indexes unless intentionally versioned.

## Restore procedure

1. Obtain the release archive or Git tag.
2. Verify archive integrity.
3. Restore into a clean directory.
4. Run `python3 30_AUTOMATION/validate_vault.py --root .`.
5. Run the automated test suite.
6. Validate the RAG index can be rebuilt.
7. Record the recovery result.

## Recovery objective

Define deployment-specific RPO/RTO before production adoption. This repository does not assume values for your environment.
