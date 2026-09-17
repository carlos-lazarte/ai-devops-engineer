import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from twin.simulator import Simulator


def main() -> int:
    parser = argparse.ArgumentParser(description="Digital Twin simulator")
    parser.add_argument("--scenario", default=str(ROOT / "scenarios" / "k8s-node-notready.json"))
    parser.add_argument("--action", choices=["inject", "reset"], default="inject")
    args = parser.parse_args()

    sim = Simulator()
    twin, fault, verification = sim.load(args.scenario)

    if args.action == "inject":
        sim.inject(twin, fault)
        result = {
            "scenario_twin": twin.twin_id,
            "fault_id": fault.fault_id,
            "state": twin.components[fault.target].state,
            "verification": sim.verify(twin, verification),
            "external_infrastructure_contacted": False,
        }
    else:
        sim.inject(twin, fault)
        sim.reset(twin, fault)
        result = {
            "scenario_twin": twin.twin_id,
            "fault_id": fault.fault_id,
            "state": twin.components[fault.target].state,
            "verification": sim.verify(twin, verification),
            "external_infrastructure_contacted": False,
        }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
