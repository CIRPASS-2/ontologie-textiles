# Textile 2.0.0 resolver coordination brief

Prepared locally on 2026-10-27. This is a routing proposal for review, not a
deployment instruction. No redirects, canonical metadata or remote resources
were changed. Release publication remains subject to owner authorization.

## Complete identity and destination inventory

Notation: `E = https://w3id.org/eudpp/` and
`D = https://cirpass-2.github.io/ontologies-docs/Textile/2.0.0/`.
Every IRI below is the exact concatenation of E and its displayed suffix.
Every destination is the exact concatenation of D and its displayed path.
The machine-readable [HTTP record](../migration/resolver-http-observations.json)
contains all 20 full ontology IRIs, their actual declared version IRIs, canonical
source paths and individual responses. These destinations are proposed paths;
their existence is not asserted before deployment.

| Ontology IRI suffix (current alias) | Actual declared version IRI suffix | Proposed HTML | Proposed current Turtle |
|---|---|---|---|
| textile-assessment | textile-assessment/1.1.2 | assessment/index-en.html | package/ontology/textile-assessment.ttl |
| textile-associated-materials | textile-associated-materials/2.0.0 | associated-materials/index-en.html | package/ontology/textile-associated-materials.ttl |
| textile-connector | textile-connector/1.1.2 | connector/index-en.html | package/ontology/textile-connector.ttl |
| textile-context | textile-context/1.1.2 | context/index-en.html | package/ontology/textile-context.ttl |
| textile-core | textile-core/1.1.2 | core/index-en.html | package/ontology/textile-core.ttl |
| textile-durability | textile-durability/1.1.2 | durability/index-en.html | package/ontology/textile-durability.ttl |
| textile-indicator | textile-indicator/1.1.2 | indicator/index-en.html | package/ontology/textile-indicator.ttl |
| textile-ontology | textile-ontology/2.0.0 | index.html | package/ontology/textile-ontology.ttl |
| textile-process | textile-process/1.1.2 | process/index-en.html | package/ontology/textile-process.ttl |
| textile-recyclability | textile-recyclability/2.0.0 | recyclability/index-en.html | package/ontology/textile-recyclability.ttl |
| textile-repairability | textile-repairability/1.1.2 | repairability/index-en.html | package/ontology/textile-repairability.ttl |
| textile-soc | textile-soc/2.0.0 | soc/index-en.html | package/ontology/textile-soc.ttl |
| textile-structure | textile-structure/1.1.2 | structure/index-en.html | package/ontology/textile-structure.ttl |
| textile-actor-mireot | textile-actor-mireot/2.0.0 | package/docs/DEPENDENCIES.md | package/mireot/actor-textile-mireot.ttl |
| textile-con-mireot | textile-con-mireot/2.0.0 | package/docs/DEPENDENCIES.md | package/mireot/con-textile-mireot.ttl |
| textile-dpp-mireot | textile-dpp-mireot/2.0.0 | package/docs/DEPENDENCIES.md | package/mireot/dpp-textile-mireot.ttl |
| textile-event-mireot | textile-event-mireot/2.0.0 | package/docs/DEPENDENCIES.md | package/mireot/event-textile-mireot.ttl |
| textile-mat-mireot | textile-mat-mireot/2.0.0 | package/docs/DEPENDENCIES.md | package/mireot/mat-textile-mireot.ttl |
| textile-si-mireot | textile-si-mireot/1.1.2 | package/docs/DEPENDENCIES.md | package/mireot/si-textile-mireot.ttl |
| textile-soc-mireot | textile-soc-mireot/2.0.0 | package/docs/DEPENDENCIES.md | package/mireot/soc-textile-mireot.ttl |

The MIREOT guide is Markdown source, not a generated HTML representation. It is
listed as the proposed human-readable destination pending an agreed HTML guide
or source-view service. Do not advertise it as `text/html` as-is. Turtle-only
resolution with a documented source/guide link is a viable interim alternative.
The root landing page is a network guide, not a complete WIDOCO root rendering.

For each of the 12 non-root Textile modules, XML, N-Triples and JSON-LD downloads
are also available at `D + <module>/ontology.owl`, `ontology.nt` and
`ontology.jsonld`; `ontology.ttl` is an equivalent Turtle download. No equivalent
XML/JSON-LD root or MIREOT exports are promised by this package.

## Current HTTP observations and existing CORE routes

Read-only GET requests on 2026-10-27 at the UTC time in the linked JSON, with
redirect following disabled: all 40 active ontology and declared-version
endpoints returned **404**, with both `Accept: text/html` and `text/turtle`.
Lowercase `E + soc` also returned 404 for both. There were 94 requests in total,
including the following six CORE endpoints. A 404 does not establish namespace
ownership or permission to add a route. These observations cover initial
responses, not downstream availability or all possible media types.

All six CORE routes returned **303** for both Accept values, to
`https://dpp.vocabulary-hub.eu/api/ontology/-/version/OntologyVersion_` plus the
identifier below plus `/export?format=ttl`:

| Existing CORE suffix | Existing destination identifier (must remain unchanged) |
|---|---|
| ACTOR | e11d0f5e-fe86-4d51-86c4-53f9f66ac536 |
| MAT | 978009d5-042d-4d13-9ed6-7885433c1bce |
| EVENT | d3d95451-f2ac-4b4d-b2d0-5b413754591b |
| SOC | 11fcca33-b738-476a-a029-be53a333d81b |
| P_DPP | ab5a976e-95f4-4363-87c9-3abd11ee556b |
| CON | a50b649e-28cc-4107-a8e6-b69c3a401944 |

Preserve these routes and all other existing CORE rules. Never replace uppercase
SOC with lowercase legacy soc, redirect CORE modules to Textile MIREOT subsets,
or claim ownership of the shared `https://w3id.org/eudpp#` term namespace.
The six probes are a bounded inventory, not a claim that no other CORE routes exist.

## Nine retained module version identities

The nine modules assessment, connector, context, core, durability, indicator,
process, repairability and structure still declare `/1.1.2`. Their canonical
documents carry the approved creator additions; their bytes therefore differ
from the historical 1.1.2 documents. Versionless imports in those documents also
resolve differently in the active and historical catalogues. They are not
byte-unchanged historical documents. SI also retains `/1.1.2`, but its source
bytes are unchanged. This proposal does not invent any `/2.0.0` version IRI for
these ten graphs or change their accepted metadata.

The [nine-module comparison](../migration/retained-version-identities.json)
records exact current/historical hashes and each import's target in both
catalogues. All nine graphs are isomorphic to their historical counterparts
after excluding only `dcterms:creator`; all nine byte hashes differ. Thus the
direct graph difference is creator metadata, while the transitive runtime
context also changes. Reproduce this comparison offline with
`python -B scripts/observe_textile_resolvers.py --retained-only`.

Distinguish four concepts:

| Concept | Meaning and proposed treatment |
|---|---|
| Historical ontology identity | A declared old version IRI, such as `E + textile-connector/1.1.2`; pin to the exact preserved historical file, never the creator-updated candidate. |
| Current released ontology document | The reviewed canonical graph selected for a release, including its existing metadata; publication is still pending here. |
| Release-package snapshot URL | An immutable document address such as `D + package/ontology/textile-connector.ttl`; its 2.0.0 path identifies the package snapshot, not a newly minted ontology version IRI. |
| Current versionless alias | `E + textile-connector`; after authorization it may select the current released document through content negotiation. It is not a reproducible historical selector. |

**Recommendation:** keep the accepted metadata unchanged in this release; route
old version-specific IRIs to exact preserved old bytes and route current aliases
to reviewed 2.0.0 snapshot documents. Document that the retained `owl:versionIRI`
does not identify the current package's bytes for those nine modules. Resolve
current packages with the active offline catalogue; load historical packages in
a separate resolver session. This preserves old identities with the least
disruption, but requires explicit owner and namespace-maintainer agreement to
the documented identity limitation.

Alternatives requiring an explicit decision: (1) a later, separately authorized
metadata revision giving the affected modules distinct current version IRIs;
(2) leave historical HTTP aliases unresolved and support history only through
the preserved catalogue until maintainers can guarantee correct routing. Serving
modified bytes at an old version-specific IRI is not an acceptable alternative.

## Historical closure and content negotiation

For historical `/1.1.2` and SoC MIREOT `/1.1.3`, use exact corresponding files
under `D + package/migration/historical/1.1.2/ontology/` or `mireot/`.
If a legacy lowercase `/soc` route is agreed, use only the preserved
`dependencies/soc.ttl` in that historical subtree. There is no historical CON
MIREOT. Do not synthesize one or regenerate any historical RDF.

An old versioned entry file alone does not ensure historical closure: its imports
are absolute versionless IRIs. Reproducible loading requires the preserved
`migration/historical/1.1.2/catalog-v001.xml`, paths relative to that directory,
network fallback disabled and no simultaneous active catalogue. Use separate
ontology managers for history and current data. The root and SoC historical
closures remain 19 and 12 graphs respectively. A package snapshot URL without
its catalogue is not a promise of an isolated HTTP import closure.

At the namespace resolver, negotiate HTML and RDF with explicit Accept handling,
303 responses where appropriate, `Vary: Accept`, correct destination media types,
and an agreed default/406 policy for unsupported formats. Test q-values and
fragment-bearing term IRIs as well as ontology IRIs. GitHub Pages cannot execute
server redirect rules; negotiation belongs to the namespace service. Place
explicit historical/version routes before broad versionless aliases. Keep old
public documentation paths available; do not overwrite them with 2.0.0 content.

## Responsibilities and authorization questions

CIRPASS-2 owns preparation of reviewed Textile files, immutable package paths,
checksums, documentation hosting, source/release sign-off and post-deployment
destination tests. Existing eudpp namespace maintainers own resolver configuration,
rule precedence, content negotiation, protection of existing CORE routes,
resolver review/deployment and rollback. Neither party's preparation authorizes
the other's deployment. A named maintainer and the authoritative configuration
repository remain to be confirmed; no guessed configuration path is proposed.

Before any remote action, agree:

- Who maintains eudpp routing, where is its authoritative configuration, and who
  reviews/deploys Textile-only rules while preserving all CORE routes?
- Do owner and maintainers accept the nine-module identity policy above, or
  require a separate metadata decision before routing current aliases?
- Which historical aliases are supported, and who guarantees exact old bytes
  and explains catalogue-bound closure rather than mixed HTTP imports?
- What are the HTML destination for MIREOTs, supported Accept formats/defaults,
  cache/rollback policy and post-deployment acceptance tests?
- Who authorizes source merge, documentation deployment, release artifacts and
  version tag, and when may versionless aliases advance to 2.0.0?

No merge, tag, push, publication or redirect implementation is authorized by this
brief. The accepted 2.0.0 target and separate documentation path remain unchanged.
