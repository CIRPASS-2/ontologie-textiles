# Issue #20 point 2 implementation for maintainer review

Branch: `fix/issue-20-point-2`, created from committed point 1 at
`c87568e707d1c183a8ef24090180fcae01001f7c`. Changes are unstaged and uncommitted.
No point 3 or later change, push, merge, release or publication is included.

## Exact semantic delta

ASSESSMENT adds nine RDF triples and removes none: eight triples declare and
annotate `txtass:isRepresentedByProductEvent`, and one imports the existing
bounded EVENT MIREOT. The domain is AssessmentExecution; the range is ProductEvent.
The definition separates conceptual product events from technical EPCIS carriers.
Traceability points to TXT-DEC-012 with modellingAbstraction, without JRC evidence.
No functional/cardinality restriction, inverse, alignment, chain or event class is
introduced. The point-1 property and all other canonical ontology graphs remain
unchanged. EVENT, PROCESS, CORE, EPCIS mappings, MIREOTs, SHACL and migration
infrastructure retain their bytes.

Standalone ASSESSMENT loads six existing documents rather than five; the full
Textile runtime remains twenty. The bounded subset has no carrier-mapping axioms.
The example therefore illustrates existing full EVENT 1.0.0 semantics without
adding mappings to the Textile runtime. OBSERVE / inspecting alone does not
establish a qualifying ProductEvent, and range inference does not validate input.

The unpublished 2.1.0-dev version and existing catalogue are retained; no new
version management is needed. The 2.0.0 baseline remains immutable in Git at
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`. Committed point-1 examples, tests,
SHACL, decision and review record are unchanged.

## Minimality and existing contracts

One illustrative RDF example and one focused test module are added. No new SHACL
profile is required. Two existing test files need narrow adaptations: the exact
approved-delta fixture must include the later nine triples so frozen creator,
version and MAT proofs continue to run; the protected-input test must allow only
the named example and one additional traceability row. Earlier rows and existing
protected bytes are still checked. No production validator or migration script
change is needed.

Existing documentation updates describe the relation and correct counts.
Only ASSESSMENT documentation/downloads and the landing-page count are regenerated
using the established WIDOCO workflow. Unchanged generation outputs are retained
without diffs. The diagram inventory count changes without regenerating images.
Traceability, manifest and SHA256SUMS follow the existing package contract.

## Validation and limitations

- Focused checks: **15 passed** in 44.33 seconds (14 point-2 tests and the
  existing active protected-input check).
- Full existing suite: **267 passed** in 222.83 seconds; 12 existing RDFLib
  JSON-LD deprecation warnings. This includes all committed point-1 coverage.
- `python -B scripts/validate_public.py --full --complete-report`: **PASS**;
  13 examples, 16 SHACL scenarios, six inference scenarios, RDFS negative
  control, traceability, public ADRs, 121 HTML link audits and package integrity.
- Existing export regressions cover 48 downloads across all twelve modules.
  A separate baseline comparison verifies each of the four ASSESSMENT RDF
  exports matches canonical source and has exactly nine additional triples.
- New tests run OWL-RL over both bounded runtime and runtime supplemented with
  unchanged full EVENT 1.0.0. They verify expected domain/range/inverse entailments,
  absent cross-classification/identity entailments and no OWL-RL clash reports.
  Observation-only data stays outside ProductEvent; deliberate carrier misuse
  demonstrates range classification rather than validation.
- Standalone ASSESSMENT has six catalogue-resolved documents; the full network
  remains twenty. Missing and two explicit event links pass existing SHACL.
- All other canonical ontology sources, dependencies, MIREOTs, migration files,
  SHACL, public validator, catalogue and version file are byte-checked against
  the point-1 commit. Original point-1 example, test, decision and report retain
  their bytes. All 799 published-baseline checksums verify directly against Git.
- ASSESSMENT documentation was regenerated with the established WIDOCO command.
  `git diff --check` and whitespace checks of all four new files pass.
- The final report and its checksum were completed after the full suite; a final
  structural public-validator run verifies the resulting package bytes.

Complete OWL DL consistency with HermiT and reporter-converter round trips are
not verified: no HermiT/ROBOT tool or reporter fixtures are available. OWL-RL,
SHACL and export checks do not establish complete OWL DL consistency. The example
is a link illustration, not a complete EPCIS payload or conformance certificate.
WIDOCO cannot retrieve the previous 2.0.0 ontology for its optional automatic
changelog; local source-based documentation/download generation completes.

## Exact changed-file inventory

Scope review: **25 files, comprising 21 modified and four added**, relative to
committed point 1. Each retained change below serves this correction or an
existing consistency/preservation contract. No unrelated change remains.

| File | Direct justification |
|---|---|

| `CHANGELOG.md` | Record the approved point-2 bridge and existing bounded import. |
| `PUBLICATION_MANIFEST.txt` | Include exactly the four new point-2 package files under the existing contract. |
| `README.md` | Correct example/resource counts and describe point-2 scope and carrier distinction. |
| `SHA256SUMS` | Refresh hashes for the exact final package; no checksum rules change. |
| `diagrams/DIAGRAM_INDEX.md` | Correct ASSESSMENT object-property count from 27 to 28; images are unchanged. |
| `docs/ISSUE20_POINT2_IMPLEMENTATION.md` | Provide the requested maintainer-review inventory, semantic delta, results and limits. |
| `docs/MODELLING_GUIDE.md` | Document the optional bridge and standalone import/carrier-mapping boundary. |
| `docs/PUBLICATION_SCOPE.md` | Replace the now-incomplete point-1-only scope statement. |
| `docs/decisions/TXT-DEC-012.md` | Supply the issue-specific sourceLocator and approved semantic decision without invented evidence. |
| `docs/widoco/assessment/ontology.jsonld` | Regenerated RDF download must match canonical ASSESSMENT; exactly nine added graph triples. |
| `docs/widoco/assessment/ontology.nt` | Regenerated RDF download must match canonical ASSESSMENT; exactly nine added graph triples. |
| `docs/widoco/assessment/ontology.owl` | Regenerated RDF download must match canonical ASSESSMENT; exactly nine added graph triples. |
| `docs/widoco/assessment/ontology.ttl` | Existing contract requires byte equality with canonical ASSESSMENT Turtle. |
| `docs/widoco/assessment/sections/crossref-en.html` | Generated definition/domain/range/import documentation reflects the new property. |
| `docs/widoco/assessment/sections/description-en.html` | Generated section remains byte-identical to the updated editorial source. |
| `docs/widoco/assessment/sections/overview-en.html` | Generated property index includes the new ASSESSMENT relation. |
| `docs/widoco/assessment/webvowl/data/ontology.json` | Generated ASSESSMENT graph view reflects the new property and dependency. |
| `docs/widoco/index.html` | Generated landing page corrects the ASSESSMENT property count. |
| `examples/example-13-assessment-product-event-v2.1.0-dev.ttl` | One minimal illustration of assessment, conceptual event and distinct EPCIS carrier roles. |
| `ontology/textile-assessment.ttl` | Only the approved property declaration/annotations and direct bounded EVENT import. |
| `tests/issue20_support.py` | Add only the exact later nine-triple delta to the existing test-only historical proof fixture. |
| `tests/test_issue20_point2.py` | Fourteen focused regressions covering exact delta, imports, preservation, entailments and optionality. |
| `tests/test_mat_alignment.py` | Preserve active protected-input checks while permitting only the named new example and exact traceability row. |
| `traceability/textile-resource-traceability.csv` | Add one derived modelling-abstraction row with zero external/JRC evidence; old rows preserved. |
| `widoco/sections/assessment/description-en.html` | Explain the bridge and carrier boundary in the existing ASSESSMENT editorial section. |

ASSESSMENT is the only changed canonical ontology file. No version-header,
network-entry, catalogue, production-validator, migration, SHACL or diagram-image
change was required, so none is included. Generated ASSESSMENT index/provenance
files whose bytes remained unchanged are also excluded from the diff. No generic
framework, archive, auxiliary checking script or carrier mapping was introduced.
Serialization ordering/blank-node labels account for large generated XML/JSON
text diffs; the RDF graph checks constrain their actual delta to the nine triples.

The pre-existing untracked `migration/PUBLICATION_PLAN_2.0.0.md` is untouched and
excluded from the package and this inventory. HEAD remains the committed point-1
baseline; the index is empty. Main and the point-1 branch have not been changed.

Recommendation: accept point 2 for maintainer review within the explicit OWL DL
and converter-validation limits above. No points 3-6 are implemented.
