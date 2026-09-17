# Signing and Verification

## Reference model

```text
Build
 ↓
SHA-256
 ↓
Signature
 ↓
Registry
 ↓
Trust store
 ↓
Verify before install
```

The signature provides artifact authenticity/integrity. It does not grant runtime authorization. Authorization remains a Policy Engine decision.

## Minimum verification

1. Verify signature against a trusted publisher key.
2. Verify checksum.
3. Verify manifest identity and version.
4. Run compatibility and policy checks.
5. Record the installation in the audit trail.
