# Evaluation API contract

Base URL: `http://127.0.0.1:8000`. OpenAPI schema: `/openapi.json`; optional interactive documentation: `/docs`. The interactive documentation loads FastAPI's default CDN assets and requires network access. The default evaluation dashboard runs offline. This API runs synthetic evaluation incidents.

Call `/api/cases` or `/api/state` first and preserve the returned HTTP-only, same-site session cookie. A browser profile has one session; another profile has another. Use a cookie jar for command-line clients. State responses are not cached. The cookie is marked secure over HTTPS.

| Method | Route | Behavior |
| --- | --- | --- |
| GET | `/healthz` | Process/version health; no incident allocated |
| GET | `/readyz` | Verify frozen evaluation assets against their hashes |
| GET | `/api/cases` | Return 100 frozen UI cases and current case id |
| GET | `/api/state` | Return the observable incident state; initialize a session if needed |
| POST | `/api/reset` | Reset a frozen case or an ad-hoc seed |
| POST | `/api/deploy` | Execute a simulated survey with a valid site and effort |
| POST | `/api/reveal` | Reveal evaluator-only truth after the budget is spent |
| GET | `/api/receipt` | Download versioned JSON containing the current gated snapshot |
| POST | `/api/plan`, `/api/execute` | Original two-stage rehearsal interface |

Reset request:

```json
{"case_id": "incident_079"}
```

Or use `{"seed": 42}`. Seeds must be integers in `[0, 999999]`; do not send both selectors. Unknown cases return a conflict. Extra request fields are rejected.

Deployment request:

```json
{"site_id": "384", "effort": 6, "expected_round": 0}
```

`effort` must be an integer exactly equal to 1, 3 or 6. The site must be available in the current incident, cannot be the already confirmed first site and must satisfy the current loop/budget gates. `expected_round` is optional for older clients; new clients should always send the last observed `resources.round`. A duplicate or stale decision then returns 409 without another deployment.

| Status | Meaning |
| --- | --- |
| 200 | Operation succeeded |
| 403 | Cross-origin browser mutation rejected |
| 409 | Invalid mission phase/site/budget, stale decision, expired or missing session |
| 422 | Invalid request shape/type/range or conflicting selectors |
| 503 | Session capacity exhausted or readiness assets invalid |

Session capacity returns `Retry-After: 60`; it does not discard existing active work. Expired mutation sessions return 409. Reloading/reading state starts a new evaluation. Server restarts lose all sessions.

## Receipt and truth boundary

The JSON download contains `schema_version`, `software_version`, `mode: "simulation_evaluation"` and `state`. Before reveal, performance and hidden truth remain absent/null exactly as in `/api/state`. After reveal, the snapshot includes the adaptive, static and operator-path evaluation. The receipt is evidence from a local simulation, not a signed or tamper-proof operational log.

## Reproduce a decision

```bash
curl -c /tmp/crab-cookies.txt http://127.0.0.1:8000/api/state
curl -b /tmp/crab-cookies.txt -H 'Content-Type: application/json' \
  -d '{"site_id":"384","effort":6,"expected_round":0}' \
  http://127.0.0.1:8000/api/deploy
curl -b /tmp/crab-cookies.txt http://127.0.0.1:8000/api/receipt -o decision-receipt.json
```

Site 384 is specific to the default frozen case; integrations must select ids from the current state. The API has no authentication, authorization, external dispatch, real-observation ingestion or persistence. Keep evaluation access local or behind a buyer-controlled access boundary. [Deployment](DEPLOYMENT.md).
