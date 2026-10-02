import json
import subprocess
import sys

from adaptive_response.resources import ASSET_DIR, verify_assets


def test_bundled_assets_match_the_original_frozen_receipts():
    assert len(verify_assets()) == 5
    assert len(json.loads((ASSET_DIR / "ui_case_manifest_v1.json").read_text())["cases"]) == 100


def test_data_and_frozen_case_helpers_import_without_torch():
    result = subprocess.run([sys.executable, "-c", "import sys; "
        "from adaptive_response.rl.real_graph_cases import build_real_incident_case; "
        "from adaptive_response.rl.r8_manifest_cases import load_frozen_manifest; "
        "assert 'torch' not in sys.modules; assert load_frozen_manifest()['cases']"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
