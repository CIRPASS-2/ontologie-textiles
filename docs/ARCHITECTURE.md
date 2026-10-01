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
