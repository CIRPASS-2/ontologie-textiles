# TXT-DEC-010 — October 2026 CORE migration

The owner authorises a breaking 2.0.0 candidate using bounded SOC 2.2.0,
CON 2.4.0, P_DPP 2.2.0, EVENT 1.0.0, ACTOR 2.2.0 and MAT 1.1.0 sources.
The final reconciliation (M1–M9, A1–A9) and OD-01 through OD-06 govern this
implementation. IDENT is deferred.

Positive SoC relationships entail SubstanceOfConcern. Qualification applicability
remains presence-scoped. Generic TextileChemicalSubstance remains a Substance.
Concentration is mandatory only in the separately selected complete-report
profile. Structured locations, material groups, denominators, regulatory source
references, thresholds, evaluations and free-text instructions remain Textile-owned.

Exact/maximum/range threshold expression roles specialise the existing common
QuantitativeValue. The common quantitative SHACL profile permits precisely these
three roles: ordinary values still require their scalar; maximum and range roles
receive their own scalar/endpoint validation. Its ban on arbitrary new quantity
subclasses remains. This deliberate extension reconciles A4 with the old scalar-only
profile; it does not suppress the original regression constraints.

Concentration wrappers are removed only when uniquely owned and metadata do not
conflict. Node correspondence records the transfer. Unknown identifier schemes
remain unknown. Mass fractions retain their decimal ratios and use approved SI
unit identities; no unit owl:sameAs is introduced.

An evaluation refers to an explicitly applicable threshold interpreted in that
concentration's scope. Explicit threshold basis/level/part overrides must agree.
For non-negative mass fractions, maximum-only reports represent [0, maximum].
Strictly separated intervals support BelowThreshold/AboveThreshold. Exact equality
supports AtThreshold; overlapping intervals support only an indeterminate result.
These vocabulary values assert a comparison, not compliance or exemption.

Historical catalogue and RDF bytes are preserved separately. Previous version
IRIs resolve to those bytes; the new closure excludes all legacy SOC identities.
Only changed module graphs receive 2.0.0 candidate identities. No release or
creator-metadata approval is implied.
