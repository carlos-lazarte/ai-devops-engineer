---
type: runbook
domain: sre
status: active
---
# AI System Incident Response

## Trigger examples

- Secret exposure.
- Unauthorized tool invocation.
- Retrieval corruption.
- Repeated unsupported claims.
- Provider outage.
- Unexpected policy bypass.

## Immediate containment

1. Disable the affected integration or tool.
2. Preserve audit evidence.
3. Revoke exposed credentials.
4. Freeze the affected release.
5. Determine scope and impact.

## Recovery

Restore from a known-good release, re-run validation/evaluation, then re-enable capabilities incrementally.

## Post-incident

Create a [[19_TEMPLATES/Template-Postmortem]] and link the incident to the affected architecture, tool, prompt, and release.
