# Issue 17: textile care symbols

Base: `637b937481ccdfb87ca9798cb66549183453c167`.

The existing product-to-instruction pattern supports linked digital instructions,
but does not identify individual care symbols. `CareSymbolConcept` describes a
controlled representation of a care-labelling symbol. `hasCareSymbol` links a
`TextileCareInstruction` to such a concept. Instructions describe prescribed
care; symbols represent treatments or conditions; care methods describe process
techniques; process executions describe actual operations. Neither instruction
nor symbol entails an executed care process. Existing care classes and links,
including `CareMethodConcept` and the digital `dpp:webLink` pattern, are unchanged.

`CareSymbolScheme` is a small pilot, not a complete classification. Two project
concepts describe normal washing at maximum 70 degrees Celsius and flat drip
drying. Their references identify ISO 7000 registrations [3096](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Agrs%3A7000%3A3096)
and [3101](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Agrs%3A7000%3A3101),
both registered 2011-10-16. ISO's registry identifies their care-labelling
purpose and refers to ISO 3758. [ISO 3758:2023](https://www.iso.org/standard/74401.html)
is the relevant care-labelling code, and the [GINETEX overview](https://www.ginetex.net/fr/labelling/care-labelling/care-symbols/)
and [2023 standard preview](https://www.iteh.us/catalog/standards/cen/01e8ee25-4eb1-4c84-b067-f9a4d8cdbf0f/en-iso-3758-2023)
identify the corresponding treatments. These are Textile concepts informed by
the registrations, not copied ISO identifiers or verified exact mappings. The
ISO entries themselves cite ISO 3758 without identifying a particular edition;
possible graphical differences must be checked individually. No `skos:notation`,
`skos:exactMatch`, `owl:sameAs`, graphics or normative table is reproduced.
The source-locator projection marks project decisions as partial; ISO references
are retained explicitly as `dcterms:references`, not falsely projected as a
registered external source. [GINETEX](https://www.ginetex.net/en/care-labelling/)
states that the care graphics are protected trademarks in most countries; their
reuse and any reproduction of ISO material require a separate rights review.

Example 20 connects one illustrative apparel product to one digital instruction
with two symbol concepts. It does not assert that a real product qualifies for
those treatments. Multiple values are permitted, not required; no new SHACL
requirements, cardinalities or DPP obligations are introduced. Under RDFS and
OWL, the property domain infers a care instruction and the range infers a care
symbol concept; neither entails a care execution or process-method concept.

No new CORE class is assumed. A future adopted CORE label model might reference
existing Textile instructions and composition information, subject to its actual
published semantics and separate approval, without redefining that information
as a label. CORE issue #55 is outside Textile governance. Remaining decisions
include future vocabulary coverage, source and graphic licensing, ISO edition
management, and any optional exchange profile or CORE alignment.

## RDF delta and validation

Textile Process adds 55 RDF triples and removes none: one class, one object
property, one concept scheme and two concept individuals. The SKOS portion has
three concept/scheme type assertions and nine SKOS-predicate triples. Other
canonical ontology graphs, production SHACL and dependency/MIREOT graphs are
unchanged. The cumulative production contract checks the exact additive graph.
Focused issue 17 tests and issue 14 compatibility controls passed, including
RDFS/OWL reasoning and SHACL validation of the original and new examples. The
cumulative contract verified 13 canonical graphs, 799 frozen checksums and 869
Phase 3 checksums. Generated Process documentation and RDF downloads are updated;
the WIDOCO automated changelog could not retrieve the previous development IRI.
Public runtime validation passed all 21 examples, 16 SHACL scenarios and six
reasoning scenarios, including its RDFS negative control. Public structural
validation parsed 188 RDF files and checked the package manifest and checksums.

The traceability projection uses issue-specific notes for the five new resources,
retaining their `PARTIAL` status and all prior evidence rows. Recursive SHACL
regression compares the full inventory and contents, including nested profiles.
