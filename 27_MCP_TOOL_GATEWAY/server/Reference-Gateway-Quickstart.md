---
type: lab
domain: ai
technology: mcp
status: prototype
---

# Reference Gateway Quickstart

The included server is a local reference implementation for experimenting with tool routing and policy. It is **not a production MCP server** and does not execute commands or contact external systems.

## Requirements

Python 3.11+.

## Run

From the Vault root:

```bash
python 27_MCP_TOOL_GATEWAY/server/reference_gateway.py \
  --vault . \
  --stdio
```

The process reads one JSON request per line from stdin and emits one JSON response per line to stdout.

## Example

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

Then call a tool:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_notes","arguments":{"query":"kubernetes node notready","limit":5}}}
```

## Important distinction

This is a **MCP-shaped reference interface** using JSON-RPC-style messages. It is intended to validate contracts, routing, policy, and retrieval independently of a particular MCP SDK or client integration.
