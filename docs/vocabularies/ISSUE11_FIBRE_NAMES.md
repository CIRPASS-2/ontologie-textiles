# Issue #11: EU fibre names reference vocabulary

## Scope and provenance

The CIRPASS-2 Textile Ontology project maintains [this separate reference dataset](eu-annex-i-fibre-names.ttl); it is derived from legislation and is not an official European Commission vocabulary. The proposed namespace is `https://w3id.org/eudpp/textile-fibre-annex-i#`. Its source is the [English consolidated Regulation (EU) No 1007/2011 as at 15 February 2018](https://eur-lex.europa.eu/eli/reg/2011/1007/2018-02-15/eng), the current consolidated version listed by EUR-Lex at review. [Delegated Regulation (EU) 2018/122](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32018R0122) added entry 50, polyacrylate. The project must monitor amendments and review vocabulary changes under [SKOS governance](../governance/skos-vocabulary-governance.md).

The [coverage table](eu-annex-i-coverage.csv) records all 50 entry numbers and each separately represented name, with the source and resulting project IRI. Entry numbers are `dcterms:identifier` source references, not unique concept codes: 12 different concepts cite entry 2. The identifiers are proposed project identifiers and are not an official Commission nomenclature.

## Decisions

* Existing JRC fibre concepts, their classifications and `FIBRE_*` notations remain unchanged. The new reference scheme is not imported; consumers load its Turtle dataset explicitly with the relevant Textile ontology. There is no new ontology identity, catalogue route, OWL import or hierarchy.
* Entry 2 has one concept per listed animal-specific name. Its permitted suffix wording is recorded as a scope note, not as a false equivalence between species. Entry 3 is one general animal-or-horsehair concept with an open animal designation, not a fabricated exhaustive animal list.
* Entry 48 is a SKOS concept for the **open naming rule**, not a fibre-name individual; it is deliberately not typed `txt:FibreTypeConcept`. It does not validate an arbitrary material name.
* Flax/linen, abaca/Manila hemp and polyamide/nylon are represented as one concept apiece with English alternative labels because the annex presents each pair as alternate wording for the same described category. The coconut parenthesis in coir (coconut) is a source indication and is not made a separate legal name. The article 2 animal-specific names are distinct concepts, not lexical alternatives of a single hair concept.
* The other 60 concepts are typed `txt:FibreTypeConcept`, which is already a subclass of CORE `dpp:MaterialType`. Existing `txt:hasFibreType` keeps its domain and range; this type permits reuse but does not establish legal admissibility. No JRC concept is renamed or deprecated. No ontology axiom, import or SHACL restriction is added.
* No SKOS mapping assertions are published. The [T19 evidence inventory](ebiz-t19-mapping-evidence.csv) covers every source code, indicates possible JRC and Annex concepts where supported as candidates by available wording, and keeps the predicate undetermined. T19 does not supply stable per-code concept IRIs here, and its short descriptions generally repeat labels. `hair`, `cuprous`, animal names, and mismatched labels require substantive review. Mappings to external concepts require owner-controlled identifiers, definition-level evidence and separate review.

ISO 2076:2021 concerns man-made fibre generic names and ISO 6938:2012 concerns natural fibre generic names. Individual standard definitions and identifiable SKOS concepts were not available in the supplied sources; ISO mappings and codes remain unasserted pending authoritative access and rights review.

## Conformance and maintenance

Scheme membership is not proof that a product, its label or declaration complies with Regulation (EU) No 1007/2011. A future optional profile, separately approved, must define its scope, accepted identifiers, external mappings, conditions and exceptions; a finite list alone does not capture entry 48 or other legal rules. The generic composition model remains unchanged.

A future change must assess the legal source version, language variants, species-specific suffix wording, source-owned identifiers, semantic scope, and downstream consumers before adding mappings or importing this dataset. Adding or changing project-maintained concepts requires the existing governance review. Current `integration-2026-11.3` canonical ontology identities and the 20-document active import closure are preserved.
