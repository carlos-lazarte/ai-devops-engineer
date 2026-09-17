from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class IncidentStore:
    """Small persistence adapter: PostgreSQL in Docker, SQLite for zero-dependency local demos/tests."""

    def __init__(self, database_url: str | None = None, sqlite_path: str | Path = "runtime-data/local.db"):
        self.url = database_url or os.getenv("DATABASE_URL", "")
        self.sqlite_path = Path(sqlite_path)
        self._postgres = self.url.startswith("postgresql://") or self.url.startswith("postgres://")
        if not self._postgres:
            self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    @contextmanager
    def _conn(self) -> Iterator[Any]:
        if self._postgres:
            try:
                import psycopg
            except ImportError as exc:
                raise RuntimeError("psycopg_package_missing") from exc
            conn = psycopg.connect(self.url)
            try:
                yield conn
                conn.commit()
            finally:
                conn.close()
        else:
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            finally:
                conn.close()

    def init_schema(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            environment TEXT NOT NULL,
            state TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence DOUBLE PRECISION NOT NULL,
            candidate_reason TEXT NOT NULL,
            signals_json TEXT NOT NULL,
            provenance_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            telemetry_sql = """
            CREATE TABLE IF NOT EXISTS telemetry_events (
                event_id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                environment TEXT NOT NULL,
                timestamp DOUBLE PRECISION NOT NULL,
                component TEXT NOT NULL,
                metric_family TEXT NOT NULL,
                condition TEXT NOT NULL,
                severity_hint TEXT NOT NULL,
                value_json TEXT,
                source TEXT NOT NULL,
                labels_json TEXT NOT NULL,
                topology_neighbors_json TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                ingested_at TEXT NOT NULL
            )
            """
            cur.execute(telemetry_sql)
            investigation_sql = """
            CREATE TABLE IF NOT EXISTS investigations (
                investigation_id TEXT PRIMARY KEY,
                incident_id TEXT NOT NULL,
                tenant_id TEXT NOT NULL,
                environment TEXT NOT NULL,
                status TEXT NOT NULL,
                mode TEXT NOT NULL,
                trigger_json TEXT NOT NULL,
                telemetry_json TEXT NOT NULL,
                evidence_json TEXT NOT NULL,
                hypotheses_json TEXT NOT NULL,
                unknowns_json TEXT NOT NULL,
                requested_diagnostics_json TEXT NOT NULL,
                proposed_actions_json TEXT NOT NULL,
                knowledge_json TEXT NOT NULL,
                plan_json TEXT NOT NULL,
                agent_json TEXT,
                safety_json TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
            cur.execute(investigation_sql)

    def upsert_incident(self, incident: dict[str, Any]) -> None:
        values = (
            incident["incident_id"], incident["tenant_id"], incident["environment"],
            incident["state"], incident["severity"], float(incident["confidence"]),
            incident.get("candidate_reason", ""), json.dumps(incident.get("signals", [])),
            json.dumps(incident.get("provenance", [])), incident["created_at"], incident["updated_at"],
        )
        if self._postgres:
            sql = """
            INSERT INTO incidents (incident_id,tenant_id,environment,state,severity,confidence,candidate_reason,
              signals_json,provenance_json,created_at,updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (incident_id) DO UPDATE SET
              tenant_id=EXCLUDED.tenant_id, environment=EXCLUDED.environment, state=EXCLUDED.state,
              severity=EXCLUDED.severity, confidence=EXCLUDED.confidence, candidate_reason=EXCLUDED.candidate_reason,
              signals_json=EXCLUDED.signals_json, provenance_json=EXCLUDED.provenance_json, updated_at=EXCLUDED.updated_at
            """
        else:
            sql = """
            INSERT INTO incidents VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(incident_id) DO UPDATE SET
              tenant_id=excluded.tenant_id, environment=excluded.environment, state=excluded.state,
              severity=excluded.severity, confidence=excluded.confidence, candidate_reason=excluded.candidate_reason,
              signals_json=excluded.signals_json, provenance_json=excluded.provenance_json, updated_at=excluded.updated_at
            """
        with self._conn() as conn:
            conn.cursor().execute(sql, values)

    def save_telemetry_events(self, events: list[dict[str, Any]]) -> None:
        from datetime import datetime, timezone
        ingested_at = datetime.now(timezone.utc).isoformat()
        values = []
        for event in events:
            values.append((
                event["event_id"], event["tenant_id"], event["environment"], float(event["timestamp"]),
                event["component"], event["metric_family"], event["condition"], event.get("severity_hint", "info"),
                json.dumps(event.get("value")), event.get("source", "unknown"), json.dumps(event.get("labels", {})),
                json.dumps(event.get("topology_neighbors", [])), json.dumps(event.get("provenance", {})), ingested_at,
            ))
        if not values:
            return
        if self._postgres:
            sql = """
            INSERT INTO telemetry_events
              (event_id,tenant_id,environment,timestamp,component,metric_family,condition,severity_hint,value_json,source,labels_json,topology_neighbors_json,provenance_json,ingested_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (event_id) DO NOTHING
            """
        else:
            sql = """
            INSERT OR IGNORE INTO telemetry_events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """
        with self._conn() as conn:
            conn.cursor().executemany(sql, values)

    def list_telemetry_events(self, tenant_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 1000))
        with self._conn() as conn:
            cur = conn.cursor()
            if self._postgres:
                if tenant_id:
                    cur.execute("SELECT * FROM telemetry_events WHERE tenant_id=%s ORDER BY timestamp DESC LIMIT %s", (tenant_id, limit))
                else:
                    cur.execute("SELECT * FROM telemetry_events ORDER BY timestamp DESC LIMIT %s", (limit,))
                names = [d.name for d in cur.description]
                rows = [dict(zip(names, row)) for row in cur.fetchall()]
            else:
                if tenant_id:
                    cur.execute("SELECT * FROM telemetry_events WHERE tenant_id=? ORDER BY timestamp DESC LIMIT ?", (tenant_id, limit))
                else:
                    cur.execute("SELECT * FROM telemetry_events ORDER BY timestamp DESC LIMIT ?", (limit,))
                rows = [dict(row) for row in cur.fetchall()]
        for row in rows:
            row["value"] = json.loads(row.pop("value_json")) if row.get("value_json") is not None else None
            row["labels"] = json.loads(row.pop("labels_json"))
            row["topology_neighbors"] = json.loads(row.pop("topology_neighbors_json"))
            row["provenance"] = json.loads(row.pop("provenance_json"))
        return rows

    def list_incidents(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        with self._conn() as conn:
            cur = conn.cursor()
            if self._postgres:
                sql = "SELECT * FROM incidents WHERE (%s IS NULL OR tenant_id=%s) ORDER BY updated_at DESC"
                cur.execute(sql, (tenant_id, tenant_id))
                rows = cur.fetchall()
                names = [d.name for d in cur.description]
                rows = [dict(zip(names, row)) for row in rows]
            else:
                cur.execute("SELECT * FROM incidents WHERE (? IS NULL OR tenant_id=?) ORDER BY updated_at DESC", (tenant_id, tenant_id))
                rows = [dict(row) for row in cur.fetchall()]
        for row in rows:
            row["signals"] = json.loads(row.pop("signals_json"))
            row["provenance"] = json.loads(row.pop("provenance_json"))
        return rows

    def get_incident(self, incident_id: str) -> dict[str, Any] | None:
        rows = self.list_incidents()
        for row in rows:
            if row["incident_id"] == incident_id:
                return row
        return None

    def save_investigation(self, investigation: dict[str, Any]) -> None:
        values = (
            investigation["investigation_id"], investigation["incident_id"], investigation["tenant_id"],
            investigation["environment"], investigation["status"], investigation["mode"],
            json.dumps(investigation.get("trigger", {}), ensure_ascii=False),
            json.dumps(investigation.get("telemetry", {}), ensure_ascii=False),
            json.dumps(investigation.get("evidence", []), ensure_ascii=False),
            json.dumps(investigation.get("hypotheses", []), ensure_ascii=False),
            json.dumps(investigation.get("unknowns", []), ensure_ascii=False),
            json.dumps(investigation.get("requested_diagnostics", []), ensure_ascii=False),
            json.dumps(investigation.get("proposed_actions", []), ensure_ascii=False),
            json.dumps(investigation.get("knowledge", {}), ensure_ascii=False),
            json.dumps(investigation.get("plan", {}), ensure_ascii=False),
            json.dumps(investigation.get("agent"), ensure_ascii=False) if investigation.get("agent") is not None else None,
            json.dumps(investigation.get("safety", {}), ensure_ascii=False),
            json.dumps(investigation.get("provenance", {}), ensure_ascii=False),
            investigation["created_at"], investigation["updated_at"],
        )
        if self._postgres:
            sql = """
            INSERT INTO investigations (
              investigation_id,incident_id,tenant_id,environment,status,mode,trigger_json,telemetry_json,
              evidence_json,hypotheses_json,unknowns_json,requested_diagnostics_json,proposed_actions_json,
              knowledge_json,plan_json,agent_json,safety_json,provenance_json,created_at,updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (investigation_id) DO UPDATE SET
              status=EXCLUDED.status, mode=EXCLUDED.mode, trigger_json=EXCLUDED.trigger_json,
              telemetry_json=EXCLUDED.telemetry_json, evidence_json=EXCLUDED.evidence_json,
              hypotheses_json=EXCLUDED.hypotheses_json, unknowns_json=EXCLUDED.unknowns_json,
              requested_diagnostics_json=EXCLUDED.requested_diagnostics_json,
              proposed_actions_json=EXCLUDED.proposed_actions_json, knowledge_json=EXCLUDED.knowledge_json,
              plan_json=EXCLUDED.plan_json, agent_json=EXCLUDED.agent_json, safety_json=EXCLUDED.safety_json,
              provenance_json=EXCLUDED.provenance_json, updated_at=EXCLUDED.updated_at
            """
        else:
            sql = """
            INSERT INTO investigations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(investigation_id) DO UPDATE SET
              status=excluded.status, mode=excluded.mode, trigger_json=excluded.trigger_json,
              telemetry_json=excluded.telemetry_json, evidence_json=excluded.evidence_json,
              hypotheses_json=excluded.hypotheses_json, unknowns_json=excluded.unknowns_json,
              requested_diagnostics_json=excluded.requested_diagnostics_json,
              proposed_actions_json=excluded.proposed_actions_json, knowledge_json=excluded.knowledge_json,
              plan_json=excluded.plan_json, agent_json=excluded.agent_json, safety_json=excluded.safety_json,
              provenance_json=excluded.provenance_json, updated_at=excluded.updated_at
            """
        with self._conn() as conn:
            conn.cursor().execute(sql, values)

    @staticmethod
    def _decode_investigation(row: dict[str, Any]) -> dict[str, Any]:
        mapping = {
            "trigger_json": "trigger", "telemetry_json": "telemetry", "evidence_json": "evidence",
            "hypotheses_json": "hypotheses", "unknowns_json": "unknowns",
            "requested_diagnostics_json": "requested_diagnostics", "proposed_actions_json": "proposed_actions",
            "knowledge_json": "knowledge", "plan_json": "plan", "agent_json": "agent",
            "safety_json": "safety", "provenance_json": "provenance",
        }
        for raw, key in mapping.items():
            value = row.pop(raw, None)
            row[key] = json.loads(value) if value is not None else None
        return row

    def list_investigations(self, tenant_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 500))
        with self._conn() as conn:
            cur = conn.cursor()
            if self._postgres:
                if tenant_id:
                    cur.execute("SELECT * FROM investigations WHERE tenant_id=%s ORDER BY updated_at DESC LIMIT %s", (tenant_id, limit))
                else:
                    cur.execute("SELECT * FROM investigations ORDER BY updated_at DESC LIMIT %s", (limit,))
                names = [d.name for d in cur.description]
                rows = [dict(zip(names, row)) for row in cur.fetchall()]
            else:
                if tenant_id:
                    cur.execute("SELECT * FROM investigations WHERE tenant_id=? ORDER BY updated_at DESC LIMIT ?", (tenant_id, limit))
                else:
                    cur.execute("SELECT * FROM investigations ORDER BY updated_at DESC LIMIT ?", (limit,))
                rows = [dict(row) for row in cur.fetchall()]
        return [self._decode_investigation(row) for row in rows]

    def get_investigation(self, investigation_id: str) -> dict[str, Any] | None:
        with self._conn() as conn:
            cur = conn.cursor()
            if self._postgres:
                cur.execute("SELECT * FROM investigations WHERE investigation_id=%s", (investigation_id,))
                row = cur.fetchone()
                if row is None:
                    return None
                names = [d.name for d in cur.description]
                data = dict(zip(names, row))
            else:
                cur.execute("SELECT * FROM investigations WHERE investigation_id=?", (investigation_id,))
                row = cur.fetchone()
                if row is None:
                    return None
                data = dict(row)
        return self._decode_investigation(data)
