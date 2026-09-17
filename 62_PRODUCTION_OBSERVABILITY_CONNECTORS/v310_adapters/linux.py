from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .common import ConnectorError


class LinuxConnector:
    """Local read-only Linux observability connector using procfs/sysfs."""

    def __init__(self, proc_root: str | Path = "/proc", sys_root: str | Path = "/sys"):
        self.proc = Path(proc_root)
        self.sys = Path(sys_root)

    def _read(self, path: Path, limit: int = 200_000) -> str:
        if not path.is_file():
            raise ConnectorError("source_not_available", str(path))
        if path.stat().st_size > limit:
            raise ConnectorError("source_too_large", str(path))
        return path.read_text(errors="replace")

    def health(self) -> dict[str, Any]:
        return {
            "name": "linux",
            "status": "healthy" if self.proc.is_dir() else "unhealthy",
            "hostname": os.uname().nodename,
            "proc_root": str(self.proc),
        }

    def cpu_snapshot(self) -> dict[str, Any]:
        text = self._read(self.proc / "stat")
        line = next((x for x in text.splitlines() if x.startswith("cpu ")), "")
        fields = line.split()
        if len(fields) < 5:
            raise ConnectorError("invalid_proc_stat", "cpu line unavailable")
        values = list(map(int, fields[1:]))
        return {"name": "linux.cpu", "user": values[0], "system": values[2], "idle": values[3], "iowait": values[4] if len(values) > 4 else 0}

    def memory(self) -> dict[str, Any]:
        text = self._read(self.proc / "meminfo")
        out: dict[str, int] = {}
        for line in text.splitlines():
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            parts = val.strip().split()
            try:
                out[key] = int(parts[0]) * (1024 if len(parts) > 1 and parts[1].lower() == "kb" else 1)
            except (ValueError, IndexError):
                continue
        return {"name": "linux.memory", "mem_total_bytes": out.get("MemTotal"), "mem_available_bytes": out.get("MemAvailable"),
                "swap_total_bytes": out.get("SwapTotal"), "swap_free_bytes": out.get("SwapFree")}
