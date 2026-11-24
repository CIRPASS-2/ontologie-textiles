# Issue 13: recycled-content declarations

Base: integration commit `455d8e363148043d365919ea5a2c3051bc2c283c`.
The JRC Preparatory Study (section 9.2.4, printed page 130, lines 3488-3509)
distinguishes retail-stage discarded unsold textiles from industrial production
waste. Section 9.2.5.4 and the JRC DPP study (section 7.3, footnote 45) explain
that ISO terminology uses different categories. Recycled-input origin and the
stage at which textile waste is generated remain separate dimensions.
`preConsumerRecycledContent` uses the JRC retail-stage meaning; all three
source IRIs and their SKOS memberships remain unchanged.

`hasRecycledContentDeclaration` has one OWL union domain containing
`dpp:Product` and `dpp:MaterialOfComposition`, retaining its original range.
No material-to-product subclass axiom is added. RDFS and OWL RL reasoning do
not infer that an ordinary material constituent is a product from this link.

A declaration's fraction, recycled mass and reference mass concern its subject
and follow the applicable methodology. `hasReferenceProductMassValue` retains its
original product mass definition and IRI. The new
`hasReferenceMaterialMassValue` denotes the reference mass of the material
constituent. It is a project modelling extension; the JRC source describes
product-level information and does not mandate this new property. Product mass
excludes trims where required by the applicable methodology.

Use one declaration per source and fraction. Example 18 uses two declarations
for a 0.4 kg polyester constituent: 0.08 kg pre-consumer (0.20) and 0.12 kg
post-consumer (0.30). Example 11 remains the unchanged product declaration with
verification. Automatic mapping to CORE is not justified without checking the
denominator, percentage convention, origin categories and value associations.

The SHACL profile requires one origin and one fraction; recycled mass and one
reference mass must be supplied together or both omitted. It rejects supplying
both reference properties, even for the same value node, and checks units,
positive reference mass, nonnegative recycled mass and ratio consistency. If
all linked subjects are typed exclusively as products, the product property is
required when masses are present; if exclusively as materials, the material
property is required. When a declaration has no linked subject, an untyped or
dual-typed subject, or mixed product and material subjects, the data does not
establish a unique reference kind. SHACL accepts either single reference
property in that case, so producers must identify the subject and basis. This
is an application-profile limitation, not an OWL disjointness assertion.

`verifiesRecycledContentDeclaration` remains available. Product assessment
properties and semantics are unchanged. A complete assessment directly targeting
a constituent is not provided; `assessesProduct` must not be used on an ordinary
constituent merely to imply such support.

## Refinement delta

Relative to the initial uncommitted issue 13 implementation: ontology RDF removes
2 triples and adds 10 (restored product reference comment, removed legacy scope
note, and nine triples for the new material property). Recyclability SHACL RDF
removes 15 and adds 24 triples; quantitative SHACL adds one target triple.
These counts include changed SPARQL strings and blank-node graph differences.
The new declaration shape retains source/fraction cardinality and the existing
mass and ratio checks, extends those checks to material reference mass, rejects
two reference properties and checks unambiguous subject type.

The cumulative production contract independently applies the issue 13 ontology
delta to the authorized Phase 4 graph and pins the reviewed recyclability shape
bytes. Quantitative shape expectations are extended by the single positive-mass
target. CORE, MIREOT, issue 12 composition and the frozen 2.0.0 package remain
protected.

## Refinement validation

- `tests/test_issue13_recycled_content.py`: 16 passed, including RDFS and OWL RL
  inference, product compatibility, wrong-property failures for both kinds of
  subject, dual typing, cardinality and mass consistency.
- `tests/test_public_package.py` plus seven focused Phase 4 graph/shape
  regressions: 38 passed.
- `python -B scripts/validate_public.py --full --complete-report`: passed;
  186 RDF files parsed, 19 conformant examples, 16 SHACL scenarios, six
  reasoning scenarios and the RDFS negative control passed.
- The cumulative contract passed with the unchanged frozen 2.0.0 package path
  supplied explicitly for this nested worktree: 13 canonical graphs, 799
  frozen checksums and 869 Phase 3 checksums verified. Git LFS and pytest
  temporary-directory access required execution outside the sandbox.
- Package manifest and SHA-256 records refreshed; `git diff --check` passed.
  WIDOCO could not download the prior development version to produce an
  automatic changelog; generated documentation and canonical RDF exports passed
  the public structural checks.
