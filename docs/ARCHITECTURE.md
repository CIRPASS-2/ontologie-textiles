# Ontology architecture

The ontology is organised as a network of focused modules. Textile Core provides the central product hierarchy. Structure, Process, Durability, Assessment, Indicator and Context provide reusable domain layers. Associated Materials, Repairability, Recyclability and Textile Substances of Concern extend the core with specialised information. Connector contains patterns that are intentionally shared across modules.

The umbrella ontology `textile-ontology.ttl` is the recommended import for applications that require the complete network. Applications with a narrower scope may import individual modules and their declared dependencies.

## Modelling principles

- OWL classes represent entities, activities, information objects and measurable characteristics.
- SKOS is used for controlled value vocabularies.
- Quantitative observations use explicit value nodes, units and quantity kinds.
- Assessment methods, executions and results are represented separately.
- Substance identity is separated from product-specific presence and regulatory qualification.
- Product events are aligned with the EU DPP Event ontology through a MIREOT subset.

## Bounded CORE reuse retained for issue #9

Textile reuses original CORE IRIs; an extracted CORE subject is not a duplicate
Textile term. Bounded MIREOT graphs select CORE axioms and their associated
semantic commitments from identifiable local upstream snapshots. This limits
exposure to unrelated upstream axioms compared with importing entire modules,
while keeping the selected closure reproducible and resolvable offline through
`catalog-v001.xml`.

The approved architecture retains these extracts and their existing imports.
Selection does not guarantee full compatibility or isolate consumers that also
load other CORE axioms. It creates a maintenance responsibility: monitor upstream
evolution, compare the full candidate source, and assess changed commitments at
the actual Textile reuse boundary before adopting an update. See the
[dependency review workflow](governance/upstream-dependency-governance.md).

## October 2026 CORE boundary

The runtime has 20 graphs: 13 Textile modules and seven bounded subsets. SOC
owns substance identity, positive presence, criteria and instructions. CON owns
the selected product/presence/concentration relations. P_DPP owns quantitative
property, concentration/threshold anchors and carriers. SI supplies approved units.
Textile owns structured parts/material groups, scopes, threshold value roles,
evaluation, source references and free-text instructions. Generic chemicals and
process executions keep their existing independent types. No general IDENT,
COMP or LCA integration is added. See [migration guidance](CORE_2026_MIGRATION.md).
