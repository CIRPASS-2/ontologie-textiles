# SHACL application profiles

The three default structural profiles cover shared quantities, recyclability
and Textile SoC. Merge the documented offline ontology closure with instance
data, use RDFS inference and disable remote imports. The validator performs
this merge explicitly. Recyclability retains its RDFS entailment declaration.
No profile requires OWL entailment during validation.

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

## Optional assessed-aspect target validation (issue #20 point 1)

Select `profiles/textile-assessed-aspect-targets.ttl` to check explicit bindings.
Merge the relevant ontology and instance typing with the data: an untyped target
fails. The profile rejects protocol controls, values, criteria, indicators and
class IRIs used as individuals. It neither requires a binding on legacy results
nor restricts the number of bindings. The default loader does not select it.
Use it as pySHACL's `shacl_graph` with the same offline ontology/data merge and
`do_owl_imports=False` as the baseline. The regression tests cover valid and
invalid targets, missing/multiple links and existing examples 06/07.

## Parameter-setting values (issue #20 point 3)

MeasurementParameterSettingShape accepts a quantitative value, one or more SKOS
concepts, or both. It retains the numerical maximum of one and validates every
supplied value outside the inclusive alternatives. Units, decimal datatypes and
quantity-kind checks are unchanged. No coded maximum or exclusive xone is added.
A setting with neither form now produces a node-level OrConstraintComponent,
rather than a hasParameterValue MinCountConstraintComponent.

For a concept-typing check on supplied data, validate before RDFS materialisation
with the relevant code declarations available. The standard RDFS run can infer
Concept typing from hasParameterConcept itself; passing is not authoritative
vocabulary-membership verification. Literal code targets fail either mode.
The changed quantitative profile has version IRI ending 2.1.0-dev, approved as a
single-IRI metadata correction; its original 2.0.0 graph remains in Git history.

## Awarded points (issue #20 point 4)

AwardedScoreValueShape targets only supplied awardedScoreValue objects. Each must
be a QuantitativeValue with an actual decimal numericValue and units:one, reusing
the existing unit, quantity-kind and scalar checks. The numeric minimum excludes
threshold expressions that deliberately omit numericValue. No award is required,
and multiple links remain permitted. Negative values are not prohibited; no
method-specific maximum or calculation is imposed. A second unit still fails the
existing quantitative maximum. RDFS can infer value typing from the property's
range; pre-inference sh:class checks explicit or subclass typing instead.
