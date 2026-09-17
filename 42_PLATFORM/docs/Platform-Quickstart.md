---
type: guide
domain: platform
status: active
---

# Platform Quickstart

## 1. Validate the platform checkout

```bash
make platform-check
```

## 2. Start the reference local stack

```bash
docker compose up --build
```

## 3. Check stable API endpoints

```bash
curl http://127.0.0.1:8080/api/v1/health
curl http://127.0.0.1:8080/api/v1/ready
curl http://127.0.0.1:8080/api/v1/version
```

## 4. Execute a dry-run incident analysis

```bash
curl -s http://127.0.0.1:8080/api/v1/incidents/analyze \
  -H 'content-type: application/json' \
  -d '{"incident_id":"K8S-NOTREADY-001","mode":"dry-run"}'
```

The reference profile does not enable production mutation.
