from __future__ import annotations

from typing import Any


def _families(events: list[dict[str, Any]]) -> set[str]:
    return {str(e.get("metric_family", "")).lower() for e in events}


def _conditions(events: list[dict[str, Any]]) -> set[str]:
    return {str(e.get("condition", "")).lower() for e in events}


def build_hypotheses(incident: dict[str, Any], events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    families = _families(events)
    conditions = _conditions(events)
    env = str(incident.get("environment", ""))
    text = " ".join([
        str(incident.get("candidate_reason", "")),
        " ".join(families),
        " ".join(conditions),
    ]).lower()

    hypotheses: list[dict[str, Any]] = []
    unknowns: list[str] = []

    resource_signals = any(x in text for x in ("cpu", "memory", "resource", "pressure", "saturation"))
    restart_signals = any(x in text for x in ("restart", "crashloop", "pod"))
    if resource_signals and restart_signals:
        hypotheses.append({
            "id": "H-RESOURCE-EXHAUSTION",
            "statement": "Resource pressure may be contributing to workload instability and repeated restarts.",
            "confidence": 0.68,
            "basis": ["CPU/memory/resource signals", "restart-related signal"],
            "status": "candidate",
        })
        unknowns.extend(["actual process/pod memory working set", "configured resource requests and limits"])

    if "notready" in text or "node" in text and "kubernetes" in text:
        hypotheses.append({
            "id": "H-K8S-NODE-HEALTH",
            "statement": "Node health or kubelet availability may be contributing to the incident.",
            "confidence": 0.62,
            "basis": ["Kubernetes node-related evidence"],
            "status": "candidate",
        })
        unknowns.extend(["kubelet health and recent kubelet errors", "node conditions and taints"])

    if any(x in text for x in ("latency", "iowait", "disk", "storage")):
        hypotheses.append({
            "id": "H-STORAGE-BOTTLENECK",
            "statement": "Storage or I/O contention may be contributing to observed latency.",
            "confidence": 0.56,
            "basis": ["latency/I/O-related signal"],
            "status": "candidate",
        })
        unknowns.extend(["I/O latency by device", "queue depth and saturation history"])

    if not hypotheses:
        hypotheses.append({
            "id": "H-CORRELATED-DEGRADATION",
            "statement": "The evidence supports correlated operational degradation, but the root cause is not yet established.",
            "confidence": min(0.60, float(incident.get("confidence", 0.0))),
            "basis": ["incident correlation evidence"],
            "status": "candidate",
        })
        unknowns.append("independent root-cause evidence")

    if env == "prod":
        unknowns.append("recent approved production change context")

    deduped: list[str] = []
    for item in unknowns:
        if item not in deduped:
            deduped.append(item)
    return hypotheses, deduped
