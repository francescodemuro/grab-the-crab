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
| Actual browser interaction | Passed in GitHub Actions run 37011810795 | Chromium: six missions, budget 18, replanning after mission three, receipt download, independent browser session, zero external requests and zero JavaScript errors |
| Mobile layout | Passed at 390px in the same browser run | Screenshot captured; document width 390px, no horizontal overflow |
| Container execution | Passed in GitHub Actions run 37011810795 | Image build, readiness, static asset and API state checks |
| Python 3.11 and 3.12 | Passed in GitHub Actions run 37011810795 | Core/UI, build, fixture/evidence check and installed wheel |
| Learned-policy CI | Passed in GitHub Actions run 37011810795 | Full suite with CPU PyTorch |
| API documentation | Verified locally | OpenAPI version 0.2.0; optional Swagger viewer accessible; dashboard retains its strict content-security policy |

The dependency advisory output is in `reports/sale_review/dependency-vulnerabilities.json`. A no-findings package advisory scan is not a security certification. It must be rerun before a contractual release, with the final optional extras and container image included if those are delivered.

The full suite emits one upstream Starlette warning about TestClient's future `httpx` transition. Tests pass; the current recorded UI environment retains the supported behavior used by this release.

All five jobs completed successfully in the linked remote run. The browser job also publishes desktop/mobile screenshots and a downloaded receipt as the `browser-evaluation` artifact. Local browser execution was unavailable; the interaction results above were observed in the real Chromium instance on GitHub Actions. CI status for later revisions must be read from their actual workflow runs.

Recorded remote run: https://github.com/francescodemuro/grab-the-crab/actions/runs/37011810795 (commit `c4b78d0a15c17acc78825c7ec27bdc9b1431e47f`).
