# Publication scope and preserved reference material

The current CIRPASS Textile Ontology community review candidate occupies the repository root package areas. Its entry point is [ontology/textile-ontology.ttl](../ontology/textile-ontology.ttl), with 13 current modules and six bounded MIREOT graphs. The base package label is 1.1.2; the SoC MIREOT retains its declared 1.1.3 identity. No semantic resource or RDF serialization was changed during root-level integration.

## Package integrity contract

`PUBLICATION_MANIFEST.txt` has two sections. `CURRENT_PACKAGE` lists the current package files, including the manifest itself and `SHA256SUMS`. `SHA256SUMS` covers exactly that section except itself. `PRESERVED_REFERENCE_MATERIAL` lists the three Graphwise files for discovery only: their content bytes are outside the 1.1.2 checksum contract. Changing the explanatory inventory changes the manifest hash, but reference-file content is not hashed by that contract.

The package owns `ontology/` except `ontology/graphwise-ontology/`, plus `mireot/`, `dependencies/`, `shacl/`, `examples/`, `docs/`, `diagrams/`, `scripts/`, `tests/`, `traceability/` and `LICENSES/`. Its root members are README.md, CHANGELOG.md, LICENSE.md, VERSION, catalog-v001.xml, requirements-validation.txt, PUBLICATION_MANIFEST.txt and SHA256SUMS. Unexpected files in owned areas fail manifest validation. Existing reference data, background data models, repository configuration and Git metadata are outside the package contract. The root README describes both bodies of work and is itself a current package documentation member; that does not include the reference models in the package.

## Earlier Graphwise ontology work

[Earlier Graphwise ontology work](../ontology/graphwise-ontology/README.md) is preserved for reference and project continuity. Its original technical README remains below a short introductory note. Both preserved TTL files retain their original bytes and IRIs. They are separate reference models and must not be loaded indiscriminately with the current JRC-grounded package.

The preserved `ontology.ttl` declares ontology IRI `https://w3id.org/eudpp/` and uses slash-based terms. No shared EU DPP IRI was found between that graph and the current 19-graph closure. The preserved SHACL graph has no shared named subjects, but references the following current terms:

- `https://w3id.org/eudpp/soc#ExactQuantitativeValue`
- `https://w3id.org/eudpp/soc#MaximumQuantitativeValue`
- `https://w3id.org/eudpp/soc#QuantitativeValue`
- `https://w3id.org/eudpp/soc#RangeQuantitativeValue`
- `https://w3id.org/eudpp/soc#Unit`
- `https://w3id.org/eudpp/soc#hasUnit`
- `https://w3id.org/eudpp/soc#lowerBound`
- `https://w3id.org/eudpp/soc#maximumValue`
- `https://w3id.org/eudpp/soc#numericValue`
- `https://w3id.org/eudpp/soc#upperBound`
- `https://w3id.org/eudpp/textile-core#FibreCompositionComponent`
- `https://w3id.org/eudpp/textile-core#TextileFibre`
- `https://w3id.org/eudpp/textile-core#TextileProduct`
- `https://w3id.org/eudpp/textile-core#hasFibreComponent`
- `https://w3id.org/eudpp/textile-core#hasFibreCompositionComponent`
- `https://w3id.org/eudpp/textile-core#hasFibreType`
- `https://w3id.org/eudpp/textile-core#jrcExclusionReason`

These shared references do not establish that the earlier shapes express the current package's constraints. The public catalogue must never target Graphwise files. The validator follows the current entry-point imports and requires exactly the approved Textile/MIREOT closure. It does not parse, import, apply shapes from, or content-scan the Graphwise preservation directory as package conformance. A separately reported RDF syntax check of the reference graphs is repository hygiene only.

The two earlier files `ontology/textile materials.ttl` and `ontology/textile product data.ttl` are removed from the current tree; their original versions remain in Git history. No archive copies are included.
