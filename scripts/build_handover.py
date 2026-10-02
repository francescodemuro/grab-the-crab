"""Build a revision-pinned technical handover from a clean tracked checkout."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("artifacts/handover"))
    args = parser.parse_args()
    if run("git", "status", "--porcelain"):
        parser.error("Commit/review the source first; the handover must identify one clean revision.")
    subprocess.run([sys.executable, "scripts/check_release.py"], cwd=ROOT, check=True)
    revision = run("git", "rev-parse", "HEAD")
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = output / f"grab-the-crab-source-{revision[:12]}.zip"
    subprocess.run(["git", "archive", "--format=zip", "--prefix=grab-the-crab/", f"--output={source}", "HEAD"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "build", "--outdir", str(output / "packages")], cwd=ROOT, check=True)
    files = [source, *sorted((output / "packages").glob("grab_the_crab-0.2.0*"))]
    manifest = {"project": "Grab the Crab", "source_commit": revision,
                "transaction_terms_included": False, "trained_checkpoints_included": False,
                "artifacts": [{"file": str(p.relative_to(output)), "bytes": p.stat().st_size,
                               "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    receipt = output / "manifest.json"
    receipt.write_text(json.dumps(manifest, indent=2) + "\n")
    bundle = output / f"grab-the-crab-handover-{revision[:12]}.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in [*files, receipt]:
            archive.write(file, str(file.relative_to(output)))
        archive.write(ROOT / "reports/sale_review/live_product/summary.json", "live-audit-summary.json")
    print(json.dumps({"bundle": str(bundle), "sha256": hashlib.sha256(bundle.read_bytes()).hexdigest(), "source_commit": revision}))
