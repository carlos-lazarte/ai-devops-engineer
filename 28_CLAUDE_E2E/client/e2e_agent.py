#!/usr/bin/env python3
"""End-to-end demo: MCP gateway -> context packet -> Claude -> validation.

Default mode is dry-run and performs no network calls.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
VAULT = HERE.parents[2]
GATEWAY = VAULT / "27_MCP_TOOL_GATEWAY" / "server" / "reference_gateway.py"
FIXTURE_ROOT = VAULT / "26_OPERATIONAL_AGENT_LAB" / "fixtures"

sys.path.insert(0, str(GATEWAY.parent))
from reference_gateway import dispatch  # type: ignore  # noqa: E402

SYSTEM_PROMPT = """You are a senior DevOps/SRE reasoning assistant.
Use only supplied context. Distinguish facts from observations and hypotheses.
Do not invent commands, logs, or infrastructure state.
Do not claim an action was executed.
Return JSON matching the supplied response contract.
"""


def read_fixture(scenario: str) -> list[dict[str, Any]]:
    root = FIXTURE_ROOT / scenario
    if not root.is_dir():
        raise FileNotFoundError(f"fixture scenario not found: {scenario}")
    out = []
    for p in sorted(root.iterdir()):
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        out.append({"path": p.relative_to(VAULT).as_posix(), "content": text})
    return out


def extract_links(text: str) -> list[str]:
    return sorted(set(re.findall(r"\[\[([^\]|#]+)", text)))


def build_context(scenario: str) -> dict[str, Any]:
    case = read_fixture(scenario)
    problem = "Kubernetes Node NotReady"
    search = dispatch(VAULT, "tools/call", {"name": "search_notes", "arguments": {"query": problem, "limit": 8}})
    runbooks = dispatch(VAULT, "tools/call", {"name": "retrieve_runbook", "arguments": {"problem": problem, "technology": "kubernetes", "limit": 5}})

    reads = []
    for item in search.get("results", [])[:4]:
        result = dispatch(VAULT, "tools/call", {"name": "read_note", "arguments": {"note_id": item["note_id"]}})
        if result.get("status") == "ok":
            reads.append(result)

    return {
        "task": "Analyze Kubernetes Node NotReady incident",
        "scenario": scenario,
        "evidence": case,
        "retrieved_notes": reads,
        "retrieved_runbooks": runbooks.get("results", []),
        "rules": [
            "Evidence is authoritative only to the extent it is directly present in the packet.",
            "Hypotheses require supporting evidence and a validation step.",
            "Proposed production actions require human approval.",
            "Never claim to have executed an action.",
        ],
    }


def build_user_prompt(packet: dict[str, Any]) -> str:
    return (
        "Analyze this DevOps incident using the supplied context.\n"
        "Return ONLY JSON matching this shape:\n"
        "{summary, confidence, facts[], observations[], hypotheses[{statement,supporting_evidence[],contradicting_evidence[],validation_needed[]}], "
        "recommended_diagnostics[{step,rationale,risk}], proposed_actions[{action,risk,requires_human_approval}], unknowns[], references[]}\n\n"
        + json.dumps(packet, ensure_ascii=False, indent=2)
    )


def validate_response(obj: dict[str, Any]) -> list[str]:
    errors = []
    required = ["summary", "confidence", "facts", "observations", "hypotheses", "recommended_diagnostics", "proposed_actions", "unknowns", "references"]
    for key in required:
        if key not in obj:
            errors.append(f"missing:{key}")
    if obj.get("confidence") not in {"low", "medium", "high"}:
        errors.append("invalid:confidence")
    for idx, action in enumerate(obj.get("proposed_actions", [])):
        if action.get("requires_human_approval") is not True:
            errors.append(f"action_{idx}:human_approval_must_be_true")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="K8S-NOTREADY-001")
    parser.add_argument("--mode", choices=["dry-run", "claude"], default="dry-run")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet = build_context(args.scenario)
    user_prompt = build_user_prompt(packet)
    result: dict[str, Any] = {
        "mode": args.mode,
        "scenario": args.scenario,
        "context_packet": packet,
        "user_prompt": user_prompt,
    }

    if args.mode == "claude":
        from claude_client import call_claude, extract_text, ClaudeClientError
        try:
            raw = call_claude(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
            text = extract_text(raw)
            try:
                parsed = json.loads(text)
                validation_errors = validate_response(parsed)
            except json.JSONDecodeError as exc:
                parsed = None
                validation_errors = [f"json_parse_error:{exc}"]
            result["claude_response"] = raw
            result["analysis_text"] = text
            result["structured_analysis"] = parsed
            result["validation_errors"] = validation_errors
        except ClaudeClientError as exc:
            result["client_error"] = str(exc)
            result["validation_errors"] = ["client_error"]
            if args.output:
                args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 2
    else:
        result["validation_errors"] = ["dry_run_no_model_call"]

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
