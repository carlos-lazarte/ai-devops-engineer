from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "43_ENTERPRISE_DEPLOYMENT" / "kubernetes" / "base"
HELM = ROOT / "43_ENTERPRISE_DEPLOYMENT" / "helm" / "ai-devops-platform"


def test_kubernetes_baseline_files_exist():
    expected = {
        "namespace.yaml",
        "serviceaccount.yaml",
        "configmap.yaml",
        "deployment.yaml",
        "service.yaml",
        "pdb.yaml",
        "networkpolicy.yaml",
        "kustomization.yaml",
    }
    assert expected.issubset({p.name for p in BASE.iterdir()})


def test_runtime_security_invariants_present():
    text = (BASE / "deployment.yaml").read_text()
    assert "runAsNonRoot: true" in text
    assert "allowPrivilegeEscalation: false" in text
    assert "readOnlyRootFilesystem: true" in text
    assert 'drop: ["ALL"]' in text
    assert "RuntimeDefault" in text


def test_execution_disabled_by_default():
    text = (BASE / "configmap.yaml").read_text()
    assert 'PRODUCTION_EXECUTION_ENABLED: "false"' in text


def test_helm_chart_exists():
    assert (HELM / "Chart.yaml").is_file()
    assert (HELM / "values.yaml").is_file()
    assert (HELM / "templates" / "deployment.yaml").is_file()
