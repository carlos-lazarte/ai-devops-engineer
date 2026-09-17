# Blind Evaluation

Digital Twin ground truth stays outside the agent context.

Evaluation compares detector/correlator output against scenario truth after execution. Do not provide expected incident identity, severity, or topology labels to the agent under evaluation.

Core metrics:
- detection rate
- correlation precision
- false merge rate
- duplicate suppression rate
- time-to-candidate
- severity agreement
- tenant isolation
- provenance completeness
