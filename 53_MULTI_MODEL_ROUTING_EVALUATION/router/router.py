from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

TIER = {"standard": 1, "advanced": 2, "critical": 3}

@dataclass(frozen=True)
class ModelProfile:
    model_id: str
    provider: str
    quality_tier: str
    capabilities: List[str]
    estimated_cost_per_1k_tokens: float
    estimated_latency_ms: float

class ModelRouter:
    def __init__(self, profiles: List[ModelProfile]):
        self.profiles = profiles

    def route(
        self,
        task_id: str,
        task: str,
        task_class: str,
        environment: str,
        min_quality_tier: str = "standard",
        max_cost_per_1k_tokens: float = 0.02,
        max_latency_ms: float = 12000,
    ) -> Dict:
        required = TIER[min_quality_tier]
        critical = task_class == "critical"

        candidates = []
        for p in self.profiles:
            if TIER[p.quality_tier] < required:
                continue
            if critical and TIER[p.quality_tier] < TIER["critical"]:
                continue
            if p.estimated_cost_per_1k_tokens > max_cost_per_1k_tokens:
                continue
            if p.estimated_latency_ms > max_latency_ms:
                continue
            candidates.append(p)

        candidates.sort(key=lambda p: (TIER[p.quality_tier], p.estimated_cost_per_1k_tokens, p.estimated_latency_ms))

        if not candidates:
            return {
                "task_id": task_id,
                "decision": "blocked",
                "selected_model": None,
                "candidates": [],
                "policy_checked": True,
                "reason": "no_eligible_registered_model",
            }

        selected = candidates[0]
        return {
            "task_id": task_id,
            "decision": "selected",
            "selected_model": selected.model_id,
            "candidates": [
                {
                    "model_id": p.model_id,
                    "provider": p.provider,
                    "quality_tier": p.quality_tier,
                    "estimated_cost_per_1k_tokens": p.estimated_cost_per_1k_tokens,
                    "estimated_latency_ms": p.estimated_latency_ms,
                }
                for p in candidates
            ],
            "policy_checked": True,
            "reason": f"eligible_{selected.quality_tier}_within_constraints",
            "environment": environment,
        }
