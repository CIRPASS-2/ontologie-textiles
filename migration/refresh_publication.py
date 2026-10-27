"""Refresh candidate documentation, traceability, manifest and byte checksums."""
import hashlib
import json
import zipfile
from pathlib import Path
from rdflib import RDF, OWL
from scripts import validate_public as v

ROOT=v.ROOT


def write(path,text):
    (ROOT/path).write_text(text.replace('\r\n','\n').rstrip('\r\n')+'\n',encoding='utf8',newline='\n')


def baseline_text(path):
    with zipfile.ZipFile(next((ROOT/'migration/historical').glob('*.zip'))) as archive:
        return archive.read(str(path).replace('\\','/')).decode('utf8').replace('\r\n','\n')


def documentation():
    resources,evidence,sources,_=v.derive(v.ontology_graph(ROOT))
    for name,fields,rows in [('textile-resource-traceability.csv',v.RESOURCE_FIELDS,resources),('textile-resource-evidence.csv',v.EVIDENCE_FIELDS,evidence),('source-documents.csv',v.SOURCE_FIELDS,sources)]:
        (ROOT/'traceability'/name).write_bytes(v.csv_bytes(fields,rows))
    stats=v.summary(resources,evidence,sources)
    text=baseline_text('README.md')
    start=text.index('The 13 Textile ontology graphs declare version')
    end=text.index('## Package contents',start)
    text=text[:start]+'''The proposed breaking-change candidate is **2.0.0**. Changed Textile SOC,
Associated Materials, Recyclability and the network entry point declare new
2.0.0 candidate identities. Unchanged Textile modules and SI retain 1.1.2.
Six rebuilt CORE subsets declare 2.0.0 candidate identities; together with SI
they form seven MIREOT graphs and a 20-graph runtime closure.

Load [ontology/textile-ontology.ttl](ontology/textile-ontology.ttl) with the local
[catalogue](catalog-v001.xml). Historical version IRIs resolve to preserved bytes,
including SoC MIREOT 1.1.3 and its former 1.1.2 alias. The old lowercase SOC
ontology identity resolves only to its historical source. For a historical
runtime use the preserved standalone historical catalogue, never a mixed closure.
See the [migration guide](docs/CORE_2026_MIGRATION.md).

'''+text[end:]
    text=text.replace('python -B -m pytest -p no:cacheprovider tests/test_public_package.py -q','python -B -m pytest -p no:cacheprovider tests -q\npython -B scripts/validate_public.py --full --complete-report')
    text=text.replace('These three profiles are selective application constraints','The three structural profiles and optional complete-report profile are selective application constraints')
    text=text.replace('**838 resources**',f"**{stats['resource_count']} resources**")
    text=text.replace('| projectDecision | 55 |',f"| projectDecision | {stats['categories']['projectDecision']} |")
    for module in ('textile-soc','textile-associated-materials'):
        import re
        text=re.sub(r'\| '+module+r' \| \d+ \|',f"| {module} | {stats['modules'][module]} |",text)
    text=text.replace('This branch prepares the CIRPASS Textile Ontology Community Review Candidate 1.1.2 for publication in this repository.',
                      'This branch prepares a local 2.0.0 migration candidate; publication still requires owner approval.')
    text=text.replace('eight positive and eight negative SHACL fixtures, six RDFS/OWL-RL inference scenarios,',
                      'the original eight positive and eight negative SHACL fixtures, six RDFS/OWL-RL inference scenarios,')
    text=text.replace('Supply the ontology graph when executing SHACL.',
                      'The pytest suite additionally verifies forty-one migration scenarios, source fidelity, historical bytes, positive shape coverage and forbidden entailments. Merge the offline ontology closure with data when executing SHACL.')
    write('README.md',text)
    write('CHANGELOG.md','''# Changelog

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

## 1.1.2 historical baseline

Accepted baseline `1ca2aa89241785dedeab430247bc9947daf69881` is preserved with
its original changelog, manifest, catalogue, sources and generated documentation.
''')
    scopes=json.loads((ROOT/'migration/extraction-scopes.json').read_text('utf8'))
    lines=['# Dependencies and bounded reuse','',
           'The active closure contains 13 Textile graphs and seven MIREOT graphs.',
           'Full unchanged owner-designated sources in `dependencies/current-core/` are',
           'reference snapshots; they are not imported as full ontologies. IDENT, COMP',
           'and LCA are outside this migration.','',
           '| Subset | Source file | Source ontology | Selected source triples |',
           '|---|---|---|---:|']
    for key,record in scopes.items():lines.append(f"| {key.upper()} | `{record['source']}` | `{record['source_iri']}` | {record['copied_triples']} |")
    lines+=['','SI retains its approved 59-triple subset and 1.1.2 identity. See',
            '[SI provenance](../dependencies/SI_REFERENCE_POINT.md). Six rebuilt subsets',
            'have 2.0.0 candidate identities, distinct from upstream version numbers.',
            'Exact subject selections are in [extraction scopes](../migration/extraction-scopes.json).',
            'Tests compare their complete copied subgraphs, including anonymous axioms,',
            'against the supplied sources. New Textile definitions are outside MIREOT.',
            '', '## Source attribution', '',
            'Authoritative RDF and its embedded attribution/licence metadata are copied',
            'without editing. The supplied [CORE licence](../dependencies/current-core/LICENSE.md)',
            'and [README](../dependencies/current-core/README.md) accompany the sources.',
            'The current sources declare ACTOR 2.2.0, MAT 1.1.0, EVENT 1.0.0,',
            'P_DPP 2.2.0, SOC 2.2.0 and CON 2.4.0. Their digests are recorded in',
            '`dependencies/current-core/SHA256SUMS`.',
            '', '**Modified/extracted material notice:** each rebuilt MIREOT reproduces',
            'only selected source subjects and supporting axioms and adds a Textile',
            'ontology header. It is an extracted work, not the complete upstream module.',
            'Upstream terms remain externally owned. The Textile licence does not',
            'supersede upstream terms. The bundled Apache licence is retained.',
            '', '## Historical compatibility', '',
            'The accepted older dependency snapshots and MIREOT bytes are preserved in',
            'the [historical inventory](../migration/historical/inventory.json) and archive.',
            'The extracted historical runtime and its own catalogue are under',
            '`migration/historical/1.1.2/`. Root catalogue mappings for previous version',
            'IRIs and lowercase `/soc` target those original bytes. No equivalence or',
            'redirect bridges the legacy `soc#` vocabulary to the migrated runtime.',
            'See [migration guidance](CORE_2026_MIGRATION.md).','']
    write('docs/DEPENDENCIES.md','\n'.join(lines))
    text=baseline_text('docs/MODELLING_GUIDE.md')
    text=text.replace('For the supplied SoC dependency, exact, maximum and range quantitative expressions use the source ontology classes.',
       'Positive reports use CORE SubstancePresence and concernsSubstance, which entails SubstanceOfConcern typing. Applicable qualifications remain presence-scoped and must qualify that same substance. Concentrations use CORE scalar/range carriers directly; threshold expressions retain Textile roles beneath the shared QuantitativeValue. See [the migration patterns](CORE_2026_MIGRATION.md).')
    text=text.replace('../dependencies/p_dpp.owl','../dependencies/current-core/p_dpp.owl').replace('../dependencies/mat.owl','../dependencies/current-core/mat.owl')
    write('docs/MODELLING_GUIDE.md',text)
    text=baseline_text('docs/ARCHITECTURE.md')
    text+='''
## October 2026 CORE boundary

The runtime has 20 graphs: 13 Textile modules and seven bounded subsets. SOC
owns substance identity, positive presence, criteria and instructions. CON owns
the selected product/presence/concentration relations. P_DPP owns quantitative
property, concentration/threshold anchors and carriers. SI supplies approved units.
Textile owns structured parts/material groups, scopes, threshold value roles,
evaluation, source references and free-text instructions. Generic chemicals and
process executions keep their existing independent types. No general IDENT,
COMP or LCA integration is added. See [migration guidance](CORE_2026_MIGRATION.md).
'''
    write('docs/ARCHITECTURE.md',text)
    write('docs/PUBLICATION_SCOPE.md','''# Publication scope and historical preservation

This local 2.0.0 candidate comprises 13 Textile modules and seven bounded MIREOT
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
''')
    text=baseline_text('docs/SOURCE_TRACEABILITY.md')
    text+=f'''
## October 2026 migration

New retained Textile extension resources are project decisions documented in
[TXT-DEC-010](decisions/TXT-DEC-010.md). Their rows do not fabricate JRC evidence.
The projection now contains {stats['resource_count']} resources while retaining 904 evidence rows,
902 PRESENT_NOT_REVERIFIED and two UNRESOLVED relationships. Source registry
descriptions identify the adopted MAT 1.1.0 and EVENT 1.0.0 subsets. The seven
earlier locator supplements remain historical evidence statements; the migration
does not claim fresh documentary verification. The presence locator names the
current SubstancePresence pivot while retaining its ESPR source relationship.
'''
    write('docs/SOURCE_TRACEABILITY.md',text)
    text=baseline_text('traceability/README.md').replace('838 resources',f"{stats['resource_count']} resources").replace('282 resources have no external',f"{stats['zero_evidence']} resources have no external")
    write('traceability/README.md',text)
    for name in ('nader-review.md','upstream-dependency-governance.md'):
        path=ROOT/'docs/governance'/name
        text=baseline_text(path.relative_to(ROOT))
        banner='> Historical baseline examples below describe 1.1.2. The October 2026\n> adoption is implemented by [TXT-DEC-010](../decisions/TXT-DEC-010.md)\n> and the [migration guide](../CORE_2026_MIGRATION.md); policy rules remain in force.\n\n'
        if banner not in text:text=banner+text
        write(path.relative_to(ROOT),text)
    write('shacl/README.md','''# SHACL application profiles

The three default structural profiles cover shared quantities, recyclability
and Textile SoC. Merge the documented offline ontology closure with instance
data, use RDFS inference and disable remote imports. The validator performs
this merge explicitly. Recyclability retains its RDFS entailment declaration.
No profile requires OWL entailment during validation.

The SoC profile targets positive presences, qualification identity/context/source,
structured references, locations, denominator membership, concentration branches,
threshold expressions/evaluations and instruction text. It is a decimal mass-fraction
profile: approved unit IRIs are `units:one` and CORE `massFractionUnit`; values
remain ratios in [0,1]. Arbitrary or temperature units fail an IRI whitelist even
if domain/range inference gives them MeasurementUnit typing. Other quantity/unit
conventions require a separate justified profile, not numeric rescaling here.

Concentration is optional on partial presences. Add
`profiles/textile-soc-complete-report.ttl` explicitly to require it. The default
loader uses only top-level shape files. Use `--full --complete-report` to select
that additional profile in the public validator. Completeness here means the
additional concentration relationship, not ontology-wide regulatory completeness.

Named property and SPARQL constraint resources give stable result identities.
The matcher also resolves older anonymous property shapes by their actual named
container and path, and matches focus, component, path, severity and optional
message/source-constraint identity one-to-one. Forty-one migration scenarios retain
exact result multisets. Every targeted SoC shape has positive focus coverage
and discriminating negative coverage. The existing sixteen SHACL regression
scenarios and recyclability inference control remain unchanged in purpose.
''')
    for module,paragraph in {
      'soc':'Positive SoC reports use CORE SubstancePresence and concernsSubstance, with presence-specific qualification applicability. Concentrations use CORE scalar or range carriers. Textile retains separate threshold expression roles, structured locations and denominators, regulatory sources, evaluations and instruction text. Concentration completeness is a separately selected SHACL profile; IDENT is deferred.',
      'associated-materials':'TextileChemicalSubstance specialises CORE Substance without globally classifying generic chemicals as substances of concern. NonTextileComponent specialises the Textile-owned TextileProductPart. Material groups are structural reporting groupings and are not universally products or material occurrences.',
      'recyclability':'The recycled-content model remains Textile-owned. The obsolete RecycledMaterialsUse annotation has been removed. The substance-presence range IRI is retained and now reaches the migrated CORE presence pattern. Comparison outcomes do not establish regulatory compliance.'}.items():
        path=ROOT/f'widoco/sections/{module}/description-en.html'
        text=baseline_text(path.relative_to(ROOT))
        marker='<p class="core-2026-migration">'+paragraph+'</p>\n'
        if marker not in text:text+=marker
        write(path.relative_to(ROOT),text)
    # Recompute the diagram inventory from source graphs, preserving asset links.
    text=baseline_text('diagrams/DIAGRAM_INDEX.md')
    assets=text[text.index('## Assets'):]
    rows=['# Textile ontology diagrams','','SOC, Associated Materials, Recyclability and the network overview are regenerated',
          'for the 2.0.0 candidate. Other diagrams retain their accepted baseline bytes.',
          'Views are illustrative; Turtle remains the axiom authority.','',
          '| Module | Classes | Object properties | Datatype properties | SKOS concepts | SKOS schemes |',
          '|---|---:|---:|---:|---:|---:|']
    for path in sorted((ROOT/'ontology').glob('*.ttl')):
        if path.stem=='textile-ontology':continue
        graph=v.parse(path)
        counts=[len(set(graph.subjects(RDF.type,t))) for t in (OWL.Class,OWL.ObjectProperty,OWL.DatatypeProperty,v.SKOS.Concept,v.SKOS.ConceptScheme)]
        rows.append('| '+path.stem+' | '+' | '.join(map(str,counts))+' |')
    write('diagrams/DIAGRAM_INDEX.md','\n'.join(rows)+'\n\n'+assets)
    print('Documentation and deterministic traceability refreshed:',stats['resource_count'],'resources,',len(evidence),'evidence rows.')


def integrity():
    from migration.implement_core import catalog
    catalog()
    files=v.package_files(ROOT)
    write('PUBLICATION_MANIFEST.txt','# Current Textile package integrity and separate reference inventory.\n# Only CURRENT_PACKAGE participates in SHA256SUMS (except SHA256SUMS itself).\n[CURRENT_PACKAGE]\n'+'\n'.join(files)+'\n\n[PRESERVED_REFERENCE_MATERIAL]\n'+'\n'.join(v.PRESERVED_REFERENCE_MATERIAL)+'\n')
    write('SHA256SUMS',''.join(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in files if name!='SHA256SUMS'))
    print('Manifest and checksums refreshed:',len(files),'files.')


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--integrity',action='store_true')
    integrity() if p.parse_args().integrity else documentation()
