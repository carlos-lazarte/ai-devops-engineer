# Privacy and Data Minimization

Store only data required for the operational purpose.

Avoid storing:

- credentials
- access tokens
- private keys
- full production payloads when a reduced excerpt is sufficient
- unnecessary personal data

Prefer references to evidence over copying sensitive content into memory. Redact secrets before memory persistence and before sending context to an LLM.
