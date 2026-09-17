---
type: runbook
domain: ai-devops
risk: medium
status: active
tags:
  - evaluation
  - runbook
---
# Runbook — Agent Evaluation

## Purpose

Run local evaluation before a release.

## Preconditions

- Python environment available.
- Synthetic fixtures present.
- No production credentials required.

## Steps

```bash
make agent-eval
make memory-quality
make reliability-test
make release-check
```

## Verify

Inspect:

- JSON report
- failed cases
- critical safety failures
- threshold summary

## Rollback

If the release gate fails, do not publish the candidate. Return to the last passing version and inspect the diff in content, prompts, retrieval logic, memory policy, or runtime behavior.
