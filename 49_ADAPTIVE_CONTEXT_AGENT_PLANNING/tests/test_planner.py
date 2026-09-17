import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent.parent))

from planner.planner import AdaptivePlanner


def test_k8s_plan_is_plan_only():
    planner = AdaptivePlanner()
    result = planner.plan(
        task_id="PLAN-K8S-001",
        goal="diagnose Kubernetes node not ready incident",
        tenant_id="demo",
        environment="lab",
    )
    assert result["status"] == "planned"
    assert result["policy_checked"] is True
    assert result["approval_required"] is True
    assert result["selected_skills"] == ["kubernetes-troubleshooting"]
    assert result["execution_mode"] == "plan_only"


def test_critical_execution_is_disabled():
    planner = AdaptivePlanner()
    result = planner.plan(
        task_id="PLAN-CRITICAL-001",
        goal="execute production remediation",
        tenant_id="demo",
        environment="prod",
    )
    assert result["execution_mode"] == "plan_only"
    assert result["status"] in {"planned", "blocked"}
