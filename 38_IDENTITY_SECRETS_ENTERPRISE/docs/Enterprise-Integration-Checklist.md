# Enterprise Integration Checklist

## Identity

- [ ] Trusted issuer configured.
- [ ] Audience validated.
- [ ] Token expiry validated.
- [ ] Roles/scopes normalized.
- [ ] Tenant and environment claims enforced.

## Secrets

- [ ] No secret values in Git.
- [ ] No secret values in Obsidian.
- [ ] Secret manager configured.
- [ ] Short TTLs defined.
- [ ] Rotation/revocation tested.
- [ ] Redaction tested.

## Authorization

- [ ] Default deny.
- [ ] Tool risk classification current.
- [ ] Approval required for high-risk actions.
- [ ] Production permissions separated from non-prod.

## Audit

- [ ] Principal, tenant, environment and decision recorded.
- [ ] No sensitive payloads recorded.
- [ ] Audit retention defined.
