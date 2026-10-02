# Recorded validation — 2 October 2026

Source preparation baseline: `9712c241fb5f3f7f3806fda84617ec2c7a2aeb76`. Software version: **0.2.0**. The preparation preserves the frozen data, seeds and numerical live-policy behavior; packaging, HTTP session handling and presentation changed.

| Check | Recorded result | Scope |
| --- | --- | --- |
| Full suite with CPU PyTorch | 392 passed | Core, UI/session/API and existing RL/training/checkpoint tests |
| Core/UI without PyTorch | 328 passed; 7 optional modules skipped | Fresh environment; optional RL tests intentionally skipped |
| Build | Wheel and source distribution built successfully | setuptools build, Python 3.12 |
| Installed wheel outside checkout | Passed | Static/UI assets, 100 cases, six-mission default path, budget 18, reveal gate and JSON receipt; PyTorch not imported |
| Frozen fixtures | Five assets verified against SHA-256 manifest | Checkout and bundled bytes agree |
| Live policy audit | All 100 frozen UI cases reproduced | 492 missions; 40.46% vs 40.17%; descriptive audit only |
| Dependency metadata | 20 core/UI packages recorded | Version/license metadata, not complete rights clearance |
| Known dependency advisories | No known vulnerabilities reported by pip-audit 2.10.1 | Pinned Python 3.12 core/UI requirements; optional extras/container OS/source logic excluded |
| JavaScript parse | `node --check` passed | Current frontend file |
| Actual browser interaction | Not executed locally | The environment has no browser executable and browser binary download was unavailable; automated browser job provided |
| Container execution | Not executed locally | No Docker daemon available; container CI job provided |
| Python 3.11 | CI definition provided; no local interpreter available | Use declared dependency ranges; the pinned snapshot is Python 3.12 only |

The dependency advisory output is in `reports/sale_review/dependency-vulnerabilities.json`. A no-findings package advisory scan is not a security certification. It must be rerun before a contractual release, with the final optional extras and container image included if those are delivered.

The full suite emits one upstream Starlette warning about TestClient's future `httpx` transition. Tests pass; the current recorded UI environment retains the supported behavior used by this release.

CI status must be read from actual workflow runs. Definitions are not evidence that remote checks passed. Browser and container checks remain explicit verification items until executed in an environment that supports them.
