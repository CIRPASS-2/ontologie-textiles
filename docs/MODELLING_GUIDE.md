# Modelling guide

## Products and composition

Use Textile Core classes for textile products and intermediate textile products. Represent structural subdivisions and composition through Textile Structure and Associated Materials rather than by introducing ad-hoc product subclasses.

## Processes and events

Use Textile Process for process types and executions. Use the event-aligned classes when an occurrence changes the state or lifecycle status of a product. A process description and a product event may describe different aspects of the same occurrence.

## Assessments and indicators

An assessment method specifies how a characteristic is evaluated. An assessment execution applies the method under stated conditions. The result records the observed or calculated outcome. Indicators interpret or aggregate such results for a defined purpose and context.

## Quantitative values

Use explicit quantitative-value nodes. Record the numerical value, unit and quantity kind when applicable. Do not encode a measurement and its unit as an unstructured string.

Use `txtcon:QuantitativeValue` with `txtcon:numericValue`, `txtcon:hasMeasurementUnit` and, where applicable, `txtcon:hasQuantityKind`. The related SI declarations are supplied in `mireot/si-textile-mireot.ttl`. Reference-period relationships are distinct from the measured numeric value. See [the composition example](../examples/example-01-product-composition-v1.1.2.ttl) and [the structure example](../examples/example-02-structure-v1.1.2.ttl) for complete RDF patterns.

The pattern is a modelling abstraction, not a claim that JRC defines this OWL structure. [Quantitative-value rationale](decisions/TXT-DEC-001.md) and [reference-duration rationale](decisions/TXT-DEC-004.md) preserve that distinction. This pattern does not by itself establish an equivalence mapping to a quantity-value model in another ontology. SHACL requirements are application-profile requirements; OWL domain and range axioms are not form-field validation rules.

## Substances of concern

Represent the substance identity separately from the substance-presence context and from its regulatory qualification. Attach concentration, location and handling information to the presence context. For the supplied SoC dependency, exact, maximum and range quantitative expressions use the source ontology classes.
