import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from twin.simulator import Simulator


def test_inject_and_reset():
    sim = Simulator()
    scenario = ROOT / "scenarios" / "k8s-node-notready.json"
    twin, fault, verification = sim.load(scenario)

    sim.inject(twin, fault)
    assert twin.healthy("node-01") is False
    assert sim.verify(twin, verification) == "FAILED"

    sim.reset(twin, fault)
    assert twin.healthy("node-01") is True
    assert sim.verify(twin, verification) == "VERIFIED"


def test_fault_is_local_to_twin():
    sim = Simulator()
    scenario = ROOT / "scenarios" / "k8s-node-notready.json"
    twin, fault, _ = sim.load(scenario)
    result = sim.inject(twin, fault)
    assert result["status"] == "injected"
    assert twin.twin_id == "k8s-lab-01"
