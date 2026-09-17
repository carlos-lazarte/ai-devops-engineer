---
type: architecture
domain: platform
status: active
---

# Service Boundaries

| Service | Responsibility | Must not do |
|---|---|---|
| API Gateway | Authentication context, request routing | Tool-side authorization bypass |
| Identity | Normalize authenticated principals | Grant tool permissions by itself |
| Policy | Authorization, risk and approval | Store secrets |
| Agent | Plan/reason over allowed capabilities | Bypass policy |
| RAG | Retrieve knowledge/context | Execute operations |
| Memory | Store bounded state/history | Grant authorization |
| MCP Gateway | Expose approved tools | Execute undeclared tools |
| Claude Client | Model invocation | Decide permissions |
| Audit | Immutable event trail target | Contain secrets |
| Observability | Metrics/logs/traces | Become source of authorization |

The separation is architectural: an implementation may co-locate components, but the contracts and security responsibilities remain distinct.
