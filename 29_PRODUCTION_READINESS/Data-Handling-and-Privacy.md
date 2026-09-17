---
type: reference
domain: security
status: active
---
# Data Handling and Privacy

## Classification

Classify Vault content and operational evidence before sending it to an external model.

Recommended classes:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

## Rule

Do not send Restricted material to an external AI provider unless the organization's approved control framework explicitly permits it.

## Redaction

Before creating a Context Packet, remove or mask:

- credentials
- access tokens
- private keys
- personal identifiers not needed for the task
- secrets embedded in logs or command output

Record that redaction occurred; do not record the removed secret itself.
