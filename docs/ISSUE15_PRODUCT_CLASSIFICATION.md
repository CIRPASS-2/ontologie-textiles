# Issue 15: product classification and study context

The JRC-derived Textile apparel classification remains unchanged. It describes
textile product types; CN is a complementary commodity classification. Product
data may use the CORE P_DPP 2.2.0 `dpp:commodityCode` datatype property. The
bounded DPP MIREOT copies its complete source declaration. Its domain is
`dpp:Product`, its range is `xsd:string`, and its CORE comment references ESPR
Annex III(d). This is not a declaration that the field is mandatory in any
Textile SHACL profile. Commodity-code literals must be `xsd:string` values,
preserve leading zeroes, and must not be serialized as integer-typed literals.
`dpp:hasProductGroup` is not used to encode a CN code.

The classification of an individual product requires its relevant material,
construction, design and other characteristics and the applicable classification
rules. Do not infer a commodity code automatically from a JRC category. The
exchange context must identify the classification system and edition: the literal
alone records neither edition nor provenance. For mixed editions, dataset-level
metadata alone is insufficient; agree an assertion-level provenance mechanism.
A four-digit heading is not an eight-digit CN code.

To resolve a literal, use an agreed normalization that preserves leading zeroes,
then match the code to `skos:notation` in the selected official edition. Detect
missing or ambiguous matches and distinguish heading from full code. A CN concept
URI's numeric suffix is an identifier, not its commodity-code value. Successful
lookup does not establish correct customs classification. The repository's
`ref-data/EU-CN` is CN 2021 and must not be assumed valid for 2026. For a 2026
use case select CN 2026 as applicable, based on [Commission Implementing Regulation
(EU) 2025/1926](https://eur-lex.europa.eu/eli/reg_impl/2025/1926/oj) and the
[official CN 2026 catalogue](https://data.europa.eu/data/datasets/combined-nomenclature-2026?locale=en).
Edition selection remains explicit; CN 2026 is not a permanent global default.
No CN dataset is imported into the Textile closure.

## Traceability: JRC, candidate CN headings and PEFCR

The following headings are **candidates**, not verified formal SKOS mappings or
codes assigned to individual products. The CN 2026 descriptions are available
in the [CN 2026 list](https://www.statistik.at/fileadmin/pages/1135/WVZ_2026__CN2-_to_CN8-codes_with_description_EN.pdf).
The Textile definitions are adapted from [JRC Table 7](https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2025-12/Textile-Prep-Study_3rd-Milestone_20251212.pdf).
[PEFCR Apparel and Footwear v3.1](https://www.2bpolicy.eu/s/PEFCR_v31_final-20260916T141235Z-1-001.zip),
Table 5, supplies the product-category descriptions below. The download is
provided by [2B Policy](https://www.2bpolicy.eu/facilitation), which chairs the
project technical secretariat. The [European Commission announcement](https://environment.ec.europa.eu/news/new-eu-rules-measuring-environmental-impact-clothes-and-shoes-2025-06-25_en)
provides context. A [Carbonfact-hosted copy](https://www.carbonfact.com/hubfs/A%26FW_PEFCR_v3.1.pdf)
is also available; it is not a European Commission publication endpoint.

| Textile concept | Candidate CN headings | PEFCR category | Additional conditions and limitations |
| --- | --- | --- | --- |
| `txtcs:shirtOrBlouse` | 6105, 6106, 6205, 6206 | Shirts and blouses | Knit/crochet versus other construction, garment type, intended wearer and fibre; base layers may classify elsewhere. |
| `txtcs:jacketOrCoat` | 6101, 6102, 6103, 6104, 6201, 6202, 6203, 6204 | Jackets and coats | Outerwear versus suit jacket, construction, fibre and coating; special fabrics may lead elsewhere. |
| `txtcs:dressSkirtOrJumpsuit` | 6104, 6204 for dresses and skirts | Dresses, skirts and jumpsuits | The headings also contain other products; a jumpsuit needs further design and classification analysis. |
| `txtcs:hat` | 6504, 6505; potentially 6506 | Apparel accessories | Construction, material and use matter; headings include non-hats and other materials. |

The descriptions of candidate headings and PEFCR categories are source evidence;
their correspondence with a Textile category is a conditional hypothesis.
`skos:closeMatch`, `skos:broadMatch` and `skos:narrowMatch` require the actual
concept extents and direction to be justified. A future optional crosswalk may
be independently versioned and loaded separately, referencing official concept
URIs without importing the full taxonomy. No such RDF mappings are asserted now.

## Study scope and technology scenarios

Study-scope status and defaults describe the JRC Textile Preparatory Study;
they are not a legal DPP scope determination for an individual product or an
adopted ESPR delegated act. The hygiene and cleaning classes remain meaningful
product classes. BC, BAT and BNAT describe assessment or technology scenarios
from the JRC study; their presence in the domain ontology does not create a
mandatory DPP information requirement. Passport-profile separation is deferred
to issue 18. All technology concepts and assessment uses are retained.

## Compatibility and deferred decisions

No Textile classification, study-scope assertion, technology term, example or
SHACL requirement is removed. The CORE property domain entails `dpp:Product`
for a subject using it under RDFS/OWL reasoning; its range is `xsd:string`.
The property adds no inference of JRC category, CORE product group, CN concept,
code edition or code correctness. Choosing a crosswalk's edition, provenance,
individual mappings and governance remains a future owner decision.

## Validation and graph delta

Against integration base `a1d5de600c4f3a216ae7d277404f707e6d3c6715`,
Textile Core replaces four comment triples (four removed, four added); all
other canonical module graphs and all SHACL graphs are unchanged. The DPP
MIREOT adds exactly the seven upstream `commodityCode` triples. The cumulative
contract explicitly checks the new source-fidelity delta and continues to
protect other dependencies and graph changes.

The focused issue 15, source-extraction and issue 14 tests passed (18 tests).
Public validation passed all 20 examples, 16 SHACL scenarios, six reasoning
scenarios and its no-inference negative control. Structural validation parsed
187 RDF files. The cumulative contract passed its 13 canonical graphs,
799 frozen-package checksums and 869 Phase 3 checksums. WIDOCO generated the
Core documentation and equivalent RDF exports; its automated changelog could
not retrieve the previous development ontology. Package integrity is checked
separately. The legacy issue 9 dependency-byte test has stale byte-identity expectations
for several approved changes introduced after issue 9; it is not limited to the
issue 10 LCA snapshot addition. The issue 9 documentation-regeneration test
also expects an older documentation state. Both failures were reproduced on the
untouched integration base. The cumulative production contract protects the
current approved state, including its dependency inventory. The historical canonical graph restoration and Phase 4
mutation controls passed (eight selected checks).
