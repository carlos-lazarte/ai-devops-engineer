---
type: architecture
domain: ai
technology: rag
status: active
tags:
  - ai
  - rag
  - context
  - devops
---
# Architecture — AI Context and RAG for DevOps

## Problem

A language model may have useful general knowledge but still lack the current, environment-specific information needed for reliable DevOps analysis.

## Architecture

```text
                 ┌──────────────────────┐
                 │     DevOps User      │
                 └──────────┬───────────┘
                            │ question
                            ▼
                 ┌──────────────────────┐
                 │ Context Builder       │
                 │ scope + constraints  │
                 └──────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌───────────────┐       ┌───────────────┐
        │ Obsidian Vault│       │ Live Evidence │
        │ knowledge     │       │ logs/metrics  │
        │ runbooks      │       │ commands      │
        │ ADRs          │       │ traces/events │
        └───────┬───────┘       └───────┬───────┘
                │ retrieval              │
                └───────────┬────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Context Packet       │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ LLM / Claude         │
                 └──────────┬───────────┘
                            ▼
                 Structured analysis
```

## Important distinction

The Vault is durable knowledge. Live evidence is time-specific state. Keep them separate even when the model sees both.

## Retrieval goals

Retrieve notes that are:

- relevant to the technology;
- applicable to the supplied version;
- related to the symptom;
- compatible with the environment;
- current enough for the task.

## Security

Do not send credentials, private keys, tokens, session cookies or other secrets in model context.

## Failure modes

- stale notes retrieved;
- wrong version retrieved;
- too much context;
- missing recent evidence;
- contradictory sources;
- sensitive data leakage.

## Related

[[../15_AI_FOR_DEVOPS/AI-DevOps-Context-Protocol]]
[[AI-Agent-DevOps]]
