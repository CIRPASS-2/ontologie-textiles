# October 2026 CORE migration work area

This directory is outside the current publication manifest and active import
closure. It holds migration inputs and historical preservation, not a release.

Accepted baseline: `1ca2aa89241785dedeab430247bc9947daf69881`.
Migration branch: `migration/october-2026-core-2.0.0`.
Proposed future candidate: **2.0.0**, pending semantic implementation and validation.
The upstream dependency governance policy bases Textile version consequences on
observable semantic changes rather than upstream version numbers. The owner's
breaking-change decision therefore supports a new major candidate. The active
package VERSION and ontology version IRIs have not yet been changed.

## Preserved baseline

`historical/textile-1.1.2-1ca2aa89241785dedeab430247bc9947daf69881.zip`
contains 648 exact Git blobs: the accepted manifest's current package and
preserved reference inventory, plus WIDOCO generation inputs. This includes
historical dependencies, MIREOT graphs, catalogue, ontology versions, examples,
documentation, generated WIDOCO outputs, diagrams, traceability and checksums.
The SoC MIREOT retains its original 1.1.3 declaration and catalogue aliases.

The archive SHA-256 is
`4384bfd9f8f4e8a0ce1a6b7a7fd679d2190d9be33df87b2f181207aa78a46e74`.
`historical/inventory.json` records every member's SHA-256. The preparation
script verifies every accepted SHA256SUMS entry against its Git blob, then
verifies the stored ZIP members against the inventory. ZIP entry ordering,
timestamps, permissions and storage method are fixed for reproducibility.

Extract the archive into a separate directory to use the historical package's
catalogue and validation tools. Do not combine historical graphs with the
future migrated runtime. No historical version IRI has been redirected.

## Staged current CORE

`core-sources/` contains unchanged owner-designated ACTOR, CON (`connector.owl`),
EVENT, MAT, P_DPP and SOC sources, plus their README and licence.
`core-sources/SHA256SUMS` records their byte digests. IDENT is deferred and is
not staged. No source is imported into the active package at this point.

Reproduce with `python migration/prepare_inputs.py --core <source-directory>`.
The script refuses to overwrite preserved files with different bytes.

## Validation and implementation status

Before edits, the full offline validator passed: 595 package files, 19 runtime
graphs, 96 parsed RDF files, 11 examples, 16 SHACL scenarios, six reasoning
scenarios and the RDFS negative control. All 30 existing pytest tests passed.
Initial sandbox runs had temporary-directory permission errors; an approved
run outside that restriction passed. These were environment setup errors.

The independent harness improvement in `scripts/validate_public.py` now checks
the existing SHACL contracts one-to-one: focus node, owning named shape for
anonymous property shapes, actual constraint component, result path, severity
and optional message digest. Duplicate results and duplicate expectations
cannot satisfy each other. Eleven discriminating matcher tests pass. Existing
expected-result contracts have not been rewritten. The runtime suite passes
with strict matching enabled: all 11 examples, 16 SHACL scenarios, six
reasoning scenarios and the RDFS negative control remain valid. Package
structural checks pass with 596 manifest members after adding the matcher test.

Stage 1 is partially complete: branch, historical preservation and source
staging are ready. Bounded extraction and new MIREOT identities remain pending.
Stage 2 has not started. Stage 3 has the independent matcher improvement only.
Stage 4 has only the manifest/checksum maintenance required by that improvement.
Documentation, traceability, diagrams and WIDOCO remain baseline artefacts;
they have not been presented as migrated outputs.

## Required input

The task designates the **final reconciliation specification** as the primary
implementation contract, but supplies neither its contents nor its location.
It was not found in this repository. The owner decisions OD-01 through OD-06
are recorded in the task but do not specify the complete accepted term mapping,
bounded CON selection, P_DPP/EVENT changes or retained Textile extension design.

Provide that specification before implementing those dependent changes. No
substitute audit, upstream provenance investigation or invented semantic
mapping has been performed. This is missing implementation authority, not a
request to approve a new semantic design. No release approval is claimed;
no push, merge, tag or publication is authorised by this work.
