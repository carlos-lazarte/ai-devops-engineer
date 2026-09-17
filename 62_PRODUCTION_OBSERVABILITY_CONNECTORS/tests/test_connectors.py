import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from v310_adapters.common import RateLimiter, validate_endpoint
from v310_adapters.linux import LinuxConnector
from v310_adapters.kubernetes import KubernetesConnector
from v310_adapters.prometheus import PrometheusConnector
from v310_service.registry import ConnectorRegistry


def test_endpoint_validation():
    assert validate_endpoint("https://prom.example:9090") == "https://prom.example:9090"
    try:
        validate_endpoint("file:///etc/passwd")
        assert False
    except Exception as exc:
        assert getattr(exc, "code", "") == "invalid_endpoint"


def test_linux_read_only_snapshot(tmp_path):
    proc = tmp_path / "proc"
    proc.mkdir()
    (proc / "stat").write_text("cpu 10 1 20 100 2 0 0 0 0 0\n")
    (proc / "meminfo").write_text("MemTotal:       1024 kB\nMemAvailable:    512 kB\nSwapTotal: 0 kB\nSwapFree: 0 kB\n")
    c = LinuxConnector(proc, tmp_path / "sys")
    assert c.health()["status"] == "healthy"
    snap = c.cpu_snapshot()
    assert snap["idle"] == 100
    assert c.memory()["mem_available_bytes"] == 512 * 1024


def test_k8s_rejects_write_like_path():
    c = KubernetesConnector(api_server="https://kube.example", token="x")
    try:
        c._get("/api/v1/nodes/n/exec")
        assert False
    except Exception as exc:
        assert getattr(exc, "code", "") == "invalid_k8s_path"


def test_prometheus_query_is_bounded(monkeypatch):
    c = PrometheusConnector("http://prom.example")
    try:
        c.query("x" * 4097)
        assert False
    except Exception as exc:
        assert getattr(exc, "code", "") == "invalid_promql"


def test_registry_exposes_required_connectors(monkeypatch):
    reg = ConnectorRegistry()
    names = {x["name"] for x in reg.metadata()}
    assert {"prometheus", "opentelemetry", "kubernetes", "linux"} <= names


def test_rate_limiter_does_not_overflow():
    rl = RateLimiter(rate_per_second=1000, burst=2)
    rl.acquire(); rl.acquire(); rl.acquire()
    assert rl.tokens >= 0
