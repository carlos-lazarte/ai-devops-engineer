import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent.parent))

from engine.executor import ClosedLoopExecutor


def main() -> int:
    p = argparse.ArgumentParser(description="Closed-loop execution simulator")
    p.add_argument("--verification", choices=["VERIFIED", "FAILED", "UNKNOWN"], required=True)
    p.add_argument("--approval-id", default="demo-approval")
    args = p.parse_args()

    result = ClosedLoopExecutor().run(
        task_id="LOOP-CLI",
        action_id="demo-action",
        tool_id="simulated-health-tool",
        approval_id=args.approval_id,
        environment="lab",
        verification_result=args.verification,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
