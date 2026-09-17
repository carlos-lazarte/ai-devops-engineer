from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .skill_registry import SkillRegistry
from .autonomy_policy import AutonomyPolicy

@dataclass(frozen=True)
class SkillTask:
    task_id: str
    skill_id: str
    tenant_id: str
    environment: str
    evidence: tuple[str, ...]
    approved: bool = False

class SkillExecutor:
    """Simulation-only executor. Never performs real infrastructure actions."""
    def __init__(self, registry: SkillRegistry, policy: AutonomyPolicy):
        self.registry = registry
        self.policy = policy

    def run(self, task: SkillTask) -> dict:
        spec = self.registry.get(task.skill_id)
        missing = [e for e in spec.required_evidence if e not in task.evidence]
        if missing:
            return {"status": "blocked", "reason": "missing_evidence", "missing": missing}
        decision = self.policy.evaluate(spec.risk, spec.autonomy_level, task.environment, task.approved)
        if decision.decision != "allow":
            return {"status": decision.decision, "reason": decision.reason, "approval_required": decision.approval_required}
        return {
            "status": "simulated",
            "skill_id": spec.skill_id,
            "task_id": task.task_id,
            "proposed_actions": ["Simulation only: no infrastructure mutation performed"],
            "verification": ["Confirm the plan with an environment-specific validation step"],
        }
