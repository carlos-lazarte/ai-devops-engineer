# Public Demo Architecture

The public demo is deterministic and local-first. It exercises the same runtime path used by the Community Edition but uses synthetic data.

```text
Demo script
   ↓
Product API
   ↓
Telemetry Store
   ↓
Incident Candidate
   ↓
Dry-run Investigation
   ↓
Dashboard
```

No external production infrastructure is contacted by the demo.
