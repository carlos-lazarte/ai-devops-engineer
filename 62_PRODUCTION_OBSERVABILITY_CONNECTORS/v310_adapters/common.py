from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from threading import Lock
from typing import Callable, TypeVar
from urllib.parse import urlparse

T = TypeVar("T")


class ConnectorError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def validate_endpoint(url: str, allowed_schemes: tuple[str, ...] = ("http", "https")) -> str:
    value = str(url or "").strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in allowed_schemes or not parsed.netloc:
        raise ConnectorError("invalid_endpoint", "endpoint must be an absolute http(s) URL")
    if any(ch in value for ch in "\r\n"):
        raise ConnectorError("invalid_endpoint", "endpoint contains control characters")
    return value


@dataclass
class RetryPolicy:
    attempts: int = 3
    base_delay: float = 0.2
    max_delay: float = 2.0

    @classmethod
    def from_env(cls) -> "RetryPolicy":
        return cls(
            attempts=max(1, min(int(os.getenv("CONNECTOR_RETRY_ATTEMPTS", "3")), 6)),
            base_delay=max(0.0, min(float(os.getenv("CONNECTOR_RETRY_BASE_DELAY", "0.2")), 5.0)),
            max_delay=max(0.0, min(float(os.getenv("CONNECTOR_RETRY_MAX_DELAY", "2")), 15.0)),
        )


def retry_call(fn: Callable[[], T], policy: RetryPolicy | None = None,
               retry_on: tuple[type[BaseException], ...] = (Exception,)) -> T:
    p = policy or RetryPolicy.from_env()
    last: BaseException | None = None
    for attempt in range(p.attempts):
        try:
            return fn()
        except retry_on as exc:
            last = exc
            if attempt == p.attempts - 1:
                break
            delay = min(p.max_delay, p.base_delay * (2 ** attempt))
            if delay:
                time.sleep(delay + random.uniform(0, delay / 4))
    assert last is not None
    raise last


class RateLimiter:
    """Simple process-local token bucket suitable for protecting connector calls."""

    def __init__(self, rate_per_second: float = 2.0, burst: int = 4):
        self.rate = max(0.01, float(rate_per_second))
        self.capacity = max(1, int(burst))
        self.tokens = float(self.capacity)
        self.updated = time.monotonic()
        self.lock = Lock()

    def acquire(self) -> None:
        while True:
            with self.lock:
                now = time.monotonic()
                self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
                self.updated = now
                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return
                wait = (1.0 - self.tokens) / self.rate
            time.sleep(wait)
