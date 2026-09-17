# Secret Reference Model

The runtime should carry references, not secret material.

```yaml
secret_ref:
  provider: vault
  path: kv/data/ai-devops/claude
  version: latest
  purpose: llm-api
  ttl_seconds: 300
```

The adapter resolves the reference only at the point of use. The resolved value must stay in process memory and must not be returned in tool responses.
