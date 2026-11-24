# CIRPASS Textile Ontology community candidate

A modular OWL ontology network for textile Digital Product Passport information. The ontology modules directly under `ontology/` form the current JRC-grounded community review candidate; this is not a published release.

This repository brings together Textile DPP work by GS1, Graphwise and CIRPASS-2 contributors.

The Textile ontology network and its twelve modules identify **Elio Hbeich,
BOUGACHA Racem, Ivo Ladenius, Andreas Schneider, Jan Merckx and Piero de Sabbata**
as `dcterms:creator`. The owner-approved creator update preserves the established
English language-tagged literal representation and all existing creators.

## Two bodies of ontology work

The **current CIRPASS Textile Ontology** is the JRC-grounded community review candidate directly under `ontology/`, with entry point [ontology/textile-ontology.ttl](ontology/textile-ontology.ttl). It includes normalized public source traceability, modelling-decision documentation, MIREOT dependencies, SHACL profiles, examples and public validation.

[Earlier Graphwise ontology work](ontology/graphwise-ontology/README.md) is preserved for reference and project continuity. It predates the current JRC-grounded modelling approach and is separate from the current package. Its graphs are not loaded by the current catalogue or validator and are outside the package checksum contract. Load the two models separately. See [publication scope](docs/PUBLICATION_SCOPE.md).

## Issue #9 development scope

Issue #9 specifies approved documentation and annotation clarifications to
the merged 2.0.0 baseline. These clarifications are prepared for review. Issue #9 alone preserves imports and logical axioms. The combined integration
uses a separate development version identity.
See [the approved issue #9 decisions](docs/decisions/TXT-DEC-016.md).

## Selected CORE sources

| CORE module | Selected upstream version |
|---|---|
| ACTOR | 2.2.0 |
| CON | 2.4.0 |
| EVENT | 1.0.0 |
| MAT | 1.1.0 |
| P_DPP | 2.2.0 |
| SOC | 2.2.0 |

These versions are verified from the local source snapshots, not inferred from
the local MIREOT version. Textile retains bounded extracts using original CORE
term IRIs and an offline-resolvable closure. [Dependencies](docs/DEPENDENCIES.md)
identifies snapshot files, hashes, extraction scopes and update responsibilities;
no upstream commit identifier is asserted without evidence.

## Versions and entry point

This unpublished integration package uses **integration-2026-11.3**. The thirteen
Textile graphs declare distinct version IRIs under `/dev/integration-2026-11.3`
and retained module identities cite the corresponding `.2` version as prior. Common retains its migration provenance. Six CORE subsets
retain their 2.0.0 identities and SI retains its 1.1.2 identity; the runtime
closure contains 20 graphs.

Load [ontology/textile-ontology.ttl](ontology/textile-ontology.ttl) with the
active [catalogue](catalog-v001.xml). Frozen Textile 2.0.0 is an independently
verified sibling package named `dpp-textiles-frozen-2.0.0`, with its own
catalogue and original bytes. Load its versioned entry and all imports using
that catalogue only, with network fallback disabled. The preserved 1.1.2
catalogue serves its own historical closure. Never mix historical and
development catalogues. Historical bytes are preserved in Git and the frozen
local package; historical resolution is established only with the deliberately
selected historical catalogue. Public HTTP dereferencing is outside this evidence.
See the [issue #12 decision](docs/ISSUE12_MATERIAL_COMPOSITION.md),
[CORE migration guide](docs/CORE_2026_MIGRATION.md),
[1.1.2 catalogue](migration/historical/1.1.2/catalog-v001.xml), and
[Phase 2B record](migration/PHASE2B_IMPLEMENTATION.md).

## Package contents

- [Architecture](docs/ARCHITECTURE.md), [modelling guide](docs/MODELLING_GUIDE.md) and public modelling rationale under `docs/decisions/`.
- `ontology/` and `mireot/`: the complete bounded Textile network.
- [Dependencies](docs/DEPENDENCIES.md): relevant upstream snapshots for comparison and provenance.
- [SHACL profiles](shacl/README.md) and eleven [examples](examples/).
- [Diagrams](diagrams/DIAGRAM_INDEX.md): illustrative views with a recomputed inventory.
- Positive, negative and reasoning fixtures under `tests/abox_corpus/`.

## Offline validation

Use Python 3.11 or later. The candidate is tested with the installed versions recorded in `requirements-validation.txt`. Install these dependencies before offline execution:

```text
python -m pip install -r requirements-validation.txt
python -B scripts/validate_public.py
python -B scripts/validate_public.py --full
python -B -m pytest -p no:cacheprovider tests -q
python -B scripts/validate_public.py --full --complete-report
```

Runtime validation uses only files inside this directory and makes no remote-import requests. The default command checks RDF parsing, all declared import/version mappings, traceability projection, CSV integrity, public ADR links, manifest membership and SHA-256. The full command additionally checks eleven examples, the original eight positive and eight negative SHACL fixtures, six RDFS/OWL-RL inference scenarios, and a recyclability control without RDFS.

The pytest suite additionally verifies forty-one migration scenarios, source fidelity, historical bytes, positive shape coverage and forbidden entailments. Merge the offline ontology closure with data when executing SHACL. Recyclability requires explicit RDFS inference; an entailment declaration does not itself load the ontology. The three structural profiles and optional complete-report profile are selective application constraints, not complete ontology conformance. The supplied reasoning checks do not establish complete OWL DL consistency or satisfiability.

## Source traceability

The CIRPASS Textile Ontology is grounded in the JRC textile studies while explicitly distinguishing direct extraction, adapted source content, modelling abstractions, project decisions and external reuse.

- [Resource table](traceability/textile-resource-traceability.csv)
- [Evidence table](traceability/textile-resource-evidence.csv)
- [Source-document registry](traceability/source-documents.csv)
- [Traceability guide](traceability/README.md)
- [Source methodology](docs/SOURCE_TRACEABILITY.md)

The following counts are generated from the public CSV: **906 resources**, **947 evidence rows**, **6 source documents**, and **248 resources with multiple evidence records**.

| Provenance category | Resource count |
|---|---:|
| adaptedDefinition | 403 |
| adaptedRelation | 27 |
| directExtraction | 16 |
| externalReuse | 1 |
| modellingAbstraction | 383 |
| projectDecision | 76 |

| Defining module | Resource count |
|---|---:|
| textile-assessment | 59 |
| textile-associated-materials | 61 |
| textile-common | 37 |
| textile-context | 42 |
| textile-core | 70 |
| textile-durability | 58 |
| textile-indicator | 36 |
| textile-process | 131 |
| textile-recyclability | 177 |
| textile-repairability | 92 |
| textile-soc | 85 |
| textile-structure | 53 |
| textile-ontology | 0 |

Provenance-category meanings are documented in the traceability guide. Zero external evidence rows do not mean a resource is absent from the ontology: project-defined resources remain visible. Compound citations and unresolved relationships are disclosed rather than filled with inferred evidence. No row claims fresh substantive source verification. The historical Excel workbook and JRC source documents are not shipped.

The December 2025 JRC Textile Preparatory Study is a broad technical source for textile products, fibres, structures, processes, durability and testing. The May 2026 DPP-content study has a narrower scope concerning proposed apparel-DPP information. Absence from its tables does not establish absence of a JRC basis in the broader study. The later study does not supersede the entire earlier technical basis. Proposed content must not automatically be described as legally mandatory. Project modelling decisions remain distinct from JRC-derived statements.

## Licence and contributions

See [LICENSE.md](LICENSE.md) and the dependency notices in [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md). Upstream snapshot annotations retain their own terms; the candidate does not relabel them under the Textile licence. MAT redistribution evidence is recorded in the dependency documentation, with the applicable Apache 2.0 licence supplied under `LICENSES/`.

Propose issues and changes through the official [CIRPASS-2/dpp-textiles repository](https://github.com/CIRPASS-2/dpp-textiles). Include resource IRIs, applicable examples and source references. This branch prepares an unpublished integration candidate; publication still requires owner approval. The current JRC-grounded ontology is available directly under `ontology/`; earlier Graphwise work is preserved separately under `ontology/graphwise-ontology/`. The two earlier Textile draft files, `ontology/textile materials.ttl` and `ontology/textile product data.ttl`, were removed from the current tree and remain available through Git history. This candidate is not a final official release.

`PUBLICATION_MANIFEST.txt` lists every candidate file, including itself and `SHA256SUMS`. `SHA256SUMS` hashes every manifest member except itself. Verify these before distributing a candidate.

## Reference Data

For now we're collecting some [ref-data](ref-data):
- Taxonomies
- Large nomenclatures like EU CN and WCO HS (tariff codes), ECHA EC and CAS (chemicals), UN-LOCODE (places)
- Sustainability standards from [StandardsMap](https://www.standardsmap.org/)

Important: Github has a limit of 50Mb per file, so if you have some large files do this:
- For intermediate files that don't need to be shared with others because they can be reproduced:
  add them to .gitignore
- For final files that need to be shared eg because they need to be loaded in a semantic repo:
  use [git lfs](https://git-lfs.com/):
```
git lfs install
You only need to run this once per user account.
git lfs track <my-large-file>
```

Then use commit and push as for normal files.


## Publication boundary and evidence supplements

See [publication scope](docs/PUBLICATION_SCOPE.md) for the current package manifest and the separate preserved-reference inventory. Public validation excludes Graphwise material and existing reference-data collections. Seven [documentary locator supplements](traceability/evidence-locator-resolutions.csv) resolve previously missing locations without changing RDF: 944 evidence rows have recorded locators and two remain transparently unresolved. No row claims full substantive verification.

## Common and Connector compatibility

[Textile Common](ontology/textile-common.ttl) is the canonical shared ontology.
The separately generated [Connector compatibility representation](compat/textile-connector.ttl)
contains the complete Common non-header graph with the original `txtcon:` term
IRIs; it imports the SI MIREOT and does not import Common. Load one representation
for a given purpose with the active catalogue. See the [issue 16 integration
record](docs/ISSUE16_COMMON_MIGRATION.md) for version and historical resolution.

## Cumulative issue #20 integration

The internal unpublished integration identity is `integration-2026-11.3`.
Assessment supports explicit assessed aspects, product-facing event links,
categorical settings, awarded scores and controlled assessment outcomes.
Execution-time guidance reuses optional PROV timestamps without importing PROV.
See the modelling guide and decisions TXT-DEC-011 through TXT-DEC-015. The
assessed-aspect SHACL profile is optional; published 2.0.0 and the committed
`.1` and `.2` integration states retain their own isolated catalogues.
