# Local Product Architecture

```text
                         +----------------------+
                         |      Web UI          |
                         |  /api/v1 + browser   |
                         +----------+-----------+
                                    |
                              HTTP Product API
                                    |
              +---------------------+--------------------+
              |                                          |
              v                                          v
      Incident Store                              Existing Runtime
              |                                   RAG / Claude / Audit
        +-----+-----+
        |           |
   PostgreSQL     SQLite
    (Docker)     (tests)
        |
      Redis
   (reserved for async/event work)
```

The objective is not to replace the v3.x architecture. It is to provide a stable local entry point around it.

## Productization rule

Do not expose arbitrary shell, SSH or infrastructure credentials through the web API. New operational connectors must enter through the policy-controlled Tool Gateway and remain explicitly scoped by tenant, environment, action tier and approval.
