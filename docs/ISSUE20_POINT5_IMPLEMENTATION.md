# Issue #20 point 5 implementation for maintainer review

Branch: `fix/issue-20-point-5`, created from committed point 4 at
`77dfddbe8bc509a65fec0037617506dc34072d36`. Changes remain unstaged and uncommitted.
No point 6, push, merge, release or publication is included.

## Approved semantic delta

ASSESSMENT adds exactly eight triples declaring and annotating the independent
object property hasAssessmentOutcome. Its domain is AssessmentResult and its
range is skos:Concept. The definition identifies a controlled conclusion under
the applied method and context, and distinguishes aggregate recyclability
conclusions under a stated route from individual criterion outcomes. Its locator
is TXT-DEC-015 and sourceType is modellingAbstraction. No JRC attribution is added.
No other ontology statement, header metadata, import, hierarchy, inverse,
property alignment, cardinality, rule or version identity changes.

The production SHACL delta is zero additions and zero removals. Every SHACL
Turtle file remains byte-identical to the point-4 baseline. No suitable existing
development profile covers a general categorical assessment conclusion: the
quantitative profile's scope is quantitative roles and associated settings; the
optional assessed-aspect profile covers MeasurementResult subjects. The other
profiles retain their published 2.0.0 identities. The approved fallback is used:
the three-triple supplied-value guard exists only in focused tests, in memory.
No new profile or profile-version change is introduced.

## Example and semantic limits

The existing valid V06 route-specific fixture remains unchanged. Example 16
preserves all its triples under explicit instance-IRI renaming and adds one
distinct overall inconclusive conclusion
plus three application-defined SKOS concepts with method- and route-specific
overall definitions. Tests substitute positive/negative conclusions or omit the
overall link. Individual criterion outcomes stay unchanged in every variant.
These are synthetic representation examples, not checks of a real method's
decision correctness or regulatory or universally applicable classifications.
No ontology-owned concept class, scheme or code list is added.

The broad domain includes criterion results; it cannot enforce aggregate-only
use. Criterion-level concepts also pass a generic Concept type guard, but their
use as overall verdicts is semantically inappropriate and prohibited by the
documented convention. No automatic criterion-to-verdict inference is added.
Missing and multiple verdict links remain permitted. Absence does not imply
negative or inconclusive. RDFS can infer Concept typing from the range; neither
this inference nor sh:class proves vocabulary membership, aggregate scope,
coherent multiple conclusions or a method-specific decision's correctness.

The existing public validator does not select the test guard. A baseline pass
does not validate supplied outcome objects; tests explicitly demonstrate this
with a literal target that passes baseline SHACL but fails the test guard.

## Namespace correction and validation

The approved correction changes exactly one prefix line in example 16:

- Before: `https://example.org/textile-recyclability/`
- After: `https://example.org/textile-recyclability/issue20-point5/`

Only local example-instance IRIs change. All 45 example triples are preserved
under that explicit renaming, including the assessment, product, method, route,
aggregate result, seven criterion results and outcomes, overall verdict, and
three synthetic concepts. Ontology vocabulary IRIs, application-defined verdict
IRIs and literal definitions remain unchanged. Example 11 and the original V06
fixture remain byte-identical to the committed point-4 baseline.

The prior full run had 396 passes and two failures because examples 11 and 16
shared instance IRIs with different method/product/route values. Their union
violated existing maximum-one and route-consistency constraints. The correction
isolates example 16 without changing those constraints or the merge regression.

Only namespace-dependent expectations in `tests/test_issue20_point5.py` change:
`E` uses the new namespace, and `renamed_reference()` maps only V06 instance IRIs
in memory for the structural comparison and inference reference model. The
outcome-data variants and context assertions use the updated `E`. The criterion
comparison explicitly checks all seven criterion results, preventing a vacuous
comparison after renaming. The original fixture and vocabulary terms are not
rewritten. No existing regression assertion is disabled or weakened.

Final validation on 2026-11-15:

- Focused command: point-5 tests, both variants of
  `test_public_example_shacl_results_are_preserved`, and nine exact source,
  shape and frozen-input preservation checks for points 1?4.
  **45 passed in 132.48 seconds**, including all 34 point-5 tests and both
  previously failing variants (`default` and `complete-report`).
- Complete suite, with accessible temporary fixtures outside the repository:
  `python -B -m pytest -p no:cacheprovider --basetemp <temporary-directory> tests -q --tb=short`.
  **398 passed, 0 failed, 0 errors, 12 warnings in 448.81 seconds; exit 0.**
  The warnings are existing RDFLib JSON-LD ConjunctiveGraph deprecations.
- Fresh full public validator:
  `python -B scripts/validate_public.py --full --complete-report`.
  **PASS, exit 0:** 16 conformant examples, 16 SHACL scenarios, six reasoning
  scenarios and the RDFS negative control.

The public validator checks examples individually; the unchanged merged-example
regression separately verifies their union. The public validator does not select
the supplied-value guard: that guard is exercised only in focused tests and does
not establish vocabulary membership or method-specific decision correctness.

Checks confirm the exact eight-triple ontology addition with zero removals,
byte preservation of production SHACL and catalogue mappings, unchanged other
ontology modules, and four canonical-equivalent ASSESSMENT RDF exports. All 799
published 2.0.0 checksum entries verify against immutable release Git objects.
Points 1?4 remain ancestors of HEAD and their tests pass. The package retains
822 files and the implementation retains exactly 29 changed files. The
pre-existing untracked publication plan remains unchanged and excluded.

The report and checksums are updated through the existing package-file workflow.
Final structural validation, checksum/export/inventory checks and
`git diff --check` verify the completed tree. Relative to the approved recovery
state, only example 16, its point-5 test file, this report and SHA256SUMS change.
No source ontology, production SHACL, catalogue, migration script or prior
example is altered by this correction. All changes remain unstaged and
uncommitted, with an empty index.

**Maintainer recommendation: ready for maintainer review**, subject to the
remaining validation limitations below. The merged-example blocker is resolved;
no commit or publication is included.

## Remaining limits

Complete OWL DL consistency and reporter-converter fixtures are unavailable.
OWL-RL, RDFS and SHACL checks do not establish complete DL consistency or external
method conformity. The unchanged profiles deliberately provide no production
outcome-value guard. Shared code meanings and method-specific decision validity
remain application responsibilities.

The pre-existing untracked publication plan remains excluded and untouched.
Only approved point-5 changes are retained, with an empty Git index.

## Exact changed-file inventory

The retained scope is 29 files: 25 modified and four added relative to committed
point 4. Every path is required by the correction or an existing consistency
contract. No production SHACL Turtle file is changed.

| File | Direct justification |
|---|---|
| `CHANGELOG.md` | Record the optional conclusion relation and test-only validation fallback. |
| `PUBLICATION_MANIFEST.txt` | Include exactly the four new point-5 package files. |
| `README.md` | Describe conclusions and update scope, example and resource counts. |
| `SHA256SUMS` | Preserve the existing exact package-integrity contract. |
| `diagrams/DIAGRAM_INDEX.md` | Update the ASSESSMENT property inventory only; diagram images are unchanged. |
| `docs/ISSUE20_POINT5_IMPLEMENTATION.md` | Record requested deltas, inventory, validation evidence and limits. |
| `docs/MODELLING_GUIDE.md` | Document aggregate context, distinct vocabulary meanings and validation limits. |
| `docs/PUBLICATION_SCOPE.md` | Include point 5 in the development scope statement. |
| `docs/decisions/TXT-DEC-015.md` | Supply issue-specific rationale and the property's sourceLocator. |
| `docs/widoco/assessment/ontology.jsonld` | Regenerated canonical-equivalent ASSESSMENT RDF export. |
| `docs/widoco/assessment/ontology.nt` | Regenerated canonical-equivalent ASSESSMENT RDF export. |
| `docs/widoco/assessment/ontology.owl` | Regenerated canonical-equivalent ASSESSMENT RDF export. |
| `docs/widoco/assessment/ontology.ttl` | Preserve byte equality with the canonical ASSESSMENT source. |
| `docs/widoco/assessment/sections/crossref-en.html` | Generated property, domain and range documentation. |
| `docs/widoco/assessment/sections/description-en.html` | Preserve equality with the revised editorial source. |
| `docs/widoco/assessment/sections/overview-en.html` | Generated ASSESSMENT property index. |
| `docs/widoco/assessment/webvowl/data/ontology.json` | Generated view includes the one new relation. |
| `docs/widoco/index.html` | Update the generated ASSESSMENT property count. |
| `examples/example-16-assessment-outcomes-v2.1.0-dev.ttl` | One synthetic aggregate verdict, three application concepts and all V06 reference triples under the approved instance-IRI renaming. |
| `ontology/textile-assessment.ttl` | Add only the eight approved declaration/annotation triples. |
| `shacl/README.md` | Explain why production profiles remain unchanged and distinguish the test guard from baseline validation. |
| `tests/issue20_support.py` | Extend exact cumulative ontology expectations and pin only the appended SHACL guidance. |
| `tests/test_issue20_point2.py` | Permit the exact later property and documented guidance append in existing preservation checks. |
| `tests/test_issue20_point3.py` | Permit only the exact separately approved later property in the frozen graph check. |
| `tests/test_issue20_point4.py` | Permit only the exact later property in the frozen graph check; keep all point-4 shape checks unchanged. |
| `tests/test_issue20_point5.py` | Focused representation, vocabulary-limit, inference, context and preservation regressions. |
| `tests/test_mat_alignment.py` | Permit only the named example, fifth derived resource row and exact documentation extension. |
| `traceability/textile-resource-traceability.csv` | Add one derived modelling-abstraction row without external evidence. |
| `widoco/sections/assessment/description-en.html` | Update existing editorial documentation for the new conclusion relation. |

Earlier exact historical tests would otherwise reject the approved new property,
SHACL README digest, named example or derived resource row. Their changes admit
only this exact delta; no broad predicate filters, weaker fixture expectations or
protected-file exclusions are introduced. All earlier behavioural checks remain.
Only ASSESSMENT changes among ontology sources. All production SHACL constraints,
other modules, dependencies, MIREOTs, old examples, reference fixtures, decisions,
reports, catalogue, version metadata, scripts and migration sources retain bytes.

The established assessment-only WIDOCO workflow is used. Larger generated XML
and JSON diffs reflect serialization ordering and blank-node identifiers; the
four RDF exports are checked for equivalence with the canonical source. No
additional checking tools, generic framework, archive or version mechanism is
introduced. The untracked publication plan stays outside the package contract.
