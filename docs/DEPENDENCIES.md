# Dependencies and bounded reuse

The active closure contains 13 Textile graphs and seven MIREOT graphs.
Full unchanged owner-designated sources in `dependencies/current-core/` are
reference snapshots; they are not imported as full ontologies. IDENT and COMP are outside this migration. LCA 3.1 is provided separately as
a reference snapshot; it is not part of the active closure or an extracted subset.

| Subset | Source file | Source ontology | Selected source triples |
|---|---|---|---:|
| SOC | `soc.owl` | `https://w3id.org/eudpp/SOC` | 371 |
| CON | `connector.owl` | `https://w3id.org/eudpp/CON` | 32 |
| DPP | `p_dpp.owl` | `https://w3id.org/eudpp/P_DPP` | 96 |
| EVENT | `event.owl` | `https://w3id.org/eudpp/EVENT` | 33 |
| ACTOR | `actor.owl` | `https://w3id.org/eudpp/ACTOR` | 15 |
| MAT | `mat.owl` | `https://w3id.org/eudpp/MAT` | 11 |

SI retains its approved 59-triple subset and 1.1.2 identity. See
[SI provenance](../dependencies/SI_REFERENCE_POINT.md). Six rebuilt subsets
have 2.0.0 candidate identities, distinct from upstream version numbers.
Exact subject selections are in [extraction scopes](../migration/extraction-scopes.json).
Tests compare their complete copied subgraphs, including anonymous axioms,
against the supplied sources. New Textile definitions are outside MIREOT.

## Snapshot identity and maintenance

An upstream module version, a local source snapshot and a local extraction
version identify different things. The source files above are the accepted local
snapshots; their byte identities are recorded in
[SHA256SUMS](../dependencies/current-core/SHA256SUMS). The local rebuilt MIREOT
version is 2.0.0 and is not an upstream CORE version. No upstream Git commit is
asserted here: the accepted evidence identifies supplied snapshot bytes and
embedded module metadata.

The full upstream candidate sources must be compared for evolution, including
changes outside the selected subjects that could affect them. Inference,
validation and exchange impact is assessed against actually reused terms and
axioms. Adoption and any re-extraction require a separate approved dependency
update; these issue #9 clarifications change neither source bytes nor extracts.
See [governance](governance/upstream-dependency-governance.md).

## Source attribution

Authoritative RDF and its embedded attribution/licence metadata are copied
without editing. The supplied [CORE licence](../dependencies/current-core/LICENSE.md)
and [README](../dependencies/current-core/README.md) accompany the sources.
The current sources declare ACTOR 2.2.0, MAT 1.1.0, EVENT 1.0.0,
P_DPP 2.2.0, SOC 2.2.0 and CON 2.4.0. Their digests are recorded in
`dependencies/current-core/SHA256SUMS`.

**Modified/extracted material notice:** each rebuilt MIREOT reproduces
only selected source subjects and supporting axioms and adds a Textile
ontology header. It is an extracted work, not the complete upstream module.
Upstream terms remain externally owned. The Textile licence does not
supersede upstream terms. The bundled Apache licence is retained.

The 42 adapted legacy definitions/comments originate in the historical
[SOC 0.1.2 DRAFT snapshot](../migration/historical/1.1.2/dependencies/soc.ttl),
created by Elio Hbeich, issued 2026-04-17, under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Textile changes the namespace, scope and CORE alignment. Exact source
resources and copied statements are recorded in
[the attribution inventory](../migration/legacy-soc-attribution.json).
This text comparison does not independently verify underlying JRC or legal references.

## Historical compatibility

The accepted older dependency snapshots and MIREOT bytes are preserved in
the [historical inventory](../migration/historical/inventory.json) and archive.
The extracted historical runtime and its own catalogue are under
`migration/historical/1.1.2/`. Historical version IRIs and lowercase `/soc`
are deliberately absent from the active catalogue. No equivalence or
redirect bridges the legacy `soc#` vocabulary to the migrated runtime.
See [migration guidance](CORE_2026_MIGRATION.md).

## Phase 3 Common and Connector

Canonical Common and the complete Connector compatibility representation both
use the approved unchanged SI MIREOT. CORE and all MIREOT snapshots remain
byte-protected; no unconditional quantitative CORE alignment is introduced.
The [integration record](ISSUE16_COMMON_MIGRATION.md) describes offline routing.

## CORE LCA reference (issue #10)

The owner supplied `lca.owl` as a download from the CIRPASS-2 CORE ontology
repository. Its declared ontology IRI is `https://w3id.org/eudpp/LCA` and
version IRI is `https://w3id.org/eudpp/LCA/3.1`. The supplied bytes have
SHA-256 `39a523d6ef6202a1247359a4cf4c151e4b0aee42046c1b5c3b6bcef7a2b3c71b`.
No upstream commit or independently verified download URL is asserted. Its
embedded licence is CC BY 4.0. The catalogue resolves both identifiers to
this snapshot for explicit offline use; catalogue mappings do not import it.
See [issue #10 reuse notes](ISSUE10_LCA_REUSE.md).

## CORE commodity code (issue #15)

The DPP extract additionally copies the complete seven-triple source declaration
for `dpp:commodityCode` from the unchanged P_DPP 2.2.0 snapshot. It retains its
original IRI, Product domain, string range and upstream annotations. See
[the classification implementation record](ISSUE15_PRODUCT_CLASSIFICATION.md).
