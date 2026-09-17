# Claude Setup

The Vault does not ship with credentials.

## Environment

Provide the API key only through the environment used by the external client:

```bash
export ANTHROPIC_API_KEY='REPLACE_ME'
```

Do not place the key in:

- Markdown notes
- YAML frontmatter
- Git repositories
- shell history when avoidable
- incident evidence fixtures

## Safe first run

Start with the existing dry-run workflow before enabling any external call.

## Validation

Confirm that the client can:

1. build a Context Packet;
2. identify source references;
3. return structured fields;
4. distinguish facts from hypotheses;
5. request human approval for proposed changes.
