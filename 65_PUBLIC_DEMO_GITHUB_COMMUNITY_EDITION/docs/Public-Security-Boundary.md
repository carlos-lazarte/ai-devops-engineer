# Public Security Boundary

The public demo must not require or ship any secret.

Forbidden in a public release:

- `.env` files containing values
- production telemetry
- customer data
- credentials
- API keys
- private repository metadata
- local runtime databases

The release checker searches for common credential signatures and generated runtime state before packaging.
