# Provider Adapter Boundary

The platform should isolate provider-specific SDKs behind a provider adapter.

```text
Agent
  ↓
Model Router
  ↓
Provider Adapter
  ├── Anthropic
  ├── Other Provider
  └── Local Runtime
```

The evaluation harness should compare normalized responses, not provider-specific internal formats.
