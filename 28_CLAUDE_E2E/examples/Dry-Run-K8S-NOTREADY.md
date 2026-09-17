# v0.9.0 Dry Run Example

The dry-run orchestrator builds a context packet from the `K8S-NOTREADY-001` fixture and retrieves relevant Vault notes and runbooks.

Run from the Vault root:

```bash
python 28_CLAUDE_E2E/client/e2e_agent.py \
  --scenario K8S-NOTREADY-001 \
  --mode dry-run \
  --output /tmp/k8s-notready-context.json
```

This mode performs no network call and does not execute infrastructure commands.
