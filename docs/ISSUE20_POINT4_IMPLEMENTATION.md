# Issue #20 point 4 implementation for maintainer review

Branch: `fix/issue-20-point-4`, created from committed point 3 at
`8a2bef637477a7fa9e77068dc8322d3d1e3ccff6`. Changes remain unstaged and uncommitted.
No points 5-6, push, merge, release or publication are included.

## Approved semantic delta

ASSESSMENT adds exactly eight triples declaring and annotating one independent
object property, awardedScoreValue, with domain AssessmentResult and range
QuantitativeValue. The definition distinguishes actual individual awards from
measurements, rule-prescribed points and aggregate indicator values. Its source
locator is TXT-DEC-014; sourceType is modellingAbstraction, with no JRC attribution.
No other ontology statement, header metadata, import, hierarchy or restriction
changes. Existing 2.1.0-dev identities and the published 2.0.0 baseline are retained.

The quantitative SHACL profile adds exactly ten triples for one
AwardedScoreValueShape and its two anonymous property constraints. Only supplied
award objects are targeted. They must be QuantitativeValues, satisfy the existing
QuantitativeValueShape, have an actual numericValue and contain units:one among
their units. The shared maximum-one-unit constraint rejects a second unit.
The scalar minimum excludes threshold-expression alternatives without changing
their existing shapes. Award links remain optional and may be multiple. No score
bounds, non-negativity, calculations or OWL cardinalities are added. All existing
shape statements, bytes and profile metadata are preserved.

## Evidence and repository contracts

One synthetic example shows a scored robustness measurement, a scored
recyclability criterion result and an unscored assessment result. It does not
claim a complete recyclability report or conformity to a scoring standard.
Focused tests distinguish measured, prescribed, awarded and indicator values;
check expected and forbidden classifications; and validate supplied awards with
and without RDFS inference. A range can infer value typing, so sh:class is not
proof of correct scoring. Literal or structurally malformed targets still fail.

Existing exact historical tests must recognize only this separately approved
additive delta. Test-only expectations are extended; production validators,
migration code, existing fixture outcomes and protected inputs are not changed.
Documentation counts, canonical-equivalent ASSESSMENT exports, the derived
resource table, manifest and checksums follow the existing package contracts.

## Validation

- Focused point-4 and earlier exact-delta checks: **52 passed** in 164.08 seconds,
  including all 49 new point-4 cases.
- Full public validator with `--full --complete-report`: **PASS**. All 15 examples,
  the unchanged 16 SHACL scenarios, six reasoning scenarios and RDFS negative
  control pass. Traceability has 903 resources, 946 unchanged evidence rows and
  six unchanged source documents. The 20-document closure, 176 parsed RDF files,
  14 ADRs, 121 HTML documents and 818-file package pass structural checks.
- The first full suite completed with 357 passes and seven setup errors, all
  caused by sandbox denial of pytest's temporary directory; no test assertion
  failed. A fresh temporary-directory retry hit the same sandbox restriction.
  With the required temporary-fixture filesystem access, all seven affected
  tests passed in 0.71 seconds without any repository change. The subsequent
  complete suite passed: **364 tests**, 12 existing RDFLib JSON-LD deprecation
  warnings, in 697.24 seconds. It used the unchanged suite with a fresh
  `--basetemp` directory and the filesystem access required by those fixtures.
  The temporary directories were cleaned up; no fixture or validator was changed.
- Exact graph checks: ASSESSMENT **+8 / -0**; quantitative SHACL **+10 / -0**.
  The shape file is the exact point-3 byte stream with one new block inserted.
  All four ASSESSMENT RDF exports are isomorphic to the canonical source.
- All 799 published 2.0.0 manifest entries verify against immutable Git content;
  its original manifest also remains preserved. All earlier branch tips and main
  retain their original commits. Existing examples, decisions, reports, fixture
  expectations, other ontology sources, historical snapshots, MIREOTs, catalogue,
  version metadata, scripts and migration infrastructure are unchanged.
- The established assessment-only WIDOCO workflow completed successfully. Its
  optional automatic historic changelog could not retrieve the prior 2.0.0 IRI;
  local documentation and canonical exports were still generated and verified.
- Exact 29-file inventory, changed-file whitespace, `git diff --check` and empty
  index checks pass. JSON serializers retain their baseline final-newline
  convention; no unrelated formatting normalization is introduced.

The final report and its checksum were completed after the full suite. The
final structural public validator passes against those exact final package bytes.
The complete-suite command was `python -B -m pytest -p no:cacheprovider
--basetemp <fresh-temporary-directory> tests -q --tb=short`; the seven affected
temporary-file checks were also rerun separately before it. No source or test
changes were needed for the temporary-directory issue.

## Remaining limits

OWL-RL and SHACL do not establish complete OWL DL consistency. HermiT/ROBOT are
not supplied by the local tooling directory; complete DL consistency remains a
validation gate. Reporter-converter fixtures are unavailable. Method-specific
award correctness, applied-rule identification and aggregation remain outside
this correction. No automatic derivation or additional scoring infrastructure
has been introduced.

The pre-existing untracked publication plan remains untouched and excluded from
the package. All changes are for maintainer review, with an empty Git index.

## Exact changed-file inventory

The retained scope is 29 files: 25 modified and four added relative to committed
point 3. Every path serves the correction or an existing consistency contract.

| File | Direct justification |
|---|---|
| `CHANGELOG.md` | Record the approved point-4 correction and its limits. |
| `PUBLICATION_MANIFEST.txt` | Include exactly the four new point-4 package files. |
| `README.md` | Document awarded points and update scope, example and resource counts. |
| `SHA256SUMS` | Keep the existing package checksum contract exact. |
| `diagrams/DIAGRAM_INDEX.md` | Update the ASSESSMENT property count only; diagram images remain unchanged. |
| `docs/ISSUE20_POINT4_IMPLEMENTATION.md` | Record requested scope, validation, preservation and limitations for review. |
| `docs/MODELLING_GUIDE.md` | Explain actual awards, distinct roles and targeted validation. |
| `docs/PUBLICATION_SCOPE.md` | Include point 4 in the development scope statement. |
| `docs/decisions/TXT-DEC-014.md` | Supply issue-specific rationale and the property's sourceLocator. |
| `docs/widoco/assessment/ontology.jsonld` | Regenerated canonical-equivalent ASSESSMENT export. |
| `docs/widoco/assessment/ontology.nt` | Regenerated canonical-equivalent ASSESSMENT export. |
| `docs/widoco/assessment/ontology.owl` | Regenerated canonical-equivalent ASSESSMENT export. |
| `docs/widoco/assessment/ontology.ttl` | Preserve exact byte equality with the canonical source. |
| `docs/widoco/assessment/sections/crossref-en.html` | Generated property and domain/range documentation. |
| `docs/widoco/assessment/sections/description-en.html` | Preserve equality with the updated editorial source. |
| `docs/widoco/assessment/sections/overview-en.html` | Generated property index includes awardedScoreValue. |
| `docs/widoco/assessment/webvowl/data/ontology.json` | Generated visualization includes the property. |
| `docs/widoco/index.html` | Update the generated ASSESSMENT property count. |
| `examples/example-15-awarded-points-v2.1.0-dev.ttl` | One synthetic example covers both scored result categories and an unscored result. |
| `ontology/textile-assessment.ttl` | Add only the eight approved declaration and annotation triples. |
| `shacl/README.md` | Describe dimensionless scalar award validation and inference limits. |
| `shacl/textile-quantitative-shapes.ttl` | Add only the ten triples for AwardedScoreValueShape and its constraints. |
| `tests/issue20_support.py` | Extend existing exact cumulative source/profile expectations and pin the appended SHACL guidance. |
| `tests/test_issue20_point2.py` | Permit only the approved later property and exact SHACL documentation append in frozen checks. |
| `tests/test_issue20_point3.py` | Permit only the exact later property and shape addition in frozen checks. |
| `tests/test_issue20_point4.py` | Focused positive, negative, inference, exact-delta and preservation regressions. |
| `tests/test_mat_alignment.py` | Permit only the named example, fourth derived resource row and exact shape/documentation extension. |
| `traceability/textile-resource-traceability.csv` | Add one derived row with no invented external evidence. |
| `widoco/sections/assessment/description-en.html` | Update existing ASSESSMENT editorial documentation. |

Without the narrowly bounded historical-test updates, their frozen graph, byte,
protected-file inventory, SHACL README digest and traceability-row assertions
would reject this explicitly approved correction. The full earlier contracts
remain checked; no broad exclusions or ignored predicates are introduced.

No unrelated generated outputs remain changed. XML/JSON serialization ordering
and blank-node identifiers account for larger generated diffs; all four RDF
exports are checked for canonical graph equivalence. No generic checking tools,
validator code, migration infrastructure, archive or version-management changes
are retained. Existing shape bytes are preserved by a single exact insertion.

## Recommendation

Point 4 is ready for maintainer review and acceptance within the explicit OWL DL
and reporter-converter limitations above. The full 364-test suite and full public
validator pass. The correction is restricted to the approved property and one
targeted dimensionless-value shape, with existing repository contracts preserved.
All 29 implementation files remain unstaged and uncommitted on the dedicated
branch at the committed point-3 baseline. Nothing is pushed, merged, released or
published; points 5 and 6 are not implemented.
