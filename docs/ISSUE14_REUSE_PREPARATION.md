# Issue 14: reuse and preparing for reuse

Base: integration commit `5d54ad8081f7e4bc6cd6109a87de7725cd745084`.

`txtprc:ReuseProcess` means a process in which a textile product or component
that is not waste is used again for its original purpose. Directive 2008/98/EC
Article 3(13) provides the legal definition, explicitly cited in the class;
JRC Table 8 remains textile-domain evidence. The existing adapted-definition
classification remains appropriate because the legal definition is adapted to
the Textile domain. This clarifies the existing IRI
and may affect how previous instances are interpreted; no instance is silently
reclassified.

`txtprc:PreparingForReuseProcess` is a recovery process consisting of checking,
cleaning or repairing a textile product or component that has become waste so
that it can be reused without other pre-processing. Its legal basis is Directive
2008/98/EC Article 3(16). The JRC Preparatory Study section 9.2.6.1, printed
page 145, lines 4049-4053, discusses preparing for reuse as a textile waste
management pathway. The legal source is linked using `dcterms:references`; the
JRC source is separately recorded using `dcterms:source` and the project
traceability projection. Introducing a dedicated Textile class is a project
modelling decision, not a claim of an enacted ESPR DPP data requirement.

Both classes remain or are placed under `txtprc:EndOfLifeProcess`. That existing
superclass covers processes at or after the end of a use phase, including the
end of use by one holder. Another holder may reuse the product for its original
purpose without it becoming waste. Class membership alone does not entail legal
waste status. The definitions state the legal conditions, but current OWL and
SHACL profiles neither establish nor verify each input product's legal waste
status; data producers must select and support the appropriate classification.

No equivalence, disjointness, or subclass relation between the two process types is asserted, and preparing for reuse is not a
subclass of repair. Example 19 illustrates two process executions with existing
process type links; non-waste is context, not a formal negative status claim.

Recycling collection and schemes, `txtrec:TextileWaste` and its product
superclass, recycling routes, assessments, CORE and MIREOT remain unchanged.
The ontology has no new temporal waste status, legal operation code mapping or
generic collection architecture. Waste status is not automatically established
by a process type. Existing product/waste inferences and example 11 are retained.

The canonical process RDF delta against the base is one removed triple and 15
added: one replaced comment, three annotations on the existing class, and eleven
triples for the new class. There is no SHACL delta. The cumulative production
contract separately applies the explicit issue 14 graph delta after the earlier
approved integration decisions, preserving strict checks on all other graphs.

## Validation

- Five focused issue 14 tests passed, including RDFS and OWL RL inference and
  SHACL validation of the new and original recyclability examples. The additional
  historical graph restoration test passed with five negative restoration
  controls (six tests total).
- Thirty-four package, issue 9 process-boundary, issue 13 graph and Phase 4
  regressions passed. The complete issue 9 canonical graph restoration regression
  passed independently.
- All 20 public examples conformed under the default SHACL profiles. The public
  structural validator passed, parsing 187 RDF files.
- The cumulative production contract passed with the original frozen 2.0.0
  package explicitly located for the nested worktree: 13 canonical graphs, 799
  frozen checksums, 869 Phase 3 checksums and 20 historical import graphs.
  Git LFS and pytest temporary-directory restrictions required selected checks
  to run outside the sandbox; the existing frozen package was only read.
- Package checksum and manifest records refreshed; `git diff --check` passed.
  WIDOCO could not download the prior development version for an automatic
  changelog. The generated process documentation and canonical RDF exports passed
  public structural validation.
