# Public Demo Runbook

## Python path

```bash
./demo/run_demo.sh
```

The script will:

1. ensure the local virtual environment exists;
2. start the local product runtime;
3. seed a synthetic incident;
4. send synthetic CPU and memory telemetry;
5. run a dry-run investigation;
6. print the resulting dashboard summary;
7. stop the temporary server.

## Manual verification

```bash
curl -s http://127.0.0.1:8080/api/v1/product
curl -s http://127.0.0.1:8080/api/v1/dashboard/summary
```

The demo uses `demo-tenant` and synthetic `lab` data only.
