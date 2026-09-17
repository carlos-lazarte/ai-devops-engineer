# v3.12 Quickstart

```bash
cd 35_RUNTIME
python3 product_server.py --vault .. --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080/`.

For a fast demo:

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/demo/seed
curl -s -X POST http://127.0.0.1:8080/api/v1/telemetry/events \
  -H 'content-type: application/json' \
  -d '{"event_id":"ui-1","timestamp":1735689600,"tenant_id":"demo-tenant","environment":"lab","component":"node-01","metric_family":"cpu","condition":"high","severity_hint":"high","value":95,"source":"quickstart"}'

curl -s http://127.0.0.1:8080/api/v1/dashboard/summary
```
