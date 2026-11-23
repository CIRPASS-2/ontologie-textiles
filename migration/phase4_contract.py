"""Phase 4 source-pinned cumulative graph authorization."""
from pathlib import Path
from functools import lru_cache
import hashlib
import subprocess
import io
import tarfile
from xml.etree import ElementTree as ET
from rdflib import Graph, BNode, URIRef, Literal, RDF, RDFS, OWL
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS, SH, XSD
from migration import integration_contract as p1
from migration import phase3_preflight as p3

ROOT=Path(__file__).resolve().parents[1]
BASE='ce6d4a9b74c0abb70d86e93a3d2cce22f140a0d2'
SOURCE='ca4b58bb96bfa9e1854fc6d246f2ccd908c4f143'
OLD='integration-2026-11.2'
VERSION='integration-2026-11.3'
ASSESS='ontology/textile-assessment.ttl'
SHAPES='shacl/textile-quantitative-shapes.ttl'
PROFILE='shacl/profiles/textile-assessed-aspect-targets.ttl'
SOURCE_HASHES={ASSESS:'fb6612d8feb3f73aa1a0642edbdbf02a72919b8f6f8a7bc6b4670f78902093bd',SHAPES:'7cf7c333c2b64185d3220490588a3ea4bece7fc383889ec4aad757597214c284',PROFILE:'549efab46741c5288c4167d455f1dd4eb62ea2eae615c96a25fb9b9fd9924e4c'}
ASS=URIRef('https://w3id.org/eudpp/textile-assessment')
PREFIX=str(ASS)+'#'
PROPERTIES=('resultForAssessedAspect','isRepresentedByProductEvent','hasParameterConcept','awardedScoreValue','hasAssessmentOutcome')
SETTING=URIRef('https://w3id.org/eudpp/textile-shacl#MeasurementParameterSettingShape')
AWARD=URIRef('https://w3id.org/eudpp/textile-shacl#AwardedScoreValueShape')
EVENT=URIRef('https://w3id.org/eudpp/textile-event-mireot')

# This authorization is independent of the candidate manifest and checksums.
UNCHANGED_SHACL = (
    'shacl/textile-recyclability-shapes.ttl',
    'shacl/textile-soc-shapes.ttl',
    'shacl/profiles/textile-soc-complete-report.ttl',
)
APPROVED_SHACL = frozenset((SHAPES, PROFILE, *UNCHANGED_SHACL))
ISSUE20_RECORDS = (
    *(f'docs/decisions/TXT-DEC-{n:03}.md' for n in range(11, 16)),
    *(f'docs/ISSUE20_POINT{n}_IMPLEMENTATION.md' for n in range(1, 7)),
    'examples/example-12-assessed-aspects-v2.1.0-dev.ttl',
    'examples/example-13-assessment-product-event-v2.1.0-dev.ttl',
    'examples/example-14-parameter-values-v2.1.0-dev.ttl',
    'examples/example-15-awarded-points-v2.1.0-dev.ttl',
    'examples/example-16-assessment-outcomes-v2.1.0-dev.ttl',
    'examples/example-17-assessment-times-v2.1.0-dev.ttl',
)

def blob(commit,path):
    return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)

def source_graph(path):
    raw=blob(SOURCE,path)
    p1.require(hashlib.sha256(raw).hexdigest()==SOURCE_HASHES[path],'Issue 20 source bytes changed: '+path)
    return p1.parse_turtle(raw.decode('utf8'),path)

def old_graph(path):
    return p1.parse_turtle(blob(BASE,path).decode('utf8'),path)

def subgraph(graph,subject):
    """Copy all subject triples and recursively include anonymous structures."""
    result=Graph(); pending=[subject]; seen=set()
    while pending:
        item=pending.pop()
        if item in seen: continue
        seen.add(item)
        for triple in graph.triples((item,None,None)):
            result.add(triple)
            if isinstance(triple[2],BNode): pending.append(triple[2])
    return result

def replace(g,s,p,old,new):
    p1.require((s,p,old) in g,'Transition precondition failed: '+str(s)+' '+str(p))
    g.remove((s,p,old));g.add((s,p,new))

def version(g,iri):
    for predicate in (OWL.versionIRI,OWL.versionInfo):
        values=list(g.objects(iri,predicate));p1.require(len(values)==1,'Version header cardinality')
        old=values[0]
        new=URIRef(str(old).replace(OLD,VERSION)) if isinstance(old,URIRef) else Literal(str(old).replace(OLD,VERSION),lang=old.language,datatype=old.datatype)
        p1.require(new!=old,'Version identity precondition')
        replace(g,iri,predicate,old,new)
    prior=list(g.objects(iri,OWL.priorVersion))
    p1.require(len(prior)<=1,'Version predecessor cardinality')
    if prior:g.remove((iri,OWL.priorVersion,prior[0]))
    g.add((iri,OWL.priorVersion,URIRef(str(iri)+'/dev/'+OLD)))
    for old in list(g.objects(iri,DCTERMS.bibliographicCitation)):
        p1.require(OLD in str(old),'Version citation precondition')
        replace(g,iri,DCTERMS.bibliographicCitation,old,Literal(str(old).replace(OLD,VERSION),lang=old.language))

@lru_cache(maxsize=1)
def expected_graphs():
    old=p3.expected_graphs()
    for path,expected in old.items():
        p1.require(isomorphic(expected,old_graph(path)),'Committed Phase 3 graph mismatch: '+path)
    result={}
    for path in old:
        g=old_graph(path); iri=URIRef('https://w3id.org/eudpp/'+Path(path).stem)
        version(g,iri);result[path]=g
    g=result[ASSESS]; src=source_graph(ASSESS)
    for local in PROPERTIES:
        subject=URIRef(PREFIX+local)
        p1.require(not list(g.triples((subject,None,None))),'Property already present: '+local)
        g+=subgraph(src,subject)
    execution=URIRef(PREFIX+'AssessmentExecution')
    for pred in (RDFS.comment,RDFS.seeAlso):
        for obj in src.objects(execution,pred):
            if pred==RDFS.seeAlso or str(obj).startswith('Execution timing may be stated directly'):
                g.add((execution,pred,obj))
    old_comment=Literal('Quantitative results, parameter settings and thresholds use txtcon:QuantitativeValue and SI Digital Framework units through the Textile Common pattern.',lang='en')
    new_comment=Literal('Quantitative results, quantitative parameter settings and thresholds use txtcon:QuantitativeValue and SI Digital Framework units through the Textile Common pattern; categorical parameter settings use SKOS concepts.',lang='en')
    replace(g,ASS,RDFS.comment,old_comment,new_comment)
    replace(g,ASS,DCTERMS.modified,Literal('2026-10-27',datatype=XSD.date),Literal('2026-11-16',datatype=XSD.date))
    p1.require((ASS,OWL.imports,URIRef('https://w3id.org/eudpp/textile-common')) in g and (ASS,OWL.imports,EVENT) not in g,'Assessment import reconciliation precondition')
    g.add((ASS,OWL.imports,EVENT))
    return result

def expected_shapes():
    g=old_graph(SHAPES); source=source_graph(SHAPES)
    before=subgraph(g,SETTING)
    for triple in before:g.remove(triple)
    g+=subgraph(source,SETTING);g+=subgraph(source,AWARD)
    iri=URIRef('https://w3id.org/eudpp/textile-shacl/quantitative')
    replace(g,iri,OWL.versionIRI,URIRef(str(iri)+'/dev/'+OLD),URIRef(str(iri)+'/dev/'+VERSION))
    replace(g,iri,OWL.priorVersion,URIRef(str(iri)+'/2.0.0'),URIRef(str(iri)+'/dev/'+OLD))
    return g

def expected_catalogue():
    original=blob(BASE,'catalog-v001.xml').replace(('/dev/'+OLD).encode(),('/dev/'+VERSION).encode())
    anchor=b'  <uri name="https://w3id.org/eudpp/MAT"'
    routes=(b'  <uri name="https://w3id.org/eudpp/LCA" uri="dependencies/current-core/lca.owl" />\n'
            b'  <uri name="https://w3id.org/eudpp/LCA/3.1" uri="dependencies/current-core/lca.owl" />\n')
    p1.require(original.count(anchor)==1,'Unexpected catalogue anchor')
    return original.replace(anchor,routes+anchor,1)

@lru_cache(maxsize=1)
def verify_phase3_snapshot():
    checks=blob(BASE,'SHA256SUMS').decode('utf8').splitlines()
    entries=dict(line.split('  ',1)[::-1] for line in checks)
    p1.require(len(entries)==869,'Phase 3 checksum inventory changed')
    raw=subprocess.check_output(['git','archive','--format=tar',BASE],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as tar:
        members={m.name:m for m in tar if m.isfile() and m.name in entries}
        p1.require(set(members)==set(entries),'Phase 3 archive inventory mismatch')
        data={name:tar.extractfile(member).read() for name,member in members.items()}
    for name,digest in entries.items():
        p1.require(hashlib.sha256(data[name]).hexdigest()==digest,'Phase 3 checksum mismatch: '+name)
    catalog=ET.fromstring(data['catalog-v001.xml'])
    routes={x.attrib['name']:x.attrib['uri'] for x in catalog}
    queue=['https://w3id.org/eudpp/textile-ontology/dev/'+OLD];seen=set()
    while queue:
        iri=queue.pop();p1.require(iri in routes,'Unmapped Phase 3 import: '+iri)
        path=routes[iri];p1.require(path in data,'Missing Phase 3 closure member: '+path)
        if path in seen:continue
        seen.add(path)
        graph=Graph().parse(data=data[path].decode('utf8'),format='xml' if path.endswith('.owl') else 'turtle')
        queue.extend(map(str,graph.objects(None,OWL.imports)))
    p1.require(len(seen)==20,'Phase 3 closure changed')
    return len(entries),len(seen)

def restore_phase3(graph,path):
    expected=expected_graphs()
    p1.require(path in expected and isomorphic(graph,expected[path]),'Unauthorized Phase 4 graph: '+path)
    return old_graph(path)

def validate():
    if not __debug__:raise p1.ContractError('Optimized Python disables required assertions')
    from scripts import generate_common_connector as compat
    from scripts.validate_public import catalogue_import_closure, package_files
    p3.verify_issue16_source();p3.verify_phase2b_commit();phase3_checksums,phase3_closure=verify_phase3_snapshot()
    p1.require((ROOT/'VERSION').read_bytes()==(VERSION+'\n').encode(),'Package version changed')
    p1.require((ROOT/'catalog-v001.xml').read_bytes()==expected_catalogue(),'Catalogue transition mismatch')
    expected=expected_graphs()
    p1.require({p.relative_to(ROOT).as_posix() for p in (ROOT/'ontology').glob('textile-*.ttl')}==set(expected),'Canonical document inventory changed')
    for path,g in expected.items():
        actual=p1.parse_turtle((ROOT/path).read_text(encoding='utf8'),path)
        p1.require(isomorphic(actual,g),'Unauthorized canonical RDF difference (Phase 4): '+path)
    actual_shacl={path.relative_to(ROOT).as_posix()
                  for path in (ROOT/'shacl').rglob('*.ttl') if path.is_file()}
    p1.require(actual_shacl==APPROVED_SHACL,
               'Unauthorized SHACL document inventory: '+repr(sorted(actual_shacl ^ APPROVED_SHACL)))
    for path in UNCHANGED_SHACL:
        p1.require((ROOT/path).read_bytes()==blob(BASE,path),
                   'Protected SHACL bytes changed: '+path)
    for path in ISSUE20_RECORDS:
        p1.require((ROOT/path).is_file() and (ROOT/path).read_bytes()==blob(SOURCE,path),
                   'Approved issue 20 source record changed: '+path)
    actual=p1.parse_turtle((ROOT/SHAPES).read_text(encoding='utf8'),SHAPES)
    p1.require(isomorphic(actual,expected_shapes()),'Unauthorized quantitative SHACL graph')
    source_graph(PROFILE)
    p1.require((ROOT/PROFILE).read_bytes()==blob(SOURCE,PROFILE),'Optional profile changed')
    public_script='scripts/validate_public.py'
    expected_loader=blob(BASE,public_script).replace(('/dev/'+OLD).encode(),('/dev/'+VERSION).encode())
    p1.require((ROOT/public_script).read_bytes()==expected_loader,'Public profile selection changed')
    common=p1.parse_turtle((ROOT/p3.COMMON_PATH).read_text(encoding='utf8'),p3.COMMON_PATH)
    connector=p1.parse_turtle((ROOT/'compat/textile-connector.ttl').read_text(encoding='utf8'),'compat/textile-connector.ttl')
    p1.require((ROOT/'compat/textile-connector.ttl').read_text(encoding='utf8')==compat.render(common),'Connector generation mismatch')
    terms,triples=compat.verify(common,connector)
    prior=URIRef(str(compat.CONNECTOR)+'/dev/'+OLD)
    p1.require(set(connector.objects(compat.CONNECTOR,OWL.priorVersion))=={prior},'Connector predecessor mismatch')
    # Restore the independently authorized .2 header for its existing strict
    # 14-triple verifier; no expectation is obtained from the generator.
    restored=connector+Graph()
    subject=compat.CONNECTOR
    for pred,new,old in ((OWL.versionIRI,URIRef(str(subject)+'/dev/'+VERSION),URIRef(str(subject)+'/dev/'+OLD)),
                         (OWL.versionInfo,Literal('Version '+VERSION),Literal('Version '+OLD)),
                         (OWL.priorVersion,prior,URIRef(str(subject)+'/dev/integration-2026-11.1'))):
        replace(restored,subject,pred,new,old)
    p3.verify_connector_header(restored)
    protected=['dependencies','mireot','migration/core-sources','migration/historical']
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',*protected],cwd=ROOT,text=True).splitlines()
    package=set(package_files(ROOT));names=[name for name in names if name in package]
    expected_names=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',*protected],cwd=ROOT,text=True).splitlines())
    expected_names={name for name in expected_names if '/graphwise-ontology/' not in name}
    actual_names={name for name in package if any(name==area or name.startswith(area+'/') for area in protected)}
    lca='dependencies/current-core/lca.owl'
    lca_hash='39a523d6ef6202a1247359a4cf4c151e4b0aee42046c1b5c3b6bcef7a2b3c71b'
    p1.require(actual_names==expected_names | {lca},'Protected source inventory changed')
    p1.require(hashlib.sha256((ROOT/lca).read_bytes()).hexdigest()==lca_hash,'LCA source bytes changed')
    sums='dependencies/current-core/SHA256SUMS'
    base_lines=blob(BASE,sums).decode('utf8').splitlines()
    expected_sums=sorted(base_lines+[lca_hash+'  lca.owl'],key=lambda line:line.split('  ',1)[1])
    for name in names:
        expected_bytes=('\n'.join(expected_sums)+'\n').encode() if name==sums else blob(BASE,name)
        p1.require((ROOT/name).read_bytes()==expected_bytes,'Protected file changed: '+name)
    legacy='migration/legacy-soc-attribution.json'
    p1.require((ROOT/legacy).read_bytes()==blob(BASE,legacy),'Protected file changed: '+legacy)
    for iri,n in [('https://w3id.org/eudpp/textile-assessment',6),('https://w3id.org/eudpp/textile-ontology',20),('https://w3id.org/eudpp/textile-common',2),('https://w3id.org/eudpp/textile-connector',2)]:
        p1.require(len(catalogue_import_closure(ROOT/'catalog-v001.xml',iri))==n,'Import closure mismatch: '+iri)
    from migration import phase2b_contract as phase2
    frozen,closure=phase2.check_frozen()
    return {'version':VERSION,'canonical_graphs':len(expected),'issue9_annotation_added':14,'issue9_annotation_removed':14,'issue12_logical_removed':1,'compatibility_terms':terms,'compatibility_payload_triples':triples,'protected_files':len(names),'frozen_checksums':frozen,'historical_closure':closure,'phase3_checksums':phase3_checksums,'phase3_closure':phase3_closure}
