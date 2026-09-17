# Routing Learning Feedback

After an evaluation or real execution in an authorized environment, the platform may record:

- task class
- model
- success
- grounding
- safety
- latency
- cost
- timestamp

The feedback is used to improve routing decisions for future tasks.

It must not mutate:
- IAM
- RBAC
- tool permissions
- production execution policy
- secret access

without a separate reviewed policy change.
