from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from .core import utc_now


def audit(event: dict[str, Any]) -> None:
    path = Path(os.getenv("AUDIT_LOG", "runtime-data/audit.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema_version": "1.0",
        "timestamp": utc_now(),
        **event,
    }
    # Never write API keys or auth headers. Callers are expected to pass bounded fields only.
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
