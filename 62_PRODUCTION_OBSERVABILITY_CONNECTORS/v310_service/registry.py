from __future__ import annotations

import os
from typing import Any

from v310_adapters.common import ConnectorError
from v310_adapters.kubernetes import KubernetesConnector
from v310_adapters.linux import LinuxConnector
from v310_adapters.prometheus import PrometheusConnector


class ConnectorRegistry:
    def __init__(self):
        self.connectors = {
            "prometheus": PrometheusConnector(),
            "kubernetes": KubernetesConnector(),
            "linux": LinuxConnector(os.getenv("LINUX_PROC_ROOT", "/proc"), os.getenv("LINUX_SYS_ROOT", "/sys")),
            "opentelemetry": {"kind": "collector-gateway", "endpoint": os.getenv("OTEL_COLLECTOR_URL", "")},
        }

    def metadata(self) -> list[dict[str, Any]]:
        return [
            {"name": "prometheus", "mode": "read-only", "credential": "optional bearer token"},
            {"name": "opentelemetry", "mode": "receiver", "credential": "collector-managed"},
            {"name": "kubernetes", "mode": "read-only", "credential": "bearer token / service account"},
            {"name": "linux", "mode": "read-only local procfs/sysfs", "credential": "none"},
        ]

    def health(self) -> dict[str, Any]:
        result = {"status": "ok", "connectors": []}
        for name, connector in self.connectors.items():
            if hasattr(connector, "health"):
                item = connector.health()
            else:
                configured = bool(connector.get("endpoint"))
                item = {"name": name, "status": "configured" if configured else "not_configured", **connector}
                item.pop("endpoint", None) if "endpoint" not in item else None
            result["connectors"].append(item)
        return result

    def get(self, name: str):
        try:
            return self.connectors[name]
        except KeyError as exc:
            raise ConnectorError("connector_not_found", name) from exc
