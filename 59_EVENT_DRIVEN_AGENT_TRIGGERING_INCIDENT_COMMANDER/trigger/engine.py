from __future__ import annotations
from typing import Dict

_ALLOWED = {"CANDIDATE", "TRIAGED", "INVESTIGATING"}

def evaluate_trigger(incident: Dict, min_confidence: float = 0.55) -> Dict:
    state = incident.get("state")
    confidence = float(incident.get("confidence", 0.0))
    tenant = incident.get("tenant_id")
    env = incident.get("environment")
    eligible = state in _ALLOWED and confidence >= min_confidence and bool(tenant) and bool(env)
    severity = incident.get("severity", "low")
    human = severity in {"high", "critical"}
    decision = "REQUIRE_HUMAN" if eligible and human else ("ALLOW_ANALYSIS" if eligible else "DENY")
    return {
        "eligible": eligible,
        "policy_decision": decision,
        "approval_required": human,
        "execution_mode": "ANALYSIS_ONLY" if decision != "DENY" else "ANALYSIS_ONLY",
        "reason": "eligible incident candidate" if eligible else "candidate failed trigger eligibility policy",
    }

def build_trigger_request(incident: Dict, request_id: str = "trigger-0001", min_confidence: float = 0.55) -> Dict:
    ev = evaluate_trigger(incident, min_confidence)
    return {
        "trigger_id": request_id,
        "incident_id": incident.get("incident_id"),
        "tenant_id": incident.get("tenant_id"),
        "environment": incident.get("environment"),
        "reason": ev["reason"],
        "severity": incident.get("severity", "low"),
        "confidence": float(incident.get("confidence", 0.0)),
        "policy_decision": ev["policy_decision"],
        "execution_mode": ev["execution_mode"],
        "approval_required": ev["approval_required"],
        "source_event_ids": list(incident.get("signals", [])),
        "provenance": list(incident.get("provenance", [])),
    }
