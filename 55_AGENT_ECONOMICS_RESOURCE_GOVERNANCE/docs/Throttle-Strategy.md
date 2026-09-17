# Throttle Strategy

Reference behavior:

```text
within budget      → CONTINUE
near soft limit    → THROTTLE
hard limit reached → DENY
critical safety    → NEVER bypass
```

Possible throttling actions:

- reduce context size
- reduce maximum output
- defer non-critical enrichment
- reduce optional tool calls
- route to an eligible lower-cost model

A throttle must never reduce below the hard quality tier required by policy.
