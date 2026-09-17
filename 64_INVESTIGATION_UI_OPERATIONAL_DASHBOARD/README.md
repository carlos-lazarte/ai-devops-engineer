# v3.12.0 — Investigation UI & Operational Dashboard

v3.12 adds the first operational web experience for the AI DevOps Engineer local product runtime.

The UI is deliberately dependency-light: it is served by the existing Python runtime and uses the runtime REST API. No external frontend build is required for the reference implementation.

## Capabilities

- Operational dashboard with live runtime summary.
- Incident queue with severity/state/environment/tenant context.
- Investigation queue with status/mode and quick access to results.
- Investigation detail view with evidence, hypotheses, unknowns, diagnostics, knowledge, plan and safety boundaries.
- One-click demo incident and demo telemetry creation.
- One-click `Investigate` action, still subject to the v3.7/v3.11 policy boundary.
- Read-only connector status visibility.
- Explicit production execution disabled state.
- Tenant filtering in the API surface.
- Auto-refresh with a user-controlled interval.

## Security boundary

The UI is an operator surface, not an authorization engine. It never turns a UI click into production permission. Mutation remains blocked unless a future release explicitly wires a separately scoped approval and execution path.

## Local run

```bash
cd 35_RUNTIME
python3 product_server.py --vault .. --host 127.0.0.1 --port 8080
```

Then open:

`http://127.0.0.1:8080/`

## Demo flow

1. Click **Create demo incident**.
2. Click **Send demo telemetry**.
3. Click **Refresh**.
4. Click **Investigate** on the incident.
5. Open the investigation detail to inspect evidence, hypotheses, unknowns, knowledge and plan.

## API additions

- `GET /api/v1/dashboard/summary`
- Existing incident, telemetry, connector and investigation endpoints remain available.
