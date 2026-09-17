from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from twin.model import Component, DigitalTwin
from faults.injector import Fault, FaultInjector


class Simulator:
    def load(self, scenario_path: str | Path) -> tuple[DigitalTwin, Fault, Dict]:
        data = json.loads(Path(scenario_path).read_text(encoding="utf-8"))
        twin = DigitalTwin(
            twin_id=data["twin_id"],
            components={
                c["id"]: Component(c["id"], c["kind"], c["state"])
                for c in data["components"]
            },
        )
        f = data["fault"]
        fault = Fault(
            fault_id=f["fault_id"],
            target=f["target"],
            degraded_state=f["degraded_state"],
            symptom_metric=f["symptom_metric"],
            symptom_log=f["symptom_log"],
        )
        return twin, fault, data["verification"]

    def inject(self, twin: DigitalTwin, fault: Fault) -> Dict:
        return FaultInjector().inject(twin, fault)

    def reset(self, twin: DigitalTwin, fault: Fault) -> None:
        FaultInjector().reset(twin, fault)

    def verify(self, twin: DigitalTwin, verification: Dict) -> str:
        observed = twin.components[verification["target"]].state
        return "VERIFIED" if observed == verification["expected_state"] else "FAILED"
