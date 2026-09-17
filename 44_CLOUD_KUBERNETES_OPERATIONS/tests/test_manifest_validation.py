from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_manifests

def test_reference_manifests_pass():
    assert validate_manifests.main() == 0
