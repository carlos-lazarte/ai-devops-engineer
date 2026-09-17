from dataclasses import dataclass


@dataclass
class Decision:
    allowed: bool
    reason: str


def evaluate(ctx: dict) -> Decision:
    required = ["principal", "tenant_id", "environment", "tool", "risk"]
    missing = [k for k in required if not ctx.get(k)]
    if missing:
        return Decision(False, f"missing:{','.join(missing)}")
    if ctx["tool"] == "execute_change":
        return Decision(False, "critical_tool_disabled")
    if ctx["tool"] == "propose_change" and not ctx.get("approval_id"):
        return Decision(False, "approval_required")
    return Decision(True, "allowed")


def test_default_deny_on_missing_tenant():
    d = evaluate({"principal": "u", "environment": "lab", "tool": "read_note", "risk": "low"})
    assert d.allowed is False


def test_propose_change_requires_approval():
    base = {"principal": "u", "tenant_id": "t", "environment": "lab", "tool": "propose_change", "risk": "high"}
    assert evaluate(base).allowed is False
    base["approval_id"] = "APR-1"
    assert evaluate(base).allowed is True


def test_execute_change_disabled():
    base = {"principal": "u", "tenant_id": "t", "environment": "prod", "tool": "execute_change", "risk": "critical", "approval_id": "APR-2"}
    assert evaluate(base).allowed is False
