#!/usr/bin/env python3
"""Minimal provider adapter for the Anthropic Messages API.

Secrets are read from environment variables and are never persisted to the Vault.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

API_URL = os.getenv("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages")
API_VERSION = os.getenv("ANTHROPIC_API_VERSION", "2023-06-01")


class ClaudeClientError(RuntimeError):
    pass


def call_claude(*, system_prompt: str, user_prompt: str, max_tokens: int = 1800) -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL")
    if not api_key:
        raise ClaudeClientError("ANTHROPIC_API_KEY is not set")
    if not model:
        raise ClaudeClientError("ANTHROPIC_MODEL is not set")

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ClaudeClientError(f"Anthropic HTTP {exc.code}: {detail[:800]}") from exc
    except urllib.error.URLError as exc:
        raise ClaudeClientError(f"Anthropic connection error: {exc}") from exc

    return data


def extract_text(response: dict[str, Any]) -> str:
    parts = []
    for block in response.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(x for x in parts if x).strip()
