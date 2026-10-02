"""Snapshot installed version/license metadata for the pinned demo environment."""
from importlib.metadata import distribution
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    components = []
    for line in (ROOT / "requirements/demo-py312.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        name, pinned = line.split("==")
        dist = distribution(name)
        assert dist.version == pinned, f"{name}: installed version differs from the recorded lock"
        metadata = dist.metadata
        classifiers = [v for v in metadata.get_all("Classifier", []) if v.startswith("License ::")]
        license_name = metadata.get("License-Expression") or "; ".join(classifiers) or metadata.get("License") or "Not declared in metadata"
        if len(license_name) > 160:
            license_name = "See upstream License metadata/file"
        components.append({"name": name, "version": pinned, "license_metadata": license_name,
            "license_files": metadata.get_all("License-File", []),
            "project_urls": metadata.get_all("Project-URL", [])})
    output = ROOT / "reports/sale_review/dependencies.json"
    output.write_text(json.dumps({"scope": "pinned_python312_core_ui", "source": "installed_distribution_metadata",
        "rights_clearance": False, "components": components}, indent=2) + "\n")
    lines = ['# Dependency inventory', '',
        'Observed package metadata for the pinned Python 3.12 core/UI environment. This is not a complete license clearance or vulnerability audit. PyTorch/LLM extras are excluded from this snapshot and require their own delivery review.', '',
        '| Package | Version | Declared license metadata |', '| --- | --- | --- |']
    lines.extend(f'| {c["name"]} | {c["version"]} | {c["license_metadata"].replace("|", "/")} |' for c in components)
    lines.extend(['', 'Recreate with `python scripts/export_dependency_inventory.py` in the pinned environment. Exact license-file names and upstream URLs are in `reports/sale_review/dependencies.json`. Preserve required upstream notices in any distribution.'])
    (ROOT / "docs/DEPENDENCIES.md").write_text('\n'.join(lines) + '\n')
    print(f"Recorded metadata for {len(components)} demo dependencies.")
