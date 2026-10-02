"""Validate release evidence and documentation without re-running an audit."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

from adaptive_response.resources import ASSET_DIR, verify_assets

ROOT = Path(__file__).resolve().parents[1]


def main():
    digests = verify_assets()
    directory = ROOT / "reports/sale_review/live_product"
    summary = json.loads((directory / "summary.json").read_text())
    with (directory / "cases.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    manifest = json.loads((ASSET_DIR / "ui_case_manifest_v1.json").read_text())
    assert [r["case_id"] for r in rows] == [r["case_id"] for r in manifest["cases"]]
    assert len(rows) == summary["case_count"] == 100
    assert summary["scope"] == "all_frozen_ui_cases"
    assert summary["asset_sha256"] == digests
    delta, adaptive, static, efforts = [], [], [], Counter()
    for row in rows:
        path = json.loads(row["effort_path"])
        sites = json.loads(row["site_path"])
        assert sum(path) == int(row["adaptive_effort"]) == int(row["static_effort"]) == 18
        assert set(path) <= {1, 3, 6}
        assert len(path) == len(sites) == int(row["missions"])
        assert len(set(sites)) == int(row["distinct_sites"])
        assert len(set(path)) == int(row["distinct_effort_levels"])
        total = int(row["occupied_total"])
        a, b = int(row["adaptive_detected"]) / total, int(row["static_detected"]) / total
        assert 0 <= a <= 1 and 0 <= b <= 1
        assert math.isclose(a, float(row["adaptive_detected_fraction"]), abs_tol=1e-12)
        assert math.isclose(b, float(row["static_detected_fraction"]), abs_tol=1e-12)
        assert math.isclose(100 * (a-b), float(row["delta_percentage_points"]), abs_tol=1e-12)
        adaptive.append(a)
        static.append(b)
        delta.append(100 * (a-b))
        efforts.update(path)
    delta = np.array(delta)
    for key, value in {
        "adaptive_mean_detected_fraction": np.mean(adaptive),
        "static_mean_detected_fraction": np.mean(static),
        "mean_delta_percentage_points": delta.mean(),
        "relative_difference_percent": 100 * (np.mean(adaptive)/np.mean(static)-1),
        "matched_or_exceeded_cases": np.sum(delta >= 0),
        "strictly_better_cases": np.sum(delta > 0),
        "tied_cases": np.sum(delta == 0), "worse_cases": np.sum(delta < 0),
        "missions": sum(efforts.values()),
        "cases_with_multiple_effort_levels": sum(int(r["distinct_effort_levels"]) > 1 for r in rows),
        "cases_with_revisits": sum(int(r["missions"]) > int(r["distinct_sites"]) for r in rows),
    }.items():
        assert math.isclose(summary[key], value, abs_tol=1e-12), key
    assert summary["effort_action_counts"] == {str(e): efforts[e] for e in (1, 3, 6)}
    assert summary["mission_count_range"] == [min(int(r["missions"]) for r in rows), max(int(r["missions"]) for r in rows)]
    bs = summary["paired_descriptive_bootstrap"]
    rng = np.random.default_rng(bs["seed"])
    means = delta[rng.integers(0, len(rows), size=(bs["replicates"],len(rows)))].mean(axis=1)
    assert np.allclose(np.quantile(means, [0.025,0.975]), bs["interval95_percentage_points"], atol=1e-12)
    assert (ROOT / "THIRD_PARTY_NOTICES.md").read_bytes() == (ASSET_DIR / "THIRD_PARTY_NOTICES.md").read_bytes()
    for document in [ROOT / "README.md", ROOT / "COMMERCIAL.md", ROOT / "THIRD_PARTY_NOTICES.md", *sorted((ROOT / "docs").glob("*.md"))]:
        for target in re.findall(r'\]\(([^\s)]+)\)', document.read_text()):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            local = (document.parent / target.split("#",1)[0]).resolve()
            assert local.is_file(), f"Broken documentation link: {document.name} -> {target}"
    print(json.dumps({"release_checks": "ok", "frozen_assets": len(digests), "audited_cases": len(rows),
                      "case_csv_sha256": hashlib.sha256((directory / "cases.csv").read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
