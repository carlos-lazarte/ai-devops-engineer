from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_observability_files_exist():
    required = [
        ROOT / "prometheus" / "prometheus.yml",
        ROOT / "alerts" / "runtime-alerts.yml",
        ROOT / "grafana" / "dashboards" / "runtime-overview.json",
        ROOT / "docs" / "SLOs.md",
    ]
    assert all(p.is_file() for p in required)
