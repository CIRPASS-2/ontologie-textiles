# SHACL application profiles

The three default structural profiles implement selective application-level
constraints on shared quantities, recyclability and Textile SoC information.
They are project validation artefacts, not complete DPP exchange requirements,
complete ontology conformance rules or normative regulatory requirements.

| Default profile | Principal coverage | Limits |
| --- | --- | --- |
| [Quantitative](textile-quantitative-shapes.ttl) | Shared value nodes, decimals, units, fractions, parameter settings, supplied awards, thresholds and reference periods. | No general unit conversion, composition-total check or method-specific scoring calculation. |
| [Recyclability](textile-recyclability-shapes.ttl) | Assessment/result and route structure, criterion coverage, scoring bounds, product/material recycled-content declarations and mass-ratio consistency. | Does not establish actual recyclability, method correctness or regulatory compliance. |
| [Textile SoC](textile-soc-shapes.ttl) | Positive presences, qualifications, locations, concentrations, thresholds, evaluations and handling information. | Partial presences may omit concentration; source presence and structural checks do not verify legal applicability or authoritative substance-list membership. |

OWL axioms describe semantics: subclass, domain and range assertions can infer
types and relationships. SHACL checks the supplied validation graph against
explicit targets, paths and constraints. An OWL existential restriction is not
a requirement for an explicit field in a supplied graph. Conversely, passing
these shapes does not establish complete OWL consistency or that unconstrained
information is complete or correct.

## Public validation and examples

With `--full`, [the public validator](../scripts/validate_public.py) merges the
13 canonical Textile graphs (including Common) and seven bounded MIREOT graphs
with each `examples/*.ttl` file separately. It merges all three top-level
`shacl/*.ttl` files into one shapes graph and calls pySHACL with
`inference='rdfs'`, `advanced=True` and `do_owl_imports=False`. Full CORE snapshots,
historical graphs and the Connector compatibility representation are not added
to this active closure. Recyclability retains its RDFS entailment declaration;
the declaration itself neither loads the ontology nor configures inference.
No profile requires OWL entailment during validation.

There is no one-to-one pairing of examples and profiles: several profiles can
apply to one graph, while some have no instance targets in a given example.
The quantitative profile also checks its schema-level
`NoQuantitativeValueSubclassShape` on every merged graph. A passing example
therefore does not prove coverage of all illustrated concepts. The
[example inventory](../examples/README.md) distinguishes relevant coverage
from illustration. Dedicated regression fixtures additionally test negative
cases and selected entailments; they are distinct from the public examples.

## Optional profiles and test-only guards

The default loader does not recurse into `profiles/`. Two shipped add-ons are
available; neither changes the scope into a complete DPP specification:

| Optional profile | Exact additional constraint | Selection |
| --- | --- | --- |
| [SoC complete-report](profiles/textile-soc-complete-report.ttl) | `CompleteTextilePresenceShape` targets `txtsoc:TextileSubstanceOfConcernPresenceContext`; `CompletePresenceConcentration` adds `sh:minCount 1` on `dpp:hasConcentration`. It adds no maximum or requirement for every other possible report field. | Add to the default shapes; the public validator supports `--full --complete-report`. |
| [Assessed-aspect targets](profiles/textile-assessed-aspect-targets.ttl) | `ExplicitAssessedAspectShape` targets subjects of `txtass:resultForAssessedAspect`. Each supplied object must be a blank node or IRI typed as `dpp:Property`, `ObservedDegradationPhenomenon`, `FailureMode` or `ExternalDamage`, and must not be an AssessmentElement, Indicator, QuantitativeValue, OWL Class or RDFS Class. No link or link cardinality is required. | Explicitly merge this file with the selected shapes and supply the relevant ontology/instance typing; the public validator has no selection flag for it. |

Temporary guards constructed for focused tests are test code, not shipped
application profiles or additional public-validator selections. In particular,
the issue #20 source implementation records describe test-only guards for
assessment outcomes and execution times; no production guard for those values
is supplied here. Passing the default profiles does not validate those fields.
See the [cumulative integration record](../migration/PHASE4_IMPLEMENTATION.md)
and the [point-5](../docs/ISSUE20_POINT5_IMPLEMENTATION.md) and
[point-6](../docs/ISSUE20_POINT6_IMPLEMENTATION.md) source records.

## SoC reporting details

The SoC profile targets positive presences, qualification identity/context/source,
structured references, locations, denominator membership, concentration branches,
threshold expressions/evaluations and instruction text. It is a decimal mass-fraction
profile: approved unit IRIs are `units:one` and CORE `massFractionUnit`; values
remain ratios in [0,1]. Arbitrary or temperature units fail an IRI whitelist even
if domain/range inference gives them MeasurementUnit typing. Other quantity/unit
conventions require a separate justified profile, not numeric rescaling here.

Concentration is optional on partial presences. Add
`profiles/textile-soc-complete-report.ttl` explicitly to require it. The default
loader uses only top-level shape files. Use `--full --complete-report` to select
that additional profile in the public validator. Completeness here means the
additional concentration relationship, not ontology-wide regulatory completeness.

Named property and SPARQL constraint resources give stable result identities.
The matcher also resolves older anonymous property shapes by their actual named
container and path, and matches focus, component, path, severity and optional
message/source-constraint identity one-to-one. Forty-one migration scenarios retain
exact result multisets. Every targeted SoC shape has positive focus coverage
and discriminating negative coverage. The existing sixteen SHACL regression
scenarios and recyclability inference control remain unchanged in purpose.

## Reference duration and interval validation (issue #16)

The default profile retains both endpoints, one endpoint and duration, and
duration alone. Duration alone is an unanchored extent and does not identify
a calendar interval. Endpoints, when comparable, must be strictly ordered;
incomparable date-times are rejected. Date-times without offsets do not provide
an unambiguous global instant. The profile does not derive endpoints, check
duration consistency with endpoints, or implement calendar arithmetic.

A reference duration must have a positive decimal scalar and one supported
time unit. The current offline profile accepts SI Reference Point identifiers
`units:second`, `units:minute`, `units:hour`, and `units:day`. Second is an SI
base unit; minute, hour and day are non-SI units accepted for use with SI.
The selected SI MIREOT already declares minute and day. Second and hour are explicitly accepted
based on the authoritative SI Reference Point, not inferred from unit labels:
https://si-digital-framework.org/SI/units/second and
https://si-digital-framework.org/SI/units/hour. This bounded exchange profile
does not claim these are the only temporal units. Other valid time units,
prefixed or structured unit expressions, and calendar months/years require a
separately reviewed profile extension with authoritative dimensional evidence.
Unknown identifiers, literals and blank-node units fail this duration profile.
Existing data using a different time unit needs a reviewed mapping or extension;
it is not automatically converted. A `day` is an elapsed SI-compatible unit,
not a calendar-day or daylight-saving arithmetic convention.

When `txtcon:hasQuantityKind` is supplied on a reference duration, the default
profile requires the SI Reference Point time quantity kind
`https://si-digital-framework.org/quantities/TIME`. It remains optional. A
different quantity kind, including length, is rejected even if the unit is a
time unit. The TIME individual is already present in the selected SI MIREOT.

## Issue #20 Assessment profiles

### Optional assessed-aspect target validation

Select `profiles/textile-assessed-aspect-targets.ttl` explicitly as an
additional pySHACL `shacl_graph`; it is excluded from the default top-level
loader so existing results are not required to use this optional validation.
Merge the relevant offline ontology closure and instance typing with the data,
and set `do_owl_imports=False` to prevent remote ontology loading. Supply the
appropriate class typing for assessed-aspect individuals: an untyped target
fails when the relevant type is not available or inferred. The profile rejects
protocol controls, values, criteria, indicators and class IRIs used as
individuals. It does not require a binding or restrict the number of bindings.
It has no ontology or version declaration and retains its source shape IRI.

### Quantitative and categorical parameter settings

A MeasurementParameterSetting may have a quantitative value, one or more SKOS
concepts, or both. The alternatives use inclusive `sh:or`; a setting with
neither form fails with `OrConstraintComponent`. The numerical maximum of one
and all supplied-value type checks apply outside the alternatives. Units,
decimal datatypes and quantity-kind constraints remain in force; multiple
concepts are permitted.

Before RDFS inference, `sh:class` requires available explicit or subclass
Concept typing. After RDFS inference, the range of `hasParameterConcept` can
supply `skos:Concept` typing for a resource. A passing `sh:class` check does not
establish membership in the intended authoritative vocabulary or equivalence
between a code and a supplied number. Literal concept targets fail either way.

### Awarded scores and conclusions

Supplied `awardedScoreValue` objects require an actual decimal scalar and unit
`units:one`; the shared quantitative checks still apply. The relation is
optional and can occur multiple times. No universal score bound, calculation
or positivity rule is introduced. No production outcome or execution-time
guard is added. The existing RangeThresholdValue scalar-presence limitation
remains deferred.
