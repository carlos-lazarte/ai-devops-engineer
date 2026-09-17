# Compatibility Resolution

Compatibility is checked against the platform API, contract version, environment, and declared required tools.

The resolver supports a small, explicit constraint vocabulary for the marketplace reference implementation:

- exact: `1.2.3`
- caret-like major compatibility: `^1.2.0`
- wildcard minor: `1.x`

Unsupported constraint syntax is rejected rather than guessed.
