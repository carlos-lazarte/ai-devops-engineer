# Memory Lifecycle and Retention

| Memory class | Purpose | Default retention | Mutation policy | Promotion |
|---|---|---:|---|---|
| working | current task context | 24h | mutable within task | never automatic |
| episodic | incidents/decisions/outcomes | 180d | append-only events | human review |
| semantic | durable technical knowledge | controlled by Vault policy | reviewed change | explicit approval |

These are reference defaults, not universal compliance requirements. Production retention must be set according to organizational policy and applicable regulation.

### Deletion

Deletion should be a policy-driven lifecycle event with audit evidence. A memory record must not be deleted merely because an agent wants to reduce context.
