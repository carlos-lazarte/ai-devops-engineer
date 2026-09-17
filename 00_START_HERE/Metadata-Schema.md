---
type: reference
domain: core
status: active
tags: [vault, metadata, obsidian]
---
# Metadata Schema

Canonical Properties for the Vault. Keep field names stable so searches, scripts, and future retrieval pipelines can rely on them.

| Property | Type | Purpose |
|---|---|---|
| `type` | string | Content type |
| `domain` | string | Primary area |
| `technology` | string | Main technology when applicable |
| `difficulty` | string | beginner/intermediate/advanced/expert |
| `status` | string | draft/review/active/deprecated |
| `tags` | list | Classification and search |
| `version` | string | Technology version when material |
| `risk` | string | low/medium/high/critical |
| `severity` | string | Incident/troubleshooting impact |
| `task` | string | Main task for prompt/workflow |

## Rules

1. Controlled values are lowercase.
2. Use one primary `type` per note.
3. Never store secrets in Properties.
4. Use links for relationships and tags for classification.
5. Deprecated notes should point to a replacement.

## `type` vocabulary

`knowledge`, `concept`, `technology`, `architecture`, `troubleshooting`, `runbook`, `checklist`, `incident`, `postmortem`, `prompt`, `workflow`, `template`, `lab`, `decision`, `reference`, `project`

## Other controlled values

`difficulty`: `beginner`, `intermediate`, `advanced`, `expert`  
`status`: `draft`, `review`, `active`, `deprecated`  
`risk`: `low`, `medium`, `high`, `critical`
