# TXT-DEC-014: Issue #20 point 4 - points awarded to individual results

The maintainer approved `txtass:awardedScoreValue`, an object property with domain
AssessmentResult and range QuantitativeValue. It records the number of points
actually awarded to an individual result under the applicable scoring method.
This is an issue-specific modelling abstraction, not a JRC extraction. The
property uses this decision as its sourceLocator and introduces no import,
class, alignment, inverse, functional restriction or OWL cardinality.

MeasurementResult is an AssessmentResult. RecyclabilityCriterionResult is a
RecyclabilityAssessmentResult and hence an AssessmentResult. The new relation
does not turn either into an Indicator, scoring rule, method or execution.
Its domain remains AssessmentResult; it is not restricted to these two examples.

Keep four roles distinct: hasMeasuredValue reports the underlying measurement;
txtrec:awardsScoreValue prescribes a rule's points; awardedScoreValue records the
actual award; txtind:hasQuantitativeValue reports an indicator's value. An
indicator's derivedFrom provenance does not itself identify an awarded
contribution. The execution and method provide interpretation context. No applied
rule link, calculation, aggregation, method-conformance check or score comparison
is introduced.

AwardedScoreValueShape targets only objects of the new property. It requires
QuantitativeValue typing, reuses QuantitativeValueShape, requires numericValue,
and requires hasMeasurementUnit to contain units:one. The shared shape retains
its decimal datatype, maximum one scalar, maximum one unit and optional quantity
kind checks. A threshold expression without numericValue is not an actual award.
This explicit scalar requirement does not change the existing threshold shapes.

Score links remain optional and may be multiple. There is no universal
non-negativity, maximum score or score-link cardinality. The existing
recyclability rule and aggregate-indicator constraints keep their original
targets; they are not inherited by the new property. The dimensionless convention
uses the existing units:one IRI and does not introduce a score unit or code list.

Before inference, sh:class checks supplied explicit or subclass typing. RDFS can
infer QuantitativeValue from the new range (or existing numeric/unit properties),
so resource-type checks may pass after inference. This does not verify correct
scoring. Literal targets and malformed supplied values still fail. OWL-RL checks
are not complete OWL DL consistency checks; reporter-converter fixtures remain
unavailable.

The development identity remains 2.1.0-dev. All existing ontology-header metadata,
imports, classes, disjointness axioms, existing shapes and points 1-3 are preserved.
The published 2.0.0 baseline remains in Git at
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`.
See `examples/example-15-awarded-points-v2.1.0-dev.ttl` and
`tests/test_issue20_point4.py`. Points 5 and 6 are outside this decision.
