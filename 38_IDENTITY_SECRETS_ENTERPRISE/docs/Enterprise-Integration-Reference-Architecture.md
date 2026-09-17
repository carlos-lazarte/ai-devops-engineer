# Enterprise Integration Reference Architecture

```text
                 Identity Provider
                        │
                     OIDC/SSO
                        ▼
                  AI DevOps Runtime
                        │
                Principal Normalizer
                        │
                        ▼
                  Policy Engine
                 ┌──────┼──────┐
                 ▼      ▼      ▼
              RAG/Vault MCP Gateway Audit
                 │      │        │
                 └──────┼────────┘
                        ▼
                 Secret Manager
                        │
                  short-lived use
```

The Obsidian Vault remains a knowledge artifact. Enterprise secrets and identity state live outside it.
