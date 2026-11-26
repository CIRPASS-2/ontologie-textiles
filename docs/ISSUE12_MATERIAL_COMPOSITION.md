# Issue 12 material composition: implementation record

Base: 40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b. Development identity: 2.1.0-issue12-dev; 2.0.0 remains the historical baseline in Git and is not remapped to the development graph. The active catalogue does not resolve Textile 2.0.0 version IRIs locally. This branch is independent of issue 16 and PR 21.

| Reviewer proposal | Approved decision | Change |
|---|---|---|
| Replace fibre properties with CORE | Retain the three textile properties, FibreCompositionComponent, its MAT superclass and hasFibreType superproperty. Defer product-to-hasMaterial alignment pending CORE confirmation. | Documentation and constituent definition clarification; no new property axiom. |
| Replace mass fraction with CORE percentage | Retain quantitative node and profile. Conversion requires matching material, mass basis, denominator, unit and scale. | Documentation only; no conversion or alignment. |
| Remove the textile constituent class | Retain and clarify the contextual material constituent, its existing restrictions and IRI. | Class comment changed. |
| Replace non-textile parts with CORE products | Retain TextileProductPart specialization and existing part properties. Product typing and CORE isComponentOf are not universal. | No structural change. |
| Remove packaging from textile composition | Retain packaging class, properties and controlled types; remove only unconditional MAT superclass. No disjointness. | One subclass triple removed; comment and modelling note clarified. |

Baseline inference, full selected import closure: fibre entry is MaterialOfComposition and its fibre type entails hasMaterialType; the product-to-entry edge does not entail hasMaterial. An ordinary non-textile component is neither Product nor MaterialOfComposition solely through its part type. PackagingMaterial was inferred as MaterialOfComposition; after removal it is not entailed for a minimal packaging example unless an independent assertion or property supplies that type. Explicit typing remains permitted.

The source ontology cites the JRC Preparatory Study as domain motivation. Regulation (EU) No 1007/2011 Articles 5, 9, 11 and Annex I provide relevant legal context, not retroactive provenance. See the modelling guide for the scope and limitations. No comprehensive compliance validator is claimed.

Canonical semantic difference: one removed subclass triple. Annotation differences: fibre constituent comment; packaging material comment and modelling note. Development version, prior-version and citation metadata change for the thirteen Textile ontology headers. No changes to CORE or MIREOT. Historical graph proofs restore the exact approved changes before applying prior frozen checks. Generated exports and validation/package metadata reflect the development graphs.

CORE coordination: confirm whether hasMaterial connects a product to a contextual material-of-composition individual used in this manner; determine any future material percentage conventions and mappings. PR 21 integration must reconcile development identities, shared ontology documentation and generated exports. Issue 16 integration must reconcile the Connector-to-Common migration, metadata and generated artifacts without dropping either branch's approved axioms.

The packaging regression tests the bounded closure separately from the selected full CORE CONNECTOR snapshot. OWL RL checks are not complete OWL DL consistency proofs. The negative fraction case checks the focus node, value path and MaxInclusive constraint component.
