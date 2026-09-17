from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from typing import Any

from .product import ProductService
from .ui import HTML


def make_product_handler(service: ProductService):
    class Handler(BaseHTTPRequestHandler):
        server_version = "AI-DevOps-Product/3.13"

        def send_json(self, code: int, obj: dict[str, Any]):
            raw = json.dumps(obj, ensure_ascii=False, indent=2).encode()
            self.send_response(code); self.send_header("content-type", "application/json; charset=utf-8")
            self.send_header("content-length", str(len(raw))); self.end_headers(); self.wfile.write(raw)

        def send_html(self):
            raw = HTML.encode(); self.send_response(200); self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("content-length", str(len(raw))); self.end_headers(); self.wfile.write(raw)

        def body(self):
            n = int(self.headers.get("content-length", "0"))
            if n > 1_000_000: raise ValueError("payload_too_large")
            return json.loads(self.rfile.read(n) or b"{}")

        def do_GET(self):
            parsed = urlparse(self.path)
            path = parsed.path
            try:
                if path in {"/", "/ui"}: return self.send_html()
                if path == "/api/v1/product": return self.send_json(200, service.product_info())
                if path == "/api/v1/dashboard/summary":
                    tenant = parse_qs(parsed.query).get("tenant_id", [None])[0]
                    return self.send_json(200, service.dashboard_summary(tenant))
                if path == "/api/v1/incidents":
                    tenant = parse_qs(parsed.query).get("tenant_id", [None])[0]
                    return self.send_json(200, service.list_incidents(tenant))
                if path == "/api/v1/telemetry/events":
                    q = parse_qs(parsed.query)
                    tenant = q.get("tenant_id", [None])[0]
                    limit = int(q.get("limit", [100])[0])
                    return self.send_json(200, service.list_telemetry_events(tenant, limit))
                if path == "/api/v1/connectors":
                    return self.send_json(200, service.connector_metadata())
                if path == "/api/v1/connectors/health":
                    return self.send_json(200, service.connector_health())
                if path == "/api/v1/connectors/linux/snapshot":
                    return self.send_json(200, service.linux_snapshot())
                if path == "/api/v1/connectors/kubernetes/pods":
                    namespace = parse_qs(parsed.query).get("namespace", [""])[0]
                    return self.send_json(200, service.k8s_pods(namespace))
                if path == "/api/v1/telemetry/status":
                    import os
                    return self.send_json(200, {"status":"ok", "prometheus_configured": bool(os.getenv("PROMETHEUS_URL"))})
                if path == "/api/v1/investigations":
                    q = parse_qs(parsed.query)
                    tenant = q.get("tenant_id", [None])[0]
                    limit = int(q.get("limit", [100])[0])
                    return self.send_json(200, service.list_investigations(tenant, limit))
                if path.startswith("/api/v1/investigations/"):
                    return self.send_json(200, service.get_investigation(path.rsplit("/",1)[-1]))
                if path.startswith("/api/v1/incidents/") and path.endswith("/investigate"):
                    incident_id = path.split("/")[-2]
                    return self.send_json(200, service.investigate_incident(incident_id, {"mode": "dry-run"}))
                if path.startswith("/api/v1/incidents/"):
                    return self.send_json(200, service.get_incident(path.rsplit("/",1)[-1]))
                return self.send_json(404, {"status":"error","error_code":"not_found"})
            except FileNotFoundError as exc: return self.send_json(404, {"status":"error","error_code":str(exc)})
            except Exception as exc: return self.send_json(400, {"status":"error","error_code":str(exc)})

        def do_POST(self):
            try:
                if self.path == "/api/v1/demo/seed": return self.send_json(201, service.seed_demo())
                if self.path == "/api/v1/incidents": return self.send_json(201, service.create_incident(self.body()))
                if self.path == "/api/v1/telemetry/events":
                    payload = self.body()
                    if "events" in payload: return self.send_json(202, service.ingest_telemetry_events(payload))
                    return self.send_json(202, service.ingest_telemetry_event(payload))
                if self.path == "/api/v1/telemetry/otlp":
                    payload = self.body()
                    tenant = self.headers.get("X-AIOPS-Tenant", "")
                    environment = self.headers.get("X-AIOPS-Environment", "")
                    severity = self.headers.get("X-AIOPS-Severity", "info")
                    return self.send_json(202, service.ingest_otlp(payload, tenant, environment, severity))
                if self.path == "/api/v1/telemetry/prometheus/query":
                    return self.send_json(200, service.query_prometheus(str(self.body().get("query", ""))))
                if self.path == "/api/v1/telemetry/prometheus/poll":
                    return self.send_json(202, service.poll_prometheus(self.body()))
                if self.path == "/api/v1/investigations":
                    payload = self.body()
                    return self.send_json(201, service.investigate_incident(str(payload.get("incident_id", "")), payload))
                if self.path.startswith("/api/v1/incidents/") and self.path.endswith("/investigate"):
                    incident_id = self.path.split("/")[-2]
                    return self.send_json(201, service.investigate_incident(incident_id, self.body()))
                return self.send_json(404, {"status":"error","error_code":"not_found"})
            except Exception as exc: return self.send_json(400, {"status":"error","error_code":str(exc)})

        def log_message(self, fmt, *args): return
    return Handler


def serve_product(service: ProductService, host: str, port: int):
    server = ThreadingHTTPServer((host, port), make_product_handler(service))
    print(f"AI DevOps Product Runtime listening on http://{host}:{port}")
    server.serve_forever()
