# Buyer demo — approximately four minutes

## Setup

Follow the root README or run `docker compose up --build`. Open `http://127.0.0.1:8000`. Leave **Online imagery** unchecked so the presentation has no external asset dependency. Open `/readyz` beforehand and check that it reports `ready`.

The default is **incident_079**, selected for clear evidence-driven adaptation and effort diversity, not because it beats the comparator. Site positions and context are derived from real monitoring data; hidden occupancy and survey returns are synthetic.

## Presentation sequence

| Time | Action | Explanation |
| --- | --- | --- |
| 0:00–0:30 | Show the first detection, uncertain surrounding sites and 18-unit budget | “One confirmed location does not tell us how far the invasion extends.” |
| 0:30–1:10 | Inspect the next-site recommendation and effort choices | “The engine chooses both the location and the amount of evidence to collect. The operator can override either.” |
| 1:10–2:20 | Use the recommendation and deploy through the first three missions | “A non-detection changes the posterior. Watch the next recommendation change after the third survey.” |
| 2:20–3:10 | Follow the remaining recommendations | “This case uses effort 6, 6, 3, 1, 1, 1 and spends exactly 18 units.” |
| 3:10–3:40 | Reveal the extent and compare the paths | “The comparison uses the same hidden incident and budget. A single trajectory is not a performance guarantee.” |
| 3:40–4:00 | Export the decision receipt; show the full audit CSV | “The buyer can reproduce and review the decisions and all 100 outcomes.” |

The default path surveys sites **384, 207, 383, 201, 198, 204**. In this case no additional occupied site is found beyond the initial confirmation; the policies tie on detected extent. Present it as a demonstration of adaptation, not a winning result.

## Buyer interaction

Reset the case and invite the buyer to choose a different site or effort level. Do not reveal truth early or select a winning case and call it representative. Different browser profiles maintain separate evaluation sessions; tabs in one browser profile share a session.

## Follow-up evidence

```bash
grab-the-crab audit --out artifacts/live-audit
```

Open `cases.csv` and `summary.json` in the output folder. The audit follows the current recommendation in every case, checks full-budget conservation and reports strict wins, ties and losses separately. Explain that a real field pilot, authenticated deployment and integration with the buyer's observations remain outside this evaluation release.
