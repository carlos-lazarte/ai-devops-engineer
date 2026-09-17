---
type: guide
domain: ai
task: quickstart
status: active
tags:
  - claude
  - e2e
  - quickstart
---

# Claude E2E Quickstart

## 1. Dry run first

```bash
python 28_CLAUDE_E2E/client/e2e_agent.py \
  --scenario K8S-NOTREADY-001 \
  --mode dry-run
```

## 2. Configure Claude API mode

Set `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` in the shell. Keep both outside Git and outside the Vault.

```bash
export ANTHROPIC_API_KEY='...'
export ANTHROPIC_MODEL='...'
```

Then:

```bash
python 28_CLAUDE_E2E/client/e2e_agent.py \
  --scenario K8S-NOTREADY-001 \
  --mode claude \
  --output /tmp/k8s-notready-e2e.json
```

## 3. Review before action

A successful model response is not an execution approval. Review facts, provenance, hypotheses and proposed actions before any operational change.
