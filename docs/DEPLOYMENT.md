# Installation and operation

## Verified local route

The Python 3.12 dependency snapshot is `requirements/demo-py312.txt`. It pins the core/UI environment used for the recorded preparation checks. PyTorch and LLM dependencies are optional and excluded. Python 3.11 can resolve the supported dependency ranges with `pip install -e '.[dev,ui]'`; the 3.12 snapshot is not a 3.11 lock.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/demo-py312.txt
python -m pip install --no-deps -e .
grab-the-crab doctor
grab-the-crab demo --port 8000
```

A wheel is also installable without the source checkout:

```bash
python -m pip install -r requirements/demo-py312.txt
python -m pip install --no-deps dist/grab_the_crab-0.2.0-py3-none-any.whl
grab-the-crab demo
```

The wheel includes the UI and five frozen context/case assets. It does not need a raw-data download. A checkout's canonical context files and their bundled copies must match the asset manifest; `doctor` and `/readyz` detect drift. Preserve the frozen files. If intentionally producing a new data release, update the bundled copies, manifest, evaluation and claims together rather than editing a frozen fixture silently.

## Docker evaluation

```bash
docker compose up --build
```

Compose binds the service to `127.0.0.1:8000`, drops Linux capabilities and uses a read-only container filesystem with a temporary `/tmp`. The image runs as uid 10001 with a single worker. The application consumes only local fixtures by default. `python:3.12-slim` is a version-tagged base; resolve and record an immutable image digest for a contractual release. This container is an evaluation configuration, not a service SLA or multi-tenant production platform.

Container verification is a CI job. Where a Docker daemon is unavailable, the image recipe cannot be called locally verified; consult [Validation](VALIDATION.md) for the checks actually run.

## Session and access model

Default capacity is 16 browser-profile sessions with an idle lifetime of one hour. Tabs in the same browser profile share an incident. Session mutations are serialized and the UI supplies the expected round to avoid spending twice on a stale deployment. Data disappears on restart. Use **one worker**; multiple workers would own incompatible in-memory stores.

The local launcher binds loopback. To allow a buyer to access a remote demo, place a single worker behind authenticated buyer-controlled access and HTTPS, configure trusted proxy headers appropriately, and preserve same-origin URLs. There is no application login, user-level authorization, durable database, rate limit or production audit log in this release. Network exposure and buyer access are deployment decisions, not completed features.

## External services

- The default map is an offline geographic network view. Enabling **Online imagery** sends tile requests to Esri and possibly OpenStreetMap; provider attribution is then shown. Provider access/terms and commercial use need a separate review.
- The species illustration is a bundled SVG derived from the project's existing crab mark; no remote photograph is loaded.
- Optional natural-language tools use the `llm` extra and an externally supplied `OPENAI_API_KEY`. They are not required by the default UI. Confirm data-sharing terms before using them with private buyer data.
- Raw dataset download utilities are separate from the offline demo. They may require network access and upstream service availability.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `grab-the-crab` command missing | Activate the intended environment and reinstall the project |
| Missing FastAPI/uvicorn | Install the UI extra or the pinned demo requirements |
| Missing/drifted fixture | Run `grab-the-crab doctor`; restore the matching source/package asset and manifest |
| 409 after an idle session or restart | Reload to start a new evaluation; earlier state was in memory |
| 409 after a duplicate decision | Fetch current state and send its round before deciding again |
| 503 session capacity | Wait for idle expiry or restart an evaluation instance when no active work needs preserving |
| Missing temperature layer | Raw temperature logger data is optional; no values are imputed |
| GNN benchmark cannot find a checkpoint | Supply the separately delivered/retrained checkpoint; none is bundled |

Stop the local process with Ctrl-C or use `docker compose down`. No data migration is required for this release because incidents are not persisted.
