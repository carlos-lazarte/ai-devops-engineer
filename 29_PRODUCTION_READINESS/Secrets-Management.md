---
type: runbook
domain: security
status: active
---
# Secrets Management

## Required rule

Secrets must not be stored in Markdown notes, prompts, fixtures, logs, Git history, or generated context packets.

## Preferred flow

```text
Secret Store / Environment
        |
        v
Application runtime
        |
        v
Claude client / MCP client
```

## Example contract

```bash
export ANTHROPIC_API_KEY="<injected-at-runtime>"
```

Do not place real values in shell history, README files, fixtures, or issue trackers.

## Rotation

1. Revoke compromised credential.
2. Issue a replacement credential.
3. Update runtime secret store.
4. Validate the client in a non-production environment.
5. Record rotation metadata without recording the secret value.
