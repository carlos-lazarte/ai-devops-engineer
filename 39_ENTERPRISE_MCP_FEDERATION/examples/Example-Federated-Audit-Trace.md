---
type: example
domain: ai
topic: audit
status: active
tags:
  - audit
  - federation
---

# Example Federated Audit Trace

```text
correlation_id=demo-incident-001
  |
  +-- router: accepted task
  +-- sre: allowed
  +-- devops: allowed
  +-- vault-knowledge/search_notes: allowed
  +-- vault-knowledge/retrieve_runbook: denied
  +-- aggregator: partial result
  +-- human_review: required
```

The trace demonstrates that each delegated capability receives an independent policy decision.
