# Model Evaluation Methodology

All candidate models receive the same:
- task
- evidence
- scenario state
- policy context
- expected output contract

Compare:
- task success
- evidence grounding
- safety
- latency
- token/cost estimate

Do not compare results when inputs or policy conditions differ without recording the difference.

## Evaluation principle

A model can be cheaper or faster without being suitable for a critical task. Quality and safety gates are evaluated independently.
