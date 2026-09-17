from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}

@dataclass(frozen=True)
class Decision:
    request_id: str
    decision: str
    reason: str
    risk: str
    approval_required: bool
    policy_version: str

class PolicyEngine:
    def __init__(self, policy_path: str | Path):
        self.policy_path = Path(policy_path)
        self.policy: dict[str, Any] = yaml.safe_load(self.policy_path.read_text(encoding="utf-8"))

    def authorize(self, request: dict[str, Any]) -> Decision:
        request_id = str(request.get("request_id", "unknown"))
        role = request.get("role")
        tool = request.get("tool")
        operation = request.get("operation")
        approval_id = request.get("approval_id")

        role_cfg = self.policy.get("roles", {}).get(role)
        tool_cfg = self.policy.get("tools", {}).get(tool)

        if not role_cfg:
            return self._deny(request_id, "unknown role", "critical", False)
        if not tool_cfg:
            return self._deny(request_id, "tool is not registered", "critical", False)
        if tool_cfg.get("enabled", True) is False:
            return self._deny(request_id, "tool is disabled", tool_cfg.get("risk", "critical"), bool(tool_cfg.get("approval", False)))
        if tool not in role_cfg.get("allowed", []):
            return self._deny(request_id, "role is not authorized for tool", tool_cfg.get("risk", "critical"), bool(tool_cfg.get("approval", False)))
        if operation != tool:
            return self._deny(request_id, "operation does not match tool", tool_cfg.get("risk", "critical"), bool(tool_cfg.get("approval", False)))

        risk = tool_cfg.get("risk", "critical")
        max_risk = role_cfg.get("max_risk", "low")
        if RISK_ORDER[risk] > RISK_ORDER[max_risk]:
            return self._deny(request_id, "risk exceeds role maximum", risk, bool(tool_cfg.get("approval", False)))

        approval_required = bool(tool_cfg.get("approval", False))
        if approval_required and not approval_id:
            return self._deny(request_id, "human approval required", risk, True)

        return Decision(request_id, "allow", "authorized by policy", risk, approval_required, str(self.policy.get("version", "unknown")))

    def _deny(self, request_id: str, reason: str, risk: str, approval_required: bool) -> Decision:
        return Decision(request_id, "deny", reason, risk, approval_required, str(self.policy.get("version", "unknown")))
