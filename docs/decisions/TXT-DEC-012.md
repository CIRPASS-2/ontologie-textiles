# TXT-DEC-012: Issue #20 point 2 - assessment product-event bridge

The maintainer approved one optional ASSESSMENT property after focused semantic
review: `txtass:isRepresentedByProductEvent`, with domain AssessmentExecution and
range ProductEvent. It links the concrete execution to its conceptual,
product-facing event, distinct from any technical EPCIS carrier. This is a project
modelling abstraction, not a JRC extraction.

The property is independent of the PROCESS bridge: reusing that bridge would
also infer TextileProcessExecution typing. No subproperty alignment, inverse,
property chain, functional restriction, cardinality or event class is added.
Missing and multiple links remain permitted. The point-1 property is unchanged.

ASSESSMENT directly imports the existing bounded EVENT MIREOT so standalone
loading supplies ProductEvent and ESPREvent. Its closure grows from five to six
documents; the full Textile closure remains twenty. EVENT, PROCESS, CORE,
MIREOTs and EPCIS mappings are unchanged. The unpublished 2.1.0-dev identities
remain appropriate; no release identity or migration infrastructure changes.

The bounded subset does not supply `dpp:isRepresentedByCarrier` or its inverse.
The example illustrates the existing full EVENT 1.0.0 pattern with separate
AssessmentExecution, ProductEvent and ObjectEvent individuals; applications
provide their existing carrier-mapping definitions. OBSERVE / inspecting alone
does not establish ProductEvent semantics. The example assumes a qualifying
product-facing inspection; it is not a complete EPCIS payload.

An OWL range classifies its object. Pointing the new property directly at an
ObjectEvent would also classify that node as ProductEvent, without necessarily
causing inconsistency: those two classes are not declared disjoint. This is not
the intended use. No new SHACL constraints are introduced for this correction.

See `examples/example-13-assessment-product-event-v2.1.0-dev.ttl` and
`tests/test_issue20_point2.py`. Reporter converter fixtures are unavailable;
OWL-RL checks are not a complete OWL DL consistency proof. The original 2.0.0
baseline and committed point 1 remain preserved in Git.
