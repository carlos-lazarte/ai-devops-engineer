# Predictive SRE Limits

A predicted degradation is not a confirmed incident.

The system should represent:

```text
OBSERVED
CORRELATED
ANOMALOUS
PREDICTED
CONFIRMED
```

The reference implementation only produces observed/correlated/anomalous/predicted states from synthetic telemetry.

Confirmation requires independent operational evidence.
