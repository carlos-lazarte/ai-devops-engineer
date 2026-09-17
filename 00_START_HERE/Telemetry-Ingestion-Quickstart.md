# Telemetry Ingestion Quickstart

## Generic event

```bash
curl -s http://127.0.0.1:8080/api/v1/telemetry/events \
  -H content-type:application/json \
  -d @61_REAL_TELEMETRY_EVENT_INGESTION/fixtures/sample-event.json
```

## Recent telemetry

```bash
curl -s http://127.0.0.1:8080/api/v1/telemetry/events
```

## Prometheus

Set `PROMETHEUS_URL` and use the read-only query/poll endpoints.

## OTLP

Send the supported JSON metrics subset to `/api/v1/telemetry/otlp` with `X-AIOPS-Tenant` and `X-AIOPS-Environment` headers.
