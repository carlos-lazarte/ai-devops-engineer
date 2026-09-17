from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from twin.model import DigitalTwin


@dataclass(frozen=True)
class Fault:
    fault_id: str
    target: str
    degraded_state: str
    symptom_metric: str
    symptom_log: str


class FaultInjector:
    def inject(self, twin: DigitalTwin, fault: Fault) -> Dict:
        twin.set_state(fault.target, fault.degraded_state)
        twin.add_metric(fault.symptom_metric)
        twin.add_log(fault.symptom_log)
        return {
            "fault_id": fault.fault_id,
            "target": fault.target,
            "status": "injected",
        }

    def reset(self, twin: DigitalTwin, fault: Fault) -> None:
        twin.set_state(fault.target, "healthy")
