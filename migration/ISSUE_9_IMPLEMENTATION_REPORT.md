# Issue #9 implementation and audit corrections

This report records the issue #9 implementation against baseline
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b` and the subsequent independent
audit corrections. Its Git and validation observations describe the review
snapshot, not the state of any future commit or release.

## Approved decisions and corrections

The five original proposals retain bounded CORE reuse, clarify durability and
indicator/process interpretations, document the implemented SOC migration,
identify the selected source versions, and govern future dependency adoption.
The decision is recorded in [TXT-DEC-016](../docs/decisions/TXT-DEC-016.md).
The baseline and issue #12/#16 branches use identifiers through 010; PR #21's
branch uses 011-015. Identifier 016 was available in these inspected branches.

- M1: CON 2.4.0 defines `dpp:concernsProduct` with ProductEvent domain and
  Product range. The selected CON MIREOT excludes it, so it is absent from the
  20-graph Textile runtime. A hypothetical subproperty bridge with the relevant
  CORE axioms loaded would infer ProductEvent for the indicator or execution.
  No bridge is asserted.
- m1: README language describes the scope without depending on Git working state.
- m2: the local qualification applicability note now identifies CORE `dpp:DPP`
  correctly. Local domain/range and the absence of an OWL bridge are unchanged.
- m3: the first correction replaced four computed documents with frozen copies,
  suppressing dynamic updates. The second audit corrected this. The generator computes the original content and inserts issue #9 fragments at
  unique checked anchors in ARCHITECTURE, DEPENDENCIES, SOURCE_TRACEABILITY,
  governance and README. The README fragments also restore the existing
  creator paragraph omitted by the baseline generator. MODELLING_GUIDE is
  maintained directly: the generator verifies that its single issue #9
  section is present and writes the file back unchanged. Links in fragments
  resolve from their generated targets. Tests perturb the inputs and check
  regeneration and preservation of unrelated source content.
- m4: appearance means retention of observable characteristics, not preference
  or emotional attachment. The note identifies the project interpretation as
  informed by JRC rather than a verbatim JRC or regulatory definition; the
  general/intrinsic distinction and formal hierarchy remain intact.
- m5: the descriptions specify indicator domain Indicator and range Product;
  isIndicatorOf is its subproperty and has inverse hasIndicator; no inverse is
  asserted for indicator concernsProduct. Process
  domain is TextileProcessExecution, range TextileProduct, with
  hasProcessExecution as its inverse.
- m6: the alert threshold comment says SoC type (d) and retains its conditional
  account of operational and regulatory consequences.

## Exact RDF transition and protected inputs

The complete machine-readable before/after list is
[issue9-annotation-delta.json](issue9-annotation-delta.json). Against the
baseline, the 13 canonical graphs have exactly 14 annotation additions and 14
removals (14 replacements), comprising five comments, three definitions and
six modelling notes. Whole-graph isomorphism after applying the exact allowlist
establishes zero other changes, including logical axioms, version metadata,
declarations and imports. The checks do not globally exclude annotation predicates.
Historical attribution remains the original 42-resource, 70-statement evidence.
CORE snapshots, MIREOTs, catalogue, SHACL, examples and traceability are protected
by baseline byte comparisons. The 2.0.0 version identities remain unchanged.

The previous review snapshot recorded 240 passing tests before the independent
audit. That snapshot's counts and Git status are historical and do not describe
the revised audit correction. Current validation and exact file inventory are
reported in the validation snapshot below.

## Integration and boundaries

Issue #12 and #16 make independent changes and require integration checks against
their eventual merged content. PR #21 already occupies decision IDs 011-015;
016 avoids the observed collision but should be rechecked at integration.
No publication, deployment, push or merge is implied by this report.
WIDOCO generation can report unavailable historical changelog endpoints; this
does not substitute for checking external links or full OWL DL consistency.

## Second audit corrections

N1 restores computed dependency and traceability statistics and uses checked,
unique anchors to retain the approved issue #9 prose. README and modelling-guide
additions are also retained. The earlier frozen full-document source templates
have been removed. N2 repairs this report's corrupted identifiers and corrects
its account of the former generator regression. N3 explicitly states the inverse
of isIndicatorOf and the absence of an asserted inverse for concernsProduct,
without changing RDF axioms.


## Second audit validation snapshot

- Complete pytest: 243 passed, 12 RDFLib JSON-LD deprecation warnings, 472.57 s.
  It includes MAT alignment, historical attribution, mutation controls, WIDOCO
  graph equivalence, dynamic documentation and local-link checks.
- Normal documentation generation ran twice in a temporary copy. Every sandbox
  file was byte-idempotent, and the six affected documents and traceability CSVs
  matched the review worktree. All 63 local links in those documents resolved.
- Controlled test inputs changed the SOC copied-triple count from 371 to 388,
  derived resource count from 899 to 900 and evidence count from 946 to 947.
  The corresponding generated values changed while issue #9 and independently
  maintained content remained present.
- Public structural, full and complete-report profiles passed. Each runtime
  profile checked 11 examples, 16 SHACL scenarios, six reasoning scenarios
  and an RDFS negative control.
- Exact 13-graph comparison passed with 14 approved annotation additions and
  14 removals, zero logical and zero ontology metadata changes.
- WIDOCO link check passed with zero errors; 5,405 external references were not
  checked. The two affected descriptions were synchronized directly.
- Git diff whitespace check passed. Manifest and checksum validation covers
  805 and 804 files respectively, with SHA256SUMS excluding itself.

The older generator still reconstructs unrelated CHANGELOG.md, governance
nader-review.md and diagrams/DIAGRAM_INDEX.md from historical sources that omit
later maintained content. Changing those unrelated generation behaviors is
outside this correction. For this reason normal generation was verified in a
temporary copy rather than allowed to overwrite those working-tree files. A
separately scoped repair is needed before unrestricted worktree generation.

At this review snapshot HEAD was the baseline, the index was empty, and the
following entries were unstaged or untracked:

```text
 M PUBLICATION_MANIFEST.txt
 M README.md
 M SHA256SUMS
 M docs/ARCHITECTURE.md
 M docs/DEPENDENCIES.md
 M docs/MODELLING_GUIDE.md
 M docs/SOURCE_TRACEABILITY.md
 M docs/decisions/TXT-DEC-010.md
 M docs/governance/upstream-dependency-governance.md
 M docs/widoco/durability/ontology.jsonld
 M docs/widoco/durability/ontology.nt
 M docs/widoco/durability/ontology.owl
 M docs/widoco/durability/ontology.ttl
 M docs/widoco/durability/sections/crossref-en.html
 M docs/widoco/durability/sections/description-en.html
 M docs/widoco/durability/webvowl/data/ontology.json
 M docs/widoco/indicator/sections/description-en.html
 M docs/widoco/process/sections/description-en.html
 M docs/widoco/soc/ontology.jsonld
 M docs/widoco/soc/ontology.nt
 M docs/widoco/soc/ontology.owl
 M docs/widoco/soc/ontology.ttl
 M docs/widoco/soc/sections/crossref-en.html
 M docs/widoco/soc/webvowl/data/ontology.json
 M migration/mat_alignment.py
 M migration/refresh_publication.py
 M ontology/textile-durability.ttl
 M ontology/textile-soc.ttl
 M tests/test_audit_corrections.py
 M widoco/sections/durability/description-en.html
 M widoco/sections/indicator/description-en.html
 M widoco/sections/process/description-en.html
?? docs/decisions/TXT-DEC-016.md
?? migration/ISSUE_9_IMPLEMENTATION_REPORT.md
?? migration/issue9-annotation-delta.json
?? migration/issue9_annotations.py
?? tests/test_issue9_annotations.py
```
