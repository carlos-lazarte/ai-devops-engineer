# Memory Architecture

```text
                     AGENT EXECUTION
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         Working       Episodic      Semantic
         Memory        Memory        Memory
          (TTL)       (history)    (curated Vault)
              │            │            │
              └────────────┼────────────┘
                           ▼
                     Context Builder
                           │
                           ▼
                        Claude
                           │
                           ▼
                    Structured Result
                           │
                     Human validation
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       Keep as episode            Promote to Vault
                                   only after review
```

## Separation rules

1. Working memory is scoped to a correlation ID and expires.
2. Episodic memory is immutable-by-default and must preserve provenance.
3. Semantic promotion creates a new Vault draft; it does not mutate canonical knowledge automatically.
4. Memory retrieval is filtered by tenant and environment before content is returned.
5. Memory cannot grant a tool permission.
