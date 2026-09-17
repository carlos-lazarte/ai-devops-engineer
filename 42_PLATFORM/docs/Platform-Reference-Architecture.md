---
type: architecture
domain: platform
status: active
---

# Platform Reference Architecture

```text
                      Client / UI / Automation
                                │
                                ▼
                         API v1 Gateway
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
      Identity              Policy                 Audit
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                ▼
                         Agent Orchestrator
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                   RAG        Memory       MCP
                    │           │           │
                    └───────────┼───────────┘
                                ▼
                           Claude Client
                                │
                                ▼
                           Vault / Data
                                │
                         Observability
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                 Metrics                  Audit
```

All boundaries are contract-driven. Implementations may evolve without changing the public contract unless a versioned API change is declared.
