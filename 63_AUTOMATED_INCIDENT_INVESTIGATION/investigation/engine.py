from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "35_RUNTIME"
V47 = ROOT / "47_KNOWLEDGE_SKILL_MARKETPLACE_INTELLIGENCE"
V48 = ROOT / "48_KNOWLEDGE_GRAPH_CONTEXT_INTELLIGENCE"
V49 = ROOT / "49_ADAPTIVE_CONTEXT_AGENT_PLANNING"
V59 = ROOT / "59_EVENT_DRIVEN_AGENT_TRIGGERING_INCIDENT_COMMANDER"
V62 = ROOT / "62_PRODUCTION_OBSERVABILITY_CONNECTORS"
for path in (RUNTIME, V47, V48, V49, V59, V62):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.core import VaultReader  # noqa: E402
from app.claude_client import analyze_with_claude  # noqa: E402
from app.audit import audit  # noqa: E402
from discovery.discover import discover  # noqa: E402
from graph.build_graph import build  # noqa: E402
from context.context_planner import plan as plan_context  # noqa: E402
from planner.planner import AdaptivePlanner  # noqa: E402
from trigger.engine import build_trigger_request  # noqa: E402
from v310_service.registry import ConnectorRegistry  # noqa: E402
from .evidence import build_evidence, summarize_telemetry  # noqa: E402
from .hypotheses import build_hypotheses  # noqa: E402


class AutomatedIncidentInvestigator:
    """Deterministic, evidence-first incident investigation with optional LLM augmentation.

    This component never executes remediation. External connector calls are read-only and
    only run when the investigation policy and connector configuration permit them.
    """

    def __init__(self, vault_root: Path, store: Any, connectors: ConnectorRegistry | None = None):
        self.vault_root = vault_root.resolve()
        self.store = store
        self.vault = VaultReader(self.vault_root)
        self.connectors = connectors or ConnectorRegistry()
        self.planner = AdaptivePlanner()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _id(prefix: str) -> str:
        return f"{prefix}-{uuid4().hex[:12]}"

    def _collect_connector_observations(self, incident: dict[str, Any], enabled: bool) -> list[dict[str, Any]]:
        if not enabled:
            return []
        observations: list[dict[str, Any]] = []
        # Linux procfs/sysfs describes the runtime host itself. Do not attach it to a remote
        # incident unless the operator explicitly opts in.
        import os
        if os.getenv("INVESTIGATION_LOCAL_LINUX", "false").lower() in {"1", "true", "yes"}:
            try:
                linux = self.connectors.get("linux")
                observations.append({
                    "evidence_id": "connector:linux.cpu",
                    "type": "connector_observation",
                    "connector": "linux",
                    "status": "observed",
                    "data": linux.cpu_snapshot(),
                    "provenance": {"method": "procfs", "mode": "read-only", "scope": "investigator-host"},
                })
                observations.append({
                    "evidence_id": "connector:linux.memory",
                    "type": "connector_observation",
                    "connector": "linux",
                    "status": "observed",
                    "data": linux.memory(),
                    "provenance": {"method": "procfs", "mode": "read-only", "scope": "investigator-host"},
                })
            except Exception as exc:
                observations.append({
                    "evidence_id": "connector:linux.error",
                    "type": "connector_observation",
                    "connector": "linux",
                    "status": "unavailable",
                    "error": str(exc),
                    "provenance": {"mode": "read-only", "scope": "investigator-host"},
                })

        # Kubernetes is queried only when explicitly configured; never use exec/attach/write paths.
        k8s = self.connectors.get("kubernetes")
        if getattr(k8s, "api_server", ""):
            try:
                namespace = str(incident.get("labels", {}).get("namespace", "")) if isinstance(incident.get("labels"), dict) else ""
                pods = k8s.list_pods(namespace)
                observations.append({
                    "evidence_id": "connector:kubernetes.pods",
                    "type": "connector_observation",
                    "connector": "kubernetes",
                    "status": "observed",
                    "scope": {"namespace": namespace or "all"},
                    "data": {"items": pods.get("items", [])[:100]},
                    "provenance": {"method": "kubernetes-api-get", "mode": "read-only"},
                })
            except Exception as exc:
                observations.append({
                    "evidence_id": "connector:kubernetes.error",
                    "type": "connector_observation",
                    "connector": "kubernetes",
                    "status": "unavailable",
                    "error": str(exc),
                    "provenance": {"mode": "read-only"},
                })
        return observations

    def _knowledge(self, incident: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
        families = sorted({str(e.get("metric_family", "")) for e in events if e.get("metric_family")})
        query = " ".join([
            str(incident.get("candidate_reason", "")),
            str(incident.get("environment", "")),
            " ".join(families),
        ]).strip() or "incident troubleshooting"
        rag = [h.__dict__ for h in self.vault.search(query, 8)]
        graph = build(self.vault_root)
        kg = plan_context(query, graph, max_items=10, max_hops=2)
        skills = discover(query, str(incident.get("environment", "")) or None, 6)
        return {
            "query": query,
            "rag": rag,
            "knowledge_graph": {"items": kg.get("items", []), "limits": kg.get("limits", {})},
            "skills": skills,
        }

    def investigate(self, incident_id: str, mode: str = "dry-run", include_connectors: bool = True) -> dict[str, Any]:
        if mode not in {"dry-run", "claude"}:
            raise ValueError("invalid_mode")
        incident = self.store.get_incident(incident_id)
        if not incident:
            raise FileNotFoundError("incident_not_found")

        trigger = build_trigger_request(incident)
        if trigger["policy_decision"] == "DENY":
            raise ValueError("investigation_trigger_denied")

        events = self.store.list_telemetry_events(incident["tenant_id"], 250)
        allowed_events = [
            e for e in events
            if e.get("environment") == incident["environment"]
            and (not incident.get("signals") or e.get("event_id") in set(incident.get("signals", [])) or e.get("component") in set(incident.get("signals", [])))
        ]
        if not allowed_events:
            allowed_events = [e for e in events if e.get("environment") == incident["environment"]][:40]

        connector_observations = self._collect_connector_observations(incident, include_connectors)
        evidence = build_evidence(incident, allowed_events, connector_observations)
        telemetry_summary = summarize_telemetry(allowed_events)
        hypotheses, unknowns = build_hypotheses(incident, allowed_events)
        knowledge = self._knowledge(incident, allowed_events)

        goal = "incident investigation: " + " ".join([
            str(incident.get("candidate_reason", "")),
            " ".join(telemetry_summary["metric_families"].keys()),
        ])
        plan = self.planner.plan(
            task_id=incident_id,
            goal=goal,
            tenant_id=incident["tenant_id"],
            environment=incident["environment"],
        )
        selected_skill_ids = [row["skill_id"] for row in knowledge["skills"] if row.get("policy_decision") == "eligible"][:3]
        if selected_skill_ids:
            plan["selected_skills"] = selected_skill_ids
        plan["evidence_found"] = [e["evidence_id"] for e in evidence]
        plan["status"] = "investigation_plan_ready"
        plan["execution_mode"] = "plan_only"

        requested_diagnostics = [
            {"order": idx + 1, "objective": item, "approval_required": False}
            for idx, item in enumerate(plan.get("evidence_required", [])[:8])
        ]
        if not requested_diagnostics:
            requested_diagnostics = [
                {"order": 1, "objective": "validate the leading hypothesis with independent read-only evidence", "approval_required": False},
                {"order": 2, "objective": "inspect recent change context", "approval_required": False},
            ]

        proposed_actions = [
            {
                "action_id": "A-COLLECT-READONLY-EVIDENCE",
                "description": "Collect additional read-only evidence required to discriminate hypotheses.",
                "risk": "low",
                "approval_required": False,
                "execution_enabled": False,
            },
            {
                "action_id": "A-PROPOSE-REMEDIATION",
                "description": "Prepare a bounded remediation proposal only after evidence review.",
                "risk": "high",
                "approval_required": True,
                "execution_enabled": False,
            },
        ]

        agent_result: dict[str, Any] | None = None
        if mode == "claude":
            prompt_context = {
                "incident": incident,
                "trigger": trigger,
                "telemetry_summary": telemetry_summary,
                "evidence": evidence,
                "knowledge": knowledge,
                "hypotheses": hypotheses,
                "unknowns": unknowns,
                "requested_diagnostics": requested_diagnostics,
                "proposed_actions": proposed_actions,
                "policy": {
                    "execution_enabled": False,
                    "human_approval_required": True,
                    "read_only_evidence_only": True,
                },
            }
            prompt = self._build_llm_prompt(prompt_context)
            agent_result = analyze_with_claude(prompt)

        investigation = {
            "investigation_id": self._id("inv"),
            "incident_id": incident_id,
            "tenant_id": incident["tenant_id"],
            "environment": incident["environment"],
            "status": "ANALYZED",
            "mode": mode,
            "trigger": trigger,
            "telemetry": telemetry_summary,
            "evidence": evidence,
            "hypotheses": hypotheses,
            "unknowns": unknowns,
            "requested_diagnostics": requested_diagnostics,
            "proposed_actions": proposed_actions,
            "knowledge": knowledge,
            "plan": plan,
            "agent": agent_result,
            "safety": {
                "production_execution_enabled": False,
                "human_approval_required": True,
                "connector_mode": "read-only",
                "root_cause_confirmed": False,
            },
            "provenance": {
                "source_incident": incident_id,
                "source_event_ids": incident.get("signals", []),
                "connector_count": len(connector_observations),
            },
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        self.store.save_investigation(investigation)
        audit({
            "request_id": investigation["investigation_id"],
            "actor": "automated-investigator",
            "operation": "incident_investigation",
            "incident_id": incident_id,
            "mode": mode,
            "result": "ok",
        })
        return investigation

    @staticmethod
    def _build_llm_prompt(context: dict[str, Any]) -> str:
        return """You are an AI DevOps incident investigator. Analyze only the supplied evidence.
Never claim that a command, change, restart, remediation, or external action was executed.
Never invent telemetry or missing evidence. Explicitly separate facts, observations, hypotheses,
missing evidence, recommended diagnostics, and proposed actions. Root cause must remain unconfirmed
unless the supplied evidence independently establishes it. Production execution is disabled and all
remediation requires human approval. Return JSON with keys: summary, confidence, facts, observations,
 hypotheses, recommended_diagnostics, proposed_actions, unknowns, references.

CONTEXT:
""" + json.dumps(context, indent=2, ensure_ascii=False)
