# Budget Model

Budgets can be defined at multiple scopes:

```text
tenant
  ↓
environment
  ↓
priority
  ↓
task
  ↓
execution
```

Recommended budget dimensions:

```text
max_cost
max_input_tokens
max_output_tokens
max_context_tokens
max_tool_calls
max_latency_ms
max_retries
```

## Consumption semantics

A request is evaluated against the remaining budget before starting a potentially expensive operation.

After execution, actual or estimated usage is recorded.

A budget breach is not silently ignored.
