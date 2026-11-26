"""Refresh candidate documentation, traceability, manifest and byte checksums."""
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from rdflib import RDF, OWL
from scripts import validate_public as v

ROOT=v.ROOT

# Issue #9 fragments are inline because their links resolve from the generated document.
README_CREATORS = 'The twelve domain/shared Textile modules and the network entry-point ontology\n(thirteen canonical Textile graphs in total) identify **Elio Hbeich,\nBOUGACHA Racem, Ivo Ladenius, Andreas Schneider, Jan Merckx and Piero de Sabbata**\nas `dcterms:creator`. The owner-approved creator update preserves the established\nEnglish language-tagged literal representation and all existing creators.\n\n'
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


def check_shacl_guide(text):
    """Preserve the approved technical body while allowing reviewed user guidance."""
    original = subprocess.check_output(
        ['git', 'show', 'cd57c4e47662cbc58c1d1146af9c32cba0fe81e5:shacl/README.md'], cwd=ROOT).decode('utf8')
    anchor = 'The SoC profile targets positive presences, qualification identity/context/source,'
    assert text.endswith(original[original.index(anchor):]), 'SHACL technical guidance changed'
    for heading in ('## Public validation and examples', '## Optional profiles and test-only guards', '## SoC reporting details'):
        assert text.count(heading) == 1, 'Missing or duplicate SHACL guide section: ' + heading
    for path in ('textile-quantitative-shapes.ttl', 'textile-recyclability-shapes.ttl', 'textile-soc-shapes.ttl',
                 'profiles/textile-soc-complete-report.ttl', 'profiles/textile-assessed-aspect-targets.ttl'):
        assert '](' + path + ')' in text, 'Missing profile link: ' + path
    assert "inference='rdfs'" in text and "do_owl_imports=False" in text


def checked_sub(pattern, replacement, text, label):
    text, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(label + ': expected exactly one generated field; found ' + str(count))
    return text


def documentation():
    resources,evidence,sources,_=v.derive(v.ontology_graph(ROOT))
    for name,fields,rows in [('textile-resource-traceability.csv',v.RESOURCE_FIELDS,resources),('textile-resource-evidence.csv',v.EVIDENCE_FIELDS,evidence),('source-documents.csv',v.SOURCE_FIELDS,sources)]:
        (ROOT/'traceability'/name).write_bytes(v.csv_bytes(fields,rows))
    stats=v.summary(resources,evidence,sources)
    # Current prose includes approved decisions made after the historical archive.
    # Refresh owned numerical fields in place, without reconstructing that prose
    # from 1.1.2 or treating the maintained document as a frozen generated output.
    text=(ROOT/'README.md').read_text('utf8')
    for fragment in (README_CREATORS, README_ISSUE9):
        assert text.count(fragment.rstrip()) == 1, 'README approved section missing or duplicated'
    for label, count in (('resources', stats['resource_count']), ('evidence rows', len(evidence)),
                         ('source documents', len(sources)), ('resources with multiple evidence records', stats['multiple_evidence'])):
        text=checked_sub(r'\*\*\d+ '+label+r'\*\*', '**'+str(count)+' '+label+'**', text, 'README '+label)
    for key,count in {**stats['categories'], **stats['modules']}.items():
        text=checked_sub(r'^\| '+re.escape(key)+r' \| \d+ \|$', '| '+key+' | '+str(count)+' |', text, 'README '+key)
    text=checked_sub(r'\d+ evidence rows have recorded locators', str(stats['locator_statuses']['PRESENT_NOT_REVERIFIED'])+' evidence rows have recorded locators', text, 'README locators')
    write('README.md',text)

    scopes=json.loads((ROOT/'migration/extraction-scopes.json').read_text('utf8'))
    text=(ROOT/'docs/DEPENDENCIES.md').read_text('utf8')
    assert text.count(DEPENDENCIES_ISSUE9.rstrip()) == 1
    for key,record in scopes.items():
        row='| '+key.upper()+' | `'+record['source']+'` | `'+record['source_iri']+'` | '+str(record['copied_triples'])+' |'
        text=checked_sub(r'^\| '+key.upper()+r' \| .* \| \d+ \|$', lambda match: row, text, 'dependency '+key)
    write('docs/DEPENDENCIES.md',text)

    text=(ROOT/'docs/MODELLING_GUIDE.md').read_text('utf8')
    if text.count('## Approved issue #9 clarifications\n') != 1 or text.count(GUIDE_ISSUE9) != 1:
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
    text=(ROOT/'docs/SOURCE_TRACEABILITY.md').read_text('utf8')
    assert text.count(TRACEABILITY_ISSUE9.rstrip()) == 1
    text=checked_sub(r'The projection contains \d+ resources and \d+ evidence rows:',
                     f"The projection contains {stats['resource_count']} resources and {len(evidence)} evidence rows:", text, 'traceability projection')
    text=checked_sub(r'There are \d+ PRESENT_NOT_REVERIFIED rows, two UNRESOLVED rows and zero VERIFIED rows',
                     f"There are {stats['locator_statuses']['PRESENT_NOT_REVERIFIED']} PRESENT_NOT_REVERIFIED rows, two UNRESOLVED rows and zero VERIFIED rows", text, 'traceability locators')
    write('docs/SOURCE_TRACEABILITY.md',text)

    text=(ROOT/'shacl/README.md').read_text('utf8')
    check_shacl_guide(text)
    write('shacl/README.md',text)
    # These narratives and diagram assets have their own maintenance workflows.
    # Preserve later approved content rather than overwrite it from the archive.
    for name in ('CHANGELOG.md', 'traceability/README.md', 'docs/governance/nader-review.md',
                 'docs/governance/upstream-dependency-governance.md', 'diagrams/DIAGRAM_INDEX.md',
                 'examples/README.md', *(f'widoco/sections/{module}/description-en.html'
                 for module in ('soc','associated-materials','recyclability'))):
        write(name,(ROOT/name).read_text('utf8'))
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
