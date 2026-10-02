# Buyer handover and acceptance

## Delivery procedure

1. Complete the rights and transaction-scope checks in `COMMERCIAL.md`.
2. Select a clean, reviewed source commit. Run the full applicable tests, `grab-the-crab doctor`, `python scripts/check_release.py` and the installed-wheel check.
3. Reproduce the 100-case audit using the delivered version and compare its case rows to the committed evidence. Investigate any divergence before shipment.
4. Build the wheel/source archives and generate a revision/hash manifest with `python scripts/build_handover.py --out artifacts/handover`.
5. Deliver the final archive and source revision through the agreed private channel. Include separate model checkpoint files and source obligations only if the contract includes them.
6. The buyer reruns the acceptance procedure in its environment and records acceptance against that source revision and manifest.

The handover builder refuses a dirty checkout, uses tracked source only, and excludes untracked private data, credentials and checkpoint folders. Ignored files are not automatically part of the sale. The builder includes the source archive, wheel, source distribution, live audit summary and per-file SHA-256 receipts. Signed contracts and contributor assignments are not embedded.

## Suggested technical acceptance

| Check | Procedure | Expected evaluation behavior |
| --- | --- | --- |
| Delivery identity | Compare SHA-256 values with manifest | Every included artifact matches the agreed revision |
| Fixture integrity | `grab-the-crab doctor` | All five bundled assets match canonical receipts |
| Installation | Install wheel outside the checkout | UI/static assets and real-site fixtures are available |
| Default scenario | Open UI in a fresh browser profile | Frozen case `incident_079`, 18-unit budget, truth locked |
| Recommendation path | Follow all default recommendations | Efforts 6, 6, 3, 1, 1, 1; six missions; no overspend |
| Reveal gate | Attempt reveal before budget exhaustion | 409; no hidden evaluation exposed |
| Operator control | Override a valid site/effort | Belief updates through the same inference path |
| Session isolation | Use independent browser profiles | One operator's deployment does not change the other's incident |
| Stale deployment | Repeat a request with its old `expected_round` | 409; budget not spent again |
| Receipt | Download before and after reveal | Observable snapshot before reveal, complete simulated evaluation after |
| Full audit | `grab-the-crab audit --out artifacts/live-audit` | 100 cases, 492 adaptive missions, current recorded metrics |
| Optional GNN delivery | Validate supplied checkpoint hash and R8/R11 run | Required only if trained policy/model performance is in scope |

These are proposed software acceptance criteria. Field-operational criteria, deadlines and financial terms require buyer agreement and are not commitments made by this repository.

## Integration work to scope

A live monitoring deployment needs authoritative input adapters, effort/catchability calibration, real field observations, identity/access control, durable incident storage and an operational runbook. Pilot one geography/protocol before claiming transferability. Decide whether GNN training and selected weights are part of delivery or later research work.

## Operational transition

Agree named support contacts, availability, issue ownership and the duration/cost of transition support privately. The repository currently establishes no warranty, uptime commitment or support SLA. Provision buyer-owned infrastructure and keys; do not transfer personal developer credentials.
