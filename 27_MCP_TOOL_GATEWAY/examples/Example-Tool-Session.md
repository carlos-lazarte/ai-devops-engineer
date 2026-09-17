---
type: lab
domain: ai
technology: mcp
status: active
---

# Example Tool Session

## 1. Discover tools

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

## 2. Search the Vault

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_notes","arguments":{"query":"Kubernetes NodeNotReady","limit":5}}}
```

## 3. Read a returned note

Use the returned `note_id` as the exact input to `read_note`.

## 4. Retrieve the related runbook

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"retrieve_runbook","arguments":{"problem":"node recovery","technology":"kubernetes","limit":5}}}
```

## 5. Agent behavior

The agent should cite the retrieved note paths as provenance and clearly separate factual content from any inference it generates.
