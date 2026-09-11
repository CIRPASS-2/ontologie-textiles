# SHACL profiles

The SHACL files define application-level data-quality constraints for quantitative values, recyclability results and textile substances-of-concern information. They are RDF graphs that declare application profiles; they are not a claim of complete Textile Ontology conformance.

## Validation environment

Validate an instance or example graph with the applicable Textile Ontology and import closure available as the validation ontology graph. Ontology/import closure is part of the validation environment: an `sh:entailment` declaration does not import ontology axioms.

The recyclability profile graph (`https://w3id.org/eudpp/textile-shacl/recyclability`) declares the RDFS entailment regime using the exact identifier `<http://www.w3.org/ns/entailment/RDFS>`. This is required because that profile contains constraints whose expected result depends on RDFS hierarchy entailments, including the specialised recyclability assessment-property modelling. A processor that cannot support this declared regime cannot claim successful execution of that declared profile environment. The standalone validator explicitly sets `inference="rdfs"`; it does not rely on the declaration to configure the processor. The versions tested for this candidate are pinned in `requirements-validation.txt`.

No profile declares an OWL entailment requirement. The quantitative and substances-of-concern profiles do not currently declare RDFS entailment because their representative validation results are unchanged with and without explicit RDFS inference. The supplied examples remain unchanged; in particular, no duplicate `txtass:assessesProduct` assertion is added for the specialised recyclability assessment assertion.

## Profile scope and conformance claims

The repository currently supplies three official SHACL profiles: `textile-quantitative-shapes.ttl`, `textile-recyclability-shapes.ttl`, and `textile-soc-shapes.ttl`. They are selective application-level profiles. Each validates only the targets, paths, and constraint components declared in its own shapes graph.

| Profile | Current application purpose from declared shapes | Representative declared targets / paths | Entailment note |
| --- | --- | --- | --- |
| Quantitative | Bounded quantitative values, measurement/threshold roles, and reference-period patterns | `txtcon:QuantitativeValue`; `txtass:MeasurementParameterSetting`; `txtcon:numericValue`; `txtcon:hasMeasurementUnit` | No RDFS declaration is currently required. |
| Recyclability | Bounded recyclability assessments, scoring, recycled-content declarations, and related result patterns | `txtrec:RecyclabilityAssessment`; `txtrec:RecycledContentDeclaration`; `txtass:assessesProduct`; `txtrec:hasRecyclabilityScore` | Explicit RDFS processing is required. |
| Substances of concern | Bounded SoC quantitative values, concentration information, and textile threshold patterns | `soc:ExactQuantitativeValue`; `txtsoc:TextileConcentrationInformation`; `soc:numericValue`; `soc:hasThresholdQuantitativeValue` | No RDFS declaration is currently required. |

Successful validation means that supplied data conforms to the executed supplied profile constraints under the documented processing environment. It does not prove complete conformance with the entire Textile Ontology. Resources, classes, and properties not constrained by the supplied shapes are outside the demonstrated SHACL coverage unless another profile or rule explicitly covers them. Ontology semantics and SHACL validation are related but not interchangeable; absence of a SHACL constraint for an ontology construct is not, by itself, evidence that the construct is invalid or unsupported.

The repository does not currently commit to an ontology-wide complete normative SHACL profile. Broader normative coverage may be evaluated separately in a future profile revision; no roadmap or delivery commitment is made. The recyclability RDFS requirement and the absence of an OWL entailment requirement apply to this candidate.
