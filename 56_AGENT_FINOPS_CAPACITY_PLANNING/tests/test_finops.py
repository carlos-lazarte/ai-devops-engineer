import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from finops.allocator import allocate
from forecasting.simple_forecast import forecast_cost
from capacity.planner import plan
from anomaly.detector import detect


def test_cost_allocation():
    events = [
        {"tenant_id":"a","environment":"lab","model_id":"m1","skill_id":"s1","task_class":"standard","estimated_cost":1.0,"input_tokens":10,"output_tokens":5,"tool_calls":1},
        {"tenant_id":"a","environment":"lab","model_id":"m1","skill_id":"s1","task_class":"standard","estimated_cost":2.0,"input_tokens":20,"output_tokens":5,"tool_calls":2},
    ]
    out = allocate(events)
    assert out[0]["cost"] == 3.0
    assert out[0]["tokens"] == 40
    assert out[0]["tool_calls"] == 3


def test_forecast():
    out = forecast_cost([1.0, 2.0, 3.0], 2)
    assert out["forecast_cost"] == 4.0


def test_capacity_headroom():
    out = plan({"tokens":800}, {"tokens":1000})
    assert out["headroom"]["tokens"] == 0.2


def test_anomaly_levels():
    assert detect(100,100)["severity"] == "info"
    assert detect(160,100)["severity"] == "warning"
    assert detect(210,100)["severity"] == "critical"
