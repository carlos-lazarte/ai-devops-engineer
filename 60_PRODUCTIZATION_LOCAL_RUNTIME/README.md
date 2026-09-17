---
type: productization
version: 3.8.0
status: active
---

# v3.8.0 — Productization & Local Runtime

This release turns the reference architecture into a runnable local product slice.

## What is now real

```text
Browser
  ↓
Product HTTP API
  ↓
Incident Store
  ├── PostgreSQL 17 in Docker
  └── SQLite fallback for local tests
```

The runtime exposes a small Community Edition surface:

- web dashboard at `/`
- product metadata at `/api/v1/product`
- incident list and filtering
- incident creation
- demo incident seeding
- persistent storage
- Docker Compose with PostgreSQL + Redis
- existing RAG, Claude, policy, audit and v3.7 Incident Commander components remain available

## Start on a Docker host

```bash
cd 35_RUNTIME
cp .env.example .env
# add ANTHROPIC_API_KEY only when Claude mode is desired
docker compose up --build
```

Then open:

```text
http://localhost:8080/
```

Click **Create demo incident** to populate PostgreSQL and display the incident.

## API examples

```bash
curl http://localhost:8080/api/v1/product
curl http://localhost:8080/api/v1/incidents
curl -X POST http://localhost:8080/api/v1/demo/seed
```

Create an incident:

```bash
curl -X POST http://localhost:8080/api/v1/incidents \
  -H 'content-type: application/json' \
  -d '{"incident_id":"INC-1001","tenant_id":"demo","environment":"lab","severity":"high","confidence":0.87,"candidate_reason":"Node pressure with repeated pod restarts","signals":["cpu-1","pod-7"],"provenance":["synthetic/telemetry.json"]}'
```

## Safety boundary

v3.8 does **not** enable production remediation. The local product can ingest, persist, inspect and prepare incidents; execution remains behind policy and human-approval boundaries.
