# Offline vs Live Measurements

v3.2.0 uses reference historical measurements and deterministic routing.

The following are not live provider observations:
- estimated model cost
- estimated model latency
- reference success rates

A production deployment should replace these with controlled telemetry gathered in the target environment while preserving the same policy boundary.
