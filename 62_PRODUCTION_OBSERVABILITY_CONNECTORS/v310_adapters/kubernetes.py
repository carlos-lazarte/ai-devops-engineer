from __future__ import annotations

import json
import os
import ssl
import urllib.request
from pathlib import Path
from typing import Any

from .common import ConnectorError, RateLimiter, RetryPolicy, retry_call, validate_endpoint


class KubernetesConnector:
    """Read-only Kubernetes API connector using a bounded ServiceAccount-style token."""

    def __init__(self, api_server: str | None = None, token: str | None = None,
                 ca_file: str | None = None, timeout: float | None = None):
        self.api_server = validate_endpoint(api_server or os.getenv("K8S_API_SERVER", "")) if (api_server or os.getenv("K8S_API_SERVER")) else ""
        self.token = token or os.getenv("K8S_BEARER_TOKEN", "")
        self.ca_file = ca_file or os.getenv("K8S_CA_FILE", "")
        self.timeout = float(timeout or os.getenv("K8S_TIMEOUT", "5"))
        self.rate_limiter = RateLimiter(float(os.getenv("K8S_RATE", "1")), int(os.getenv("K8S_BURST", "2")))
        self.max_response_bytes = int(os.getenv("K8S_MAX_RESPONSE_BYTES", "3000000"))
        self._ssl = self._build_ssl()

    def _build_ssl(self):
        if self.api_server.startswith("http://"):
            return None
        context = ssl.create_default_context()
        if self.ca_file:
            context.load_verify_locations(self.ca_file)
        return context

    def _get(self, path: str) -> dict[str, Any]:
        if not self.api_server:
            raise ConnectorError("k8s_not_configured", "K8S_API_SERVER is not configured")
        if not path.startswith("/api/") and not path.startswith("/apis/") and path != "/version":
            raise ConnectorError("invalid_k8s_path", "only Kubernetes API paths are allowed")
        if ".." in path or any(token in path.split("/") for token in ("exec", "attach", "portforward", "proxy")):
            raise ConnectorError("invalid_k8s_path", "exec/attach/portforward/proxy and traversal paths are not allowed")
        self.rate_limiter.acquire()
        req = urllib.request.Request(self.api_server + path, method="GET")
        req.add_header("Accept", "application/json")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        def call():
            with urllib.request.urlopen(req, timeout=self.timeout, context=self._ssl) as resp:
                raw = resp.read(self.max_response_bytes + 1)
                if len(raw) > self.max_response_bytes:
                    raise ConnectorError("response_too_large", "Kubernetes response exceeded configured limit")
                return json.loads(raw.decode("utf-8"))
        return retry_call(call, RetryPolicy.from_env(), retry_on=(OSError, TimeoutError, json.JSONDecodeError))

    def health(self) -> dict[str, Any]:
        try:
            out = self._get("/version")
            return {"name": "kubernetes", "status": "healthy", "endpoint": self.api_server,
                    "gitVersion": out.get("gitVersion")}
        except Exception as exc:
            return {"name": "kubernetes", "status": "unhealthy", "endpoint": self.api_server or None,
                    "error": getattr(exc, "code", str(exc))}

    def list_pods(self, namespace: str = "") -> dict[str, Any]:
        namespace = namespace.strip()
        if len(namespace) > 63 or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in namespace):
            raise ConnectorError("invalid_namespace", "invalid Kubernetes namespace")
        path = f"/api/v1/namespaces/{namespace}/pods" if namespace else "/api/v1/pods"
        return self._get(path)
