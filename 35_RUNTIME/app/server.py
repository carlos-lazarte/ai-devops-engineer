from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from time import perf_counter
from typing import Any

from prometheus_client import CONTENT_TYPE_LATEST

from .audit import audit
from .claude_client import analyze_with_claude
from .core import RAG_TOP_K, VaultReader, assemble_context, build_prompt, request_id
from .metrics import (
    CLAUDE_DURATION,
    CLAUDE_REQUESTS,
    HTTP_INFLIGHT,
    HTTP_REQUESTS,
    HTTP_REQUEST_DURATION,
    INCIDENT_REQUESTS,
    SEARCH_REQUESTS,
    metrics_payload,
)


class RuntimeService:
    def __init__(self, vault_root: Path):
        self.vault = VaultReader(vault_root)

    def search(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            hits = self.vault.search(payload.get("query", ""), int(payload.get("limit", RAG_TOP_K)))
            SEARCH_REQUESTS.labels(outcome="success").inc()
            return {"request_id": request_id(), "status": "ok", "results": [h.__dict__ for h in hits]}
        except Exception:
            SEARCH_REQUESTS.labels(outcome="error").inc()
            raise

    def incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        incident_id = str(payload.get("incident_id", "")).strip()
        mode = str(payload.get("mode", "dry-run")).strip()
        try:
            context = assemble_context(self.vault, incident_id, RAG_TOP_K)
            prompt = build_prompt(context)
            result: dict[str, Any] = {
                "request_id": request_id(),
                "status": "ok",
                "mode": mode,
                "incident_id": incident_id,
                "context": context,
                "prompt": prompt,
                "approval_required": True,
            }
            if mode == "claude":
                started = perf_counter()
                try:
                    result["claude"] = analyze_with_claude(prompt)
                    CLAUDE_REQUESTS.labels(outcome="success").inc()
                except Exception:
                    CLAUDE_REQUESTS.labels(outcome="error").inc()
                    raise
                finally:
                    CLAUDE_DURATION.observe(perf_counter() - started)
            elif mode != "dry-run":
                raise ValueError("invalid_mode")
            INCIDENT_REQUESTS.labels(mode=mode, outcome="success").inc()
            audit({
                "request_id": result["request_id"],
                "actor": "runtime-api",
                "operation": "incident_analyze",
                "incident_id": incident_id,
                "mode": mode,
                "result": "ok",
            })
            return result
        except Exception:
            if mode not in {"dry-run", "claude"}:
                normalized_mode = "invalid"
            else:
                normalized_mode = mode
            INCIDENT_REQUESTS.labels(mode=normalized_mode, outcome="error").inc()
            raise


def make_handler(service: RuntimeService):
    class Handler(BaseHTTPRequestHandler):
        server_version = "AI-DevOps-Runtime/2.1"

        def _send(self, code: int, obj: dict[str, Any], content_type: str = "application/json; charset=utf-8"):
            raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("content-type", content_type)
            self.send_header("content-length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _canonical_path(self) -> str:
            aliases = {
                "/api/v1/health": "/health",
                "/api/v1/ready": "/ready",
                "/api/v1/metrics": "/metrics",
                "/api/v1/version": "/version",
                "/api/v1/search": "/search",
                "/api/v1/incidents/analyze": "/incident/analyze",
            }
            return aliases.get(self.path, self.path)

        def _route_name(self) -> str:
            canonical = self._canonical_path()
            if canonical in {"/health", "/ready", "/metrics", "/version", "/search", "/incident/analyze"}:
                return canonical
            return "UNMATCHED"

        def _record(self, route: str, started: float, code: int):
            status_class = f"{code // 100}xx"
            HTTP_REQUESTS.labels(route=route, method=self.command, status_class=status_class).inc()
            HTTP_REQUEST_DURATION.labels(route=route, method=self.command).observe(perf_counter() - started)
            HTTP_INFLIGHT.dec()

        def _begin(self):
            HTTP_INFLIGHT.inc()
            return perf_counter()

        def do_GET(self):  # noqa: N802
            started = self._begin()
            route = self._route_name()
            code = 200
            try:
                if self._canonical_path() == "/health":
                    self._send(200, {"status": "ok"})
                    return
                if self._canonical_path() == "/ready":
                    self._send(200, {"status": "ready", "vault": str(service.vault.root)})
                    return
                if self._canonical_path() == "/version":
                    self._send(200, {"status": "ok", "platform_version": "2.1.0", "api_version": "v1", "runtime_version": "2.1"})
                    return
                if self._canonical_path() == "/metrics":
                    raw, content_type = metrics_payload()
                    self.send_response(200)
                    self.send_header("content-type", content_type)
                    self.send_header("content-length", str(len(raw)))
                    self.end_headers()
                    self.wfile.write(raw)
                    return
                code = 404
                self._send(code, {"status": "error", "error_code": "not_found"})
            finally:
                self._record(route, started, code)

        def do_POST(self):  # noqa: N802
            started = self._begin()
            route = self._route_name()
            code = 200
            try:
                try:
                    length = int(self.headers.get("content-length", "0"))
                except ValueError:
                    code = 400
                    self._send(code, {"status": "error", "error_code": "invalid_content_length"})
                    return
                if length > 1_000_000:
                    code = 413
                    self._send(code, {"status": "error", "error_code": "payload_too_large"})
                    return
                try:
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    if self._canonical_path() == "/search":
                        self._send(200, service.search(payload))
                        return
                    if self._canonical_path() == "/incident/analyze":
                        self._send(200, service.incident(payload))
                        return
                    code = 404
                    self._send(code, {"status": "error", "error_code": "not_found"})
                except FileNotFoundError as exc:
                    code = 404
                    self._send(code, {"status": "error", "error_code": str(exc)})
                except RuntimeError as exc:
                    code = 503
                    self._send(code, {"status": "error", "error_code": str(exc)})
                except (ValueError, TypeError, json.JSONDecodeError) as exc:
                    code = 400
                    self._send(code, {"status": "error", "error_code": str(exc)})
                except Exception:
                    code = 500
                    self._send(code, {"status": "error", "error_code": "internal_error"})
            finally:
                self._record(route, started, code)

        def log_message(self, fmt, *args):
            return

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path(".."))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    service = RuntimeService(args.vault)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(service))
    print(f"AI DevOps Runtime listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
