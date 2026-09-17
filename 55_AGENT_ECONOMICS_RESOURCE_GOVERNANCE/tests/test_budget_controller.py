import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "metering"))

from controller.budget_controller import BudgetController, Budget
from metering.meter import Usage


def budget():
    return Budget(
        max_cost=0.10,
        max_input_tokens=10000,
        max_output_tokens=5000,
        max_context_tokens=8000,
        max_tool_calls=10,
        max_latency_ms=10000,
        max_retries=2,
    )


def test_continue_within_budget():
    result = BudgetController().decide(
        Usage(input_tokens=1000, output_tokens=500, context_tokens=1000, tool_calls=2, latency_ms=1000, estimated_cost=0.01),
        budget(),
    )
    assert result["decision"] == "CONTINUE"


def test_throttle_near_budget():
    result = BudgetController().decide(
        Usage(input_tokens=8000, output_tokens=500, context_tokens=1000, tool_calls=2, latency_ms=1000, estimated_cost=0.01),
        budget(),
    )
    assert result["decision"] == "THROTTLE"


def test_deny_hard_breach():
    result = BudgetController().decide(
        Usage(input_tokens=10001, output_tokens=0, context_tokens=0, tool_calls=0, latency_ms=0, estimated_cost=0.0),
        budget(),
    )
    assert result["decision"] == "DENY"
