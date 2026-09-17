---
type: troubleshooting
domain: security
technology: TLS
difficulty: intermediate
severity: high
status: active
tags: [security, troubleshooting]
---
# Troubleshooting-TLS-Certificate

TLS problems require examining both certificate validity/identity and protocol negotiation/trust.

## First checks
```bash
openssl s_client -connect host:443 -servername host -showcerts
openssl x509 -in certificate.pem -noout -subject -issuer -dates
```

## Evidence
Capture endpoint, SNI/hostname, certificate chain, validity, trust-store context, and client/server errors.

## Common branches
- Expired/not-yet-valid certificate
- SAN/hostname mismatch
- Incomplete chain
- Trust-store issue
- Protocol/cipher mismatch

Related: [[Runbook-TLS-Certificate-Renewal]]
