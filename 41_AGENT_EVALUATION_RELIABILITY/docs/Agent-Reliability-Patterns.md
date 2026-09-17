---
type: knowledge
domain: ai-devops
status: active
tags:
  - reliability
  - agent
---
# Agent Reliability Patterns

- Timeouts must become explicit failures, not silent retries without bounds.
- Retries require idempotency awareness.
- Malformed model output must be rejected by schema validation.
- Partial federation results must remain labeled partial.
- Duplicate submissions should be detected using correlation/task identifiers when the workflow contract permits it.
- Policy failures must be fail-closed.
- Memory failures must not silently broaden authorization.
