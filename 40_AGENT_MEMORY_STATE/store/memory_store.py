#!/usr/bin/env python3
"""Local-only SQLite memory store with tenant/environment isolation."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

MEMORY_CLASSES = {"working", "episodic", "semantic"}
STATUSES = {"active", "verified", "unverified", "superseded", "expired"}


def now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Memory:
    memory_id: str
    memory_class: str
    tenant_id: str
    environment: str
    content: str
    correlation_id: str
    incident_id: str
    status: str
    source_refs: tuple[str, ...]
    provenance: dict[str, Any]
    created_at: str
    expires_at: str | None
    reviewed_by: str | None = None
    reviewed_at: str | None = None
    supersedes: str | None = None


class MemoryStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                memory_class TEXT NOT NULL,
                tenant_id TEXT NOT NULL,
                environment TEXT NOT NULL,
                content TEXT NOT NULL,
                correlation_id TEXT NOT NULL,
                incident_id TEXT,
                status TEXT NOT NULL,
                source_refs TEXT NOT NULL,
                provenance TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT,
                reviewed_by TEXT,
                reviewed_at TEXT,
                supersedes TEXT
            )"""
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mem_tenant_env ON memories(tenant_id, environment)"
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mem_class_status ON memories(memory_class, status)"
        )
        self.conn.commit()

    def add(self, *, memory_class: str, tenant_id: str, environment: str, content: str,
            correlation_id: str, incident_id: str = "", source_refs: list[str] | None = None,
            provenance: dict[str, Any] | None = None, ttl_hours: int | None = None,
            status: str = "active", reviewed_by: str | None = None) -> Memory:
        if memory_class not in MEMORY_CLASSES:
            raise ValueError("invalid_memory_class")
        if status not in STATUSES:
            raise ValueError("invalid_status")
        created = now()
        expires = created + timedelta(hours=ttl_hours) if ttl_hours is not None else None
        memory = Memory(
            memory_id=f"mem-{uuid4().hex[:12]}",
            memory_class=memory_class,
            tenant_id=tenant_id,
            environment=environment,
            content=content,
            correlation_id=correlation_id,
            incident_id=incident_id,
            status=status,
            source_refs=tuple(source_refs or []),
            provenance=provenance or {},
            created_at=created.isoformat(),
            expires_at=expires.isoformat() if expires else None,
            reviewed_by=reviewed_by,
            reviewed_at=created.isoformat() if reviewed_by else None,
        )
        self.conn.execute(
            """INSERT INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                memory.memory_id, memory.memory_class, memory.tenant_id, memory.environment,
                memory.content, memory.correlation_id, memory.incident_id, memory.status,
                json.dumps(memory.source_refs), json.dumps(memory.provenance), memory.created_at,
                memory.expires_at, memory.reviewed_by, memory.reviewed_at, memory.supersedes,
            ),
        )
        self.conn.commit()
        return memory

    def get(self, memory_id: str, *, tenant_id: str, environment: str) -> Memory | None:
        row = self.conn.execute(
            "SELECT * FROM memories WHERE memory_id=? AND tenant_id=? AND environment=?",
            (memory_id, tenant_id, environment),
        ).fetchone()
        return self._row(row) if row else None

    def search(self, query: str, *, tenant_id: str, environment: str,
               memory_class: str | None = None, limit: int = 10) -> list[Memory]:
        """Bounded keyword retrieval; RAG can replace ranking later."""
        if memory_class and memory_class not in MEMORY_CLASSES:
            raise ValueError("invalid_memory_class")
        args: list[Any] = [tenant_id, environment]
        sql = "SELECT * FROM memories WHERE tenant_id=? AND environment=?"
        if memory_class:
            sql += " AND memory_class=?"
            args.append(memory_class)
        if query.strip():
            sql += " AND content LIKE ?"
            args.append(f"%{query.strip()}%")
        sql += " ORDER BY created_at DESC LIMIT ?"
        args.append(max(1, min(int(limit), 50)))
        rows = self.conn.execute(sql, args).fetchall()
        return [self._row(r) for r in rows if not self._expired(self._row(r))]

    def promote(self, memory_id: str, *, tenant_id: str, environment: str,
                reviewer: str) -> Memory:
        record = self.get(memory_id, tenant_id=tenant_id, environment=environment)
        if record is None:
            raise ValueError("memory_not_found")
        if record.memory_class != "episodic":
            raise ValueError("only_episodic_memory_can_be_promoted")
        now_iso = now().isoformat()
        self.conn.execute(
            "UPDATE memories SET status='verified', reviewed_by=?, reviewed_at=? WHERE memory_id=?",
            (reviewer, now_iso, memory_id),
        )
        self.conn.commit()
        return self.get(memory_id, tenant_id=tenant_id, environment=environment)  # type: ignore[return-value]

    def expire_working(self) -> int:
        current = now().isoformat()
        cur = self.conn.execute(
            "UPDATE memories SET status='expired' WHERE memory_class='working' AND expires_at IS NOT NULL AND expires_at < ? AND status='active'",
            (current,),
        )
        self.conn.commit()
        return cur.rowcount

    @staticmethod
    def _row(row: sqlite3.Row) -> Memory:
        return Memory(
            row["memory_id"], row["memory_class"], row["tenant_id"], row["environment"],
            row["content"], row["correlation_id"], row["incident_id"] or "", row["status"],
            tuple(json.loads(row["source_refs"])), json.loads(row["provenance"]), row["created_at"],
            row["expires_at"], row["reviewed_by"], row["reviewed_at"], row["supersedes"],
        )

    @staticmethod
    def _expired(memory: Memory) -> bool:
        return bool(memory.expires_at and datetime.fromisoformat(memory.expires_at) < now())
