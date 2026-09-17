# Verification Strategy

Verification is defined before execution where practical.

Each action should declare:

- expected effect
- verification method
- acceptable result
- timeout
- rollback / recovery path

## Outcome states

```text
VERIFIED
FAILED
UNKNOWN
```

`UNKNOWN` means evidence is insufficient to conclude success or failure.

## Example

Action:
Restart a simulated service.

Expected effect:
Service returns to healthy state.

Verification:
Health probe reports healthy.

Observed:
Health probe reports unhealthy.

Outcome:
FAILED

The agent must not mark the task successful.
