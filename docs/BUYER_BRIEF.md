# Grab the Crab — acquisition brief

## The decision problem

A first detection of an invasive species establishes presence at one location. It leaves an operational question: how should a response team allocate a limited survey budget to learn the invasion's extent? A non-detection provides uncertain evidence, and spending more effort at one site leaves less capacity elsewhere.

Grab the Crab implements this sequential workflow. It combines an explicit probabilistic belief with survey recommendations, operator control and an inspectable decision history. An environmental software provider or ecological services company could evaluate it as an adaptive survey-planning module inside an existing monitoring or incident-response platform.

## Product value

- **Plan under imperfect evidence.** Interpret non-detections using detectability and effort rather than treating an empty survey as guaranteed absence.
- **Adapt resource allocation.** Recompute the next site and effort level after each observation, subject to a conserved budget.
- **Explain and review decisions.** Show posterior beliefs, action diagnostics and operator overrides, and export a receipt of the evaluation.
- **Retain planner choice.** The engine supports transparent baselines and an optional learned-policy stack under a shared mission contract.

These are implemented capabilities. Reduced staffing, fuel use, ecological damage and monetary costs are outcomes for a buyer's pilot to measure, not established benefits of this release.

## What is available today

The default interface evaluates simulated incidents on real Salish Sea monitoring sites. It runs locally, without an API key or model checkpoint, and includes 100 frozen scenarios. The current live policy uses all three effort levels and conserves the same 18-unit budget as the static comparator.

The complete live audit reports 40.46% versus 40.17% mean detected occupied extent, including the first confirmed site. It is strictly better in 13 cases, tied in 77 and worse in 10; its descriptive resampling interval crosses zero. This evidence establishes reproducibility and adaptive behavior, not demonstrated superiority in real field operations. [Evidence and raw results](EVIDENCE.md).

The GNN/RL architecture, training and benchmark code are included as a development asset. Trained checkpoint files and their historical evaluations require separate delivery. The default UI is not running the GNN.

## Suggested acquisition scope

Acquire the project code, UI/API, inference and planning engine, learning/evaluation implementation, frozen evaluation fixtures, tests and technical handover, subject to contributor authority and third-party terms. Agree separately on trained weights, buyer-specific adaptation and transition support.

No valuation, asking price, revenue, customer traction or field savings is asserted in this brief. The three named contributors and external data obligations are recorded in [the rights inventory](RIGHTS_AND_ASSETS.md).

## Buyer evaluation path

1. Run the default demo and export a complete decision receipt.
2. Reproduce the current 100-case audit and inspect unfavorable cases.
3. Review the SDK/API boundary against the buyer's monitoring data and operational requirements.
4. Agree a field pilot with existing-practice comparators, explicit effort costs and independently assessed outcomes.
5. Complete ownership and delivery checks before a signed acquisition or license.

A pilot should begin with one geography and protocol. Calibrate detectability, map field resources to effort units and validate the effect of non-detections before operational reliance. Transferability to another species or coastline has not yet been validated.
