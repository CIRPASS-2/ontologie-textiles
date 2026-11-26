# Phase 1 cumulative validation contract

> Historical Phase 1 record. The active cumulative contract is described in
> [Phase 2B](PHASE2B_IMPLEMENTATION.md); the Phase 1 text below records its
> original scope and is retained for traceability.

Run `python -B -m migration.integration_contract`. The production entry
point accepts only the exact approved issue #9 annotation transition. It
constructs expected graphs from the frozen 2.0.0 Git objects and the committed
issue #9 delta, then compares the complete current graphs by RDF isomorphism.
It checks the frozen ontology paths against an independently specified
13-document inventory and requires the active inventory to match. Future
document additions, removals and replacements need explicit authorization and
a revised inventory contract.

The Turtle parser preserves the RDF lexical forms of typed literals for
baseline, evidence and candidate data. It uses a local parser and sink rather
than changing RDFLib's process-global normalization setting, so unrelated
concurrent RDFLib parsing is unaffected. The implementation is tied to the
pinned RDFLib parser APIs and has regression tests for typed dates, integer,
decimal, double and token lexical forms, including shorthand numeric tokens.
Python optimization is rejected before the existing assertion-based historical
proofs run.

The two transition IDs, graph mappings, source commit, issue number and exact
decision and implementation references are checked. The referenced documents
must exist in the approved source commit. Those checks establish technical
attribution and reproducibility; document presence and Git history do not in
themselves confer owner approval. The approved issue #9 delta evidence is
byte-pinned to that commit.

The entry point also invokes the existing strict MAT protected-file inventory
and byte proof, and checks VERSION and historical SoC attribution against the
frozen 2.0.0 commit. Existing issue #9, dependency, SHACL, catalogue and
historical proofs remain in force. No Phase 1 ontology, catalogue, SHACL or
version changes are introduced.

The transition engine checks ordering, preconditions and exact repeated triples.
The snapshot and delta APIs are experimental preparation, not production
authorization: a before graph, after graph and their matching computed
differences do not independently prove approval. Before any future snapshot or
logical transition is accepted, its source evidence and exact graph changes
must be independently reviewed and pinned; categories must be verified against
actual changed triples rather than trusted as labels.

Future overlap analysis must examine subject/predicate relationships as well
as identical triples, while allowing legitimate multi-valued RDF properties.
The present exact-triple overlap guard does not establish that broader property.
The production entry point must continue to reject future logical and
anonymous-graph transitions until these safeguards and their tests are in
place. Reconciliation metadata must identify all contributing decisions and
issues.

The reported zero logical, header, import, version and SHACL change counters
are Phase 1 results derived from its exact approved annotation contract; they
are not general-purpose measurements for arbitrary transition categories.
Future phases must implement independently verified category-specific counts,
reviewed source evidence, and explicit file/dependency/SHACL contracts. A
source branch or matching graph difference alone is not authorization.
