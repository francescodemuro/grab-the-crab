# Third-party data and services

These notices document provenance for the evaluation package. They do not license original project code or transfer ownership of third-party material. Exact downstream obligations must be checked against the files/services included in the agreed delivery.

## Washington Sea Grant Crab Team datasets

**Rubinoff, Benjamin; Grason, Emily; McDonald, P. Sean; Watkins, Lisa (2025).** Data from: High-resolution monitoring of Salish Sea estuarine communities through participatory science [Dataset]. Dryad. [10.5061/dryad.0rxwdbsdt](https://doi.org/10.5061/dryad.0rxwdbsdt).

Used for monitoring/habitat context and CAMA calibration; the optional direct temperature layer requires the separately downloaded logger CSV. The frozen package does not include the full abundance or temperature dataset.

**Grason, Emily; Pineda, Jessica; McDonald, P. Sean (2025).** Data from: Tracking two invasions for the cost of one: Opportunistically tracking the range expansion of non-native Palaemon macrodactylus in the Salish Sea through participatory science [Dataset]. Dryad. [10.5061/dryad.sqv9s4ndp](https://doi.org/10.5061/dryad.sqv9s4ndp).

Used for shared site geography and sampling metadata. The shrimp PAMA measurements are not green crab CAMA outcomes.

Dryad's [reuse guidance](https://datadryad.org/help/guides/reuse), checked 2 October 2026, states that its datasets are published under CC0, including commercial reuse. Attribution is retained here. Derived site/context files also contain other sources; CC0 does not automatically classify every column in a merged table.

## SalishSeaCast

Derived graph audits contain water-route context generated from the SalishSeaCast ocean-model mesh. The [SalishSeaCast grid repository](https://github.com/SalishSeaCast/grid) identifies its files as copyright by the project contributors and the University of British Columbia, under Apache-2.0. The [model-data documentation](https://salishsea-meopar-tools.readthedocs.io/en/latest/erddap/ERDDAP_datasets.html) provides grid/data licensing context.

The complete raw mesh is not bundled. Confirm the exact source endpoint, dataset/version and required notices for any redistribution of raw files or derivatives in the final transaction.

## Washington DNR ShoreZone

Derived site metadata includes ShoreZone contextual descriptors. The code records the [Washington DNR GIS services](https://gis.dnr.wa.gov/site3/rest/services/). Data/service reuse terms have not been cleared in this preparation. Do not imply that ShoreZone nearest matches are authoritative monitoring coordinates.

## Optional map services

When enabled, online imagery is loaded directly from Esri World Imagery with OpenStreetMap tiles as fallback. The UI shows provider attribution. No tiles are bundled or resold. Review [Esri terms](https://www.esri.com/en-us/legal/terms/full-master-agreement) and the [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/) for the intended deployment. Provider requests are disabled by default.

The UI's crab illustration is based on the project's existing SVG mark. The previously referenced Wikimedia species photograph is no longer requested or bundled in the evaluation UI.

## Software dependencies

The core/UI environment is pinned in `requirements/demo-py312.txt`; observed version/license metadata is recorded in `reports/sale_review/dependencies.json` and `docs/DEPENDENCIES.md`. The optional RL and LLM extras use PyTorch and the OpenAI Python SDK respectively. Upstream copyrights and license notices remain applicable. This inventory is not an assertion that all redistribution conditions have been completed.

## No endorsement

Washington Sea Grant, WDFW, the University of Washington, Washington DNR, UBC, SalishSeaCast, Esri and OpenStreetMap are sources/providers. No sponsorship, customer contract, agency approval or endorsement is claimed.
