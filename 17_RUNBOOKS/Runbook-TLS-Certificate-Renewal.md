---
type: runbook
domain: security
technology: TLS
difficulty: intermediate
risk: high
status: active
tags: [runbook, security]
---
# Runbook-TLS-Certificate-Renewal

## Purpose
Renew a TLS certificate with validation and rollback criteria.

## Procedure
1. Inspect current certificate.
2. Validate replacement subject/SAN, dates, and chain.
3. Deploy using the platform-approved mechanism.
4. Reload/restart only as required.
5. Test with expected hostname/SNI.

## Verification
Use TLS inspection plus an application-level health check.

## Rollback
Restore the previous certificate/key through the approved secret-management process.

Related: [[Troubleshooting-TLS-Certificate]]
