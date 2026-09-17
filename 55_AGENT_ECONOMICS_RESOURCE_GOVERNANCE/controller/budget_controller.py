from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from metering.meter import Usage


@dataclass(frozen=True)
class Budget:
    max_cost: float
    max_input_tokens: int
    max_output_tokens: int
    max_context_tokens: int
    max_tool_calls: int
    max_latency_ms: float
    max_retries: int


class BudgetController:
    def __init__(self, soft_ratio: float = 0.80) -> None:
        self.soft_ratio = soft_ratio

    def decide(self, usage: Usage, budget: Budget) -> Dict:
        hard_breach = []
        soft_breach = []

        checks = {
            "cost": (usage.estimated_cost, budget.max_cost),
            "input_tokens": (usage.input_tokens, budget.max_input_tokens),
            "output_tokens": (usage.output_tokens, budget.max_output_tokens),
            "context_tokens": (usage.context_tokens, budget.max_context_tokens),
            "tool_calls": (usage.tool_calls, budget.max_tool_calls),
            "latency_ms": (usage.latency_ms, budget.max_latency_ms),
        }

        for name, (actual, limit) in checks.items():
            if limit <= 0:
                continue
            if actual > limit:
                hard_breach.append(name)
            elif actual >= limit * self.soft_ratio:
                soft_breach.append(name)

        if hard_breach:
            decision = "DENY"
            reasons = [f"hard_limit:{x}" for x in hard_breach]
        elif soft_breach:
            decision = "THROTTLE"
            reasons = [f"soft_limit:{x}" for x in soft_breach]
        else:
            decision = "CONTINUE"
            reasons = []

        remaining = {
            name: max(limit - actual, 0)
            for name, (actual, limit) in checks.items()
        }

        return {
            "decision": decision,
            "policy_checked": True,
            "reasons": reasons,
            "remaining": remaining,
        }
