from __future__ import annotations
from dataclasses import dataclass

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
LEVEL_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}

@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    reason: str
    approval_required: bool

class AutonomyPolicy:
    def __init__(self, production_enabled: bool = False):
        self.production_enabled = production_enabled

    def evaluate(self, risk: str, autonomy_level: str, environment: str, approved: bool = False) -> PolicyDecision:
        if LEVEL_ORDER[autonomy_level] >= LEVEL_ORDER["L4"] and not self.production_enabled:
            return PolicyDecision("deny", "L4 execution is disabled", False)
        approval_required = risk in {"high", "critical"} or LEVEL_ORDER[autonomy_level] >= LEVEL_ORDER["L3"]
        if approval_required and not approved:
            return PolicyDecision("needs_approval", "Explicit approval is required", True)
        if environment == "prod" and not approved:
            return PolicyDecision("deny", "Production requires bound approval", True)
        return PolicyDecision("allow", "Policy conditions satisfied", approval_required)
