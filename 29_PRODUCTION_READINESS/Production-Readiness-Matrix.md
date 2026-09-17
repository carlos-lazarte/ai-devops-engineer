---
type: reference
domain: operations
status: active
---
# Production Readiness Matrix

This matrix is the release gate for the Vault and its supporting tooling. A version is not considered production-ready merely because documentation exists; controls must be implemented, tested, and evidenced.

| Area | Required outcome | Evidence for v1.0.0 | Status |
|---|---|---|---|
| Versioning | Immutable release identifier | Git tag + CHANGELOG | ready |
| Knowledge integrity | Detect broken/unsafe links and malformed frontmatter | `validate_vault.py` | ready |
| RAG safety | Retrieval preserves provenance and source paths | RAG schemas + evaluation set | ready |
| Agent safety | Default-deny tools and approval gates | MCP policy + agent policy | ready |
| Secrets | No credentials in Vault | `.gitignore`, env-var contract | ready |
| Backup | Recoverable Vault archive | Backup/restore procedure | conditional |
| Auditability | Material AI/tool actions traceable | audit event schema | conditional |
| Monitoring | Health/quality checks defined | observability procedure | conditional |
| External integrations | Credentials, network, rate limits, and provider controls validated in target environment | deployment-specific runbook | not verified here |
| Production execution | Destructive actions gated and separately authorized | execution policy | not enabled |

## Interpretation

`ready` means the design and local validation artifacts exist in this repository.

`conditional` means the control is documented and partially scaffolded but requires deployment-specific implementation and evidence.

`not verified here` means this repository does not prove the target environment is production-safe.
