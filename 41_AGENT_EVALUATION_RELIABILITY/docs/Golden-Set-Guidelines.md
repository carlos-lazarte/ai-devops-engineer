---
type: procedure
domain: ai-devops
status: active
tags:
  - evaluation
  - golden-set
---
# Golden Set Guidelines

A golden case contains:

- user/task prompt
- tenant/environment context
- expected evidence references
- required response fields
- forbidden behaviors
- acceptable uncertainty
- expected tool or memory interactions

## Rules

- Prefer small, diagnostic scenarios over huge stories.
- Keep evidence synthetic and deterministic.
- Do not encode secrets.
- Do not make the expected answer depend on hidden model behavior.
- Version the golden set whenever semantics change.
- Record why a case changed.
