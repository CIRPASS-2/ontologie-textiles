# Issue #10: LCA reuse and textile reference data

[Issue #10](https://github.com/CIRPASS-2/ontologie-textiles/issues/10)
requests textile-specific references and no duplicate LCA model. Its available
activity contains no substantive comments. The supplied LCA 3.1 source has no
`owl:imports` declarations; its descriptive dependency text mentions ACTOR
and P_DPP via CON. Its origin and digest are recorded in [Dependencies](DEPENDENCIES.md).

`TextileProduct` is a subclass of CORE `Product`. CORE Connector defines
`hasLCAStudy` with domain `Product` and range `LCAStudy`; this relationship
is available when the upstream Connector is loaded, but is not in the active
Textile MIREOT. CORE LCA defines `followsPEFCR` from `LCAStudy` to `PEFCR`.
It also defines `hasComplianceDeclaration` from `LCAStudy` to
`ComplianceDeclaration` and `referenceToComplianceSystem` from that
declaration to `ComplianceSystem`. These domains and ranges entail the
respective subject and object types when used. `PEFCR` and `ComplianceSystem`
are separately declared subclasses of `Source`; no subclass, equivalence,
or disjointness between the two is asserted by this integration. A compliance
declaration is a separate claim, not implied by following a PEFCR.

Textile assessment already supplies `TestingStandard`, `AssessmentStandard`,
`definesMethod`, `isDefinedByStandard`, `appliesMethod` and `assessesProduct`.
Existing CORE and Textile terms can express product studies, followed PEFCRs,
explicit compliance claims, standards and methods without a new Textile property
or a redundant `TextileProduct` relationship. LCA and Textile assessment are
not asserted to be interchangeable; no extra domain or range is introduced.

The [optional reference dataset](../examples/issue10-textile-reference-individuals.ttl)
provides one CORE `PEFCR` individual and two `TestingStandard` individuals,
using illustrative `https://example.org/textile/issue10#` identifiers,
existing semantics and official reference pages. It does not assert
a study, compliance claim, regulatory obligation or standard-to-method link.
Load the dataset and the relevant CORE and Textile graphs explicitly. It is
not imported into a versioned ontology; this preserves the exact committed
`integration-2026-11.3` graph identities. Choosing to make these references
part of an ontology release requires an owner-approved new version and
placement. No LCA MIREOT is warranted because no active Textile ontology uses
LCA terms. The catalogue mappings enable explicit offline access only.

The PEFCR is represented as a `PEFCR`, not also as a `ComplianceSystem`:
whether a distinct compliance-system representation should be curated remains
a governance decision. ISO confirms [4484-1](https://www.iso.org/standard/82238.html)
and [4484-3](https://www.iso.org/standard/81035.html) as distinct published
2023 testing standards. The [Commission](https://environment.ec.europa.eu/news/new-eu-rules-measuring-environmental-impact-clothes-and-shoes-2025-06-25_en)
describes the apparel and footwear PEFCR; no delegated-act requirement is
asserted. Future passport requirements remain outside this change.
