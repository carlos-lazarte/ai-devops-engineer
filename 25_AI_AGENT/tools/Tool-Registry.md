---
type: reference
domain: ai
status: active
---

# Tool Registry

| Tool | Access | Purpose | Approval |
|---|---|---|---|
| `search_notes` | read | semantic / metadata retrieval | no |
| `read_note` | read | exact note retrieval | no |
| `list_related_notes` | read | graph traversal | no |
| `retrieve_runbook` | read | find operational procedure | no |
| `get_context_packet` | read | inspect evidence bundle | no |
| `create_draft` | write-draft | create proposed content | yes before publish |
| `propose_patch` | write-draft | propose note changes | yes before publish |

No tool outside this registry is considered available.
