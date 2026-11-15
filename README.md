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

## Versions and entry point

The current uncommitted development candidate is **2.1.0-dev**, implementing
issue #20 points 1-6. ASSESSMENT and the network entry point have new
2.1.0-dev version identities; the other eleven modules and all seven MIREOTs
retain their existing identities and axioms. Nothing on this branch is published.

The complete 2.0.0 baseline remains preserved in Git at
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`. Check out that commit separately to
load its original catalogue, documentation and exports. The active catalogue
does not resolve changed modules' 2.0.0 identities to development graphs.
See [the modelling decision](docs/decisions/TXT-DEC-011.md).

Load [ontology/textile-ontology.ttl](ontology/textile-ontology.ttl) with the local
[catalogue](catalog-v001.xml). Historical version IRIs and lowercase SOC are
intentionally absent from this active catalogue. Load historical versions with
the standalone `migration/historical/1.1.2/catalog-v001.xml` for the entire
session, with network fallback disabled; never combine these catalogues.
See the [migration guide](docs/CORE_2026_MIGRATION.md).

## Package contents

- [Architecture](docs/ARCHITECTURE.md), [modelling guide](docs/MODELLING_GUIDE.md) and public modelling rationale under `docs/decisions/`.
- `ontology/` and `mireot/`: the complete bounded Textile network.
- [Dependencies](docs/DEPENDENCIES.md): relevant upstream snapshots for comparison and provenance.
- [SHACL profiles](shacl/README.md) and seventeen [examples](examples/).
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

Runtime validation uses only files inside this directory and makes no remote-import requests. The default command checks RDF parsing, all declared import/version mappings, traceability projection, CSV integrity, public ADR links, manifest membership and SHA-256. The full command additionally checks seventeen examples, the original eight positive and eight negative SHACL fixtures, six RDFS/OWL-RL inference scenarios, and a recyclability control without RDFS.

The pytest suite additionally verifies forty-one migration scenarios, source fidelity, historical bytes, positive shape coverage and forbidden entailments. Merge the offline ontology closure with data when executing SHACL. Recyclability requires explicit RDFS inference; an entailment declaration does not itself load the ontology. The three structural profiles and optional complete-report profile are selective application constraints, not complete ontology conformance. The supplied reasoning checks do not establish complete OWL DL consistency or satisfiability.

## Source traceability

The CIRPASS Textile Ontology is grounded in the JRC textile studies while explicitly distinguishing direct extraction, adapted source content, modelling abstractions, project decisions and external reuse.

- [Resource table](traceability/textile-resource-traceability.csv)
- [Evidence table](traceability/textile-resource-evidence.csv)
- [Source-document registry](traceability/source-documents.csv)
- [Traceability guide](traceability/README.md)
- [Source methodology](docs/SOURCE_TRACEABILITY.md)

The following counts are generated from the public CSV: **904 resources**, **946 evidence rows**, **6 source documents**, and **248 resources with multiple evidence records**.

| Provenance category | Resource count |
|---|---:|
| adaptedDefinition | 403 |
| adaptedRelation | 27 |
| directExtraction | 16 |
| externalReuse | 1 |
| modellingAbstraction | 383 |
| projectDecision | 74 |

| Defining module | Resource count |
|---|---:|
| textile-assessment | 64 |
| textile-associated-materials | 61 |
| textile-connector | 37 |
| textile-context | 42 |
| textile-core | 70 |
| textile-durability | 58 |
| textile-indicator | 36 |
| textile-process | 130 |
| textile-recyclability | 176 |
| textile-repairability | 92 |
| textile-soc | 85 |
| textile-structure | 53 |
| textile-ontology | 0 |

Provenance-category meanings are documented in the traceability guide. Zero external evidence rows do not mean a resource is absent from the ontology: project-defined resources remain visible. Compound citations and unresolved relationships are disclosed rather than filled with inferred evidence. No row claims fresh substantive source verification. The historical Excel workbook and JRC source documents are not shipped.

The December 2025 JRC Textile Preparatory Study is a broad technical source for textile products, fibres, structures, processes, durability and testing. The May 2026 DPP-content study has a narrower scope concerning proposed apparel-DPP information. Absence from its tables does not establish absence of a JRC basis in the broader study. The later study does not supersede the entire earlier technical basis. Proposed content must not automatically be described as legally mandatory. Project modelling decisions remain distinct from JRC-derived statements.

## Licence and contributions

See [LICENSE.md](LICENSE.md) and the dependency notices in [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md). Upstream snapshot annotations retain their own terms; the candidate does not relabel them under the Textile licence. MAT redistribution evidence is recorded in the dependency documentation, with the applicable Apache 2.0 licence supplied under `LICENSES/`.

Propose issues and changes through the official [CIRPASS-2/dpp-textiles repository](https://github.com/CIRPASS-2/dpp-textiles). Include resource IRIs, applicable examples and source references. This branch prepares an unpublished 2.1.0-dev extension of the preserved 2.0.0 package; publication still requires owner approval. The current JRC-grounded ontology is available directly under `ontology/`; earlier Graphwise work is preserved separately under `ontology/graphwise-ontology/`. The two earlier Textile draft files, `ontology/textile materials.ttl` and `ontology/textile product data.ttl`, were removed from the current tree and remain available through Git history. This candidate is not a final official release.

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

## Issue #20 point 1 development validation

The result-to-aspect pattern is illustrated by
[example 12](examples/example-12-assessed-aspects-v2.1.0-dev.ttl).
The optional assessed-aspect target profile under `shacl/profiles/` checks
explicit bindings without requiring them or imposing a cardinality. The existing
validation commands above include the new example and regression coverage.
Complete OWL DL consistency remains unverified; OWL-RL checks do not prove it.

## Issue #20 point 2 assessment event bridge

`txtass:isRepresentedByProductEvent` links an assessment execution to its
conceptual ProductEvent. It is optional and independent of the PROCESS bridge.
[Example 13](examples/example-13-assessment-product-event-v2.1.0-dev.ttl) keeps
the ProductEvent separate from its EPCIS ObjectEvent carrier. The existing
bounded EVENT import supplies ProductEvent, not the carrier mapping axioms;
those remain available in the unchanged full EVENT 1.0.0 reference source.
See [TXT-DEC-012](docs/decisions/TXT-DEC-012.md).

## Issue #20 point 3 coded parameter settings

`txtass:hasParameterConcept` supplies categorical protocol values alongside the
existing quantitative setting pattern. [Example 14](examples/example-14-parameter-values-v2.1.0-dev.ttl)
shows both kinds of setting. Inclusive SHACL alternatives permit either or both
forms, preserve numeric validation and impose no categorical maximum. Concept
typing after RDFS inference does not verify controlled-vocabulary membership.
See [TXT-DEC-013](docs/decisions/TXT-DEC-013.md) and [SHACL guidance](shacl/README.md).

## Issue #20 point 4 awarded result points

`txtass:awardedScoreValue` records points actually awarded to an individual
assessment result, separately from its measured value, a scoring rule's prescribed
points and a derived indicator. [Example 15](examples/example-15-awarded-points-v2.1.0-dev.ttl)
shows both result categories and an unscored result. Supplied awards require an
actual decimal value and units:one; award links are optional and may be multiple.
No scoring bounds or automatic calculation are added. See
[TXT-DEC-014](docs/decisions/TXT-DEC-014.md) and [SHACL guidance](shacl/README.md).

## Issue #20 point 5 assessment conclusions

`txtass:hasAssessmentOutcome` optionally links a result to its controlled
conclusion under the applied method and context. For recyclability, use the
aggregate route-specific result and application-defined overall verdict concepts;
keep individual criterion outcomes separate. [Example 16](examples/example-16-assessment-outcomes-v2.1.0-dev.ttl)
uses synthetic concepts without regulatory or universal meaning. No production
SHACL profile changes: the small supplied-value guard exists only in focused
tests. Concept typing does not establish vocabulary membership or a correct
method-specific decision. See [TXT-DEC-015](docs/decisions/TXT-DEC-015.md).

## Issue #20 point 6 assessment execution times

[Example 17](examples/example-17-assessment-times-v2.1.0-dev.ttl) reuses PROV
start/completion timestamps on explicitly typed AssessmentExecution/Activity
instances, independently of EPCIS. A date-only source uses dcterms:date with
xsd:date as a coarse associated date, without inventing a time or implying start
or completion. Results retrieve execution times through resultOfAssessment.
No ontology source, import, version identity or production SHACL profile changes.
The optional supplied-value guard is test-only; authoritative PROV reasoning is
checked separately in memory. See the [modelling guide](docs/MODELLING_GUIDE.md)
and [validation report](docs/ISSUE20_POINT6_IMPLEMENTATION.md).
