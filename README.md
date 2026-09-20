# Grab the Crab

**Adaptive first-response mission control for marine invasive species.** HackMIT 2026.

A newly detected invasive species has an unknown true extent. Grab the Crab maintains an explicit probabilistic belief over that hidden extent, allocates limited field effort under imperfect detection, ingests new field evidence, updates its belief, and replans the next mission.

```
OBSERVE → INFER → DECIDE → SURVEY → LEARN → REPLAN
```

Built on real Washington Sea Grant Crab Team monitoring data (Salish Sea, European green crab, *Carcinus maenas*): real site coordinates, real habitat classes, a real 49-site/118-edge monitoring graph, and water-constrained travel routing from the SalishSeaCast ocean model.

## Results

On 280 frozen benchmark incidents built on the real monitoring graph, the effort-aware planner found **4.67% more of the true infestation** than a fixed maximum-effort strategy at identical field-effort budget (41.9% vs 40.0% detected, 95% bootstrap CI excluding zero). It matched or beat that baseline in 88% of incidents. Equivalently, the traditional strategy needs about **21% more field effort** to reach the same outcome — on Washington's real program, that is on the order of **164 volunteer field-days a year**, or roughly **$1.28M/year** at current state funding, as an illustrative projection (see `reports/ramp_v2/economic_impact/receipt.md` for the full calculation and sources).

## How it works

**Belief engine.** A pure-Python, framework-free finite-ensemble Bayesian engine (`src/adaptive_response/spatial_belief.py`). Each hypothesis pairs an ecological extent (which sites are occupied) with a detectability parameter q, updated exactly under `P(no detection | occupied, effort e) = (1 - q)^e`. Extents are sampled from four world-model families (`src/adaptive_response/world_models.py`): graph diffusion, spatial clustering, habitat-driven, and fragmented-patchy.

**Hidden-truth firewall.** The true occupancy state lives in a separate simulator object (`HiddenWorld`) that planners and the UI structurally cannot reach before reveal — enforced by the type boundary, not by convention, and checked by tests.

**Planners** (`src/adaptive_response/`):
- `planners.py` — a transparent frontier heuristic and an information-gain planner that scores every (site, effort) pair by expected entropy reduction over possible worlds.
- `effort_aware_planner.py` — separates *where* to survey (belief-first site ranking) from *how much* effort to spend (information gained per unit cost), with an optional early-stop rule.
- `dynamic_delimitation_planner.py` — a deterministic, non-Bayesian reactive baseline: a confirmed positive expands the local search frontier, a negative closes that branch without expanding it. Used as an honest operational comparator with a tested information firewall (it never reads belief, uncertainty, or possible worlds).
- `rl/` — a graph neural network actor-critic policy (PyTorch) that picks (site, effort) jointly from the same observable graph state, trained via on-policy RL with independently seeded runs for reproducibility.

**Product.** FastAPI backend (`web_app.py`, `mission_control.py`), a hand-written JavaScript/SVG frontend (`web/`) with a real coastline map, posterior-occupancy heat, a "probable worlds" panel, and full decision/outcome receipts. An interactive judge mode lets anyone play a full response campaign against the planner on the same hidden incident, then reveals the truth and scores every strategy side by side. Optional natural-language mission briefings via OpenAI (`narrate.py`, `copilot.py`).

**Discipline.** Frozen, planner-independent benchmark case manifests with validation/test splits (`reports/milestones/`), multiple independently-seeded training runs, and paired bootstrap comparisons (`scripts/r8_paired_comparison.py`, `scripts/r11_paired_comparison.py`) rather than single-run point estimates.

## Running it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ui]"

python -m uvicorn adaptive_response.web_app:app --port 8000
```

Open `http://127.0.0.1:8000`.

Optional extras: `pip install -e ".[dev,rl]"` for the GNN/RL stack (requires PyTorch), `pip install -e ".[dev,llm]"` for the OpenAI-powered mission briefings.

## Testing

```bash
pip install -e ".[dev,ui]"
pytest
```

## Reproducing the benchmark results

```bash
# Fixed-effort vs effort-aware planner vs GNN/RL on the frozen 180-case manifest
python scripts/run_spatial_benchmark_r8.py --rl-checkpoint <checkpoint>.pt --out reports/r8_benchmark.csv
python scripts/r8_paired_comparison.py --rl-csv reports/r8_benchmark_seed0.csv ... --out reports/r8_paired_comparison.md

# GNN/RL vs the deterministic Dynamic Delimitation baseline
python scripts/run_r11_dynamic_benchmark.py --rl-checkpoint <checkpoint>.pt --out reports/r11_benchmark.csv
python scripts/r11_paired_comparison.py --gnn-csv reports/r11_benchmark_seed0.csv ... --out reports/r11_paired_comparison.md

# Effort-to-Parity: how much extra field effort a simpler strategy needs to
# match the learned policy's result at the same budget
python scripts/r11_effort_to_parity.py --gnn-csv reports/r11_benchmark_seed0.csv ... --out-csv reports/r11_effort_to_parity.csv --out-md reports/r11_effort_to_parity.md

# Retrain the GNN/RL policy from scratch
python scripts/train_spatial_gnn_policy.py --run-name my_run --seed 0
```

## Data sources

- Washington Sea Grant Crab Team monitoring data, Dryad (2017–2023, *Carcinus maenas*, Salish Sea).
- Washington Sea Grant Crab Team volunteer program structure (`wsgcrabteam.uw.edu`).
- Washington Dept. of Fish & Wildlife European Green Crab management publications and budget figures.
- SalishSeaCast ocean model mesh (UBC), for water-constrained travel routing.

## Team

Francesco — learning and evaluation (GNN/RL policy, training, benchmark protocol and paired-comparison tooling, effort-aware planner, economic/time-savings analysis).
Pablo — environment and product (simulator, belief engine, real-data pipeline, mission-control backend, interactive UI).
Federico — ecological response logic (frontier delimitation strategy, species/habitat framing, demo narrative).
