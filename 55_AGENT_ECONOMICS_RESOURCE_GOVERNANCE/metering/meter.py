from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    context_tokens: int = 0
    tool_calls: int = 0
    latency_ms: float = 0.0
    estimated_cost: float = 0.0


class UsageMeter:
    def __init__(self) -> None:
        self.usage = Usage()

    def record(self, usage: Usage) -> Usage:
        self.usage = Usage(
            input_tokens=self.usage.input_tokens + usage.input_tokens,
            output_tokens=self.usage.output_tokens + usage.output_tokens,
            context_tokens=self.usage.context_tokens + usage.context_tokens,
            tool_calls=self.usage.tool_calls + usage.tool_calls,
            latency_ms=self.usage.latency_ms + usage.latency_ms,
            estimated_cost=self.usage.estimated_cost + usage.estimated_cost,
        )
        return self.usage
