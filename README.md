# Grab the Crab

**Adaptive survey planning for invasive-species response.**

After a first confirmed detection, Grab the Crab helps an operator decide **where to survey next and how much effort to allocate**. It represents uncertainty about the invasion's extent, interprets imperfect detections, updates the evidence and recommends the next mission within a fixed budget.

**Release 0.2.0 is a reproducible technical evaluation package.** Surveys and hidden occupancy are simulated on real monitoring geography. Operational field effectiveness, customer adoption and monetary savings have not been established. Commercial transfer requires the rights review described in [Commercial readiness](COMMERCIAL.md).

## Evaluate it in five minutes

Use Python **3.12** for the recorded evaluation environment. Python 3.11 is also supported through the dependency ranges in `pyproject.toml`.

```bash
git clone --branch sale-readiness https://github.com/francescodemuro/grab-the-crab.git
cd grab-the-crab
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/demo-py312.txt
python -m pip install --no-deps -e .
grab-the-crab doctor
grab-the-crab demo
```

On Windows, use `py -3.12 -m venv .venv` and `.venv\Scripts\Activate.ps1` instead of the first two Python/environment commands. Open **http://127.0.0.1:8000**. No API key, model checkpoint or source-data download is needed to run the default demo. Installing dependencies initially requires an internet connection; the installed demo runs offline with online imagery disabled.

Alternatively, with Docker:

```bash
docker compose up --build
```

Follow [the buyer demo](docs/BUYER_DEMO.md): accept a recommendation, inspect how a non-detection changes the belief and next decision, spend the 18-unit budget and reveal the paired outcome. Export the decision receipt for review.

## What an acquirer receives

| Component | Included implementation |
| --- | --- |
| Inference engine | Finite-ensemble Bayesian belief over occupied extent and detectability; non-detections depend on survey effort |
| Decision layer | Frontier, information-gain and effort-aware planners; deterministic Dynamic Delimitation comparator |
| Product interface | FastAPI API, JavaScript/SVG dashboard, operator overrides and JSON decision receipts |
| Learning stack | Optional PyTorch GNN actor-critic, joint `(site, effort)` policy, training and checkpoint code |
| Evaluation assets | Real-site geometry/context, derived topology, 100 frozen UI incidents and the R8 case manifest |
| Delivery tooling | Installable wheel with assets, CLI, Python 3.12 dependency snapshot, Docker configuration and CI definitions |
| Handover material | Architecture, API contract, data provenance, evidence register, transfer inventory and acceptance procedure |

**Trained GNN checkpoint files are not present in this repository.** The default UI uses the transparent live heuristic, not a trained GNN. Buyer-specific data integration, live field-return ingestion, authentication, durable incident storage and production operations are separate work. See [Architecture](docs/ARCHITECTURE.md) and [Handover](docs/HANDOVER.md).

## Evidence you can reproduce

The current live-policy audit covers **all 100 frozen UI incidents**, with **18 effort units for each policy**:

| Measure | Current live adaptive policy | Paired static response |
| --- | ---: | ---: |
| Mean occupied extent detected, including the initial confirmed site | 40.46% | 40.17% |
| Mean absolute difference | +0.30 percentage points | Reference |
| Strictly better / tied / worse incidents | 13 / 77 / 10 | Reference |
| Matched or exceeded comparator | 90 of 100 | Reference |
| Adaptive effort use over 492 missions | e1: 117; e3: 189; e6: 186 | e6 at each of 3 missions |

This is a **descriptive product-behavior audit**, not a prospective field trial. Its paired bootstrap resampling interval for the mean difference is **[-1.41, +2.01] percentage points** and crosses zero. It does not establish superiority. [Raw case rows](reports/sale_review/live_product/cases.csv), [summary and asset hashes](reports/sale_review/live_product/summary.json), and [interpretation](docs/EVIDENCE.md) are included.

```bash
grab-the-crab audit --out artifacts/live-audit
```

Earlier frozen research receipts report different numbers and configurations. They are preserved as historical material, with their reproducibility gaps identified in [the evidence register](docs/EVIDENCE.md). Do not describe their simulated effort gap as measured annual savings or assign it to the current live UI.

## Validate and build

```bash
python -m pip install -e '.[dev,ui]'
pytest -ra
python scripts/check_release.py
python -m build
```

The core/UI suite does not require PyTorch. To validate the learned-policy stack too, install `.[dev,ui,rl]`; on Linux a CPU-only PyTorch installation avoids the GPU distribution. The `llm` extra enables optional external briefings and is independent of the default demo.

CI definitions cover Python 3.11/3.12, the optional RL stack, installed-wheel execution outside the checkout, and the container. A workflow definition by itself is not a passing execution result; see [Validation](docs/VALIDATION.md) for this preparation's recorded checks.

## Documentation

- [Buyer brief](docs/BUYER_BRIEF.md): problem, acquisition scope and integration opportunity.
- [Buyer demo](docs/BUYER_DEMO.md): a short reproducible presentation.
- [Architecture](docs/ARCHITECTURE.md) and [API](docs/API.md): implementation and integration boundary.
- [Deployment](docs/DEPLOYMENT.md): installation, runtime limits and troubleshooting.
- [Evidence](docs/EVIDENCE.md): current measurements and historical claim register.
- [Commercial readiness](COMMERCIAL.md), [rights inventory](docs/RIGHTS_AND_ASSETS.md) and [third-party notices](THIRD_PARTY_NOTICES.md): conditions for transfer.
- [Handover](docs/HANDOVER.md): delivery and acceptance steps.

## Origins and authorship

Built at HackMIT 2026 by **Pablo Ronco, Federico Passarelli and Francesco Demuro**. The original team descriptions and research narrative are preserved in [the HackMIT README](docs/HACKMIT_README.md). Washington Sea Grant, WDFW, the University of Washington and SalishSeaCast are data/context sources; no affiliation, endorsement or customer relationship is claimed.

No project-wide software license has been selected in this repository. A commercial agreement must establish the rights and permissions for evaluation, licensing or acquisition with the relevant rights holders; public availability does not establish sole ownership or exclusivity.
