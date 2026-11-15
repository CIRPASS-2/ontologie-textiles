# Changelog

## 2.1.0-dev - issue #20 point 6 - 2026-11-15

Document optional PROV start/completion timestamps and coarse dcterms:date values
on assessment executions. Add an isolated synthetic example and focused tests
for precision, result lookup and EPCIS independence. Keep ontology schemas,
imports, versions, production SHACL and all earlier corrections unchanged.

## 2.1.0-dev - issue #20 point 5 - 2026-11-12

Add the optional independent hasAssessmentOutcome relation for controlled result
conclusions under the applied method and context. Keep aggregate recyclability
verdicts separate from criterion outcomes and use only synthetic application
concepts in the example. Preserve all production SHACL profiles; exercise the
optional supplied-value guard in tests. No new vocabulary class, code list or
decision rule is added. See TXT-DEC-015.

## 2.1.0-dev - issue #20 point 4 - 2026-11-10

Add awardedScoreValue for points actually awarded to individual assessment
results, distinct from measurements, prescribed rule points and indicators.
Validate only supplied award values as decimal, dimensionless QuantitativeValues.
No mandatory awards, score bounds or calculation are introduced. Preserve points
1-3, other ontology sources and existing shapes. See TXT-DEC-014.

## 2.1.0-dev - issue #20 point 3 - 2026-11-09

Add hasParameterConcept for categorical protocol-setting values. Change only the
measurement-parameter setting shape to inclusive numerical/categorical presence,
keeping numerical checks unconditional and allowing multiple concepts. Advance
only the changed quantitative profile version IRI to 2.1.0-dev with explicit
maintainer approval. Points 1 and 2 and other shapes are preserved. See TXT-DEC-013.

## 2.1.0-dev - issue #20 point 2 - 2026-11-09

Add the optional ASSESSMENT isRepresentedByProductEvent bridge and a direct
import of the existing bounded EVENT MIREOT. Keep assessment executions,
conceptual ProductEvents and technical EPCIS carriers distinct. Preserve the
point-1 correction and existing PROCESS/EVENT definitions. See TXT-DEC-012.

## 2.1.0-dev - issue #20 point 1 - 2026-11-09

Add resultForAssessedAspect to ASSESSMENT, linking a MeasurementResult to its
individual assessed subject. Provide opt-in target checking without cardinality constraints;
the baseline remains compatible. Add
multi-result, degradation and structural examples and negative/inference tests.
Preserve the 2.0.0 baseline in existing Git history. Only ASSESSMENT
and the network advance version identity. No other issue point is implemented,
and no release is published. See TXT-DEC-011.

## CORE MAT classification alignment - 2026-11-02

Addressed Nader Jelassi's source PR #19 review: FibreTypeConcept now subclasses
CORE MaterialType and hasFibreType specializes CORE hasMaterialType. These two
project-approved OWL bridges preserve SKOS classifications, structured
composition and product roles. No JRC-prescribed alignment is claimed.
Removed the obsolete local skos:closeMatch declaration from Textile Connector
and corrected the fibre-composition and PackagingMaterial modelling notes.
Candidate version identities, six creators, CORE/MIREOT inputs and historical
bytes remain unchanged. See the
[finalization record](migration/PUBLICATION_CANDIDATE_FINALIZATION.md).

## Final creator metadata update - 2026-10-27

Added Ivo Ladenius, Andreas Schneider, Jan Merckx and Piero de Sabbata as
creators on all 13 Textile ontology headers, preserving Elio Hbeich and
BOUGACHA Racem. Canonical graphs change only by those 52 creator triples.
Regenerated all twelve WIDOCO modules and the network landing page. The owner
also approved normalizing 27 previously inconsistent non-Turtle documentation
exports to their canonical sources; exact differences are recorded in
[creator update evidence](migration/CREATOR_UPDATE.md). Candidate version and
semantic axioms are unchanged.

## 2.0.0 candidate — 2026-10-27

Breaking migration to owner-designated October 2026 CORE: bounded SOC/CON,
updated P_DPP/EVENT and structurally compatible ACTOR/MAT reuse. Retained Textile
threshold expressions, evaluations, reference bases, reporting levels, parts,
regulatory sources and instructions. IDENT remains deferred.

E10 is now `example-10-textile-soc-v2.0.0.ttl`. V08/I08 retain maximum/range
threshold behaviour and the original inverted-range defect. Strict SHACL result
matching, a separate complete-report profile and migration/inference controls
cover the changed contract. Historical 1.1.2/SoC MIREOT 1.1.3 bytes are preserved.
No creator changes or publication approval are included.

## Targeted independent audit corrections

Historical catalogue isolation; attribution for 42 copied SOC definitions;
inverse and non-textile component membership; evaluation ownership; complete
96-resource mapping inventory; explicit converter failures; metadata and E10
restoration; bounded CON fidelity; additional constraint regressions.
See [correction evidence](migration/AUDIT_CORRECTIONS.md).

## 1.1.2 historical baseline

Accepted baseline `1ca2aa89241785dedeab430247bc9947daf69881` is preserved with
its original changelog, manifest, catalogue, sources and generated documentation.
