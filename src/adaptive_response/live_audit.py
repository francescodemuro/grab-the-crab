"""Reproducible product-behavior audit of the live policy on frozen demo cases.

This audit is descriptive simulation evidence, not a field-effectiveness study
or a substitute for the frozen R8/R11 learned-policy protocols.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from importlib.metadata import version
from pathlib import Path

import numpy as np

from .mission_control import MissionControlSession
from .resources import verify_assets


def run_live_audit(case_ids: list[str] | None = None):
    digests = verify_assets()
    session = MissionControlSession()
    available = [row["case_id"] for row in session.case_library()["cases"]]
    selected = available if case_ids is None else case_ids
    if not selected or len(selected) != len(set(selected)) or not set(selected) <= set(available):
        raise ValueError("Select one or more unique case ids from the frozen UI library.")
    rows = []
    efforts: Counter = Counter()
    for case_id in selected:
        snapshot = session.reset(case_id=case_id)
        sites, path = [], []
        while not snapshot["can_reveal"]:
            recommendation = snapshot["global_recommendations"][0]
            site, effort = recommendation["site_id"], int(recommendation["recommended_effort"])
            sites.append(site)
            path.append(effort)
            snapshot = session.deploy(site_id=site, effort=effort)
        revealed = session.reveal()
        adaptive = revealed["performance"]["marine"]
        static = revealed["performance"]["static"]
        followed = revealed["performance"]["you"]
        if adaptive["detected_occupied"] != followed["detected_occupied"] or adaptive["mission_efforts"] != path:
            raise RuntimeError("Following the recommendation diverged from the adaptive comparator.")
        if sum(path) != 18 or static["effort_spent"] != 18:
            raise RuntimeError("Paired audit did not spend the same 18-unit budget.")
        efforts.update(path)
        total = int(adaptive["occupied_total"])
        adaptive_fraction = adaptive["detected_occupied"] / total
        static_fraction = static["detected_occupied"] / total
        rows.append({
            "case_id": case_id, "occupied_total": total,
            "adaptive_detected": adaptive["detected_occupied"],
            "static_detected": static["detected_occupied"],
            "adaptive_detected_fraction": adaptive_fraction,
            "static_detected_fraction": static_fraction,
            "delta_percentage_points": 100 * (adaptive_fraction - static_fraction),
            "adaptive_effort": sum(path), "static_effort": static["effort_spent"],
            "missions": len(path), "distinct_sites": len(set(sites)),
            "distinct_effort_levels": len(set(path)),
            "effort_path": json.dumps(path), "site_path": json.dumps(sites),
        })
    adaptive_mean = float(np.mean([r["adaptive_detected_fraction"] for r in rows]))
    static_mean = float(np.mean([r["static_detected_fraction"] for r in rows]))
    delta = np.array([r["delta_percentage_points"] for r in rows])
    rng = np.random.default_rng(20261002)
    bootstrap = delta[rng.integers(0, len(rows), size=(10_000, len(rows)))].mean(axis=1)
    summary = {
        "schema_version": 1, "software_version": version("grab-the-crab"),
        "audit_type": "descriptive_simulation_product_audit",
        "scope": "all_frozen_ui_cases" if selected == available else "selected_frozen_ui_cases",
        "case_count": len(rows), "available_case_count": len(available),
        "asset_sha256": digests,
        "budget_per_policy": 18,
        "detected_fraction_includes_confirmed_initial_site": True,
        "adaptive_mean_detected_fraction": adaptive_mean,
        "static_mean_detected_fraction": static_mean,
        "mean_delta_percentage_points": float(delta.mean()),
        "relative_difference_percent": 100 * (adaptive_mean / static_mean - 1),
        "matched_or_exceeded_cases": int(np.sum(delta >= 0)),
        "strictly_better_cases": int(np.sum(delta > 0)),
        "tied_cases": int(np.sum(delta == 0)),
        "worse_cases": int(np.sum(delta < 0)),
        "missions": sum(efforts.values()),
        "effort_action_counts": {str(e): efforts[e] for e in (1, 3, 6)},
        "cases_with_multiple_effort_levels": sum(r["distinct_effort_levels"] > 1 for r in rows),
        "cases_with_revisits": sum(r["missions"] > r["distinct_sites"] for r in rows),
        "mission_count_range": [min(r["missions"] for r in rows), max(r["missions"] for r in rows)],
        "paired_descriptive_bootstrap": {
            "replicates": 10_000, "seed": 20261002,
            "interval95_percentage_points": [float(x) for x in np.quantile(bootstrap, [0.025, 0.975])],
            "interpretation": "Resampling sensitivity within this frozen demo library; not field effectiveness or a formal held-out benchmark.",
        },
        "field_effectiveness_validated": False,
        "measured_monetary_savings": None,
    }
    return rows, summary


def write_audit(output: Path, rows: list[dict], summary: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    with (output / "cases.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
