from __future__ import annotations

from typing import Dict, List


class AdaptivePlanner:
    """Deterministic, plan-only reference planner."""

    def plan(
        self,
        task_id: str,
        goal: str,
        tenant_id: str,
        environment: str,
    ) -> Dict:
        normalized = goal.lower()
        selected_skills: List[str] = []
        evidence_required: List[str] = []

        if "kubernetes" in normalized or "node not ready" in normalized:
            selected_skills = ["kubernetes-troubleshooting"]
            evidence_required = [
                "node status",
                "kubelet logs",
                "recent change context",
            ]
        elif "tls" in normalized or "certificate" in normalized:
            evidence_required = [
                "certificate metadata",
                "endpoint verification",
                "recent rotation record",
            ]
        elif "terraform" in normalized or "drift" in normalized:
            evidence_required = [
                "terraform plan",
                "state context",
                "change history",
            ]

        approval_required = (
            environment == "prod"
            or any(
                term in normalized
                for term in ("incident", "change", "remediate", "execute", "restart")
            )
        )

        steps = [
            {
                "order": 1,
                "objective": "collect relevant evidence",
                "evidence": evidence_required,
            },
            {
                "order": 2,
                "objective": "retrieve relevant knowledge and runbooks",
                "evidence": [],
                "skill": selected_skills[0] if selected_skills else None,
            },
            {
                "order": 3,
                "objective": "identify hypotheses and missing evidence",
                "evidence": evidence_required,
            },
            {
                "order": 4,
                "objective": "produce bounded diagnostic or remediation proposal",
                "evidence": [],
                "approval_required": approval_required,
            },
        ]

        return {
            "task_id": task_id,
            "tenant_id": tenant_id,
            "environment": environment,
            "status": "planned",
            "assumptions": [],
            "evidence_required": evidence_required,
            "evidence_found": [],
            "selected_skills": selected_skills,
            "selected_tools": [],
            "steps": steps,
            "policy_checked": True,
            "approval_required": approval_required,
            "execution_mode": "plan_only",
        }
