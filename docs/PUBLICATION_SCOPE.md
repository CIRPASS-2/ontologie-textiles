# Development scope and published preservation

The working package is an unpublished 2.1.0-dev implementation of issue #20
points 1-5. ASSESSMENT and the network entry point advance; all other modules and
MIREOTs retain their prior bytes. The complete 2.0.0 baseline remains in Git at
`40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b`; use a separate checkout and its original
catalogue to load it. No duplicate package archive is added. The development
catalogue does not redirect changed 2.0.0 version IRIs to new source graphs.

The published 2.0.0 baseline comprises 13 Textile modules and seven bounded MIREOT
graphs. Only that 20-graph import closure is used for current runtime validation.
Full current CORE snapshots and historical RDF are reference inputs, not runtime
imports. No release approval or publication is claimed.

`CURRENT_PACKAGE` in `PUBLICATION_MANIFEST.txt` enumerates owned package areas,
including the migration specification, reproducibility scripts, historical archive
and extracted historical runtime. SHA256SUMS covers every member except itself.
The archive has its own immutable per-member inventory and digest. Previous
version identities resolve to original bytes, and its standalone catalogue
reproduces the historical closure. Never mix historical and current runtimes.

`PRESERVED_REFERENCE_MATERIAL` lists the three earlier Graphwise reference files.
They remain outside current runtime and the direct checksum contract. Their
historical archive copies are preserved as ZIP members; unpacked Graphwise
copies are excluded from the current package inventory. No current catalogue
entry points to a Graphwise graph. The two earlier root Textile drafts remain
in Git history. See [dependencies](DEPENDENCIES.md) and
[migration treatment](CORE_2026_MIGRATION.md).
