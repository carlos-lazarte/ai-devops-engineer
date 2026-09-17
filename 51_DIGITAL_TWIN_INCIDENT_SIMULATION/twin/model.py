from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Component:
    component_id: str
    kind: str
    state: str = "healthy"


@dataclass
class DigitalTwin:
    twin_id: str
    components: Dict[str, Component] = field(default_factory=dict)
    telemetry: Dict[str, List[str]] = field(default_factory=lambda: {"metrics": [], "logs": []})

    def set_state(self, component_id: str, state: str) -> None:
        if component_id not in self.components:
            raise KeyError(component_id)
        self.components[component_id].state = state

    def add_metric(self, metric: str) -> None:
        self.telemetry["metrics"].append(metric)

    def add_log(self, log: str) -> None:
        self.telemetry["logs"].append(log)

    def healthy(self, component_id: str) -> bool:
        return self.components[component_id].state == "healthy"
