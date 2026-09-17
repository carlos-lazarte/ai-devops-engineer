import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "27_MCP_TOOL_GATEWAY" / "server" / "reference_gateway.py"


def call(payload):
    proc = subprocess.run(
        [sys.executable, str(SERVER), "--vault", str(ROOT), "--stdio"],
        input=json.dumps(payload) + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


def result(resp):
    return resp["result"]


def test_tools_list():
    r = result(call({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}))
    assert r["status"] == "ok"
    assert "search_notes" in {x["name"] for x in r["tools"]}


def test_search():
    r = result(call({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_notes", "arguments": {"query": "Kubernetes NodeNotReady", "limit": 5}}}))
    assert r["status"] == "ok"
    assert r["results"]


def test_denied_unknown_tool():
    r = result(call({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "exec_shell", "arguments": {"cmd": "id"}}}))
    assert r["status"] == "denied"
    assert r["error_code"] == "tool_not_allowed"


def test_path_traversal_denied():
    r = result(call({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "read_note", "arguments": {"note_id": "../README.md"}}}))
    assert r["status"] == "denied"
    assert r["error_code"] == "path_escape"
