# Phase 2B integration contract

The integration package identity is `integration-2026-11.1`. Textile ontology
version IRIs use the `/dev/integration-2026-11.1` suffix; their prior versions
are the corresponding 2.0.0 IRIs. These are local development identifiers, not
a public release decision. Seven MIREOT identities and source bytes are unchanged.

The exact source-pinned transition is defined in `phase2b_contract.py` and
verified against issue #12 commit `196fdf762eb75faec00b7627994e9c445efebcbf`.
Expected graphs are built from frozen 2.0.0, issue #9, issue #12, then approved
development headers. Actual complete graphs and RDF delta categories are checked.
The frozen sibling package `dpp-textiles-frozen-2.0.0` is verified against
the original 799 checksums and its own catalogue resolves a 20-graph closure
without network fallback. Do not mix historical and development catalogues.

The existing fraction shape remains unchanged. Its range-threshold scalar
presence exception is documented for separate quantitative-profile review.
No Common/Connector architecture change or later issue is applied here.

## Decision provenance and historical reconstruction

The development identity is a separately owner-approved Phase 2B decision.
The local transition contract and this uncommitted report express that decision;
neither is an immutable Git evidence record yet. The eventual Phase 2B commit
will provide stable implementation provenance. Issue #9's source commit does
not approve the development headers. The source issue #12 decision record is
preserved verbatim, including its original branch-specific development identity.

With the approved baseline Git objects available, run from the repository root:

```powershell
python -B -m migration.reconstruct_frozen_2_0_0 <new-destination>
```

Choose an absent destination; the tool refuses to overwrite it. It extracts the
800 manifest-listed baseline files directly from Git, checks the original 799
SHA-256 entries and exact inventory, then resolves the 20-document import closure
using only the frozen catalogue. It marks files read-only on Windows. Use a new
isolated destination for reproduction tests; do not overwrite the existing
`dpp-textiles-frozen-2.0.0` sibling. Missing Git objects or frozen inputs fail
closed. Public HTTP resolution is not checked.

## Exact Phase 2B worktree inventory

Git status at handoff; `M` denotes a modified tracked file and `??` a new file.

```text
 M CHANGELOG.md
 M PUBLICATION_MANIFEST.txt
 M README.md
 M SHA256SUMS
 M VERSION
 M catalog-v001.xml
 M docs/MODELLING_GUIDE.md
 M docs/PUBLICATION_SCOPE.md
 M docs/TEXTILE_IRI_RESOLVER_COORDINATION_2.0.0.md
 M docs/widoco/assessment/index-en.html
 M docs/widoco/assessment/ontology.jsonld
 M docs/widoco/assessment/ontology.nt
 M docs/widoco/assessment/ontology.owl
 M docs/widoco/assessment/ontology.ttl
 M docs/widoco/assessment/provenance/provenance-en.html
 M docs/widoco/assessment/provenance/provenance-en.ttl
 M docs/widoco/assessment/webvowl/data/ontology.json
 M docs/widoco/associated-materials/index-en.html
 M docs/widoco/associated-materials/ontology.jsonld
 M docs/widoco/associated-materials/ontology.nt
 M docs/widoco/associated-materials/ontology.owl
 M docs/widoco/associated-materials/ontology.ttl
 M docs/widoco/associated-materials/provenance/provenance-en.html
 M docs/widoco/associated-materials/provenance/provenance-en.ttl
 M docs/widoco/associated-materials/sections/crossref-en.html
 M docs/widoco/associated-materials/webvowl/data/ontology.json
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
 M docs/widoco/core/sections/crossref-en.html
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
 M migration/INTEGRATION_CONTRACT_PHASE1.md
 M migration/integration_contract.py
 M migration/issue9_annotations.py
 M migration/mat_alignment.py
 M migration/refresh_publication.py
 M ontology/textile-assessment.ttl
 M ontology/textile-associated-materials.ttl
 M ontology/textile-connector.ttl
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
 M scripts/validate_public.py
 M tests/test_integration_contract.py
 M tests/test_issue9_annotations.py
 M tests/test_migration_publication.py
 M tests/test_public_package.py
 M tests/test_version_identities.py
?? docs/ISSUE12_MATERIAL_COMPOSITION.md
?? migration/PHASE2B_IMPLEMENTATION.md
?? migration/phase2b_contract.py
?? migration/reconstruct_frozen_2_0_0.py
?? tests/test_issue12_composition.py
?? tests/test_phase2b_contract.py
```
