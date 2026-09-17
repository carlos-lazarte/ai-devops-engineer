---
type: quickstart
domain: incident-investigation
technology: runtime, rag, knowledge-graph, skills, planner
status: active
---
# Automated Investigation Quickstart

Run the product runtime:

```bash
cd 35_RUNTIME
python3 product_server.py --vault .. --host 127.0.0.1 --port 8080
```

Create a demo incident:

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/demo/seed
```

Investigate the returned incident in deterministic mode:

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/incidents/<INCIDENT_ID>/investigate \
  -H 'content-type: application/json' \
  -d '{"mode":"dry-run","include_connectors":true}'
```

List stored investigations:

```bash
curl -s http://127.0.0.1:8080/api/v1/investigations
```

For model-assisted synthesis, configure `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL`, then use `{"mode":"claude"}`. The model remains advisory and cannot execute remediation.
