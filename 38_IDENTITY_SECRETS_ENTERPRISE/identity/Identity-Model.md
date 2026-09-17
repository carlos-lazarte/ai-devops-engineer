# Identity Model

## Principal

Every runtime request must resolve to an explicit principal.

```yaml
principal:
  subject: user-or-workload-id
  issuer: https://issuer.example
  roles: [analyst]
  tenant_id: tenant-a
  environment: lab
  authn_method: oidc
```

## Identity sources

Preferred patterns:

1. Human users: OIDC/OAuth2 SSO with short-lived tokens.
2. Workloads: workload identity or platform-issued service identity.
3. Local development: explicitly scoped development credentials.

## Trust boundaries

Identity claims are untrusted input until signature, issuer, audience, expiry and relevant claims are validated.

Authorization is separate from authentication. A valid token does not imply permission to call a tool.
