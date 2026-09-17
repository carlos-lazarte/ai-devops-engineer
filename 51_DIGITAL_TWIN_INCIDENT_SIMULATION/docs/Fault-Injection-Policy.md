# Fault Injection Policy

Fault injection is intentionally constrained to the Digital Twin.

Allowed examples:
- synthetic node health degradation
- synthetic kubelet failure
- synthetic disk pressure
- synthetic DNS failure
- synthetic TLS expiration
- synthetic network packet loss

Forbidden:
- injecting faults into real infrastructure
- using real credentials
- contacting external networks
- destructive host operations

Every injection must have:
- scenario ID
- fault ID
- timestamp
- target twin
- expected symptoms
- rollback/reset operation
