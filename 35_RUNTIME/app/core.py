from __future__ import annotations

import json
import os
import re
import uuid
from time import perf_counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .metrics import VAULT_SEARCH_DURATION

MAX_QUERY_CHARS = int(os.getenv("MAX_QUERY_CHARS", "500"))
MAX_NOTE_BYTES = int(os.getenv("MAX_NOTE_BYTES", "100000"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def request_id(prefix: str = "req") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class SearchHit:
    note_id: str
    title: str
    snippet: str
    score: float
    provenance: str


class VaultReader:
    """Bounded, read-only access to a configured Markdown Vault."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        if not self.root.is_dir():
            raise ValueError(f"vault_not_found: {self.root}")

    def _safe(self, note_id: str) -> Path:
        if not note_id or "\x00" in note_id:
            raise ValueError("invalid_note_id")
        candidate = (self.root / note_id).resolve()
        if candidate == self.root or self.root not in candidate.parents:
            raise ValueError("path_escape")
        if candidate.suffix != ".md":
            raise ValueError("not_markdown")
        if not candidate.is_file():
            raise FileNotFoundError("note_not_found")
        if candidate.stat().st_size > MAX_NOTE_BYTES:
            raise ValueError("note_too_large")
        return candidate

    def notes(self):
        for p in self.root.rglob("*.md"):
            if any(x in {".git", ".obsidian", ".venv"} for x in p.parts):
                continue
            yield p

    @staticmethod
    def title(text: str, fallback: str) -> str:
        m = re.search(r"^#\s+(.+)$", text, re.M)
        return m.group(1).strip() if m else fallback

    def read(self, note_id: str) -> dict[str, Any]:
        p = self._safe(note_id)
        text = p.read_text(encoding="utf-8", errors="replace")
        return {
            "note_id": p.relative_to(self.root).as_posix(),
            "title": self.title(text, p.stem),
            "content": text,
            "provenance": [p.relative_to(self.root).as_posix()],
        }

    def search(self, query: str, limit: int = RAG_TOP_K) -> list[SearchHit]:
        query = str(query).strip()
        if not query:
            return []
        if len(query) > MAX_QUERY_CHARS:
            raise ValueError("query_too_long")
        terms = [t for t in re.findall(r"[a-zA-Z0-9_-]+", query.lower()) if t]
        hits: list[SearchHit] = []
        started = perf_counter()
        try:
            for p in self.notes():
                text = p.read_text(encoding="utf-8", errors="replace")
                low = text.lower()
                title = self.title(text, p.stem)
                path = p.relative_to(self.root).as_posix()
                path_low = path.lower()
                score = 0.0
                for term in terms:
                    score += low.count(term)
                    score += 5.0 * title.lower().count(term)
                    score += 2.0 * path_low.count(term)
                if score <= 0:
                    continue
                snippet = " ".join(text.strip().split())[:320]
                hits.append(SearchHit(path, title, snippet, score, path))
            hits.sort(key=lambda h: (-h.score, h.note_id))
            return hits[: max(1, min(int(limit), 20))]
        finally:
            VAULT_SEARCH_DURATION.observe(perf_counter() - started)


def assemble_context(vault: VaultReader, incident_id: str, top_k: int) -> dict[str, Any]:
    scenario_dir = vault.root / "26_OPERATIONAL_AGENT_LAB" / "fixtures" / incident_id
    if not scenario_dir.is_dir():
        raise FileNotFoundError("incident_not_found")
    evidence = []
    for p in sorted(scenario_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8", errors="replace")
        evidence.append({"name": p.name, "content": text[:8000]})
    search_text = " ".join([incident_id, "Kubernetes NodeNotReady", "troubleshooting", "runbook"])
    hits = [h.__dict__ for h in vault.search(search_text, top_k)]
    return {
        "context_id": request_id("ctx"),
        "incident_id": incident_id,
        "generated_at": utc_now(),
        "evidence": evidence,
        "retrieved_notes": hits,
        "policy": {
            "read_only": True,
            "human_approval_required": True,
            "allowed_action_tier": "draft",
        },
    }


def build_prompt(context: dict[str, Any]) -> str:
    return f"""You are an AI DevOps incident-analysis assistant.\n\nRules:\n- Treat evidence as authoritative only when explicitly present.\n- Separate facts, observations, hypotheses, missing evidence, and proposed actions.\n- Do not claim a command was executed.\n- Do not invent telemetry.\n- Every operational action must require human approval.\n- Return JSON matching the requested structure.\n\nContext:\n{json.dumps(context, indent=2)}\n\nReturn JSON with keys: summary, confidence, facts, observations, hypotheses, recommended_diagnostics, proposed_actions, unknowns, references.\n"""
