# Workload Identity

Use workload identity instead of embedding cloud/API credentials in containers.

Preferred sequence:

```text
Runtime workload
  ↓
Platform identity
  ↓
Identity provider / STS
  ↓
Short-lived credential
  ↓
Target service
```

The runtime should request only the scope required for the operation and should never persist issued credentials in the Vault.
