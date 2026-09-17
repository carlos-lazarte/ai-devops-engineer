# Gateway tests

The reference tests use `pytest`.

Run:

```bash
python -m pytest -q 27_MCP_TOOL_GATEWAY/tests/test_reference_gateway.py
```

The tests cover tool discovery, retrieval, unknown-tool denial, and path traversal denial.
