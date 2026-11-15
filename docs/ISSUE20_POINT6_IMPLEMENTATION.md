# Issue #20 point 6 implementation for maintainer review

Branch: `fix/issue-20-point-6`, based on committed point 5 at
`5a0e76a39b543ef09f52d915e6215bd98bc6ea8e`. Changes remain unstaged and uncommitted.

## Approved scope

Zero ontology-schema changes, including declarations, imports, hierarchies,
annotations and version metadata. All production SHACL files, catalogue,
dependencies, MIREOTs, migration infrastructure, generated ontology exports and
five earlier corrections are preserved. No new local temporal property,
alignment, event class, synchronization rule or runtime framework is introduced.

Example 17 uses an isolated namespace and explicitly types assessment executions
as prov:Activity. PROV start and completion timestamps are optional xsd:dateTime
values. A coarse associated dcterms:date uses xsd:date; it does not inherently mean
start or completion and does not generate a clock time or timezone. Results query
execution time through resultOfAssessment. EPCIS occurrence/recording and result
generation/validation remain independent notions. The complete approved policy
is in the modelling guide.

The optional supplied-value guard is test-only, scoped to AssessmentExecution.
It checks every supplied value without presence, count or chronology constraints.
The public validator does not select it. The ordinary tests use a small test-only
PROV axiom projection and remain offline. A separate focused check loads the
authoritative W3C graph into memory, verifies the projection and checks the full
graph with the Textile closure and reference EVENT source. Nothing is imported
or copied into production ontologies.

## Validation

Final validation on 2026-11-15:

- Complete suite: `python -B -m pytest -p no:cacheprovider --basetemp <temporary-directory> tests -q --tb=short`.
  **435 passed, 0 failed, 0 errors, 12 warnings in 570.95 seconds; exit 0.**
  The warnings are existing RDFLib JSON-LD ConjunctiveGraph deprecations.
  Temporary fixtures and the retained result log are outside the repository.
- Focused scope comprises 37 new point-6 cases and three existing checks: the
  exact protected-input inventory and both merged-example SHACL variants. Initial
  runs exposed test-only lexical/normalization and historical checkout-EOL
  assumptions. After correction, the 39 other focused checks passed, the isolated
  preservation rerun passed (102.37 seconds), and both final timestamp reasoning
  cases passed (12.64 seconds). The final complete suite confirms all 40 checks
  together, including all earlier point-1 through point-5 regressions.
- Fresh full public validator: `python -B scripts/validate_public.py --full --complete-report`.
  **PASS, exit 0:** 17 conformant examples, 16 SHACL scenarios, six reasoning
  scenarios and the RDFS negative control. The package has 825 files, 178 parsed
  RDF files and the unchanged 20-graph runtime closure. Traceability stays at
  904 resources, 946 evidence rows and six source documents.
- Authoritative in-memory PROV verification: **PASS** with the full W3C PROV-O
  graph (1,146 triples), the Textile runtime closure and the unchanged full EVENT
  reference source. All seven test-projection triples occur in the authoritative
  graph. OWL-RL inferred Activity from a supplied completion timestamp on a probe
  lacking explicit Activity typing; no unintended result, process-execution,
  ProductEvent or EPCISEvent typing or OWL-RL error messages occurred. Coarse dates
  and absent values did not generate timestamps; event, completion and recording
  times stayed separate. No result-generation time was inferred.

Authoritative source: [W3C PROV-O RDF](https://www.w3.org/ns/prov-o), retrieved on
2026-11-15. Retrieved serialization SHA256:
`7d203989f67b38bca572253942acc5a1bf24ce3ccfece16f072dcb4be2b79a96`.
The graph was held only in memory. Normal regressions use the verified seven-triple
projection without network access; they do not claim to reload all PROV axioms.

The first complete run reported 433 passes and two failures confined to new
lexical timestamp comparisons. OWL-RL changes RDFLib's datatype converters, so
parsing may retain Z or normalize it to +00:00 depending on earlier tests. Final
assertions retain the exact datatype, one value and the expected instant while
accepting equivalent UTC spellings. No semantic data or production constraints
were relaxed. The final complete run above supersedes that failure.

The test-only guard checks each supplied value, including incorrect resource
objects, datatype mismatches, malformed literals and date-only precision. It
rejects explicitly typed dateTimeStamp where dateTime is required. A small
lexical check requires an actual time component because RDFLib can otherwise
accept a date-only spelling typed as dateTime. Negative lexical tests preserve
the supplied spelling; a guard cannot recover evidence already erased by upstream
normalization. No chronology, presence or maximum-count rule is introduced.
Production SHACL validation does not select this guard, as a negative control
explicitly demonstrates.

Preservation and integrity checks confirm zero ontology/production-SHACL changes,
unchanged imports/catalogue/version identities, unchanged exports and traceability,
and the exact ten-file inventory below. All 799 published 2.0.0 checksum entries
verify against immutable Git objects. The three existing Graphwise reference
files are outside the byte-owned package and have pre-existing checkout EOL
differences; the new preservation test compares their full normalized text while
retaining strict byte comparison for owned sources/profiles/dependencies.

The final structural validator, package checksums, four ASSESSMENT RDF-export
comparisons, exact file inventory and whitespace checks verify the completed
report and refreshed checksums. The index remains empty. No production generator
or migration code changes were needed.

**Recommendation: ready for maintainer review**, with the limitations below.
All changes remain unstaged and uncommitted.

## Exact changed-file inventory

Ten files: seven modified and three new. No generated ontology export changes
are needed because the schema is unchanged. No traceability CSV row is added
because no ontology resource or source annotation is introduced.

| File | Justification |
|---|---|
| `CHANGELOG.md` | Record the approved documented temporal-reuse pattern. |
| `PUBLICATION_MANIFEST.txt` | Include the three new package files. |
| `README.md` | Expose point-6 guidance and update the public example count. |
| `SHA256SUMS` | Refresh the existing package-integrity records. |
| `docs/MODELLING_GUIDE.md` | Specify PROV reuse, coarse dates, EPCIS separation and validation limits. |
| `docs/PUBLICATION_SCOPE.md` | Identify point 6 as instance/documentation-only within the existing development scope. |
| `docs/ISSUE20_POINT6_IMPLEMENTATION.md` | Record scope, evidence, inventory and limitations for review. |
| `examples/example-17-assessment-times-v2.1.0-dev.ttl` | Demonstrate the six requested temporal situations without changing earlier examples. |
| `tests/test_issue20_point6.py` | Focused representation, datatype, inference, guard-scope and byte-preservation checks. |
| `tests/test_mat_alignment.py` | Permit only the named example-17 path in the existing exact inventory assertion; all existing assertions remain. |

## Remaining limits

Full OWL DL consistency and reporter-converter validation remain unavailable.
OWL-RL checks are not complete DL consistency proof. No actual source timestamp
or method correctness is verified by the synthetic example. Timezone-less values
do not determine a universal instant; date-only values supply still less precision.
Multiple values may require application reconciliation. The production validator
does not apply the test-only temporal guard, and explicitly typed dateTimeStamp
values are not interchangeable with dateTime in that guard.

The published 2.0.0 baseline remains preserved in Git. The pre-existing untracked
`migration/PUBLICATION_PLAN_2.0.0.md` is unchanged and excluded. No staging, commit,
push, merge, release or publication is part of this delivery.
