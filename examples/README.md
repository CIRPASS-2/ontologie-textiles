# Textile RDF instance examples

This directory contains 20 numbered illustrative examples and one optional
reference-individual dataset for the unpublished `integration-2026-11.3`
package. They show ABox instances, relationships, values and, in some files,
application-supplied SKOS concepts. They do not define new ontology classes or
properties and contain no `owl:imports`. Load the current ontology closure with
the [package catalogue](../catalog-v001.xml); see the
[modelling guide](../docs/MODELLING_GUIDE.md).

These graphs are not complete production-ready DPPs or regulatory compliance
evidence. Examples 01 and 09 explicitly say their numeric data are illustrative
and not extracted from JRC; 10 disclaims regulatory determinations; 11 identifies
its scoring approach as illustrative; 12-17 explicitly identify synthetic data;
and 20 disclaims classification of a real product. The remaining graphs present
example situations without evidence of real product observations. A standard
identifier or source citation does not establish that a test was performed or
that a product conforms to that standard. The separate reference dataset cites
sources for the named references, not for product performance or compliance.

## Illustration and automated validation

[The public validator](../scripts/validate_public.py), with `--full`, uses all
21 Turtle files as positive validation inputs. Each is checked separately with
the offline ontology closure and all three default SHACL profiles, using RDFS
inference and remote imports disabled. This is not a set of independent module
unit tests, nor a combined product dataset. Some examples reuse identifiers;
merging all files is not the documented validation procedure.

Dedicated positive, negative and reasoning fixtures live under
[`tests/abox_corpus/`](../tests/abox_corpus/); additional tests construct graphs
in memory. They exercise failures and entailments that an illustrative example
need not cover. A passing public example establishes only conformance to the
selected constraints. See the [SHACL guide](../shacl/README.md) for loading,
optional profiles and limits.

## Inventory

Module names below refer to the corresponding `textile-*` ontology files.
**Common** supplies the shared `txtcon:` terms historically owned by Connector.
**Q**, **R** and **S** denote the default quantitative, recyclability and SoC
profiles; **A** denotes the optional assessed-aspect target profile. A dash means
no instance-level targets for these profiles; Q's schema-level subclass check
still runs. Coverage describes what is checked, not every illustrated concept.

In the CORE column, **explicit** means a `dpp:` term occurs in the example.
**Inherited** means Textile schema axioms expose CORE semantics when the relevant
inference is available. In particular, Textile products specialize CORE Product;
fibre composition entries specialize MaterialOfComposition; fibre-type concepts
specialize MaterialType; and hasFibreType specializes hasMaterialType. Product
components and contextual composition entries are different roles. See
[Textile Core](../ontology/textile-core.ttl) and the
[CORE reuse guidance](../docs/MODELLING_GUIDE.md).

| File | Purpose | Relevant Textile modules | CORE reuse | Relevant SHACL coverage |
| --- | --- | --- | --- | --- |
| [01 product composition](example-01-product-composition-v1.1.2.ttl) | T-shirt, 95/5 cotton-elastane composition and fibre/yarn/fabric component chain. | Core, Common | Explicit: isComponentOf. Inherited: Product and MAT composition/type semantics. | Q: scalar values, fraction bounds and units; no composition-total check. |
| [02 structure](example-02-structure-v1.1.2.ttl) | Fabric surface density, thread count, breathability and structured SI units. | Core, Structure, Common | Inherited: Product, Property. | Q: supplied characteristic values and quantities; no dimensional verification. |
| [03 process](example-03-process-v1.1.2.ttl) | Weaving/dyeing types and executions, parameter settings, chemical use and separate digital product instructions. | Core, Process, Associated Materials, Common | Explicit: webLink. Inherited: Product, Substance and instruction/property semantics. | Q: quantities; no general process/instruction validation. |
| [04 durability](example-04-durability-v1.1.2.ttl) | Shirt durability, pilling resistance/observation and colour fading. | Core, Durability | Inherited: Product, Durability, Property. | -; no general durability validation. |
| [05 associated materials](example-05-associated-materials-v1.1.2.ttl) | Jacket zipper/material, packaging material and separate finishing chemical/execution. | Core, Associated Materials, Process | Explicit: MaterialOfComposition, MaterialType, hasMaterialType. Inherited: Product, Substance; packaging alone does not imply MaterialOfComposition. | -. |
| [06 assessment](example-06-assessment-v1.1.2.ttl) | T-shirt abrasion method, standard reference, execution, cycle setting, result and threshold. | Core, Assessment, Durability, Common | Inherited: Product, Property. | Q: setting, measured value and threshold; no method-conformity check. |
| [07 indicator](example-07-indicator-v1.1.2.ttl) | Shirt robustness indicator derived from two results, with assumptions. | Core, Indicator, Assessment, Durability, Common | Inherited: Product and durability semantics. | Q: quantitative value; no score calculation. |
| [08 context](example-08-context-v1.1.2.ttl) | Annual washing-frequency and categorical drying-practice observations. | Core, Context, Process, Common | Inherited: Product. | Q: quantity and reference period. |
| [09 repairability](example-09-repairability-v1.1.2.ttl) | Jacket repair service, actor, guidance, conditions, assessment/result and repair event. | Core, Repairability, Associated Materials, Durability, Process, Assessment, Context, Common | Explicit: Actor, webLink. Inherited: Product, repair-event and property/instruction semantics. | Q: positive response time and nonnegative cost ratio. |
| [10 Textile SoC](example-10-textile-soc-v2.0.0.ttl) | Jacket substance presence, qualification, location/material group, concentration, threshold evaluation and handling. | SoC, Core, Associated Materials, Common | Explicit: CORE presence/qualification/concentration links, SoCQualificationAssertion, CriterionA and massFractionUnit. Inherited: Product and SOC/P_DPP anchors. | S + Q; also compatible with optional concentration completeness. |
| [11 recyclability](example-11-textile-recyclability-v1.1.2.ttl) | Shirt recycling route, stages, criterion results, scoring, recycled-content verification, event, yield and waste. | Core, Recyclability, Assessment, Indicator, Process, Associated Materials, Common | Inherited: Product, Property, recovered MaterialOfComposition and ProductEvent. | R + Q; relies on RDFS; no proof of actual recyclability. |
| [12 assessed aspects](example-12-assessed-aspects-v2.1.0-dev.ttl) | Fabric results separately bound to performance, pilling and structural aspects. | Core, Assessment, Durability, Structure, Common | Inherited: Product, Property. | Q; A when selected explicitly. |
| [13 assessment event](example-13-assessment-product-event-v2.1.0-dev.ttl) | Assessment execution, conceptual product event and separate EPCIS carrier. | Assessment | Explicit: ProductEvent, isRepresentedByCarrier. Carrier mapping definitions require the full EVENT source separately. | -; no event/carrier conformance guard. |
| [14 parameter values](example-14-parameter-values-v2.1.0-dev.ttl) | Protocol condition with numerical cycle count and application-defined coded setting. | Assessment, Common | No explicit CORE term or product instance. | Q: numerical/categorical alternatives and supplied values; no authoritative code-list membership check. |
| [15 awarded points](example-15-awarded-points-v2.1.0-dev.ttl) | Measured value versus awarded points; unscored and criterion results. | Assessment, Recyclability, Common | No explicit CORE term or product instance. | Q: supplied awards/quantities; not a complete route-wide report. |
| [16 assessment outcomes](example-16-assessment-outcomes-v2.1.0-dev.ttl) | Route-specific assessment and criterion results with application-defined overall conclusion. | Assessment, Recyclability | Product semantics through the assessment's product link. | R: assessment/result structure; no production outcome-value guard. |
| [17 assessment times](example-17-assessment-times-v2.1.0-dev.ttl) | Completion, duration, event/record times, coarse date and undated execution. | Assessment; external PROV-O, EPCIS and Dublin Core terms | Explicit: Product, ProductEvent, isRepresentedByCarrier; carrier mapping definitions require full EVENT separately. | - for timestamps; no production execution-time guard. |
| [18 constituent recycled content](example-18-recycled-content-constituent.ttl) | Shirt composition with two recycled-origin declarations relative to a polyester constituent's mass. | Core, Recyclability, Common | Explicit: MaterialOfComposition. Inherited: Product and MAT composition/type semantics. | R + Q: declaration structure, correct reference-mass property, fractions and mass consistency. |
| [19 reuse/preparation](example-19-reuse-preparation.ttl) | Non-waste shirt reuse versus discarded-jacket preparation for reuse. | Core, Process, Recyclability | Inherited: Product, including the textile waste resource. | -; legal waste status is not verified. |
| [20 care symbols](example-20-care-symbols.ttl) | Apparel product with digital instruction and two pilot care-symbol concepts. | Core, Process | Explicit: webLink. Inherited: Product, DigitalInstruction and hasProperty. | -; symbol selection and product suitability are not validated. |
| [Optional reference individuals](issue10-textile-reference-individuals.ttl) | One PEFCR and two testing-standard references; no product, LCA study or compliance claim. | Assessment; optional full CORE LCA definitions | Explicit: PEFCR. Load the relevant CORE graph explicitly; it is outside the active Textile import closure. | No dedicated default instance constraints on these references. |

## Product-level entry points

Start with **01** for a small product/composition/component graph, **10** for
explicit Textile + CORE substance reporting, and **18** for product composition
with CORE material constituents and distinct recycled-content mass bases.
Each provides a coherent view of an identified illustrative product and selected
related entities. None supplies a complete production DPP, verified real-product
identity or regulatory determination. Extending a graph requires agreed product
granularity, identifiers, evidence and an application-specific exchange scope.

## Filename versions and package loading

The retained `v1.1.2`, `v2.0.0` and `v2.1.0-dev` filename suffixes record example
history; they do not select the ontology version to load. All files in this
active directory are validated against the current integration package. Common
retains the `textile-connector#` term namespace, so existing `txtcon:` instance
terms require no renaming. Use historical example bytes only with the matching
historical package and its isolated catalogue; do not mix historical and current
closures. See [publication scope](../docs/PUBLICATION_SCOPE.md) and the
[CORE migration guide](../docs/CORE_2026_MIGRATION.md).
