# Issue #20 point 3 implementation for maintainer review

Branch: `fix/issue-20-point-3`, created from committed point 2 at
`97304854623b9bc669ba8778bfed2c57c1023e2a`. Changes are unstaged and uncommitted.
No points 4-6, staging, commit, push, merge, release or publication are included.

## Approved OWL and SHACL changes

ASSESSMENT declares exactly one new object property, hasParameterConcept, with
domain MeasurementParameterSetting and range skos:Concept. Eight triples declare
and annotate it, including sourceLocator TXT-DEC-013 and modellingAbstraction,
without JRC evidence. One existing ontology-header comment is clarified to avoid
claiming that all parameter settings use QuantitativeValue: the complete RDF
delta is nine additions and one removal, with only the comment replacement
outside the property declaration. There are no new classes, imports, hierarchies,
alignments, restrictions or code lists. Points 1 and 2 retain their axioms.

MeasurementParameterSettingShape alone changes its constraints: inclusive sh:or
requires at least one numerical or categorical value. Both type checks and the
existing quantitative maximum of one are unconditional, outside the alternatives.
Both forms and multiple codes are permitted; a setting with neither form fails. Existing
quantity, unit, quantity-kind and decimal-datatype shapes remain byte-identical.
The complete quantitative-profile RDF delta is 20 additions and seven removals
(after blank-node canonicalisation): the setting subgraph plus the one
version-IRI replacement. The numerical constraint message is updated. Missing-value diagnostics now use
OrConstraintComponent rather than hasParameterValue MinCountConstraintComponent.

The maintainer explicitly approved the proposed single-IRI correction: the
quantitative profile version IRI now ends in 2.1.0-dev instead of 2.0.0, matching
the established development version. No other profile metadata changes. Its
unversioned identity and all ontology version headers remain unchanged. The
catalogue replaces only the corresponding quantitative-profile version mapping:
the existing public validator rejects an unmapped version, and the old 2.0.0
version mapping must not resolve to changed development content.
The original 2.0.0 profile and package are preserved in immutable Git history.

## Scope and contract preservation

One illustrative protocol example supplies a numerical and a categorical setting
under an AssessmentCondition. Its synthetic Concept is not an authoritative code
list. The new test module distinguishes pre-inference typing checks from RDFS
range classification and covers non-bypassable quantitative constraints.

The existing exact-delta test helper includes the precise approved later changes.
Two older test files need narrow updates: the point-2 frozen-graph test must allow
only the later property/comment and exact shape/documentation changes; the active
protected-input check must allow that same exact shape delta, the pinned SHACL
README, the named example and the new derived resource row. It still verifies
all other protected inputs and every unrelated shape. No production validation
or migration infrastructure is changed. No test fixture expectations for the
existing sixteen SHACL scenarios are changed.

Existing documentation and counts are updated; ASSESSMENT downloads and affected
WIDOCO sections are regenerated through the established workflow. Only changed
outputs remain in the diff. No diagram images or generation code are changed.
Traceability, manifest and checksums follow the existing publication contract.

## Validation

- Final stable-tree full suite: **315 passed** in 284.65 seconds; 12 existing
  RDFLib JSON-LD deprecation warnings. This includes all point-1 and point-2
  regression coverage and 48 new point-3 cases.
- `python -B scripts/validate_public.py --full --complete-report`: **PASS**,
  including 14 examples, 16 SHACL scenarios, six inference scenarios, RDFS
  negative control, traceability, ADR links, 121 HTML link audits and integrity.
- Focused checks initially had 46 passes and five failures from one missing RDFS
  import in the test helper; that import was corrected and the five checks passed
  on rerun. The first full run used test modules loaded before the catalogue
  correction and had 312 passes/three catalogue-preservation failures. All four
  affected shape/catalogue/preservation checks passed after the exact mapping
  adjustment; the final full run above supersedes those intermediate results.
- Exact source checks confirm eight new property triples and one replaced header
  annotation, with no other ontology/import changes. Exact SHACL graph and byte
  checks constrain the edit to the named setting shape, SKOS prefix declaration
  and approved version IRI. Every other shape and all other profile metadata
  retain their original statements and bytes.
- The public validator initially rejected the new unmapped SHACL version. This
  demonstrated the need for the one catalogue-entry substitution; no validator
  code was changed. The old profile-version IRI is absent from the active
  catalogue and its replacement resolves to the correct existing shape file.
- Numerical-only, categorical-only, both forms and multiple concepts pass.
  Neither form and multiple numerical values fail. A valid concept cannot hide
  wrong numerical typing before inference, invalid numeric datatypes, missing
  numbers/units, multiple units or literal quantity-kind values. A valid number
  cannot hide wrong concept typing before inference or literal code targets.
- Both inference modes are tested explicitly. Range inference can make wrongly
  typed or untyped resource codes pass RDFS validation; literal targets fail in
  both modes. OWL-RL checks expected domain/range classifications, distinct roles
  and absence of clash reports on the representative valid data.
- All 48 existing module downloads pass canonical-export checks. Separate checks
  verify each ASSESSMENT export has the exact canonical graph and a net eight
  additional triples, including the header-comment replacement.
- All 799 original 2.0.0 package checksums verify directly against immutable Git
  content; the original checksum file is also retained. No archive is duplicated.
- The established WIDOCO generation completed. `git diff --check`, all four new
  files' whitespace checks and the final 29-path scope check pass.
- The review record and its checksum were completed after the full suite; final
  structural public validation checks the resulting exact package bytes.

## Remaining limits

RDFS can infer Concept typing from hasParameterConcept, masking untyped or
incorrectly typed resource targets that fail before inference. Literal targets
fail in both modes. Passing sh:class is not authoritative vocabulary-membership
verification; code-to-number agreement is not checked. These are documented
limits, not new rules or a generic value framework.

HermiT/ROBOT consistency checking and reporter-converter fixtures are unavailable.
OWL-RL and SHACL checks do not establish complete OWL DL consistency. WIDOCO's
optional historic automatic changelog cannot retrieve the prior 2.0.0 ontology;
local generation of documentation and canonical exports still completes.

## Exact changed-file inventory

The final review retains **29 files: 25 modified and four added** relative to
the committed point-2 baseline. Every retained path is justified below. No
unrelated source, feature, infrastructure or version-policy change remains.

| File | Direct justification |
|---|---|

| `CHANGELOG.md` | Record the approved coded-setting correction and explicitly approved profile identity correction. |
| `PUBLICATION_MANIFEST.txt` | Include exactly the four new point-3 files under the existing package contract. |
| `README.md` | Describe coded settings and update example/resource/module counts and cumulative issue scope. |
| `SHA256SUMS` | Maintain exact hashes for the final existing package contract. |
| `catalog-v001.xml` | Replace only the quantitative-profile version mapping, required by the existing validator and to avoid resolving 2.0.0 to changed development constraints. |
| `diagrams/DIAGRAM_INDEX.md` | Correct ASSESSMENT property count from 28 to 29; all diagram images remain unchanged. |
| `docs/ISSUE20_POINT3_IMPLEMENTATION.md` | Supply the requested review inventory, exact deltas, tests, preservation evidence and limits. |
| `docs/MODELLING_GUIDE.md` | Document categorical protocol values, distinct semantic roles, inclusive validation and the inference boundary. |
| `docs/PUBLICATION_SCOPE.md` | Replace the incomplete points-1-and-2-only development scope statement. |
| `docs/decisions/TXT-DEC-013.md` | Provide the new property sourceLocator and record approved shape/version semantics without JRC evidence. |
| `docs/widoco/assessment/ontology.jsonld` | Regenerated canonical-equivalent RDF export of the property and clarified header comment. |
| `docs/widoco/assessment/ontology.nt` | Regenerated canonical-equivalent RDF export of the property and clarified header comment. |
| `docs/widoco/assessment/ontology.owl` | Regenerated canonical-equivalent RDF export of the property and clarified header comment. |
| `docs/widoco/assessment/ontology.ttl` | Preserve the existing byte-equality contract with canonical ASSESSMENT Turtle. |
| `docs/widoco/assessment/sections/crossref-en.html` | Generated property/domain/range documentation reflects hasParameterConcept. |
| `docs/widoco/assessment/sections/description-en.html` | Preserve byte equality with the revised existing editorial source. |
| `docs/widoco/assessment/sections/overview-en.html` | Generated ASSESSMENT property index includes the one new relation. |
| `docs/widoco/assessment/webvowl/data/ontology.json` | Generated view reflects the new property; no modelling or renderer changes. |
| `docs/widoco/index.html` | Correct the generated ASSESSMENT property count. |
| `examples/example-14-parameter-values-v2.1.0-dev.ttl` | One focused synthetic protocol with numerical and categorical settings; no new ontology class or code list. |
| `ontology/textile-assessment.ttl` | Add exactly one annotated object property and clarify the directly affected quantitative-only header guidance. |
| `shacl/README.md` | Document inclusive presence, unchanged numeric checks, diagnostic changes, inference limits and approved version identity. |
| `shacl/textile-quantitative-shapes.ttl` | Modify only MeasurementParameterSettingShape plus its needed SKOS prefix and the approved single version-IRI replacement. |
| `tests/issue20_support.py` | Extend the existing test-only exact approved-delta fixture; preserve complete old graph proofs and unrelated shape constraints. |
| `tests/test_issue20_point2.py` | Allow only the exact separately approved point-3 source/profile/catalogue/documentation delta when checking frozen point-2 evidence. |
| `tests/test_issue20_point3.py` | 48 targeted regressions: exact deltas, preserved sources, no new restrictions, both inference modes, value forms and invalid-value non-bypass. |
| `tests/test_mat_alignment.py` | Keep checking active protected inputs, permitting only the exact approved profile/catalogue changes, pinned README, named example and traceability row. |
| `traceability/textile-resource-traceability.csv` | Add one derived modelling-abstraction row; earlier rows and all external evidence remain unchanged. |
| `widoco/sections/assessment/description-en.html` | Explain coded protocol values and their validation limits in the existing ASSESSMENT editorial section. |

Only ASSESSMENT changes among canonical ontology modules. EVENT, PROCESS,
CONNECTOR, CORE, MIREOTs, migration infrastructure, production validation code,
other SHACL profiles, existing fixture expectations, the catalogue's other
entries and the root version file are unchanged. No classes, code lists,
threshold-selection mechanisms, specimen rules, additional cardinalities,
exclusive value alternatives, generic frameworks or new checking tools exist.
Large generated XML/JSON diffs reflect serialization ordering and blank-node
identifiers; graph-equivalence checks bound their actual semantic delta.

The committed point-1/point-2 examples and decisions, point-1 regression module,
and both earlier implementation reports retain their bytes. The point-2 tests
are adapted only where their exact frozen-tree assertions would otherwise reject
the explicitly approved later delta. Existing behaviour checks still execute.

The pre-existing untracked `migration/PUBLICATION_PLAN_2.0.0.md` remains untouched
and excluded from the inventory/package. HEAD remains the specified point-2
commit; the index is empty. Neither the point-1/point-2 branches nor main changed.

Recommendation: accept point 3 for maintainer review within the explicit OWL DL
and reporter-converter limits above. No points 4-6 are implemented. No staging,
commit, push, merge, release or publication occurred.
