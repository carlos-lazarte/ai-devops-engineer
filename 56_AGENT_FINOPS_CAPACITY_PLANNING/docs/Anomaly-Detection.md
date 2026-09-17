# Cost / Usage Anomaly Detection

Reference anomalies:

- spend spike
- token spike
- tool-call spike
- latency degradation
- unexpected model mix

A useful anomaly event contains:

- observed value
- baseline
- deviation
- scope
- timestamp
- provenance

An anomaly should trigger investigation or throttling according to policy, not automatic permission escalation.
