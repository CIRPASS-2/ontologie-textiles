# TXT-DEC-015: Issue #20 point 5 - controlled assessment conclusions

The maintainer approved the independent object property
`txtass:hasAssessmentOutcome`, with domain AssessmentResult and range skos:Concept.
It links a result to its controlled conclusion under the applicable method and
context. For recyclability, use it on the aggregate result under the stated
method and recycling route. Keep hasCriterionOutcome on the contained individual
criterion results. The property is an issue-specific modelling abstraction; this
decision is its sourceLocator. No JRC attribution is asserted.

RecyclabilityOutcomeConcept explicitly describes criterion outcomes. Its existing
criterionSatisfied, criterionNotSatisfied and related concepts must not be reused
as overall product-level verdicts. No existing concept definition is broadened.
The examples instead define three synthetic application-owned SKOS concepts:
positive, negative and inconclusive overall conclusions under the applicable
method and route. These example individuals establish neither a new ontology
class/scheme/code list nor regulatory or universally applicable classifications.

The aggregate result retains resultOfAssessment, the execution's appliesMethod
and assessesProduct, and resultForRecyclingRoute. Criterion outcomes, score,
label and technology level do not automatically determine an overall verdict.
The existing valid V06 route-specific assessment fixture is unchanged and is the
reference for example 16. The example adds one explicit inconclusive overall
verdict; tests substitute positive/negative conclusions and omit the link.
These tests verify representation, not correctness under an external method.

The broad AssessmentResult domain includes criterion results. It does not
formally enforce aggregate-only use or distinguish an approved vocabulary from
arbitrary concepts. Documentation and instance context provide that distinction.
No property alignment, inverse, subclass, import, cardinality, decision rule or
automatic derivation is introduced. Missing and multiple links remain permitted;
absence does not imply a negative or inconclusive conclusion.

## SHACL placement decision

No suitable existing development profile covers a general categorical assessment
conclusion. The quantitative 2.1.0-dev profile is documented for quantitative roles
and their protocol settings; its categorical setting branch belongs to that
existing value alternative. The optional assessed-aspect profile addresses
MeasurementResult subjects. Neither is a general assessment-conclusion profile.
The recyclability and SoC profiles retain published 2.0.0 identities. Changing
their scope or version solely for this guard is unnecessary and was not approved.

Therefore all production SHACL Turtle files remain byte-identical to point 4.
There is no new profile or profile-version change. Focused tests construct only
the permitted three-triple guard in memory: NodeShape, targetObjectsOf
hasAssessmentOutcome, and class skos:Concept. No count constraint is added.
The public validator does not select this guard; its baseline pass must not be
reported as validation of supplied assessment-outcome objects.

Before inference the test guard requires explicit or subclass Concept typing.
RDFS can infer Concept from the new range, including on a resource with another
type. Literal targets fail the guard in either mode. Neither sh:class nor range
inference establishes authoritative vocabulary membership, aggregate scope,
coherence of multiple conclusions or method-specific decision correctness.
Criterion-level concepts also pass this generic guard; their semantic misuse is
documented, not claimed to be detected by typing alone.

The existing 2.1.0-dev ASSESSMENT identity and all header metadata remain unchanged.
All earlier corrections and the published 2.0.0 baseline are preserved in Git.
No other ontology source, migration infrastructure or production validator changes.
Complete OWL DL consistency and reporter-converter validation remain separate
gates. See `examples/example-16-assessment-outcomes-v2.1.0-dev.ttl` and
`tests/test_issue20_point5.py`. Point 6 is outside this decision.
