from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from .state_machine import LoopState, transition


@dataclass
class ClosedLoopExecutor:
    production_execution_enabled: bool = False
    simulation_enabled: bool = True

    def run(
        self,
        task_id: str,
        action_id: str,
        tool_id: str,
        approval_id: str | None,
        environment: str,
        verification_result: str,
        mode: str = "simulate",
    ) -> Dict[str, Any]:
        if not tool_id:
            return {"status": "rejected", "reason": "tool_id_required"}

        if not approval_id:
            return {
                "status": "rejected",
                "reason": "explicit_approval_required",
                "verification_status": "NOT_RUN",
            }

        if mode == "approved_execution" and not self.production_execution_enabled:
            return {
                "status": "rejected",
                "reason": "production_execution_disabled",
                "verification_status": "NOT_RUN",
            }

        if mode == "simulate" and not self.simulation_enabled:
            return {
                "status": "rejected",
                "reason": "simulation_disabled",
                "verification_status": "NOT_RUN",
            }

        state = LoopState.PLANNED
        state = transition(state, LoopState.AWAITING_APPROVAL)
        state = transition(state, LoopState.APPROVED)
        state = transition(state, LoopState.EXECUTING)
        state = transition(state, LoopState.OBSERVING)

        vr = verification_result.upper()
        if vr == "VERIFIED":
            state = transition(state, LoopState.VERIFIED)
            state = transition(state, LoopState.CLOSED)
            return {
                "task_id": task_id,
                "action_id": action_id,
                "status": "simulated" if mode == "simulate" else "executed",
                "verification_status": "VERIFIED",
                "state": state.value,
                "audit_event_id": f"audit-{task_id}-{action_id}",
                "replanning_required": False,
            }

        if vr == "FAILED":
            state = transition(state, LoopState.FAILED)
            state = transition(state, LoopState.REPLANNING)
            return {
                "task_id": task_id,
                "action_id": action_id,
                "status": "simulated" if mode == "simulate" else "executed",
                "verification_status": "FAILED",
                "state": state.value,
                "audit_event_id": f"audit-{task_id}-{action_id}",
                "replanning_required": True,
            }

        state = transition(state, LoopState.UNKNOWN)
        state = transition(state, LoopState.REPLANNING)
        return {
            "task_id": task_id,
            "action_id": action_id,
            "status": "simulated" if mode == "simulate" else "executed",
            "verification_status": "UNKNOWN",
            "state": state.value,
            "audit_event_id": f"audit-{task_id}-{action_id}",
            "replanning_required": True,
        }
