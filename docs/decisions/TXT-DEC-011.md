# TXT-DEC-011: Issue #20 point 1 - individual result subjects

The maintainer approved `txtass:resultForAssessedAspect` on 2026-11-09 following
independent semantic review of issue #20, point 1. This branch implements that
decision for review; it does not publish a release or address points 2-6.

The property links a MeasurementResult to its direct individual subject:
`dpp:Property`, ObservedDegradationPhenomenon, FailureMode or ExternalDamage.
The anonymous union is an upper bound, not a guarantee that every member is a
suitable measurement subject. No hierarchy, disjointness, existing relation,
import or mandatory SHACL constraint changes. No functional or OWL cardinality
restriction is introduced. The property is a project modelling abstraction,
not direct JRC extraction.

The subject is distinct from the measured quantity, degree or grading dimension.
A pilling observation can concern a Pilling instance without making it a
PillingResistance characteristic. A number about pilling still needs an adequate
method/scale to distinguish severity, count and affected area. No new dimension
relation is justified without a demonstrated exchange requirement.

Characteristic classes remain OWL classes. Instance data references separate
individuals typed with those classes, following the existing assessment and
structure examples. Direct use of an OWL class IRI invokes punning and does not
inherit the class's meaning as an individual. Optional target validation rejects
that convention, protocol controls, values, criteria and derived indicators.

The optional target-validation profile under `shacl/profiles/` checks explicit
bindings without requiring a binding or imposing cardinality. It is excluded
from the default loader. Old results remain valid without the new relation.

ASSESSMENT and the network entry point advance to 2.1.0-dev. All other ontology
and MIREOT identities remain unchanged. The complete 2.0.0 baseline remains in
Git at `40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`. Use a separate checkout and its
original catalogue. No duplicate archive or runtime migration mechanism is added.
Test-only exact-delta checks preserve the earlier creator/MAT/version proofs;
active protected inputs remain byte-checked with only the specific catalogue
and one-row traceability update and SHACL documentation append permitted.

See `examples/example-12-assessed-aspects-v2.1.0-dev.ttl` and
`tests/test_issue20_point1.py`. Reporter conversion fixtures remain unavailable;
local graph, inference and validation compatibility does not prove their
round-trip contract. OWL-RL checks are not complete OWL DL consistency proofs.
