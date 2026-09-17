from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict

def request_approval(session: Dict, action: str, scope: Dict, requested_by: str = "incident-commander") -> Dict:
    rid = f"approval-{len(session.get('approval_ids', []))+1:04d}"
    return {"request_id": rid, "incident_id": session["incident_id"], "action": action, "scope": scope, "requested_by": requested_by, "decision": "PENDING", "requested_at": datetime.now(timezone.utc).isoformat()}

def apply_approval(request: Dict, approver: str, decision: str, reason: str = "") -> Dict:
    if decision not in {"APPROVED", "REJECTED"}:
        raise ValueError("decision must be APPROVED or REJECTED")
    out = dict(request)
    out.update({"decision": decision, "approver_identity": approver, "reason": reason, "approved_at": datetime.now(timezone.utc).isoformat()})
    return out

def is_usable(request: Dict, tenant_id: str, environment: str) -> bool:
    return request.get("decision") == "APPROVED" and request.get("scope", {}).get("tenant_id") == tenant_id and request.get("scope", {}).get("environment") == environment
