from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import yaml

REQUIRED = {"skill_id","version","goal","domains","required_evidence","allowed_tools","forbidden_actions","risk","autonomy_level","output_schema","verification"}
ALLOWED_TOOLS = {"search_notes","read_note","retrieve_runbook"}

def evaluate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    missing = REQUIRED - data.keys()
    errors.extend(f"missing:{key}" for key in sorted(missing))
    errors.extend(f"undeclared-tool:{tool}" for tool in data.get("allowed_tools", []) if tool not in ALLOWED_TOOLS)
    if data.get("autonomy_level") == "L4":
        errors.append("L4-disabled-in-v2.3.0")
    if data.get("risk") in {"high", "critical"} and data.get("autonomy_level") not in {"L3"}:
        errors.append("high-risk-skill-must-use-L3-or-lower")
    return errors
