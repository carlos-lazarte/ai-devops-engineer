# Model Routing Policy

Routing considers:

1. task criticality
2. task class
3. minimum quality tier
4. maximum estimated cost
5. maximum latency
6. policy restrictions

The router must fail closed when no eligible model satisfies the constraints.

The router does not execute actions and does not bypass approval gates.
