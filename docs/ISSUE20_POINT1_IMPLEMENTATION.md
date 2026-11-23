# Issue #20 point 1: simplified implementation for maintainer review

Branch: `fix/issue-20-point-1`. No commit, staging, merge, push or publication.
Only point 1 is implemented. The complete 2.0.0 baseline is preserved in Git at
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`; no duplicate archive is needed.

The approved resultForAssessedAspect declaration is unchanged. The only logical
extension is that property with its MeasurementResult domain and reviewed union
range. There are no hierarchy, disjointness, import or cardinality changes.
ASSESSMENT/network version headers and the active catalogue retain 2.1.0-dev
identities so published 2.0.0 identities do not denote changed content.

## Simplification

Removed the duplicate 20.7 MB archive and its inventory/README, issue-specific
production helper, Java/Python OWL checker pair, atomic-cardinality profile and
supplemental assessment diagrams. Restored migration/mat_alignment.py and the
diagram generator/network image pair byte-for-byte. The diagram inventory only
updates the assessment property count and identifies the retained baseline view.

One synthetic RDF example covers two independently identifiable results from
one execution, a degradation phenomenon, a structural characteristic and a
separate protocol setting. One optional target profile checks explicit targets;
missing and multiple links remain valid. No baseline shape is changed.

The public validator has only a local exact version assertion adjustment. Without
it the existing 2.0.0-only check rejects the two necessary development headers.
No runtime archive access, version-management abstraction or framework remains.

Earlier creator, version and MAT tests must account for the new property and
headers: otherwise their exact frozen-graph digests fail. The test-only fixture
checks the entire exact approved delta against the immutable Git baseline before
returning the original graph to those proofs. The active 76 protected inputs
remain checked, permitting only the two exact catalogue substitutions and the
single new traceability row and exact SHACL documentation append, plus the
explicitly named example/profile additions.
Migration scripts themselves are unchanged.

Documentation changes explain the new relation, optional validation and baseline
checkout. The existing WIDOCO workflow refreshes ASSESSMENT and the landing page;
manifest/checksums and the one-row traceability projection maintain the existing
publication contract. Unrelated ontology modules, CORE and MIREOT bytes are kept.

## Validation

- `python -B -m pytest -p no:cacheprovider tests -q`: **253 passed** in
  300.27 seconds; 12 existing RDFLib JSON-LD deprecation warnings.
- `python -B scripts/validate_public.py --full --complete-report`: **PASS**,
  including 12 examples, 16 SHACL scenarios, six inference scenarios, RDFS
  negative control, traceability, 121 HTML link audits and package integrity.
- Existing export tests verify all 48 downloads (12 modules, four formats)
  against their canonical graph; no declaration additions are persisted.
- All 65 other packaged ontology/dependency/MIREOT/historical files retain their
  baseline bytes. All 799 original package checksums verify directly against
  Git; the original checksum file is also present, preserving all 800 members.
- A read-only, in-memory mutation of an existing baseline shape is rejected by
  the active-file guard. No source fixture was modified for that check.
- WIDOCO ASSESSMENT regeneration using the established script completed; no
  generation infrastructure changes are retained. `git diff --check`: PASS.

The initial focused run had 63 passes and one failure because the required
SHACL README append had not been allowlisted. The guard now pins that exact
append while preserving the original text; the final full run above passes it.
Only the historical changelog encoding, this review record and integrity hashes
were finalized after that run; final structural validation verifies those bytes.

The earlier 253-test result describes the larger implementation, not this revision.
OWL DL consistency with HermiT remains unverified. Earlier OWLAPI merged-profile
results were structural checks only; their 290 declaration additions were transient
serialization artifacts, not persisted source additions or a consistency proof.
The removed diagnostic is not part of the simplified package. Reporter conversion
fixtures are unavailable, so their consumer round-trip compatibility is unverified.
WIDOCO cannot fetch the previous version IRI for its automatic changelog; local
source-derived documentation/export generation still completes.

## Final retained inventory

The table below lists every retained changed/added file and its point-1 purpose.

| File | Direct justification |
|---|---|
| `CHANGELOG.md` | Record the additive point-1 correction; preserve earlier entries. |
| `PUBLICATION_MANIFEST.txt` | List exactly the current package, including the six necessary additions. |
| `README.md` | Update version, example/resource counts, pattern link and baseline checkout instructions. |
| `SHA256SUMS` | Recompute existing integrity contract after retained changes. |
| `VERSION` | Identify the unpublished additive development version. |
| `catalog-v001.xml` | Replace only two changed version mappings; never map their old 2.0.0 IRIs to development content. |
| `diagrams/DIAGRAM_INDEX.md` | Correct ASSESSMENT property count; identify the unchanged illustrative baseline diagram. |
| `docs/ISSUE20_POINT1_IMPLEMENTATION.md` | Provide requested maintainer review inventory, results, simplification and limitations. |
| `docs/MODELLING_GUIDE.md` | Explain result subjects, individual targets, protocol separation and optional target validation. |
| `docs/PUBLICATION_SCOPE.md` | Describe the development boundary and original Git baseline. |
| `docs/decisions/TXT-DEC-011.md` | Provide the new property sourceLocator and approved decision record without JRC attribution. |
| `docs/widoco/assessment/index-en.html` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/assessment/ontology.jsonld` | Generated RDF download; existing regression contract requires graph equivalence to ASSESSMENT. |
| `docs/widoco/assessment/ontology.nt` | Generated RDF download; existing regression contract requires graph equivalence to ASSESSMENT. |
| `docs/widoco/assessment/ontology.owl` | Generated RDF download; existing regression contract requires graph equivalence to ASSESSMENT. |
| `docs/widoco/assessment/ontology.ttl` | Generated canonical Turtle download; exact bytes must match ASSESSMENT source. |
| `docs/widoco/assessment/provenance/provenance-en.html` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/assessment/provenance/provenance-en.ttl` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/assessment/sections/crossref-en.html` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/assessment/sections/description-en.html` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/assessment/sections/overview-en.html` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/assessment/webvowl/data/ontology.json` | Generated ASSESSMENT documentation/provenance/WebVOWL reflects the new property or version/editorial content. |
| `docs/widoco/index.html` | Generated landing-page ASSESSMENT version/property-count consistency. |
| `examples/example-12-assessed-aspects-v2.1.0-dev.ttl` | Demonstrate independent multi-result bindings, degradation, structure and separate protocol controls. |
| `ontology/textile-assessment.ttl` | Add only the approved property/annotations and updated version metadata. |
| `ontology/textile-ontology.ttl` | Advance entry-point metadata to identify the changed closure; imports are unchanged. |
| `scripts/validate_public.py` | Change only the exact version assertion for the two changed graphs; no checks removed. |
| `shacl/README.md` | Document selecting the optional target profile without changing baseline/cardinality contracts. |
| `shacl/profiles/textile-assessed-aspect-targets.ttl` | Validate explicit aspect targets only; neither require links nor constrain their number. |
| `tests/issue20_support.py` | Test-only exact graph fixture backed by the original Git commit; no runtime mechanism. |
| `tests/test_creator_metadata.py` | Preserve frozen creator proof after verifying the exact approved later delta. |
| `tests/test_issue20_point1.py` | Positive/negative binding, inference, optional-validation, version and traceability regressions. |
| `tests/test_mat_alignment.py` | Preserve exact old MAT proof and ACTIVE protected-file checks with narrowly pinned allowed changes. |
| `tests/test_version_identities.py` | Preserve historical header proof while checking the exact current version mappings. |
| `traceability/textile-resource-traceability.csv` | Add exactly one modelling-abstraction row with zero external/JRC evidence. |
| `widoco/sections/assessment/description-en.html` | Explain the new relation in the existing ASSESSMENT editorial source. |

## Removed or reverted files from the larger implementation

Removed additions (nine files):

- `migration/historical/2.0.0/published-package.zip`
- `migration/historical/2.0.0/inventory.json`
- `migration/historical/2.0.0/README.md`
- `scripts/issue20_point1.py`
- `scripts/CheckIssue20Profile.java`
- `scripts/check_issue20_owl.py`
- `shacl/profiles/textile-assessed-aspect-atomic.ttl`
- `diagrams/textile-assessment-result-subjects.png`
- `diagrams/textile-assessment-result-subjects.svg`

Restored unchanged from HEAD (four files):

- `migration/mat_alignment.py`
- `scripts/generate-migration-diagrams.ps1`
- `diagrams/textile-ontology-network-overview.png`
- `diagrams/textile-ontology-network-overview.svg`

This removes 13 paths from the original 48-file implementation and introduces
one test-only fixture, leaving **36 retained files: 30 modified and six added**.
All script/README/ADR references to removed tools, archive and cardinality profile
were removed. The pre-existing untracked `migration/PUBLICATION_PLAN_2.0.0.md`
was not modified and is excluded from this inventory and the package contract.

The retained validator/test adaptations cannot simply be reverted: the old
validator rejects the two development version IRIs; frozen creator/version/MAT
digest proofs reject the approved new property/headers; protected inventory and
byte checks reject the required example/profile additions, catalogue mappings,
traceability row and SHACL documentation. The changes permit only those exact
transitions and keep checking current data, rather than substituting an archive.

The implementation is ready for maintainer review of point 1 within the stated
validation limits. Full OWL DL consistency and unavailable consumer fixtures
remain explicitly unverified. No action concerning point 2 is included.
