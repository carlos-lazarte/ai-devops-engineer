# OIDC Integration Contract

## Required validation

An OIDC/JWT verifier should validate, according to the selected provider and deployment:

- signature and trusted issuer;
- token expiry and not-before constraints;
- audience;
- required subject claim;
- approved algorithms;
- required tenant/environment claims where applicable.

## Output

The verifier emits a normalized principal object. It should not expose raw bearer tokens to downstream tools unless the tool contract explicitly requires delegated access.

## Example

```yaml
principal:
  subject: charles@example.invalid
  issuer: https://idp.example.invalid
  tenant_id: acme
  environment: prod
  roles:
    - operator
  scopes:
    - knowledge:read
    - incident:analyze
```
