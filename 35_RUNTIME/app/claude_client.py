from __future__ import annotations

import json
import os
from typing import Any


def analyze_with_claude(prompt: str) -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("anthropic_api_key_missing")
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic_package_missing") from exc

    client = Anthropic(api_key=api_key, base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com"))
    model = os.getenv("ANTHROPIC_MODEL", "").strip()
    if not model:
        raise RuntimeError("anthropic_model_missing")
    max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "1200"))
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text_parts = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)
    text = "\n".join(text_parts).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"raw_text": text}
    return {
        "model": model,
        "response": data,
    }
