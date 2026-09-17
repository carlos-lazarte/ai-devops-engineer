# v3.11 Quickstart

From the repository root:

```bash
cd 35_RUNTIME
python3 product_server.py --vault .. --host 127.0.0.1 --port 8080
```

Seed a demo incident, then investigate it:

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/demo/seed
```

Use the returned `incident_id`:

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/incidents/<INCIDENT_ID>/investigate \
  -H 'content-type: application/json' \
  -d '{"mode":"dry-run","include_connectors":true}'
```

List investigations:

```bash
curl -s http://127.0.0.1:8080/api/v1/investigations
```

The same flow is available through `investigatectl.py`.
