# Safety Boundaries

Automated investigation is intentionally asymmetric:

- Evidence collection can be automatic when the connector is read-only.
- Reasoning can be automatic.
- Hypothesis generation can be automatic.
- Planning can be automatic but remains plan-only.
- Infrastructure mutation is not performed by the investigator.
- Human approval remains authoritative for change/remediation.
- Tenant and environment are carried through every investigation record.
- Ground truth for evaluation remains outside agent context.
