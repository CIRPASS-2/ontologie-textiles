# Phase 4 cumulative integration record

The unpublished integration identity is `integration-2026-11.3`. Common is
canonical; Connector remains the separate complete compatibility representation.
The optional assessed-aspect SHACL document retains its source shape IRI and
has no ontology or version declaration, as explicitly selected by the owner.
It is not loaded by the default public validator.

The five issue #20 properties and their logical boundaries are source-pinned;
the three temporal discovery annotations are a separately approved refinement.
The prior `.2` state is reconstructible using `scripts/reconstruct_phase3.py`.

## Source-record provenance

The unmodified issue #20 decision and implementation records describe their
original issue-specific `2.1.0-dev` development state. The cumulative package
uses the distinct internal identity `integration-2026-11.3`.

The original point-six decision introduced no ontology-schema changes. The
AssessmentExecution temporal comment and two `rdfs:seeAlso` discovery links
were added in the later source commit and separately approved for integration.
They add no temporal property, PROV import, inference rule or production
validation requirement. Execution timestamps, result generation, and EPCIS
occurrence and recording times remain distinct.

The source changelog records the five approved Assessment interoperability
properties and the optional temporal reuse guidance. Their source decisions,
examples and limits remain preserved byte-for-byte rather than rewritten as
if they had originally described the cumulative identity.

## RDF graph changes relative to Phase 3

Counts are complete graph differences including version headers and anonymous
structures, computed by graph isomorphism. The quantitative graph changes by
31 additions and 8 removals.

| Module | Additions | Removals |
|---|---:|---:|
| ontology/textile-assessment.ttl | 60 | 6 |
| ontology/textile-associated-materials.ttl | 4 | 4 |
| ontology/textile-common.ttl | 4 | 3 |
| ontology/textile-context.ttl | 4 | 4 |
| ontology/textile-core.ttl | 4 | 4 |
| ontology/textile-durability.ttl | 4 | 4 |
| ontology/textile-indicator.ttl | 4 | 4 |
| ontology/textile-ontology.ttl | 3 | 3 |
| ontology/textile-process.ttl | 4 | 4 |
| ontology/textile-recyclability.ttl | 4 | 4 |
| ontology/textile-repairability.ttl | 4 | 4 |
| ontology/textile-soc.ttl | 4 | 4 |
| ontology/textile-structure.ttl | 4 | 4 |

The RangeThresholdValue scalar-presence limitation remains deferred. Converter
round-trip fixtures were not supplied. The independent audit reported 204 source
issue #20 cases: 190 passed and 14 assumed source-branch package identities.
Those historical assumptions do not authorize changing the `.3` identity;
cumulative version, shape and behavioral checks exercise the corresponding
integration behavior separately.

## Worktree inventory

```text
 M CHANGELOG.md
 M PUBLICATION_MANIFEST.txt
 M README.md
 M SHA256SUMS
 M VERSION
 M catalog-v001.xml
 M compat/textile-connector.ttl
 M docs/MODELLING_GUIDE.md
 M docs/SOURCE_TRACEABILITY.md
 M docs/widoco/assessment/index-en.html
 M docs/widoco/assessment/ontology.jsonld
 M docs/widoco/assessment/ontology.nt
 M docs/widoco/assessment/ontology.owl
 M docs/widoco/assessment/ontology.ttl
 M docs/widoco/assessment/provenance/provenance-en.html
 M docs/widoco/assessment/provenance/provenance-en.ttl
 M docs/widoco/assessment/sections/crossref-en.html
 M docs/widoco/assessment/sections/description-en.html
 M docs/widoco/assessment/sections/overview-en.html
 M docs/widoco/assessment/webvowl/data/ontology.json
 M docs/widoco/associated-materials/index-en.html
 M docs/widoco/associated-materials/ontology.jsonld
 M docs/widoco/associated-materials/ontology.nt
 M docs/widoco/associated-materials/ontology.owl
 M docs/widoco/associated-materials/ontology.ttl
 M docs/widoco/associated-materials/provenance/provenance-en.html
 M docs/widoco/associated-materials/provenance/provenance-en.ttl
 M docs/widoco/associated-materials/webvowl/data/ontology.json
 M docs/widoco/common/index-en.html
 M docs/widoco/common/ontology.jsonld
 M docs/widoco/common/ontology.nt
 M docs/widoco/common/ontology.owl
 M docs/widoco/common/ontology.ttl
 M docs/widoco/common/provenance/provenance-en.html
 M docs/widoco/common/provenance/provenance-en.ttl
 M docs/widoco/common/webvowl/data/ontology.json
 M docs/widoco/connector/index-en.html
 M docs/widoco/connector/ontology.jsonld
 M docs/widoco/connector/ontology.nt
 M docs/widoco/connector/ontology.owl
 M docs/widoco/connector/ontology.ttl
 M docs/widoco/connector/provenance/provenance-en.html
 M docs/widoco/connector/provenance/provenance-en.ttl
 M docs/widoco/connector/webvowl/data/ontology.json
 M docs/widoco/context/index-en.html
 M docs/widoco/context/ontology.jsonld
 M docs/widoco/context/ontology.nt
 M docs/widoco/context/ontology.owl
 M docs/widoco/context/ontology.ttl
 M docs/widoco/context/provenance/provenance-en.html
 M docs/widoco/context/provenance/provenance-en.ttl
 M docs/widoco/context/webvowl/data/ontology.json
 M docs/widoco/core/index-en.html
 M docs/widoco/core/ontology.jsonld
 M docs/widoco/core/ontology.nt
 M docs/widoco/core/ontology.owl
 M docs/widoco/core/ontology.ttl
 M docs/widoco/core/provenance/provenance-en.html
 M docs/widoco/core/provenance/provenance-en.ttl
 M docs/widoco/core/webvowl/data/ontology.json
 M docs/widoco/durability/index-en.html
 M docs/widoco/durability/ontology.jsonld
 M docs/widoco/durability/ontology.nt
 M docs/widoco/durability/ontology.owl
 M docs/widoco/durability/ontology.ttl
 M docs/widoco/durability/provenance/provenance-en.html
 M docs/widoco/durability/provenance/provenance-en.ttl
 M docs/widoco/durability/webvowl/data/ontology.json
 M docs/widoco/index.html
 M docs/widoco/indicator/index-en.html
 M docs/widoco/indicator/ontology.jsonld
 M docs/widoco/indicator/ontology.nt
 M docs/widoco/indicator/ontology.owl
 M docs/widoco/indicator/ontology.ttl
 M docs/widoco/indicator/provenance/provenance-en.html
 M docs/widoco/indicator/provenance/provenance-en.ttl
 M docs/widoco/indicator/webvowl/data/ontology.json
 M docs/widoco/process/index-en.html
 M docs/widoco/process/ontology.jsonld
 M docs/widoco/process/ontology.nt
 M docs/widoco/process/ontology.owl
 M docs/widoco/process/ontology.ttl
 M docs/widoco/process/provenance/provenance-en.html
 M docs/widoco/process/provenance/provenance-en.ttl
 M docs/widoco/process/webvowl/data/ontology.json
 M docs/widoco/recyclability/index-en.html
 M docs/widoco/recyclability/ontology.jsonld
 M docs/widoco/recyclability/ontology.nt
 M docs/widoco/recyclability/ontology.owl
 M docs/widoco/recyclability/ontology.ttl
 M docs/widoco/recyclability/provenance/provenance-en.html
 M docs/widoco/recyclability/provenance/provenance-en.ttl
 M docs/widoco/recyclability/webvowl/data/ontology.json
 M docs/widoco/repairability/index-en.html
 M docs/widoco/repairability/ontology.jsonld
 M docs/widoco/repairability/ontology.nt
 M docs/widoco/repairability/ontology.owl
 M docs/widoco/repairability/ontology.ttl
 M docs/widoco/repairability/provenance/provenance-en.html
 M docs/widoco/repairability/provenance/provenance-en.ttl
 M docs/widoco/repairability/webvowl/data/ontology.json
 M docs/widoco/soc/index-en.html
 M docs/widoco/soc/ontology.jsonld
 M docs/widoco/soc/ontology.nt
 M docs/widoco/soc/ontology.owl
 M docs/widoco/soc/ontology.ttl
 M docs/widoco/soc/provenance/provenance-en.html
 M docs/widoco/soc/provenance/provenance-en.ttl
 M docs/widoco/soc/webvowl/data/ontology.json
 M docs/widoco/structure/index-en.html
 M docs/widoco/structure/ontology.jsonld
 M docs/widoco/structure/ontology.nt
 M docs/widoco/structure/ontology.owl
 M docs/widoco/structure/ontology.ttl
 M docs/widoco/structure/provenance/provenance-en.html
 M docs/widoco/structure/provenance/provenance-en.ttl
 M docs/widoco/structure/webvowl/data/ontology.json
 M migration/integration_contract.py
 M migration/issue9_annotations.py
 M migration/mat_alignment.py
 M migration/refresh_publication.py
 M ontology/textile-assessment.ttl
 M ontology/textile-associated-materials.ttl
 M ontology/textile-common.ttl
 M ontology/textile-context.ttl
 M ontology/textile-core.ttl
 M ontology/textile-durability.ttl
 M ontology/textile-indicator.ttl
 M ontology/textile-ontology.ttl
 M ontology/textile-process.ttl
 M ontology/textile-recyclability.ttl
 M ontology/textile-repairability.ttl
 M ontology/textile-soc.ttl
 M ontology/textile-structure.ttl
 M scripts/fix_widoco_common_provenance.py
 M scripts/generate_common_connector.py
 M scripts/validate_public.py
 M shacl/README.md
 M shacl/textile-quantitative-shapes.ttl
 M tests/test_issue9_annotations.py
 M tests/test_migration_publication.py
 M tests/test_phase3_audit_corrections.py
 M tests/test_phase3_preflight.py
 M tests/test_public_package.py
 M tests/test_version_identities.py
 M traceability/textile-resource-traceability.csv
 M widoco/sections/assessment/description-en.html
?? docs/ISSUE20_POINT1_IMPLEMENTATION.md
?? docs/ISSUE20_POINT2_IMPLEMENTATION.md
?? docs/ISSUE20_POINT3_IMPLEMENTATION.md
?? docs/ISSUE20_POINT4_IMPLEMENTATION.md
?? docs/ISSUE20_POINT5_IMPLEMENTATION.md
?? docs/ISSUE20_POINT6_IMPLEMENTATION.md
?? docs/decisions/TXT-DEC-011.md
?? docs/decisions/TXT-DEC-012.md
?? docs/decisions/TXT-DEC-013.md
?? docs/decisions/TXT-DEC-014.md
?? docs/decisions/TXT-DEC-015.md
?? examples/example-12-assessed-aspects-v2.1.0-dev.ttl
?? examples/example-13-assessment-product-event-v2.1.0-dev.ttl
?? examples/example-14-parameter-values-v2.1.0-dev.ttl
?? examples/example-15-awarded-points-v2.1.0-dev.ttl
?? examples/example-16-assessment-outcomes-v2.1.0-dev.ttl
?? examples/example-17-assessment-times-v2.1.0-dev.ttl
?? migration/PHASE4_IMPLEMENTATION.md
?? migration/phase4_contract.py
?? scripts/reconstruct_phase3.py
?? shacl/profiles/textile-assessed-aspect-targets.ttl
?? tests/test_phase4_audit_mutations.py
?? tests/test_phase4_contract.py
```
