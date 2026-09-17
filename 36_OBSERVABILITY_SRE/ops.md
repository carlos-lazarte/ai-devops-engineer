# Observability Operations

## Start the control plane

```bash
docker compose up --build
```

Endpoints for a local lab:

- Runtime health: `http://localhost:8080/health`
- Runtime metrics: `http://localhost:8080/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Production note

Do not treat the default image tags, unauthenticated local ports, or single-instance Compose topology as a production security baseline. Pin images by digest, configure authentication/TLS, define retention, protect network exposure, and validate persistence/HA according to the target environment.
