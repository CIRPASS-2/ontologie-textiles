# Phase 3 cumulative integration record

The unpublished package identity is `integration-2026-11.2`. Canonical Common
and the distinct complete Connector compatibility ontology retain the `txtcon`
term namespace and import the SI MIREOT. Common is a new ontology identity; it
records the old Connector as a migration predecessor rather than an OWL prior
version. Retained ontologies and Connector identify their `.1` predecessors.
The quantitative SHACL ontology identifies its own 2.0.0 predecessor.

Expected graphs are reconstructed from the frozen baseline, issue #9, issue #12
and source-pinned issue #16 transitions. The complete compatibility body contains
395 non-header triples, including 33 supporting triples and all 37 term IRIs.
The 2.0.0 and `.1` packages use independent offline catalogues. The `.1` package
can be reconstructed with `python -B -m scripts.reconstruct_phase2b` and a new
destination. Public HTTP resolver behavior is not verified.

## RDF transition relative to Phase 2B

Common is compared to the retired canonical Connector graph; compatibility is a
separate new representation, not an extra canonical import. Header counts include
version and identity metadata. The quantitative SHACL counts include its
version and prior-version metadata.

| Canonical graph | Header + / - | Annotation + / - | Import + / - |
|---|---:|---:|---:|
| assessment | 4 / 4 | 1 / 1 | 1 / 1 |
| associated-materials | 4 / 4 | 0 / 0 | 1 / 1 |
| context | 4 / 4 | 0 / 0 | 1 / 1 |
| core | 4 / 4 | 0 / 0 | 1 / 1 |
| durability | 4 / 4 | 0 / 0 | 1 / 1 |
| indicator | 4 / 4 | 0 / 0 | 1 / 1 |
| ontology | 3 / 3 | 0 / 0 | 1 / 1 |
| process | 4 / 4 | 0 / 0 | 1 / 1 |
| recyclability | 4 / 4 | 2 / 2 | 1 / 1 |
| repairability | 4 / 4 | 0 / 0 | 1 / 1 |
| soc | 4 / 4 | 0 / 0 | 1 / 1 |
| structure | 4 / 4 | 0 / 0 | 1 / 1 |
| common replacing connector | 32 / 32 | 37 / 37 | 1 / 1 |
| total | 79 / 79 | 40 / 40 | 13 / 13 |

No canonical domain logical axiom is added or removed by this transition.
The separately generated compatibility document contains 409 triples: the
395-triple Common payload and 14 Connector header triples. The quantitative
SHACL graph comparison has 36 additions and six removals.

The fraction `RangeThresholdValue` scalar-presence limitation remains deferred.
See [issue 16 integration guidance](../docs/ISSUE16_COMMON_MIGRATION.md).

## Audit corrections

Git attributes protect the new Common and compatibility RDF bytes. The
production contract independently enumerates all 14 Connector header triples.
WIDOCO generation presents Common's replacement relationship as a migration,
without asserting that the Connector version is a prior Common revision.
Historical decision records remain unchanged; current guidance identifies
Common as canonical and the complete Connector representation as compatibility.

## Exact Phase 3 worktree inventory

`M` denotes a modified tracked path, `D` a retired tracked path and `??` a new
path. This inventory describes the unstaged review candidate.

```text
 M .gitattributes
 M CHANGELOG.md
 M PUBLICATION_MANIFEST.txt
 M README.md
 M SHA256SUMS
 M VERSION
 M catalog-v001.xml
 M diagrams/DIAGRAM_INDEX.md
 M docs/ARCHITECTURE.md
 M docs/DEPENDENCIES.md
 M docs/MODELLING_GUIDE.md
 M docs/PUBLICATION_SCOPE.md
 M docs/widoco/assessment/index-en.html
 M docs/widoco/assessment/ontology.jsonld
 M docs/widoco/assessment/ontology.nt
 M docs/widoco/assessment/ontology.owl
 M docs/widoco/assessment/ontology.ttl
 M docs/widoco/assessment/provenance/provenance-en.html
 M docs/widoco/assessment/provenance/provenance-en.ttl
 M docs/widoco/assessment/sections/introduction-en.html
 M docs/widoco/assessment/webvowl/data/ontology.json
 M docs/widoco/associated-materials/index-en.html
 M docs/widoco/associated-materials/ontology.jsonld
 M docs/widoco/associated-materials/ontology.nt
 M docs/widoco/associated-materials/ontology.owl
 M docs/widoco/associated-materials/ontology.ttl
 M docs/widoco/associated-materials/provenance/provenance-en.html
 M docs/widoco/associated-materials/provenance/provenance-en.ttl
 M docs/widoco/associated-materials/webvowl/data/ontology.json
 M docs/widoco/connector/index-en.html
 M docs/widoco/connector/ontology.jsonld
 M docs/widoco/connector/ontology.nt
 M docs/widoco/connector/ontology.owl
 M docs/widoco/connector/ontology.ttl
 M docs/widoco/connector/provenance/provenance-en.html
 M docs/widoco/connector/provenance/provenance-en.ttl
 M docs/widoco/connector/sections/abstract-en.html
 M docs/widoco/connector/sections/crossref-en.html
 M docs/widoco/connector/sections/introduction-en.html
 M docs/widoco/connector/sections/overview-en.html
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
 M docs/widoco/indicator/sections/references-en.html
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
 M docs/widoco/recyclability/sections/crossref-en.html
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
 D ontology/textile-connector.ttl
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
 M scripts/generate-widoco-docs.ps1
 M scripts/generate-widoco-index.py
 M scripts/sync-widoco-rdf.py
 M scripts/validate_public.py
 M scripts/widoco_annotations.py
 M shacl/README.md
 M shacl/textile-quantitative-shapes.ttl
 M tests/abox_corpus/expectations/shacl-expectations.json
 M tests/test_core_migration.py
 M tests/test_creator_metadata.py
 M tests/test_issue9_annotations.py
 M tests/test_mat_alignment.py
 M tests/test_migration_publication.py
 M tests/test_phase2b_contract.py
 M tests/test_public_package.py
 M tests/test_version_identities.py
 M tests/test_widoco_links.py
 M traceability/textile-resource-traceability.csv
 M widoco/sections/assessment/introduction-en.html
 M widoco/sections/connector/abstract-en.html
 M widoco/sections/connector/introduction-en.html
 M widoco/sections/indicator/references-en.html
?? compat/textile-connector.ttl
?? docs/ISSUE16_COMMON_MIGRATION.md
?? docs/widoco/common/index-en.html
?? docs/widoco/common/ontology.jsonld
?? docs/widoco/common/ontology.nt
?? docs/widoco/common/ontology.owl
?? docs/widoco/common/ontology.ttl
?? docs/widoco/common/provenance/provenance-en.html
?? docs/widoco/common/provenance/provenance-en.ttl
?? docs/widoco/common/readme.md
?? docs/widoco/common/resources/dark-mode-toggle.mjs
?? docs/widoco/common/resources/dark.css
?? docs/widoco/common/resources/extra.css
?? docs/widoco/common/resources/jquery.js
?? docs/widoco/common/resources/light.css
?? docs/widoco/common/resources/marked.min.js
?? docs/widoco/common/resources/moon.svg
?? docs/widoco/common/resources/owl.css
?? docs/widoco/common/resources/primer.css
?? docs/widoco/common/resources/rdf.icon
?? docs/widoco/common/resources/rec.css
?? docs/widoco/common/resources/slider.css
?? docs/widoco/common/resources/sun.svg
?? docs/widoco/common/sections/abstract-en.html
?? docs/widoco/common/sections/crossref-en.html
?? docs/widoco/common/sections/description-en.html
?? docs/widoco/common/sections/introduction-en.html
?? docs/widoco/common/sections/ns-en.html
?? docs/widoco/common/sections/overview-en.html
?? docs/widoco/common/sections/references-en.html
?? docs/widoco/common/webvowl/css/webvowl.app.css
?? docs/widoco/common/webvowl/css/webvowl.css
?? docs/widoco/common/webvowl/data/foaf.json
?? docs/widoco/common/webvowl/data/ontology.json
?? docs/widoco/common/webvowl/data/template.json
?? docs/widoco/common/webvowl/favicon.ico
?? docs/widoco/common/webvowl/index.html
?? docs/widoco/common/webvowl/js/d3.min.js
?? docs/widoco/common/webvowl/js/webvowl.app.js
?? docs/widoco/common/webvowl/js/webvowl.js
?? docs/widoco/common/webvowl/license.txt
?? migration/PHASE3_IMPLEMENTATION.md
?? migration/phase3_preflight.py
?? ontology/textile-common.ttl
?? scripts/fix_widoco_common_provenance.py
?? scripts/generate_common_connector.py
?? scripts/reconstruct_phase2b.py
?? tests/test_common_connector_generator.py
?? tests/test_issue16_common.py
?? tests/test_phase3_audit_corrections.py
?? tests/test_phase3_preflight.py
?? tests/test_reconstruct_phase2b.py
?? widoco/sections/common/abstract-en.html
?? widoco/sections/common/description-en.html
?? widoco/sections/common/introduction-en.html
?? widoco/sections/common/references-en.html
```
