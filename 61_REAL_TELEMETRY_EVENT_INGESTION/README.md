---
type: runtime
domain: observability
technology: prometheus, opentelemetry, ingestion
status: active
---

# v3.9.0 — Real Telemetry & Event Ingestion

v3.9 adds the first production-shaped ingestion boundary between external telemetry systems and the AI DevOps incident engine.

## Supported paths

```text
Prometheus HTTP API ─┐
                     ├─> Normalize ─> Persist ─> v3.6 Correlation ─> Incident Candidate
OTLP/HTTP JSON ──────┘

Generic Event API ────────────────────────────────┘
```

The implementation is intentionally conservative:

- ingestion does not grant permissions;
- telemetry is normalized before correlation;
- tenant/environment isolation is enforced at the service boundary;
- Prometheus pulls are read-only;
- OTLP payloads are bounded;
- production remediation remains disabled;
- incident candidates are advisory until the v3.7 human gate is reached.

## Local demo

From the repository root:

```bash
cd 35_RUNTIME
python3 -m pytest -q tests ../61_REAL_TELEMETRY_EVENT_INGESTION/tests
```

Run the product runtime with SQLite:

```bash
cd 35_RUNTIME
python product_server.py --vault .. --host 127.0.0.1 --port 8080
```

In another terminal, ingest a synthetic OTLP-style event:

```bash
curl -s http://127.0.0.1:8080/api/v1/telemetry/events \\
  -H 'content-type: application/json' \\
  -d @../61_REAL_TELEMETRY_EVENT_INGESTION/fixtures/sample-event.json
```

Then inspect incidents:

```bash
curl -s http://127.0.0.1:8080/api/v1/incidents
```

## Prometheus

Configure:

```bash
export PROMETHEUS_URL=http://prometheus.example:9090
```

Query example:

```bash
curl -s http://127.0.0.1:8080/api/v1/telemetry/prometheus/query \\
  -H 'content-type: application/json' \\
  -d '{"query":"up","tenant_id":"demo-tenant","environment":"lab"}'
```

Or use the server-side polling endpoint with an allow-listed Prometheus URL:

```bash
curl -s http://127.0.0.1:8080/api/v1/telemetry/prometheus/poll \\
  -H 'content-type: application/json' \\
  -d '{"query":"up","tenant_id":"demo-tenant","environment":"lab"}'
```

See `docs/Prometheus-Integration.md` for label mapping and safety controls.

## OTLP/HTTP

This release accepts a deliberately small JSON subset of OpenTelemetry metrics and converts data points to normalized events. It is suitable for integration tests and collector gateways, not a claim of full OTLP protocol coverage.

See `docs/OTLP-HTTP-Mapping.md`.
