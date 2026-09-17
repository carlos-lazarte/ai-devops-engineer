# Security Boundary

Telemetry ingestion is an input boundary, not an authorization boundary.

```text
External Telemetry
      |
      v
Ingestion Validation
      |
      v
Normalized Event
      |
      v
Correlation
      |
      v
Incident Candidate
      |
      v
v3.7 Human/Policy Gate
```

The runtime does not execute commands as a consequence of an incoming metric.
