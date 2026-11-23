"""Refresh candidate documentation, traceability, manifest and byte checksums."""
import hashlib
import json
import zipfile
from pathlib import Path
from rdflib import RDF, OWL
from scripts import validate_public as v

ROOT=v.ROOT

# Issue #9 fragments are inline because their links resolve from the generated document.
README_CREATORS = 'The Textile ontology network and its twelve modules identify **Elio Hbeich,\nBOUGACHA Racem, Ivo Ladenius, Andreas Schneider, Jan Merckx and Piero de Sabbata**\nas `dcterms:creator`. The owner-approved creator update preserves the established\nEnglish language-tagged literal representation and all existing creators.\n\n'
README_ISSUE9 = '## Issue #9 development scope\n\nIssue #9 specifies approved documentation and annotation clarifications to\nthe merged 2.0.0 baseline. These clarifications are prepared for review. Issue #9 alone preserves imports and logical axioms. The combined integration\nuses a separate development version identity.\nSee [the approved issue #9 decisions](docs/decisions/TXT-DEC-016.md).\n\n## Selected CORE sources\n\n| CORE module | Selected upstream version |\n|---|---|\n| ACTOR | 2.2.0 |\n| CON | 2.4.0 |\n| EVENT | 1.0.0 |\n| MAT | 1.1.0 |\n| P_DPP | 2.2.0 |\n| SOC | 2.2.0 |\n\nThese versions are verified from the local source snapshots, not inferred from\nthe local MIREOT version. Textile retains bounded extracts using original CORE\nterm IRIs and an offline-resolvable closure. [Dependencies](docs/DEPENDENCIES.md)\nidentifies snapshot files, hashes, extraction scopes and update responsibilities;\nno upstream commit identifier is asserted without evidence.\n\n'
GUIDE_ISSUE9 = '## Approved issue #9 clarifications\n\n[TXT-DEC-016](decisions/TXT-DEC-016.md) records the retained CORE extraction\narchitecture, the textile-context durability definition, the interpretive\nindicator distinction and the two role-specific concernsProduct properties.\nThese are annotation and documentation changes with no new logical commitments.\nThe existing quantity, SOC, assessment and composition models remain governed by\ntheir own decisions.\n'
ARCHITECTURE_ISSUE9 = '## Bounded CORE reuse retained for issue #9\n\nTextile reuses original CORE IRIs; an extracted CORE subject is not a duplicate\nTextile term. Bounded MIREOT graphs select CORE axioms and their associated\nsemantic commitments from identifiable local upstream snapshots. This limits\nexposure to unrelated upstream axioms compared with importing entire modules,\nwhile keeping the selected closure reproducible and resolvable offline through\n`catalog-v001.xml`.\n\nThe approved architecture retains these extracts and their existing imports.\nSelection does not guarantee full compatibility or isolate consumers that also\nload other CORE axioms. It creates a maintenance responsibility: monitor upstream\nevolution, compare the full candidate source, and assess changed commitments at\nthe actual Textile reuse boundary before adopting an update. See the\n[dependency review workflow](governance/upstream-dependency-governance.md).\n\n'
DEPENDENCIES_ISSUE9 = '## Snapshot identity and maintenance\n\nAn upstream module version, a local source snapshot and a local extraction\nversion identify different things. The source files above are the accepted local\nsnapshots; their byte identities are recorded in\n[SHA256SUMS](../dependencies/current-core/SHA256SUMS). The local rebuilt MIREOT\nversion is 2.0.0 and is not an upstream CORE version. No upstream Git commit is\nasserted here: the accepted evidence identifies supplied snapshot bytes and\nembedded module metadata.\n\nThe full upstream candidate sources must be compared for evolution, including\nchanges outside the selected subjects that could affect them. Inference,\nvalidation and exchange impact is assessed against actually reused terms and\naxioms. Adoption and any re-extraction require a separate approved dependency\nupdate; these issue #9 clarifications change neither source bytes nor extracts.\nSee [governance](governance/upstream-dependency-governance.md).\n\n'
TRACEABILITY_ISSUE9 = '## Issue #9 definition clarification\n\nThe current `txtdur:Durability` definition is a project-specific textile-context\nrefinement informed by JRC, not a quotation. Its modelling note records the\nadditional context in Sections 9.2.1.1, 9.2.1.3 and 13.10.1.1; the original\ngeneral-definition locator and source association are preserved. The CSV schema\ndoes not project definition/comment text or modelling notes, so the unchanged\nprojection is intentional. [TXT-DEC-016](decisions/TXT-DEC-016.md) records\nthe clarification. Historical SOC statement attribution remains unchanged in\n`migration/legacy-soc-attribution.json` even where current annotations are clarified.\n'
GOVERNANCE_19 = '## 19. Accepted current sources and historical examples\n\nThe merged Textile 2.0.0 baseline selects EVENT 1.0.0 and SOC 2.2.0. Both\nrebuilt local MIREOTs have 2.0.0 identities. Their module versions and local\nsnapshot hashes are distinct evidence; see [dependencies](../DEPENDENCIES.md).\nThe SOC migration is implemented, not a pending dependency upgrade.\n\n### Historical pre-migration examples\n\nThe preserved earlier runtime used EVENT `Version 0.1.0 DRAFT` and SOC\n`Version 0.1.2 DRAFT`, with local EVENT MIREOT 1.1.2 and SOC MIREOT 1.1.3.\nThese historical facts remain relevant to migration provenance; they do not\ndescribe the current dependency selection. A draft label alone did not prove\nreuse invalid or require adoption of another version.\n\n'
GOVERNANCE_21 = '## 21. Review workflow and separately approved updates\n\n1. Identify the accepted versioned CORE snapshots by file, embedded module\n   metadata, recorded hash and demonstrably known upstream identifier, if any.\n2. Obtain an identifiable new upstream candidate and compare the full sources.\n3. Identify definition, axiom and relationship changes relevant to Textile,\n   including effects on selected terms from other changed upstream axioms.\n4. Evaluate inferred types, domain/range propagation, restrictions, validation,\n   examples and data-exchange consequences at the actual reuse boundary.\n5. Record an explicit adoption decision by the authorized owner, obtaining CORE\n   maintainer confirmation where intended semantics or compatibility is unclear.\n6. Only through an independently approved update, change the relevant MIREOTs,\n   provenance, migration guidance and tests, then run the affected checks.\n\nMonitoring upstream drift does not itself authorize adoption. Reviewing the full\nCORE candidate does not mean loading it wholesale into the Textile runtime.\n\n'

def replace_once(text, anchor, replacement, document):
    count = text.count(anchor)
    if count != 1:
        raise ValueError(f'{document}: expected exactly one anchor {anchor!r}; found {count}')
    return text.replace(anchor, replacement, 1)


def insert_before(text, anchor, fragment, document):
    if fragment in text:
        raise ValueError(f'{document}: issue #9 fragment is already present')
    return replace_once(text, anchor, fragment + anchor, document)



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
    text=text[:start]+'''This unpublished integration package uses **integration-2026-11.3**. The thirteen
Textile graphs declare distinct version IRIs under `/dev/integration-2026-11.3`
and retained module identities cite the corresponding `.2` version as prior. Common retains its migration provenance. Six CORE subsets
retain their 2.0.0 identities and SI retains its 1.1.2 identity; the runtime
closure contains 20 graphs.

Load [ontology/textile-ontology.ttl](ontology/textile-ontology.ttl) with the
active [catalogue](catalog-v001.xml). Frozen Textile 2.0.0 is an independently
verified sibling package named `dpp-textiles-frozen-2.0.0`, with its own
catalogue and original bytes. Load its versioned entry and all imports using
that catalogue only, with network fallback disabled. The preserved 1.1.2
catalogue serves its own historical closure. Never mix historical and
development catalogues. Historical bytes are preserved in Git and the frozen
local package; historical resolution is established only with the deliberately
selected historical catalogue. Public HTTP dereferencing is outside this evidence.
See the [issue #12 decision](docs/ISSUE12_MATERIAL_COMPOSITION.md),
[CORE migration guide](docs/CORE_2026_MIGRATION.md),
[1.1.2 catalogue](migration/historical/1.1.2/catalog-v001.xml), and
[Phase 2B record](migration/PHASE2B_IMPLEMENTATION.md).

'''+text[end:]
    text=text.replace('python -B -m pytest -p no:cacheprovider tests/test_public_package.py -q','python -B -m pytest -p no:cacheprovider tests -q\npython -B scripts/validate_public.py --full --complete-report')
    text=text.replace('These three profiles are selective application constraints','The three structural profiles and optional complete-report profile are selective application constraints')
    text=text.replace('**838 resources**',f"**{stats['resource_count']} resources**")
    text=text.replace('**904 evidence rows**',f'**{len(evidence)} evidence rows**').replace('**5 source documents**',f'**{len(sources)} source documents**')
    text=text.replace('902 evidence rows have recorded locators',f"{stats['locator_statuses']['PRESENT_NOT_REVERIFIED']} evidence rows have recorded locators")
    text=text.replace('| projectDecision | 55 |',f"| projectDecision | {stats['categories']['projectDecision']} |")
    import re
    for category,count in stats['categories'].items():
        text=re.sub(r'\| '+category+r' \| \d+ \|',f'| {category} | {count} |',text)
    for module in ('textile-soc','textile-associated-materials'):
        import re
        text=re.sub(r'\| '+module+r' \| \d+ \|',f"| {module} | {stats['modules'][module]} |",text)
    text=text.replace('This branch prepares the CIRPASS Textile Ontology Community Review Candidate 1.1.2 for publication in this repository.',
                      'This branch prepares an unpublished integration candidate; publication still requires owner approval.')
    text=text.replace('eight positive and eight negative SHACL fixtures, six RDFS/OWL-RL inference scenarios,',
                      'the original eight positive and eight negative SHACL fixtures, six RDFS/OWL-RL inference scenarios,')
    text=text.replace('Supply the ontology graph when executing SHACL.',
                      'The pytest suite additionally verifies forty-one migration scenarios, source fidelity, historical bytes, positive shape coverage and forbidden entailments. Merge the offline ontology closure with data when executing SHACL.')
    text=insert_before(text, '## Two bodies of ontology work\n', README_CREATORS, 'README.md')
    text=insert_before(text, '## Versions and entry point\n', README_ISSUE9, 'README.md')
    text=text.replace('| textile-connector | 37 |','| textile-common | 37 |')
    text+='\n## Common and Connector compatibility\n\n[Textile Common](ontology/textile-common.ttl) is the canonical shared ontology.\nThe separately generated [Connector compatibility representation](compat/textile-connector.ttl)\ncontains the complete Common non-header graph with the original `txtcon:` term\nIRIs; it imports the SI MIREOT and does not import Common. Load one representation\nfor a given purpose with the active catalogue. See the [issue 16 integration\nrecord](docs/ISSUE16_COMMON_MIGRATION.md) for version and historical resolution.\n'
    text+='\n## Cumulative issue #20 integration\n'+'\nThe internal unpublished integration identity is `integration-2026-11.3`.\nAssessment supports explicit assessed aspects, product-facing event links,\ncategorical settings, awarded scores and controlled assessment outcomes.\nExecution-time guidance reuses optional PROV timestamps without importing PROV.\nSee the modelling guide and decisions TXT-DEC-011 through TXT-DEC-015. The\nassessed-aspect SHACL profile is optional; published 2.0.0 and the committed\n`.1` and `.2` integration states retain their own isolated catalogues.\n'
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
            '', 'The 42 adapted legacy definitions/comments originate in the historical',
            '[SOC 0.1.2 DRAFT snapshot](../migration/historical/1.1.2/dependencies/soc.ttl),',
            'created by Elio Hbeich, issued 2026-04-17, under',
            '[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).',
            'Textile changes the namespace, scope and CORE alignment. Exact source',
            'resources and copied statements are recorded in',
            '[the attribution inventory](../migration/legacy-soc-attribution.json).',
            'This text comparison does not independently verify underlying JRC or legal references.',
            '', '## Historical compatibility', '',
            'The accepted older dependency snapshots and MIREOT bytes are preserved in',
            'the [historical inventory](../migration/historical/inventory.json) and archive.',
            'The extracted historical runtime and its own catalogue are under',
            '`migration/historical/1.1.2/`. Historical version IRIs and lowercase `/soc`',
            'are deliberately absent from the active catalogue. No equivalence or',
            'redirect bridges the legacy `soc#` vocabulary to the migrated runtime.',
            'See [migration guidance](CORE_2026_MIGRATION.md).','']
    text=insert_before('\n'.join(lines), '## Source attribution\n', DEPENDENCIES_ISSUE9, 'docs/DEPENDENCIES.md')
    text+='\n## Phase 3 Common and Connector\n\nCanonical Common and the complete Connector compatibility representation both\nuse the approved unchanged SI MIREOT. CORE and all MIREOT snapshots remain\nbyte-protected; no unconditional quantitative CORE alignment is introduced.\nThe [integration record](ISSUE16_COMMON_MIGRATION.md) describes offline routing.\n'
    write('docs/DEPENDENCIES.md',text)
    # This maintained guide contains later MAT and diagnostic sections absent from
    # the historical archive. Preserve them while refreshing the issue #9 section.
    text=(ROOT/'docs/MODELLING_GUIDE.md').read_text('utf8')
    heading='## Approved issue #9 clarifications\n'
    if text.count(heading) != 1 or text.count(GUIDE_ISSUE9) != 1:
        raise ValueError('docs/MODELLING_GUIDE.md: expected exactly one approved issue #9 section')
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
    text=insert_before(text, '## October 2026 CORE boundary\n', ARCHITECTURE_ISSUE9, 'docs/ARCHITECTURE.md')
    text=text.replace('Connector contains patterns that are intentionally shared across modules.','Common contains patterns that are intentionally shared across modules; the complete Connector compatibility graph preserves the original term IRIs.')
    text+='\n## Common identity and legacy Connector\n\nCommon is the canonical shared ontology. The Connector document is a separate\ncomplete compatibility representation, not a Common import shim. Both use the\nexisting `txtcon:` namespace and import the approved SI MIREOT. A consumer\nshould select the appropriate document and catalogue for its purpose.\n'
    write('docs/ARCHITECTURE.md',text)
    write('docs/PUBLICATION_SCOPE.md',(ROOT/'docs/PUBLICATION_SCOPE.md').read_text('utf8'))
    text=baseline_text('docs/SOURCE_TRACEABILITY.md')
    text=text.replace('902 PRESENT_NOT_REVERIFIED',f"{stats['locator_statuses']['PRESENT_NOT_REVERIFIED']} PRESENT_NOT_REVERIFIED")
    text+=f'''
## October 2026 migration

Local modelling decisions are documented in [TXT-DEC-010](decisions/TXT-DEC-010.md).
Forty-two resources with copied historical SOC definitions/comments are classified
as adaptedDefinition and attributed to SOC 0.1.2 DRAFT and their exact source
resources. Local scope/alignment decisions remain separately annotated.
The projection contains {stats['resource_count']} resources and {len(evidence)} evidence rows:
the original 904 relationships plus 42 historical SOC citations, all remaining
PRESENT_NOT_REVERIFIED except the two unchanged UNRESOLVED relationships. Source registry
descriptions identify the adopted MAT 1.1.0 and EVENT 1.0.0 subsets. The seven
earlier locator supplements remain historical evidence statements; the migration
does not claim fresh documentary verification. The presence locator names the
current SubstancePresence pivot while retaining its ESPR source relationship.
'''
    anchor='current SubstancePresence pivot while retaining its ESPR source relationship.\n'
    if TRACEABILITY_ISSUE9 in text:
        raise ValueError('docs/SOURCE_TRACEABILITY.md: issue #9 fragment is already present')
    text=replace_once(text, anchor, anchor+'\n'+TRACEABILITY_ISSUE9, 'docs/SOURCE_TRACEABILITY.md')
    write('docs/SOURCE_TRACEABILITY.md',text)
    text=baseline_text('traceability/README.md').replace('838 resources',f"{stats['resource_count']} resources").replace('282 resources have no external',f"{stats['zero_evidence']} resources have no external")
    text=text.replace('904 evidence relationships and 5 source documents',f'{len(evidence)} evidence relationships and {len(sources)} source documents')
    text=text.replace('902 PRESENT_NOT_REVERIFIED',f"{stats['locator_statuses']['PRESENT_NOT_REVERIFIED']} PRESENT_NOT_REVERIFIED")
    write('traceability/README.md',text)
    for name in ('nader-review.md','upstream-dependency-governance.md'):
        path=ROOT/'docs/governance'/name
        text=baseline_text(path.relative_to(ROOT))
        banner='> Historical baseline examples below describe 1.1.2. The October 2026\n> adoption is implemented by [TXT-DEC-010](../decisions/TXT-DEC-010.md)\n> and the [migration guide](../CORE_2026_MIGRATION.md); policy rules remain in force.\n\n'
        if banner not in text:text=banner+text
        if name == 'upstream-dependency-governance.md':
            if GOVERNANCE_19 in text or GOVERNANCE_21 in text:
                raise ValueError(f'{path}: issue #9 fragment is already present')
            start='## 19. Current EVENT/SoC status as repository examples\n'
            end='## 20. Relationship to current MIREOT strategy\n'
            if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
                raise ValueError(f'{path}: expected unique ordered section 19 anchors')
            old_section=text[text.index(start):text.index(end)]
            text=replace_once(text, old_section, GOVERNANCE_19, str(path))
            heading='## 21. Relationship to future dependency-update tasks\n'
            text=replace_once(text, heading, GOVERNANCE_21+'## 22. Relationship to future dependency-update tasks\n', str(path))
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
