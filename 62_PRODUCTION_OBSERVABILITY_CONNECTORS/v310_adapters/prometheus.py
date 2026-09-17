from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Any

from .common import ConnectorError, RateLimiter, RetryPolicy, retry_call, validate_endpoint


class PrometheusConnector:
    """Read-only Prometheus connector with bounded responses, retries and rate limiting."""

    def __init__(self, base_url: str | None = None, timeout: float | None = None):
        self.base_url = validate_endpoint(base_url or os.getenv("PROMETHEUS_URL", "http://127.0.0.1:9090"))
        self.timeout = float(timeout or os.getenv("PROMETHEUS_TIMEOUT", "5"))
        self.max_response_bytes = int(os.getenv("PROMETHEUS_MAX_RESPONSE_BYTES", "2000000"))
        self.rate_limiter = RateLimiter(float(os.getenv("PROMETHEUS_RATE", "2")), int(os.getenv("PROMETHEUS_BURST", "4")))
        self.token = os.getenv("PROMETHEUS_BEARER_TOKEN", "")

    def _request(self, query: str) -> dict[str, Any]:
        if not query or len(query) > 4096:
            raise ConnectorError("invalid_promql", "PromQL is empty or too long")
        self.rate_limiter.acquire()
        params = urllib.parse.urlencode({"query": query})
        req = urllib.request.Request(f"{self.base_url}/api/v1/query?{params}", method="GET")
        req.add_header("Accept", "application/json")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        def call():
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read(self.max_response_bytes + 1)
                if len(raw) > self.max_response_bytes:
                    raise ConnectorError("response_too_large", "Prometheus response exceeded configured limit")
                payload = json.loads(raw.decode("utf-8"))
                if payload.get("status") != "success":
                    raise ConnectorError("prometheus_error", str(payload.get("error", "query failed")))
                return payload
        return retry_call(call, RetryPolicy.from_env(), retry_on=(OSError, TimeoutError, json.JSONDecodeError, ConnectorError))

    def health(self) -> dict[str, Any]:
        try:
            self._request("up")
            return {"name": "prometheus", "status": "healthy", "endpoint": self.base_url}
        except Exception as exc:
            return {"name": "prometheus", "status": "unhealthy", "endpoint": self.base_url,
                    "error": getattr(exc, "code", str(exc))}

    def query(self, query: str) -> dict[str, Any]:
        return self._request(query)
