# External dependencies and bounded reuse

Textile imports six local MIREOT subsets. Full upstream graphs in `dependencies/` are reference snapshots for inspection; they are not merged into the normal Textile runtime graph. Loading the full EVENT snapshot separately requires the bundled ACTOR and P_DPP snapshots, which the catalogue maps locally.

| Source file | Ontology IRI | Upstream version | Source triples | MIREOT file | MIREOT triples |
|---|---|---|---:|---|---:|
| `actor.owl` | https://w3id.org/eudpp/ACTOR | 2.0.0 | 371 | `actor-textile-mireot.ttl` | 21 |
| `p_dpp.owl` | https://w3id.org/eudpp/P_DPP | 2.0.0 | 436 | `dpp-textile-mireot.ttl` | 93 |
| `mat.owl` | https://w3id.org/eudpp/MAT | 1.0.2 | 101 | `mat-textile-mireot.ttl` | 19 |
| `event.ttl` | https://w3id.org/eudpp/EVENT | Version 0.1.0 DRAFT | 733 | `event-textile-mireot.ttl` | 53 |
| `soc.ttl` | https://w3id.org/eudpp/soc | Version 0.1.2 DRAFT | 1036 | `soc-textile-mireot.ttl` | 568 |

SI uses `mireot/si-textile-mireot.ttl` (59 triples). The full SI knowledge base is not bundled. See [SI provenance](../dependencies/SI_REFERENCE_POINT.md). The six subsets reproduce selected declarations and supporting axioms; their source namespaces remain external. SKOS terms are referenced through their public namespace with the local declarations needed by the model. Textile codelists are contained within the ontology modules.

The complete runtime closure is the 13 Textile graphs plus six MIREOT graphs. Inspect individual declarations and axioms to establish actual reuse; a term's presence in an upstream snapshot alone does not establish Textile use. QuantitativeValue uses explicit value nodes, units and quantity kinds. No automatic equivalence to an external quantity-value model is asserted by this documentation.

## Versions and catalogue

The SoC MIREOT declares 1.1.3; all other subsets declare 1.1.2. These are Textile subset versions, distinct from upstream source versions. Both the declared SoC 1.1.3 IRI and its legacy 1.1.2 catalogue alias resolve to the current subset. The legacy alias does not provide a historical snapshot. Source snapshots and MIREOT bytes are retained unchanged in this candidate.

## Ontology identity, term namespaces and adoption

An ontology IRI identifies a module; a term namespace forms its class/property
IRIs; a serialization prefix binding abbreviates those IRIs. The integrated
snapshots distinguish them as follows:

| Module | Ontology IRI | Own-term namespace |
| -- | -- | -- |
| ACTOR | `https://w3id.org/eudpp/ACTOR` | `https://w3id.org/eudpp#` |
| MAT | `https://w3id.org/eudpp/MAT` | `https://w3id.org/eudpp#` |
| EVENT | `https://w3id.org/eudpp/EVENT` | `https://w3id.org/eudpp#` |
| P_DPP | `https://w3id.org/eudpp/P_DPP` | `https://w3id.org/eudpp#` |
| SoC | `https://w3id.org/eudpp/soc` | `https://w3id.org/eudpp/soc#` |

For example, `soc:` is bound to `https://w3id.org/eudpp/soc#` in the SoC
snapshot. Renaming the prefix label consistently while retaining that namespace
IRI does not change RDF identifiers. Changing
`https://w3id.org/eudpp/soc#Substance` to
`https://w3id.org/eudpp#Substance` changes the RDF identifier itself and requires
an upstream namespace/migration decision.

Dependency snapshots are versioned integration inputs. New upstream drafts
must not automatically replace an integrated snapshot solely because they are
newer: adoption requires stability and the existing
[dependency compatibility/reuse review](governance/upstream-dependency-governance.md).

## Snapshot attribution and redistribution status

ACTOR and P_DPP embed Apache-2.0 licence references and a textual CC-BY-4.0 fallback statement. EVENT and SoC embed CC-BY-4.0 references. Their creator and source annotations are preserved in the supplied files.

The MAT 1.0.2 snapshot is byte-identical to `mat.owl` in CIRPASS-2/ontologies-core at commit `d19942539c9683575485df1b3ab83fa88897f143`. That commit's [README](https://github.com/CIRPASS-2/ontologies-core/blob/d19942539c9683575485df1b3ab83fa88897f143/README.md) applies Apache 2.0 to the project; its [committed licence](https://github.com/CIRPASS-2/ontologies-core/blob/d19942539c9683575485df1b3ab83fa88897f143/LICENSE.md) is supplied in [LICENSES/Apache-2.0.txt](../LICENSES/Apache-2.0.txt). No NOTICE file occurs in the inspected source tree. Source creator: Tarmo Robal. Repository attribution: Copyright 2024-2027 CIRPASS-2. The source snapshot retains its original annotations and bytes.

MAT snapshot SHA-256: `2f7cb590d275d909a9efc3d65d030db4cd4afcdebd89b7014c5393f4208cfb3e`.

**Modified/extracted material notice for `mireot/mat-textile-mireot.ttl`:** this file is a bounded extraction from MAT, with a Textile-specific ontology header; it is not the complete upstream work. Its 10 non-header triples occur exactly in the licensed snapshot. Applicable upstream attribution and Apache 2.0 terms are retained through this notice and the supplied licence. No RDF bytes were changed during repository integration. The full snapshot and the bounded extraction were assessed separately.

SI provenance is preserved in its reference-point document; no full SI distribution has been added.

The Textile licence does not supersede upstream terms. No unrelated CORE modules or source publications are included. Candidate preparation and technical validation are not authorization to distribute third-party files.
