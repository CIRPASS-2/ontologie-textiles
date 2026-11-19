# TXT-DEC-016: Approved issue #9 CORE alignment clarifications

Status: approved for local implementation and independent review; not a release.
Baseline: `40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`.

## Decision boundary

The five issue #9 proposals retain bounded MIREOT imports, existing CORE IRIs,
all classes/properties and every logical axiom. The exact annotation transition
is recorded in `migration/issue9-annotation-delta.json`. Version identities and
catalogue mappings remain unchanged; no new development version is introduced.
No upstream dependency adoption or other issue's modelling decision is included.

## 1. Retain controlled CORE extraction

[Architecture](../ARCHITECTURE.md) explains controlled commitments, offline
reproduction and maintenance responsibility. [Dependencies](../DEPENDENCIES.md)
identifies the snapshots, hashes and extraction scopes. Selection limits exposure
to unrelated axioms but does not guarantee full compatibility or remove drift risk.

## 2. Clarify Textile meanings

The approved Durability definition is:

> Ability of a textile product to maintain over time its function and performance under specified conditions of use, maintenance and repair, with regard to the material, construction and appearance characteristics relevant to its intended use.

This is a project refinement informed by the JRC Textile Preparatory Study,
not a verbatim JRC or regulatory definition. Supporting context is Section
9.2.1.1, printed page 110, lines 2890-2911; Section 9.2.1.3, printed pages
112-115, lines 2968-3055; and Section 13.10.1.1, printed pages 468-469,
lines 11065-11094. The detailed evidence concerns apparel; broader textile
coverage is a project generalization. Examples and proxy/measurement limits
belong in the existing modelling note and durability documentation. The CORE
hierarchy and the IntrinsicDurability, parameter, failure and result distinctions
remain unchanged.

DurabilityIndicator remains derived interpretive information under Indicator,
with its existing non-logical relation to CORE QualityIndicator. The latter is
a product characteristic. No new subclass bridge is approved.

The CON 2.4.0 source snapshot `dependencies/current-core/connector.owl` defines
`dpp:concernsProduct` with domain `dpp:ProductEvent` and range `dpp:Product`.
It is deliberately excluded from the selected CON MIREOT and the 20-graph Textile
runtime closure (see TXT-DEC-010). The separate local properties are retained
without an OWL alignment. A hypothetical subproperty bridge from either local
property, with the relevant full CORE axioms loaded, would infer `dpp:ProductEvent`
for the indicator or process execution subject. See the maintained WIDOCO
descriptions for their different local domains, ranges and relationships.

## 3. SOC migration already implemented

[TXT-DEC-010](TXT-DEC-010.md) remains authoritative for the implemented SOC 2.2.0
migration. No historical SOC URI occurs in an active logical position; historical
references remain provenance. Local extensions supply structured reporting and
comparison information absent from or not sufficiently represented by selected
CORE. Generic candidates may be discussed with CORE maintainers, without implying
approval for inclusion or permission to edit CORE.

MaterialGroup's current comment reflects its TextileProductPart superclass.
Threshold-purpose annotations now condition operational/regulatory consequences
on applicable rules and context. A comparison does not itself establish legal
non-compliance, mandatory reporting, exemption eligibility or treatment obligations.
Thresholds, expressions and evaluation results retain their existing distinctions.
The local qualification appliesToProduct remains separate from the CORE property
whose domain is dpp:DPP; no subproperty bridge is approved.

The 42-resource historical SOC attribution inventory preserves its original
70 definition/comment statements. Current clarifications do not rewrite that
historical evidence or create a logical dependency on it.

## 4. Identify selected CORE versions

The README records ACTOR 2.2.0, CON 2.4.0, EVENT 1.0.0, MAT 1.1.0,
P_DPP 2.2.0 and SOC 2.2.0, verified against the selected source headers.
Upstream module version, local snapshot bytes and extraction version are distinct.
No unsupported upstream commit identifier is asserted.

## 5. Govern future adoption

The [governance workflow](../governance/upstream-dependency-governance.md)
compares full candidate sources and evaluates actual Textile reuse commitments,
then requires an explicit adoption decision and a separately approved update.
Historical EVENT/SOC examples remain explicitly historical.

## Verification contract

The canonical graph transition must contain only the exact approved literal
annotation replacements: zero logical additions/removals and no entity changes.
Existing frozen proofs are checked after reversing only that verified transition;
no annotations or predicates are excluded wholesale. MIREOTs, sources, catalogue,
examples, SHACL and traceability CSVs remain byte-protected. Generated outputs
are reproduced from canonical sources, and local package hashes describe this
review worktree rather than authorizing publication.
