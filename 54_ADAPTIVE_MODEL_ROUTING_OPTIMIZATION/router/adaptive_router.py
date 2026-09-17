from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


TIER = {"standard": 1, "advanced": 2, "critical": 3}


@dataclass(frozen=True)
class Profile:
    model_id: str
    provider: str
    quality_tier: str
    estimated_cost: float
    estimated_latency_ms: float
    capabilities: List[str]


class AdaptiveRouter:
    def __init__(self, profiles: List[Profile], history: List[Dict], weights: Dict | None = None):
        self.profiles = profiles
        self.history = history
        self.weights = weights or {
            "quality": 0.45,
            "reliability": 0.30,
            "latency": 0.15,
            "cost": 0.10,
        }

    def _history_for(self, model_id: str, task_class: str) -> Dict:
        matches = [h for h in self.history if h["model_id"] == model_id and h["task_class"] == task_class]
        if not matches:
            return {}
        return max(matches, key=lambda x: x.get("observations", 0))

    def route(
        self,
        task_id: str,
        task: str,
        task_class: str,
        environment: str,
        min_quality_tier: str = "standard",
        max_cost_per_1k_tokens: float = 0.02,
        max_latency_ms: float = 12000,
        adaptive: bool = True,
    ) -> Dict:
        required = TIER[min_quality_tier]
        candidates = []

        for p in self.profiles:
            if TIER[p.quality_tier] < required:
                continue
            if task_class == "critical" and TIER[p.quality_tier] < TIER["critical"]:
                continue
            if p.estimated_cost > max_cost_per_1k_tokens:
                continue
            if p.estimated_latency_ms > max_latency_ms:
                continue

            h = self._history_for(p.model_id, task_class)
            if adaptive and h.get("observations", 0) >= 2:
                quality = (h.get("success_rate", 0) + h.get("grounding_rate", 0)) / 2
                reliability = h.get("safety_pass_rate", 0) * h.get("success_rate", 0)
                latency_score = 1 / max(h.get("mean_latency_ms", p.estimated_latency_ms), 1)
                cost_score = 1 / max(h.get("mean_cost_per_1k_tokens", p.estimated_cost) + 1e-9, 1e-9)
                candidates.append({
                    "profile": p,
                    "observations": h.get("observations", 0),
                    "quality": quality,
                    "reliability": reliability,
                    "latency_ms": h.get("mean_latency_ms", p.estimated_latency_ms),
                    "cost": h.get("mean_cost_per_1k_tokens", p.estimated_cost),
                    "latency_score": latency_score,
                    "cost_score": cost_score,
                })
            else:
                candidates.append({
                    "profile": p,
                    "observations": 0,
                    "quality": TIER[p.quality_tier] / TIER["critical"],
                    "reliability": 1.0,
                    "latency_ms": p.estimated_latency_ms,
                    "cost": p.estimated_cost,
                    "latency_score": 1 / max(p.estimated_latency_ms, 1),
                    "cost_score": 1 / max(p.estimated_cost + 1e-9, 1e-9),
                })

        if not candidates:
            return {
                "task_id": task_id,
                "decision": "blocked",
                "selected_model": None,
                "routing_mode": "adaptive" if adaptive else "static",
                "policy_checked": True,
                "candidates": [],
                "reason": "no_eligible_model",
            }

        def utility(c):
            return (
                self.weights["quality"] * c["quality"]
                + self.weights["reliability"] * c["reliability"]
                + self.weights["latency"] * (1 / max(c["latency_ms"], 1))
                + self.weights["cost"] * (1 / max(c["cost"] + 1e-9, 1e-9))
            )

        # Deterministic ordering: higher utility, then higher quality tier, then lower latency, then lower cost.
        candidates.sort(
            key=lambda c: (
                utility(c),
                TIER[c["profile"].quality_tier],
                -c["latency_ms"],
                -c["cost"],
            ),
            reverse=True,
        )

        selected = candidates[0]
        return {
            "task_id": task_id,
            "decision": "selected",
            "selected_model": selected["profile"].model_id,
            "routing_mode": "adaptive" if adaptive else "static",
            "policy_checked": True,
            "reason": "adaptive_utility_with_hard_constraints",
            "environment": environment,
            "candidates": [
                {
                    "model_id": c["profile"].model_id,
                    "quality_tier": c["profile"].quality_tier,
                    "observations": c["observations"],
                    "quality": round(c["quality"], 6),
                    "reliability": round(c["reliability"], 6),
                    "latency_ms": c["latency_ms"],
                    "cost_per_1k_tokens": c["cost"],
                }
                for c in candidates
            ],
        }
