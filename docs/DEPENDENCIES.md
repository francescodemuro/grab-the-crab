# Dependency inventory

Observed package metadata for the pinned Python 3.12 core/UI environment. This is not a complete license clearance or vulnerability audit. PyTorch/LLM extras are excluded from this snapshot and require their own delivery review.

| Package | Version | Declared license metadata |
| --- | --- | --- |
| annotated-doc | 0.0.5 | MIT |
| annotated-types | 0.8.0 | MIT |
| anyio | 4.15.1 | MIT |
| certifi | 2026.7.22 | License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0) |
| click | 8.5.0 | BSD-3-Clause |
| fastapi | 0.142.2 | MIT |
| h11 | 0.16.0 | License :: OSI Approved :: MIT License |
| httpcore | 1.0.9 | BSD-3-Clause |
| httpx | 0.28.1 | License :: OSI Approved :: BSD License |
| idna | 3.19 | BSD-3-Clause |
| networkx | 3.7 | BSD-3-Clause |
| numpy | 2.3.5 | License :: OSI Approved :: BSD License |
| opentelemetry-api | 1.45.0 | Apache-2.0 |
| pydantic | 2.13.5 | MIT |
| pydantic_core | 2.46.5 | MIT |
| PyYAML | 6.0.3 | License :: OSI Approved :: MIT License |
| starlette | 1.7.0 | BSD-3-Clause |
| typing-inspection | 0.4.4 | MIT |
| typing_extensions | 4.16.0 | PSF-2.0 |
| uvicorn | 0.54.0 | BSD-3-Clause |

Recreate with `python scripts/export_dependency_inventory.py` in the pinned environment. Exact license-file names and upstream URLs are in `reports/sale_review/dependencies.json`. Preserve required upstream notices in any distribution.
