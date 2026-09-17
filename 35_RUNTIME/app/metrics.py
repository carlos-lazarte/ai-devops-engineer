from __future__ import annotations

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

REGISTRY = CollectorRegistry()

HTTP_REQUESTS = Counter(
    "ai_devops_http_requests_total",
    "Total HTTP requests handled by the runtime.",
    ["route", "method", "status_class"],
    registry=REGISTRY,
)
HTTP_REQUEST_DURATION = Histogram(
    "ai_devops_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["route", "method"],
    registry=REGISTRY,
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 30, 60),
)
HTTP_INFLIGHT = Gauge(
    "ai_devops_http_inflight_requests",
    "Number of HTTP requests currently being handled.",
    registry=REGISTRY,
)
SEARCH_REQUESTS = Counter(
    "ai_devops_search_requests_total",
    "Search requests by outcome.",
    ["outcome"],
    registry=REGISTRY,
)
INCIDENT_REQUESTS = Counter(
    "ai_devops_incident_requests_total",
    "Incident-analysis requests by mode and outcome.",
    ["mode", "outcome"],
    registry=REGISTRY,
)
CLAUDE_REQUESTS = Counter(
    "ai_devops_claude_requests_total",
    "Claude provider requests by outcome.",
    ["outcome"],
    registry=REGISTRY,
)
CLAUDE_DURATION = Histogram(
    "ai_devops_claude_request_duration_seconds",
    "Claude provider request duration in seconds.",
    registry=REGISTRY,
    buckets=(0.25, 0.5, 1, 2, 5, 10, 30, 60, 120),
)
VAULT_SEARCH_DURATION = Histogram(
    "ai_devops_vault_search_duration_seconds",
    "Vault search duration in seconds.",
    registry=REGISTRY,
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2),
)


def metrics_payload() -> tuple[bytes, str]:
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST
