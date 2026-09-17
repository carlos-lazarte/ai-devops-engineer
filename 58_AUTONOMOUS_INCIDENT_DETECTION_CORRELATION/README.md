# v3.6.0 — Autonomous Incident Detection & Event Correlation

This module extends v3.5 Predictive SRE from **detecting correlated signals** to **creating bounded Incident Candidates automatically**.

## Capabilities

- Event normalization
- Duplicate suppression
- Temporal/topological correlation
- Tenant/environment isolation
- Advisory severity
- Incident Candidate lifecycle
- Provenance preservation
- Human-review boundary
- Digital Twin blind-evaluation hooks
- CLI reference implementation

## Example

```bash
PYTHONPATH=58_AUTONOMOUS_INCIDENT_DETECTION_CORRELATION \
python3 58_AUTONOMOUS_INCIDENT_DETECTION_CORRELATION/cli/incidentctl.py \
  correlate --input 58_AUTONOMOUS_INCIDENT_DETECTION_CORRELATION/evaluation/reference-events.json --pretty
```

Reference execution is deterministic and simulation-only.
