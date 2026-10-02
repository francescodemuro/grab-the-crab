# Evidence register

## Current live UI policy

`grab-the-crab audit --out artifacts/live-audit` runs the actual product adapter on every frozen UI case. It follows each top site/effort recommendation until the 18-unit budget is spent and compares its post-reveal result with the static response on the same incident. It writes `cases.csv` and `summary.json`.

The committed result is `reports/sale_review/live_product/`. It records software version 0.2.0, fixture hashes, per-case resource use, action paths, outcomes, strict wins/ties/losses and a reproducible descriptive bootstrap. `scripts/check_release.py` independently validates the committed case rows against their summary and frozen case identity.

| Measure | Recorded result |
| --- | ---: |
| Cases | 100 of 100 frozen UI incidents |
| Budget per policy per case | 18 effort units |
| Adaptive mean detected fraction | 0.4046496363 |
| Static mean detected fraction | 0.4016546868 |
| Mean adaptive-minus-static difference | +0.2994949495 percentage points |
| Relative difference in means | +0.7456528190% |
| Strict adaptive wins / ties / losses | 13 / 77 / 10 |
| Matched or exceeded comparator | 90% |
| Adaptive missions | 492 |
| Effort action counts, e1 / e3 / e6 | 117 / 189 / 186 |
| Cases using multiple effort levels | 56 |
| Cases with adaptive revisits | 0 |
| Mission-count range | 3–14 |
| Paired descriptive bootstrap interval, 95% | [-1.4069, +2.0063] percentage points |

### Interpretation

The detected fraction counts the initial confirmed detection in both numerator and denominator. It is not a rate of new detections. The mean is taken across case-level fractions, not pooled sites. Budget equality concerns abstract effort units; travel time, vessel fuel and staff costs are not measured by this audit.

“Matched or exceeded in 90%” contains **77 ties and 13 strict wins**; do not call it a 90% win rate. The interval crosses zero. The current data do not establish superiority over the comparator. The resampling interval describes this selected frozen simulation library, not uncertainty for a prospective field trial or a newly held-out scientific study.

The static comparator precommits the initial top three sites and surveys each with effort 6. It is a coded comparator, not a demonstrated reproduction of every agency's existing operating procedure. Ecological occupancy is synthetic; geometry and selected contextual covariates come from monitoring data.

### Reproducibility boundary

The current live audit is fully runnable from the source checkout or installed wheel. The fixture integrity receipt is in `src/adaptive_response/assets/manifest.json`. The preparation did not change the live planner's numerical rules, geometry, hidden-world generator, seeds, or existing observations; the original effort-policy sanity audit is retained at `reports/ui_effort_policy_audit.md`.

## Historical research and illustrative economics

| Historical claim/artifact | Evidence present | Missing or limiting evidence | Use in buyer presentation |
| --- | --- | --- | --- |
| Earlier live/frozen lane: 41.9% vs 40.0%, 88% match-or-exceed | Original README and HTML receipt | Complete underlying per-case CSV/configuration receipt absent; differs from the current live policy | Label historical; do not assign to current UI |
| Pooled 280-case mean advantage +1.58 pp, interval [+0.08, +2.99] pp | `reports/ramp_v2/headline_metric.json` | Original population-level case rows and complete run provenance absent; pooling includes the demo population | Historical summary only; cannot independently reconstruct all inputs here |
| Formal 180-case slice | Summary in `headline_metric.json` | Interval [-0.43, +3.24] pp crosses zero; raw outputs absent | Preserve the negative/uncertain evidence |
| ~21% extra simulated effort for parity | Historical methodology and script in `reports/ramp_v2/economic_impact/` | Script refers to absent `ramp_prospective.py` and population summary; cannot rerun unchanged | Illustrative historical calculation only |
| ~$1.28M / 164 field-days scaled illustration | Original README and economic/time visualizations | Proportional extrapolation, no measured field savings, no buyer-specific costs | Exclude as a current savings promise |
| R8/R11 GNN comparisons | Frozen protocol/case manifest, training/benchmark/comparison code | Trained checkpoint files, selected run configurations and complete benchmark CSVs absent | Development capability; learned-policy performance requires those deliveries |

None of the historical results should be retroactively attributed to the current live effort policy or used as guaranteed real-world ROI. Historical visualizations carry an archive notice, and the original narrative is preserved under `docs/HACKMIT_README.md`.

## What a field pilot must establish

Before rollout, agree the buyer's existing-practice comparator, geography, protocol, effort/cost semantics and primary outcome. Measure operational resource consumption, out-of-sample calibration, failure cases and survey outcomes; preserve logs and independent evaluation. Occupancy cannot be assumed known merely because a site was not observed. Record detectability assumptions and assess sensitivity. A successful simulation demo does not complete those requirements.
