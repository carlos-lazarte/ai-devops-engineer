---
type: procedure
domain: ai
difficulty: advanced
status: active
tags:
  - skills
  - agents
  - devops
---
# Skill Authoring Guide

## Required sections

A new skill must provide:

- `skill_id`
- `version`
- `goal`
- `domains`
- `required_evidence`
- `allowed_tools`
- `risk`
- `autonomy_level`
- `output_schema`
- `verification`
- `forbidden_actions`

## Quality gate

```text
Contract valid
  ↓
No undeclared tools
  ↓
Evidence gate defined
  ↓
Safety policy present
  ↓
Evaluation cases present
  ↓
Deterministic tests pass
```

Skills that bypass any gate are not eligible for registration.
