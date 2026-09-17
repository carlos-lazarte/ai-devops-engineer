---
type: reference
domain: observability
status: active
---
# Observability

## Health signals

Track at minimum:

- Vault validation failures.
- Retrieval errors and empty-result rates.
- Tool denials and policy violations.
- Claude API error rate, latency, and rate-limit responses.
- Structured-response validation failures.
- Human approval rejection rate.

## Quality signals

Track:

- Retrieval Recall@K.
- Evidence provenance coverage.
- Unsupported-claim rate.
- Action honesty rate.
- Evaluation pass rate by scenario.

## Golden rule

A technically available agent is not necessarily a healthy agent. Monitor both system health and response quality.
