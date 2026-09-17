# Agent Memory Quickstart

The v1.8.0 memory layer is a controlled context store, not an authorization store.

## Quick model

```text
Current task → Working memory
Incident history → Episodic memory
Reviewed knowledge → Semantic memory / Vault
```

## Local validation

```bash
python 40_AGENT_MEMORY_STATE/tests/test_memory.py
python 40_AGENT_MEMORY_STATE/tests/test_state_machine.py
```

For the complete repository workflow use the project `make test` target.
