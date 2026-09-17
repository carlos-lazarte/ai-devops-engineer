---
type: architecture
domain: ai
technology: runtime
difficulty: advanced
status: active
tags:
  - ai
  - devops
  - runtime
  - rag
  - mcp
---

# Production AI DevOps Runtime

This runtime is the executable companion to the Obsidian Vault. It separates the static product (Markdown knowledge) from the runtime services that perform retrieval, context assembly, MCP-style tool routing, Claude invocation, validation, and audit logging.

## Scope

```text
Obsidian Vault
      |
      v
  Runtime API
      |
  +---+------------------+
  |   |                  |
  v   v                  v
RAG  MCP Gateway       Claude
  |   |                  |
  +---+--------+---------+
             v
       Agent Orchestrator
             |
       Structured Output
             |
       Human Approval
```

The default runtime is read-only with respect to operational infrastructure. It can read the Vault, retrieve context, and call Claude when credentials are configured. It does not provide shell, SSH, Kubernetes, cloud, or arbitrary filesystem execution.

## Quickstart

```bash
cd 35_RUNTIME
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m app.server --vault .. --host 127.0.0.1 --port 8080
```

Health check:

```bash
curl http://127.0.0.1:8080/health
```

Search:

```bash
curl -s http://127.0.0.1:8080/search \
  -H 'content-type: application/json' \
  -d '{"query":"kubernetes node notready","limit":5}'
```

Incident analysis in dry-run mode:

```bash
curl -s http://127.0.0.1:8080/incident/analyze \
  -H 'content-type: application/json' \
  -d '{"incident_id":"K8S-NOTREADY-001","mode":"dry-run"}'
```

## Claude mode

Set `ANTHROPIC_API_KEY` and an explicit `ANTHROPIC_MODEL` in the environment or `.env`, then use `"mode":"claude"`. The runtime records only bounded metadata and does not log the API key.

## Production boundary

This release is a production-oriented baseline for the **runtime architecture and local deployment model**. It is not a certification that a specific cloud or enterprise deployment is production compliant. Deployment-specific IAM, secrets management, network controls, observability, capacity, and compliance must still be validated in the target environment.


## Automated Incident Investigation

Use `POST /api/v1/incidents/<INCIDENT_ID>/investigate` to create an evidence-first investigation. The deterministic `dry-run` mode requires no external model and keeps execution disabled.
