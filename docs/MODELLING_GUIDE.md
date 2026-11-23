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

Represent the substance identity separately from the substance-presence context and from its regulatory qualification. Attach concentration, location and handling information to the presence context. Positive reports use CORE SubstancePresence and concernsSubstance, which entails SubstanceOfConcern typing. Applicable qualifications remain presence-scoped and must qualify that same substance. Concentrations use CORE scalar/range carriers directly; threshold expressions retain Textile roles beneath the shared QuantitativeValue. See [the migration patterns](CORE_2026_MIGRATION.md).

## Verified CORE reuse and module ownership

`txt:FibreCompositionComponent` already specializes CORE
`dpp:MaterialOfComposition`. The relation `txt:hasFibreCompositionComponent`
links a product to a composition entry; it is not equivalent to
`dpp:hasMaterialType`, which links a material occurrence to its classification.
The MAT snapshot uses the `https://w3id.org/eudpp#` term namespace.

The owner-approved response to Nader Jelassi's [PR #19 review](https://github.com/CIRPASS-2/ontologie-textiles/pull/19)
adds `txt:FibreTypeConcept rdfs:subClassOf dpp:MaterialType` and
`txt:hasFibreType rdfs:subPropertyOf dpp:hasMaterialType`. Fibre concepts remain
SKOS individuals and also instantiate MAT's class of sector material
classifications. The property links a fibre composition entry, already a
`dpp:MaterialOfComposition`, to its classification at the same conceptual level
as MAT. RDFS/OWL inference therefore exposes every fibre concept as a MAT type
and every fibre-type assertion as a MAT classification assertion; consumers
without inference must materialize these consequences when needed.

The product-to-entry relation `txt:hasFibreCompositionComponent` remains distinct
and has no MAT type-property alignment. Physical `txt:TextileFibre` batches
remain products. Composition fractions, units, schemes and existing constraints
are preserved. These two OWL bridges are project modelling decisions supported
by MAT definitions, not alignments prescribed by the JRC study. See the
[alignment evidence](../migration/MAT_ALIGNMENT.md).

`dpp:materialPercentage` carries a literal decimal percentage. Textile uses
`txt:hasFibreMassFraction` to link to a structured `txtcon:QuantitativeValue`
on a 0?1 scale with `units:one`. Substitution would change the RDF kind, value
structure and scale interpretation; it is not semantics-preserving.

CORE `dpp:QuantitativeProperty` represents a quantitative property or measurand;
Textile `txtcon:QuantitativeValue` represents its structured value. The CORE
snapshot also supplies numerical-value and unit carriers, but this structural
overlap does not establish class equivalence. See the local
[CORE snapshot](../dependencies/current-core/p_dpp.owl) and
[MAT snapshot](../dependencies/current-core/mat.owl).

The five `hasTextualValue` local names belong to distinct IRIs in the
`textile-assessment#`, `textile-context#`, `textile-indicator#`,
`textile-process#` and `textile-structure#` namespaces under
`https://w3id.org/eudpp/`. Each module owns its property with a role-specific
domain. They are not duplicate declarations of one property. The shared value
structures remain in Connector; no centralization is required by this review.

See the [Nader review record](governance/nader-review.md) for evidence and
outstanding governance questions.

## Bounded CORE closeMatch compatibility

Textile no longer declares `skos:closeMatch` locally. No active Textile source
module declares or asserts this property, and no replacement declaration is
introduced. Other SKOS mapping properties and concept relationships are
unchanged.

The upstream [P_DPP snapshot](../dependencies/current-core/p_dpp.owl) declares
it as an annotation property and uses
`dpp:Product skos:closeMatch "schema:Product"`. The
[bounded CORE MIREOT](../mireot/dpp-textile-mireot.ttl) retains that assertion
exactly, without extracting the property's declaration. Neither upstream
resource is changed by this correction. The literal is a descriptive CORE
annotation, not an equivalence between Product and schema:Product.

The [SKOS standard](https://www.w3.org/TR/skos-reference/#mapping) instead
defines `skos:closeMatch` as an object property for concept mappings.
Preserving the upstream annotation does not make it a SKOS-standard concept
mapping or redefine SKOS. Loading the full SKOS ontology together with CORE's
annotation-property definition would require a separate compatibility
assessment; no such import is introduced here.

The merged diagnostic artifact can acquire an annotation-property declaration
during serialization from the retained CORE usage. That generated declaration
is not a Textile source declaration, and a merged profile pass does not prove
that the individual modules pass or that all upstream vocabulary uses follow
SKOS semantics. The following procedure makes these limits explicit.

## OWL 2 DL diagnostic procedure and limits

The 2026-11-03 diagnostic applies to the local candidate with the retained MAT
alignment, the subsequent modelling-note and metadata corrections, and the
removal of Connector's local closeMatch declaration. It does not describe the
unmodified source commit
`e9cf8542d104fefccf339761d138fcf9c32bc904`. The runtime catalogue resolved
exactly the expected 20 ontology documents, including the bounded MIREOTs;
there was no accidental loading of full CORE modules or missing import.

### Reproduce the merged-artifact check

Use ROBOT 1.9.7 from the repository root. Set `$robotJar` to that release's
JAR and `$diagnosticDir` to an existing writable scratch directory outside the
publication package. The release JAR used for the diagnostic had SHA-256
`91890c2e83d0f092dd08731376f154b36610544cfbe8685337a1bf7244ccaa2d`.
The following PowerShell commands retain ontology annotations as well as OWL
axioms, collapse the imports into one artifact, and check that artifact:

```powershell
java -jar $robotJar merge --input ontology/textile-ontology.ttl --catalog catalog-v001.xml --include-annotations true --output "$diagnosticDir/merged.owl"
java -jar $robotJar validate-profile --profile DL --input "$diagnosticDir/merged.owl" --output "$diagnosticDir/merged-profile.txt"
java -jar $robotJar reason --reasoner hermit --input "$diagnosticDir/merged.owl" --remove-redundant-subclass-axioms false --output "$diagnosticDir/reasoned.owl"
```

Inspect each exit status and the profile report before interpreting the
reasoning result. See ROBOT's [merge](https://robot.obolibrary.org/merge),
[profile validation](https://robot.obolibrary.org/validate-profile) and
[reasoning](https://robot.obolibrary.org/reason) procedures. The retained
`dpp:Product skos:closeMatch "schema:Product"` annotation was present in the
actual checked artifact; no assertion was removed for this check.

### Modular and merged results

ROBOT 1.9.7 bundles OWLAPI 4.5.29. A comparison using OWLAPI 5.1.18 produced
the same results at each stage:

| Checked representation | Profile violations (occurrences) | OWL 2 DL profile |
| --- | ---: | --- |
| Original ontology and modular imports closure | 208 | Fails declaration checks |
| Union of the same OWL axioms in memory | 47 | Fails declaration checks |
| Serialized and reloaded union | 0 | Passes |
| ROBOT merged artifact | 0 | Passes |

The 208 occurrences comprise 188 annotation-property, nine class, eight
object-property and three datatype declaration diagnostics. Deduplication by
IRI and violation type gives 19 affected IRIs: 12 annotation properties,
four classes, two object properties and one datatype. Fifteen have
declarations elsewhere in the loaded closure, outside the individual
ontology's visible import scope. Flattening removes 161 such occurrences.
The remaining 47 concern declarations absent throughout the raw closure:
`skos:scopeNote` (one occurrence), `prov:wasDerivedFrom` (42 occurrences)
and `xsd:date` (three occurrences), plus `skos:closeMatch` (one occurrence).
The total modular count remains 208 after the local declaration removal:
the CORE annotation was already outside Connector's declaration visibility.

Thus the merged artifact passes the structural profile check, but this
does not establish that each original module, or the original modular
closure as checked by OWLAPI, passes. The remaining modular diagnostics
include genuinely absent explicit declarations as well as import-visibility
limitations. No source declarations or imports were changed to suppress them.

### Declarations introduced by serialization

The diagnostic compared the union of all original OWL axioms with the
serialized, reloaded merged artifact using OWLAPI axiom-set differences.
The original 10,014 distinct axioms became 10,304. The 290 additions were
exclusively declaration axioms:

| Entity type | Added declarations |
| --- | ---: |
| Named individual | 286 |
| Annotation property: `skos:scopeNote`, `prov:wasDerivedFrom`, `skos:closeMatch` | 3 |
| Datatype: `xsd:date` | 1 |

The earlier 2026-11-02 candidate had 10,015 original axioms and 289 added
declarations. Removing the local closeMatch declaration accounts exactly
for the one-axiom decrease and the additional serialization declaration;
the merged artifact's axiom count is unchanged.

Zero original OWL axioms were removed and the logical axiom sets were equal.
All original OWL axioms, including the closeMatch annotation assertion, were
preserved. These declarations belong to the serialized diagnostic artifact;
they were not added to the canonical modules. This is an OWL axiom-preservation
result, not a claim of RDF graph identity: merging collapses ontology
boundaries and import statements. Ontology annotations were retained with
`--include-annotations true`.

### HermiT configuration and qualified consistency result

The merged artifact was reasoned over with HermiT 1.4.5.456 bundled in ROBOT
1.9.7. ROBOT's HermiT factory path uses
`ignoreUnsupportedDatatypes=true`; the bundled factory implementation and a
direct factory run were checked to confirm this setting. It is not an
additional ROBOT command-line option in the commands above. An explicit
HermiT configuration must record the same value to reproduce this result.

With that setting the merged artifact was reported consistent, with zero
unsatisfiable named classes (excluding `owl:Nothing`). The direct check also
confirmed both accepted MAT entailments and all 22 fibre classifications.
With `ignoreUnsupportedDatatypes=false`, HermiT instead raised
`UnsupportedDatatypeException` for `xsd:date`, so no strict-mode consistency
result was obtained. This exception is not evidence of inconsistency.

The positive result is conditional on ignoring unsupported datatypes; it is
not a complete consistency proof under the intended date semantics.
Declaring `xsd:date` makes the artifact pass structural declaration checks
but supplies neither a supported datatype interpretation nor a custom
datatype definition. OWL RL regression validation likewise does not
establish complete OWL DL consistency.

### The three logical uses of xsd:date

These are the three `rdfs:range xsd:date` occurrences responsible for the
datatype profile diagnostics, not a count of every date-valued metadata
literal in the repository. Here `dpp:` means `https://w3id.org/eudpp#` and
`txtsoc:` means `https://w3id.org/eudpp/textile-soc#`.

| Property | Location | Modelling purpose |
| --- | --- | --- |
| `dpp:qualificationValidFrom` | [SOC MIREOT](../mireot/soc-textile-mireot.ttl) | First date on which a `dpp:SoCQualificationAssertion` is considered valid. |
| `dpp:qualificationValidUntil` | [SOC MIREOT](../mireot/soc-textile-mireot.ttl) | Last date on which that qualification assertion is considered valid, when bounded. |
| `txtsoc:referenceDate` | [Textile SOC](../ontology/textile-soc.ttl) | Date recorded for a `txtsoc:ExternalRegulatoryReference`. |

The first two ranges are retained CORE SOC qualification-validity metadata;
the third is a Textile project decision for external regulatory references.
They express calendar dates. Replacing them with timestamps or strings
would require an explicit modelling decision and is outside this correction.

### Retained regression contract

The accepted bridges remain
`txt:FibreTypeConcept rdfs:subClassOf dpp:MaterialType` and
`txt:hasFibreType rdfs:subPropertyOf dpp:hasMaterialType`.
The existing [MAT regression tests](../tests/test_mat_alignment.py) cover
all 22 classifications, property entailment, SKOS typing, composition-model
boundaries, historical preservation and both SHACL example modes. These
tests retain their behavioural expectations. The later owner-approved
corrections are now checked as an exact seven-addition/six-removal delta
against the unchanged pre-MAT commit. The old creator and version-identity
proofs first verify that complete delta, then restore only those exact
triples before checking their unchanged historical digests. Notes, metadata,
classes and properties are not ignored wholesale.

Ten mutation tests demonstrate rejection of unauthorized changes. The frozen
catalogue and protected external, MIREOT and historical inputs remain
byte-protected. The three stale WIDOCO/WebVOWL modules are regenerated from
canonical sources using the established workflow; generated RDF is checked
for graph equivalence. The original eight failures and their individual
baselines are documented in the
[publication finalization record](../migration/PUBLICATION_CANDIDATE_FINALIZATION.md).
See its linked machine-readable delta and final validation results for the
current publication candidate. The earlier MAT-only evidence remains an
unchanged historical proof of that narrower transition.

## Approved issue #9 clarifications

[TXT-DEC-016](decisions/TXT-DEC-016.md) records the retained CORE extraction
architecture, the textile-context durability definition, the interpretive
indicator distinction and the two role-specific concernsProduct properties.
These are annotation and documentation changes with no new logical commitments.
The existing quantity, SOC, assessment and composition models remain governed by
their own decisions.

## Issue #12: fibre composition and packaging


A FibreCompositionComponent denotes a fibre material constituent in the composition of a particular textile product, characterised by fibre type and mass fraction. It need not identify an individual physical fibre batch or a separate declaration. It is distinct from a physical garment part such as a sleeve or lining. The retained subclass of CORE MaterialOfComposition expresses this contextual material interpretation. The JRC Preparatory Study remains the primary recorded modelling source; this clarification is a project decision, not an assertion that JRC defines these OWL axioms.

The product-to-constituent hasFibreCompositionComponent remains independent of CORE hasMaterial until CORE maintainers confirm the intended contextual-material semantics. hasFibreType remains a subproperty of CORE hasMaterialType and fibre type concepts remain MaterialType individuals; inference-aware consumers can discover those classification edges. hasFibreComponent remains available for presence without an explicitly represented share. It targets a fibre type, not a material node.

The Textile fraction is a QuantitativeValue object with a dimensionless 0?1 scalar; CORE MAT 1.1.0 materialPercentage is a decimal datatype property. There is no direct property alignment. Conversion is meaningful only when material, mass basis, denominator, unit and scale agree. Where a receiving CORE profile uses a 0?100 percentage, 0.95 corresponds to 95%; the snapshot does not settle that scale as a universal contract.

Regulation (EU) No 1007/2011 provides relevant context and possible validation use cases: Article 5 and Annex I address fibre names, Article 9 addresses composition and percentages by weight, and Article 11 addresses textile products with components of different fibre contents. This is not a claim of original source derivation, and this ontology does not provide a comprehensive legal compliance validator. See https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32011R1007.

A NonTextileComponent remains a TextileProductPart and is not universally a CORE Product. hasNonTextileComponent is not aligned to the transitive, product-to-product CORE isComponentOf. PackagingMaterial denotes material used in packaging associated with a textile product; it is not automatically a material of that textile product. It may independently be a material of composition of a separately modelled packaging product. No disjointness is asserted.

The RDFS and OWL-RL inference tests cover selected positive and negative entailments; absence of entailment is not logical impossibility, and these tests do not establish complete OWL DL consistency.

The existing mass-fraction SHACL profile is unchanged. A fraction node typed as
txtsoc:RangeThresholdValue can conform without a scalar numericValue because
the quantitative-value shape permits threshold roles. Review this existing
limitation separately during the future quantitative validation work.

## Common, compatibility and reference periods

Shared quantitative, provenance and weak-influence vocabulary is owned by
Textile Common; existing `txtcon:` term IRIs remain unchanged. The Connector
compatibility graph contains the complete Common payload. Quantitative-value
nodes are distinct from CORE product-property individuals; transfer of values
requires compatible meaning, scale, unit, scope and method. No unconditional
class or property equivalence is asserted.

Reference periods may use two boundaries, one boundary with a duration, or a
duration alone. Durations must be positive with an approved SI time unit; the
profile checks boundary order and compatible timezone representation, but does
not perform calendar arithmetic or prove boundary-duration consistency. The
previously documented fraction scalar-presence limitation remains deferred.

## Binding individual results to assessed subjects (integration-2026-11.3)

Use `txtass:resultForAssessedAspect` on each independently identifiable
MeasurementResult. Point to an individual typed by the relevant characteristic
or phenomenon class, following [example 12](../examples/example-12-assessed-aspects-v2.1.0-dev.ttl).
Do not point directly to an OWL class IRI: class/individual punning does not
inherit class membership. Protocol controls remain MeasurementParameterSettings
with settingForParameter and hasParameterValue or hasParameterConcept.

A reusable method's `measuresPerformanceParameter` identifies a performance
parameter within the method's scope; it does not require a product-specific
occurrence of that parameter. A result's `resultForAssessedAspect` instead
identifies the particular aspect evaluated. `MeasurementParameter` is a separate
role for protocol controls, assigned through `settingForParameter`.

Sharing a target individual between execution and result is appropriate when
both statements concern exactly the same product-specific aspect. Example 12
also shares it with a synthetic method whose scope is that particular aspect;
this is not a rule for reusable standards. A reusable method can refer to a
separate parameter individual of the appropriate performance-parameter class,
while a product and its result refer to their own aspect instance. A criterion's
parameter target likewise reflects the criterion's scope. Being instances of
the same class does not make these resources identical. No equality, automatic
mapping or requirement that method, execution, criterion and result share one
individual is asserted. Applications must retain enough method/scale context
to interpret distinct parameter and aspect resources.

The target is the direct subject, not necessarily the scalar quantity or grade
dimension. Pilling and PillingResistance remain different categories. A numeric
pilling result needs an adequate method/interpretation scale; an aspect link alone
does not distinguish severity, count and affected area. No measuredDimension
relation or automatic promotion of result values to structural characteristic
values is introduced. Existing execution-level assessesPerformanceParameter
retains its OPP range and must not be used for phenomena or structural targets.

No global cardinality is imposed. Explicit-target validation is an optional
[application profile](../shacl/README.md), without cardinality constraints.
The broad OWL union is an upper bound, not closed-world target validation.
Derived indicators remain distinct from the underlying result. The generic
MeasurementResult definition still requires a measurement/test outcome; an
arbitrary evaluation output can instead be an AssessmentResult.
See [TXT-DEC-011](decisions/TXT-DEC-011.md).


## Assessment executions and product events (issue #20 point 2)

Use `txtass:isRepresentedByProductEvent` when a conceptual, product-facing
ProductEvent represents the concrete assessment execution. The target is distinct
from the technical EPCIS carrier. An ObjectEvent with OBSERVE / inspecting does
not by itself establish a qualifying ProductEvent. The existing PROCESS bridge
would instead also classify the assessment as a TextileProcessExecution.

ASSESSMENT directly imports the unchanged bounded EVENT MIREOT. It does not load
EPCIS carrier mappings; applications using `dpp:isRepresentedByCarrier` provide
their existing EVENT definitions. No links or cardinalities are required.
See [example 13](../examples/example-13-assessment-product-event-v2.1.0-dev.ttl)
and [TXT-DEC-012](decisions/TXT-DEC-012.md).


## Numerical and categorical protocol settings (issue #20 point 3)

A MeasurementParameterSetting assigns a numerical value with hasParameterValue
or a coded value with hasParameterConcept to a MeasurementParameter. An execution
or AssessmentCondition can own the setting through hasParameterSetting. The code
is a SKOS concept supplied by the application; no code list is introduced here.
A setting is distinct from an intrinsic specimen/product characteristic and
from a rule selecting an applicable threshold. Neither role is added by point 3.

For the reporter's fabric-type case, distinguish the specimen's actual
construction characteristic from the protocol's selected fabric category.
For example, an application may record that a specimen is knitted in its product
classification data, while a separate MeasurementParameterSetting supplies an
application-defined SKOS code for the protocol's knitted-specimen conditions or
threshold-table category. `hasParameterConcept` records that protocol input;
it does not assert the specimen classification, establish the selection rule,
or prove that the selected table is appropriate. The classification and setting
may use an agreed code only when its definition fits both roles; they are not
inherently the same assertion. A PROCESS method concept denotes a process method,
not a fabric classification, and no equivalence is implied. Example 14's synthetic
cycle-mode code remains a protocol example rather than a fabric-type vocabulary.

The baseline setting shape requires at least one value form. Both may be present;
all numerical values remain checked, with a maximum of one, and all code targets
must be SKOS concepts in the validation graph. There is no categorical maximum.
Before inference, missing or incorrect concept typing fails. With RDFS, the
property range itself infers Concept typing: this is not verification against
an authoritative vocabulary. Type-check imported code data before entailment
when that distinction matters. Code-to-number agreement is not checked.
See [example 14](../examples/example-14-parameter-values-v2.1.0-dev.ttl) and
[TXT-DEC-013](decisions/TXT-DEC-013.md).


## Awarded points on results (issue #20 point 4)

Use `txtass:awardedScoreValue` on an AssessmentResult, including MeasurementResult
and RecyclabilityCriterionResult, to identify points actually awarded under the
applicable scoring method. Keep the measured value, the rule's prescribed points,
the awarded contribution and any derived indicator value as distinct roles.
The execution and its method supply interpretation context; this property does
not identify an applied rule, execute a method, aggregate or verify the award.

The quantitative profile checks every supplied award: QuantitativeValue typing,
an actual decimal numericValue, units:one and the existing quantitative constraints.
The numeric requirement excludes threshold-expression alternatives. Missing award
links and multiple awards are allowed; no universal non-negativity or maximum is
asserted. Application-specific method compliance remains outside this correction.
RDFS range typing is classification, not proof of correct data or scoring.
See [TXT-DEC-014](decisions/TXT-DEC-014.md) and
[example 15](../examples/example-15-awarded-points-v2.1.0-dev.ttl).


## Controlled assessment conclusions (issue #20 point 5)

Use `txtass:hasAssessmentOutcome` on an AssessmentResult to report a controlled
conclusion under its applied method and context. For recyclability, attach it to
the aggregate result with resultOfAssessment, the execution's appliesMethod and
assessesProduct, and resultForRecyclingRoute. Existing individual criterion
results keep hasCriterionOutcome. Criterion satisfaction, score, label, technology
level and overall verdict are distinct; none automatically determines the verdict.
Do not use criterionSatisfied or other criterion-level codes as overall outcomes.

Application-defined SKOS concepts need definitions expressing the overall
method- and route-specific conclusion. The synthetic positive, negative and
inconclusive concepts in example 16 are illustrative and establish no regulatory
classification or universal recyclability claim. Absence means no explicit
verdict was supplied; it does not mean negative or inconclusive. No code list,
concept class, scheme, inverse, property alignment or cardinality is introduced.

All production SHACL profiles remain unchanged. No suitable existing development
profile covers general assessment conclusions, so the supplied-value guard is
only a focused test fixture in memory. RDFS can infer Concept typing from the
property's range. Neither type checking nor baseline validation verifies approved
vocabulary membership, aggregate scope or a method's actual decision correctness.
The broad AssessmentResult domain also includes criterion results; intended use
on the aggregate result is a semantic convention documented here, not a new class
restriction. See [TXT-DEC-015](decisions/TXT-DEC-015.md) and
[example 16](../examples/example-16-assessment-outcomes-v2.1.0-dev.ttl).


## Assessment execution times (issue #20 point 6)

Use `prov:startedAtTime` for the beginning of an AssessmentExecution and
`prov:endedAtTime` for its completion. Explicitly type examples using this pattern
as both `txtass:AssessmentExecution` and `prov:Activity`. Values use `xsd:dateTime`;
a known timezone may be supplied, but a timezone is not required or invented.
Missing start, completion or both is permitted. Multiple supplied values are not
prohibited by this pattern; reconciling conflicting source statements is an
application responsibility. No temporal cardinalities or chronology rules are
added. Completion of a long-running execution is its end, not a claim that the
entire execution occurred at an instant or that a result was generated then.

When only a calendar date is known, use `dcterms:date "2026-11-14"^^xsd:date` on
the execution. This is a coarse associated date. DCMI Date does not intrinsically
mean start or completion, and this convention does not redefine it. Date-only
values do not contain the same temporal information as PROV timestamps. Do not
infer either PROV timestamp or manufacture midnight, a timezone or other absent
precision. This convention does not prohibit using richer DCMI date expressions
outside this limited assessment pattern.

Results can query execution completion using
`txtass:resultOfAssessment/prov:endedAtTime`, and similarly for start. This path
can return multiple values and does not copy timestamps onto results. Execution
completion, result generation or validation, EPCIS event occurrence and repository
recording are different notions. The point-2 ProductEvent relation does not equate
those times. EVENT's actual carrier is `epcis:EPCISEvent` (including ObjectEvent),
not a declared `dpp:EPCISCarrier` class. OBSERVE / inspecting alone does not prove
that a technical event qualifies as a product-facing ProductEvent.

The [synthetic example](../examples/example-17-assessment-times-v2.1.0-dev.ttl)
contains a completion without ProductEvent, a two-day execution, distinct
execution/occurrence/recording times, a coarse date, an undated execution and a
result linked to its execution. These are isolated example identifiers, not a
complete EPCIS payload or evidence of a real inspection.

`txtcon:ReferencePeriod` qualifies the interval of an observation, indicator or
other time-bound textile statement (for example, a reporting period). That is
not necessarily when an assessment was executed. Treating that reference
context as an execution timestamp would blur these roles and would still require
an agreed execution-to-period relation. Direct PROV reuse supplies start/end
semantics without adding such a local relation. An execution interval and a
statement's reference period may coincide in a particular dataset; no equality
or synchronization follows. The AssessmentExecution documentation links to both
PROV properties for discovery; these annotation links do not import their axioms.

No local temporal property, global subclass alignment, PROV import or copied
PROV declaration is added to any ontology. With authoritative PROV axioms loaded,
its start/end property domains infer Activity. Without those axioms the current
runtime does not gain that inference merely by referencing PROV terms; explicit
Activity typing makes the examples clear in either case. PROV Activity is disjoint
with Entity, so dual use of the same individual as an activity and a PROV entity
can cause inconsistency. The existing execution/result separation is preserved.

All production SHACL files retain their bytes and version identities. Tests alone
construct an optional guard scoped to AssessmentExecution: every supplied PROV
start/end value must have datatype xsd:dateTime, and a supplied coarse dcterms:date
must have datatype xsd:date. A small test-only lexical check also requires an actual time component: the
pinned RDFLib converter can otherwise accept a date-only lexical form typed as
dateTime. Negative lexical tests preserve the original literal spelling;
normalization before validation can erase evidence of a malformed source value,
so the guard cannot recover precision already lost by an upstream converter.
The guard imposes no presence or count constraints
and does not validate unrelated PROV activities. A passing public validator does
not mean these temporal values were checked by this guard.

In the pinned RDFLib/pySHACL stack, explicitly typed xsd:dateTimeStamp literals
are not accepted by sh:datatype xsd:dateTime. Use xsd:dateTime for this PROV pattern;
EPCIS carrier timestamps retain the full EVENT vocabulary's xsd:dateTimeStamp.
A bare dateTimeStamp datatype guard is not sufficient evidence of valid lexical
forms or required timezones in this stack. Tests check the chosen date/dateTime
forms and negative cases; neither validation nor OWL-RL proves that a reported
time is factually correct or constitutes complete OWL DL consistency checking.

Normative references: [PROV-O](https://www.w3.org/TR/prov-o/),
[DCMI Date](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/date/)
and [XML Schema datatypes](https://www.w3.org/TR/xmlschema11-2/).
See the [implementation evidence](ISSUE20_POINT6_IMPLEMENTATION.md) for the
separate authoritative-axiom check and remaining validation limits.


## Issue #20 exchange-gap traceability

The following paraphrases the reporter's six gaps and preserves the named
workarounds from [issue #20](https://github.com/CIRPASS-2/ontologie-textiles/issues/20),
verified on 2026-11-16. Point 6 describes proposals rather than a stated workaround.

| Point / exchange gap | Reporter workaround | Implemented representation |
|---|---|---|
| 1. Result-to-parameter association | `dcterms:subject` on the result | `resultForAssessedAspect` on each MeasurementResult; method/scale context retains grading meaning. |
| 2. Execution-to-product-event link | `dcterms:relation` to ProductEvent | Independent ASSESSMENT `isRepresentedByProductEvent`; conceptual event and EPCIS carrier stay distinct. |
| 3. Coded condition value | `dcterms:type` and `rdfs:comment` on the condition | `hasParameterConcept` on MeasurementParameterSetting; not specimen classification or threshold-selection logic. |
| 4. Points earned by a result | Derived indicator marked with `dcterms:type` | `awardedScoreValue`; separate from measured values, prescribed rule points and indicators. |
| 5. Overall verdict | Information lost | `hasAssessmentOutcome` with application-defined overall concepts; criterion codes are not overall verdicts. |
| 6. Assessment timing without EPCIS | None stated; event-time reuse or an execution-date property proposed | Optional PROV start/end; coarse `dcterms:date` when only a date is known. |

These patterns address representation, not demonstrated compatibility with the
reporter's unavailable converter fixtures. The external outcome vocabulary,
parameter/aspect correspondence and method-specific interpretation still require
agreement between exchange partners.
