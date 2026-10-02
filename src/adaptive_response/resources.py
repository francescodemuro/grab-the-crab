"""Frozen evaluation assets, available in both a checkout and an installed wheel."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ASSET_DIR = Path(__file__).with_name("assets")
REPO_ROOT = Path(__file__).resolve().parents[2]
ASSET_SOURCES = {
    "ui_case_manifest_v1.json": "configs/ui_case_manifest_v1.json",
    "real_site_context_r8.json": "configs/real_site_context_r8.json",
    "real_sites_v0.csv": "reports/milestones/r2_real_graph_v0/real_sites_v0.csv",
    "real_graph_v0_edges.csv": "reports/milestones/r2_real_graph_v0/real_graph_v0_edges.csv",
    "benchmark_cases.json": "reports/milestones/r8_benchmark_case_manifest/benchmark_cases.json",
}


def asset_path(name: str) -> Path:
    """Prefer canonical checkout files; use the identical frozen copy in wheels."""
    source = REPO_ROOT / ASSET_SOURCES[name]
    return source if source.is_file() else ASSET_DIR / name


def verify_assets() -> dict[str, str]:
    """Fail on missing files or drift between checkout, package and manifest."""
    manifest = json.loads((ASSET_DIR / "manifest.json").read_text(encoding="utf-8"))
    digests = {}
    for name, source in ASSET_SOURCES.items():
        expected = manifest["sha256"][name]
        for path in {ASSET_DIR / name, asset_path(name)}:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"Frozen asset differs from its receipt: {source}")
        digests[name] = expected
    return digests
