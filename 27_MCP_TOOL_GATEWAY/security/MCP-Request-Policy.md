---
type: security
domain: ai
technology: mcp
status: active
---

# MCP Request Policy

## Default

Every request is denied unless:

1. the tool exists in the registry;
2. the argument schema is valid;
3. the requested resource is within the allow-list;
4. the operation is permitted for the caller's tier;
5. limits are satisfied.

## Allowed resources

```text
<VaultRoot>/**/*.md
<VaultRoot>/26_OPERATIONAL_AGENT_LAB/**
```

The actual server may narrow this further through configuration.

## Path rules

Reject:

- absolute paths supplied by callers;
- `..` traversal;
- symlink escapes from the configured Vault root;
- hidden control directories unless explicitly allow-listed;
- non-Markdown files for `read_note`.

## Limits

Reference defaults:

```yaml
max_query_length: 500
max_results: 20
max_note_bytes: 100000
max_related_depth: 2
max_context_packet_bytes: 200000
```

## Future write capability

`create_draft` and `propose_patch` remain outside the v0.8.0 executable server. Any future write tool must require an explicit approval reference and a target allow-list.
