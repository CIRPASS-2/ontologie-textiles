# TXT-DEC-013: Issue #20 point 3 - coded protocol-setting values

The maintainer approved `txtass:hasParameterConcept`: an object property with
domain MeasurementParameterSetting and range skos:Concept. It links a setting
to a categorical or coded protocol value. This is a project modelling
abstraction, not a JRC extraction. No class, code list, import, property alignment,
functional restriction or OWL cardinality is added. The existing class definition
already permits quantitative or controlled values; its header guidance now
distinguishes the two representations explicitly.

Only MeasurementParameterSettingShape changes. Inclusive sh:or requires at least
one numerical or categorical value. All supplied numerical values are checked
outside the alternatives, retaining maximum one and QuantitativeValue typing.
All supplied categorical values must be SKOS concepts in the validation graph,
without a maximum count. Both forms are allowed. Other quantity, unit, decimal
datatype and quantity-kind shapes remain unchanged. No sh:xone is introduced.

The maintainer separately approved replacing only the quantitative profile's
owl:versionIRI suffix 2.0.0 with 2.1.0-dev. This avoids identifying changed
development constraints as the unchanged published profile. No other profile
metadata changes. The catalogue replaces its corresponding version mapping,
so the old version IRI does not resolve to changed development content; the
public validator requires every declared version to be mapped. The original graph remains in the 2.0.0 Git baseline at
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`.

Before inference, untyped or incorrectly typed concept targets fail sh:class.
RDFS materialisation can infer Concept typing from the new property's range,
so the same resource can pass afterwards. Literal targets fail either way.
Passing sh:class is not authoritative vocabulary-membership verification, nor
does the shape verify code-to-number equivalence when both forms are supplied.

Settings assign values to protocol parameters. Assessment conditions can own
settings through the existing hasParameterSetting relation. Intrinsic specimen
or product characteristics and rules selecting applicable thresholds are
separate roles. No threshold-selection mechanism or points 4-6 are introduced.

See `examples/example-14-parameter-values-v2.1.0-dev.ttl` and
`tests/test_issue20_point3.py`. Committed points 1 and 2 remain preserved.
