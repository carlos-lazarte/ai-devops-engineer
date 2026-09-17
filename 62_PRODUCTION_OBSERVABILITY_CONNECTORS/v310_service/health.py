from __future__ import annotations

from typing import Any

from .registry import ConnectorRegistry


def connector_health(registry: ConnectorRegistry) -> dict[str, Any]:
    out = registry.health()
    statuses = {item.get("status") for item in out["connectors"]}
    out["status"] = "ok" if statuses <= {"healthy", "configured", "not_configured"} else "degraded"
    return out
