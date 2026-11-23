# Publication scope and historical preservation

This unpublished integration candidate comprises 13 Textile modules and seven
bounded MIREOT graphs. The package uses integration-2026-11.2 and each Textile
module declares a distinct development version IRI. Only that 20-graph import closure is used for current runtime validation.
Full current CORE snapshots and historical RDF are reference inputs, not runtime
imports. No release approval or publication is claimed.

`CURRENT_PACKAGE` in `PUBLICATION_MANIFEST.txt` enumerates owned package areas,
including the migration specification, reproducibility scripts, historical archive
and extracted historical runtime. SHA256SUMS covers every member except itself.
The 1.1.2 archive has its own immutable inventory and catalogue. Textile 2.0.0
is separately frozen from the approved Git baseline in the sibling package
`dpp-textiles-frozen-2.0.0`, whose own catalogue and 799 checksums are verified.
Use one selected catalogue per load and disable network fallback.

`PRESERVED_REFERENCE_MATERIAL` lists the three earlier Graphwise reference files.
They remain outside current runtime and the direct checksum contract. Their
historical archive copies are preserved as ZIP members; unpacked Graphwise
copies are excluded from the current package inventory. No current catalogue
entry points to a Graphwise graph. The two earlier root Textile drafts remain
in Git history. See [dependencies](DEPENDENCIES.md) and
[migration treatment](CORE_2026_MIGRATION.md).

Historical 2.0.0 bytes are preserved in Git and in the frozen local package.
A deliberately selected historical catalogue resolves its offline closure; this
does not verify public HTTP dereferencing or deployment. See the
[issue #12 decision](ISSUE12_MATERIAL_COMPOSITION.md),
[CORE migration guide](CORE_2026_MIGRATION.md), and the
[1.1.2 historical catalogue](../migration/historical/1.1.2/catalog-v001.xml).

The committed `.1` package is reproducible from its pinned Git snapshot with
`python -B -m scripts.reconstruct_phase2b` and an absent destination. Its
catalogue must be selected independently of `.2`; public HTTP resolution is
not established by these local checks. Common and Connector are separate
ontology identities, with the latter generated as a complete compatibility graph.
