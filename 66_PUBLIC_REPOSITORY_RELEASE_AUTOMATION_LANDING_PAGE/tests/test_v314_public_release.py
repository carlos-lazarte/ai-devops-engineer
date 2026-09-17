from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]

def test_release_structure():
    version = (ROOT / "VERSION").read_text().strip()
    assert version, "VERSION must not be empty"
    assert version.count(".") == 2, f"Invalid semantic version: {version}"
    major, minor, patch = version.split(".")
    assert all(part.isdigit() for part in (major, minor, patch)), f"Invalid semantic version: {version}"
    for rel in [
        ".github/workflows/release.yml",
        ".github/workflows/pages.yml",
        ".github/workflows/publish-container.yml",
        "66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/site/index.html",
    ]:
        assert (ROOT / rel).exists(), rel

def test_site_check():
    p = subprocess.run(
        [sys.executable, str(ROOT/"66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/scripts/site_check.py")],
        cwd=ROOT, capture_output=True, text=True
    )
    assert p.returncode == 0, p.stdout + p.stderr
