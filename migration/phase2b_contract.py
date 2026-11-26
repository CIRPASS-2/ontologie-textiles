"""Pinned issue 12 and development-identity transition for Phase 2B."""
from collections import Counter
from pathlib import Path
import hashlib
from functools import lru_cache
import subprocess
from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.compare import graph_diff, isomorphic, to_isomorphic
from rdflib.namespace import DCTERMS
from migration import integration_contract as p1

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '196fdf762eb75faec00b7627994e9c445efebcbf'
VERSION = 'integration-2026-11.1'
SUFFIX = '/dev/' + VERSION
FROZEN = ROOT.parent / 'dpp-textiles-frozen-2.0.0'
CORE = 'ontology/textile-core.ttl'
AM = 'ontology/textile-associated-materials.ttl'
T = Namespace('https://w3id.org/eudpp/textile-core#')
A = Namespace('https://w3id.org/eudpp/textile-associated-materials#')
C = Namespace('https://w3id.org/eudpp/textile-connector#')
D = Namespace('https://w3id.org/eudpp#')
DECISIONS = ('docs/ISSUE12_MATERIAL_COMPOSITION.md',)

def term(subject, predicate, value):
    return (subject, predicate, value)

ISSUE12 = {
    CORE: (
      {term(T.FibreCompositionComponent, RDFS.comment, Literal('A structured component of a textile product fibre composition, specifying a fibre type and its quantitative share in the product.', lang='en'))},
      {term(T.FibreCompositionComponent, RDFS.comment, Literal('A fibre material constituent considered within the composition of a specific textile product, characterised by its fibre type and quantitative mass fraction. It does not necessarily represent an individually identifiable physical fibre batch or a separate composition declaration.', lang='en'))}),
    AM: (
      {term(A.PackagingMaterial, RDFS.subClassOf, D.MaterialOfComposition),
       term(A.PackagingMaterial, RDFS.comment, Literal('A material occurrence used for the packaging, transport, storage or delivery of a textile product.', lang='en')),
       term(A.PackagingMaterial, C.modellingNote, Literal('PackagingMaterial is aligned as a subclass of dpp:MaterialOfComposition. Instances of a SKOS-based classification class can also instantiate an OWL material-classification class; the SKOS representation does not prevent such alignment. Packaging-specific class and type-property alignment remains a separate modelling decision requiring its own semantic assessment. No packaging alignment is introduced here.', lang='en'))},
      {term(A.PackagingMaterial, RDFS.comment, Literal('A material used in packaging associated with a textile product, including packaging used for its protection, handling, storage or delivery. This classification does not imply that the material forms part of the textile product itself.', lang='en')),
       term(A.PackagingMaterial, C.modellingNote, Literal('Packaging material is not automatically classified as a material of composition of the textile product. It may be a material of composition of a separately modelled packaging product; no disjointness is asserted.', lang='en'))})
}

def version_transition(graph, path, suffix=SUFFIX, version=VERSION):
    ontology = URIRef('https://w3id.org/eudpp/' + Path(path).stem)
    remove, add = set(), set()
    def replace(predicate, old, new):
        p1.require((ontology,predicate,old) in graph, 'Version precondition: '+path)
        remove.add((ontology,predicate,old)); add.add((ontology,predicate,new))
    replace(OWL.versionIRI, URIRef(str(ontology)+'/2.0.0'), URIRef(str(ontology)+suffix))
    replace(OWL.versionInfo, Literal('Version 2.0.0 candidate'), Literal('Version '+version))
    old_prior = set(graph.objects(ontology,OWL.priorVersion))
    p1.require(len(old_prior) <= 1, 'Unexpected historical prior: '+path)
    if old_prior:
        p1.require(old_prior == {URIRef(str(ontology)+'/1.1.2')}, 'Unexpected historical prior: '+path)
        remove.add((ontology,OWL.priorVersion,next(iter(old_prior))))
    add.add((ontology,OWL.priorVersion,URIRef(str(ontology)+'/2.0.0')))
    citations=list(graph.objects(ontology,DCTERMS.bibliographicCitation))
    if path == 'ontology/textile-ontology.ttl':
        p1.require(not citations, 'Unexpected umbrella citation')
    else:
        p1.require(len(citations)==1 and isinstance(citations[0],Literal) and
                   str(citations[0]).endswith('Version 2.0.0 candidate.'),
                   'Unexpected citation: '+path)
        old=citations[0]
        replace(DCTERMS.bibliographicCitation, old,
                Literal(str(old).replace('Version 2.0.0 candidate.', 'Version '+version+'.'),
                        lang=old.language))
    return remove,add

def apply_changes(graph, remove, add):
    p1.require(remove <= set(graph), 'Missing approved removal')
    p1.require(not (add & set(graph)), 'Approved addition already present')
    result=graph+Graph()
    for triple in remove:result.remove(triple)
    for triple in add:result.add(triple)
    return result

def verify_source():
    """Independent exact source verification from the two named Git commits."""
    try:
        approved = subprocess.check_output(['git','show',SOURCE+':'+DECISIONS[0]], cwd=ROOT)
        actual = (ROOT/DECISIONS[0]).read_bytes()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise p1.ContractError('Issue 12 decision record unavailable') from exc
    p1.require(actual == approved, 'Issue 12 decision record differs from approved source')
    for path in sorted(p1.APPROVED_FILES):
        raw=subprocess.check_output(['git','show',p1.BASELINE+':'+path],cwd=ROOT).decode('utf8')
        base=p1.parse_turtle(raw,path)
        rem,add=ISSUE12.get(path,(set(),set()))
        expected=apply_changes(base,rem,add)
        vr,va=version_transition(expected,path,'/2.1.0-issue12-dev','2.1.0-issue12-dev')
        expected=apply_changes(expected,vr,va)
        source=p1.parse_turtle(subprocess.check_output(['git','show',SOURCE+':'+path],cwd=ROOT).decode('utf8'),path)
        p1.require(isomorphic(expected,source),'Unapproved source graph difference: '+path)


def check_subject_predicate_overlaps(entries):
    """Require explicit evidence for overlapping decisions; allow multivalues."""
    touched={}
    for entry in entries:
        keys={(entry.graph,s,p) for s,p,o in entry.remove|entry.add}
        for key in keys:
            for prior in touched.get(key,()):
                p1.require(prior.id in entry.reconciles and
                           set(prior.decisions) <= set(entry.decisions) and
                           ({prior.issue,entry.issue}|set(prior.contributing_issues)) <=
                           set(entry.contributing_issues),
                           'Subject-predicate overlap requires explicit reconciliation')
            touched.setdefault(key,[]).append(entry)

def classify_actual(base,actual):
    """Classify actual exact graph differences, including header changes."""
    counts=Counter()
    for path in sorted(base):
        _,removed,added=graph_diff(to_isomorphic(base[path]),to_isomorphic(actual[path]))
        ontology=URIRef('https://w3id.org/eudpp/'+Path(path).stem)
        for direction,triples in (('removed',removed),('added',added)):
            for subject,predicate,obj in triples:
                if subject==ontology and predicate in (OWL.versionIRI,OWL.versionInfo,OWL.priorVersion,DCTERMS.bibliographicCitation):
                    kind='header'
                elif predicate in (RDFS.comment,C.modellingNote,Namespace('http://www.w3.org/2004/02/skos/core#').definition):
                    kind='annotation'
                elif (subject,predicate,obj)==(A.PackagingMaterial,RDFS.subClassOf,D.MaterialOfComposition):
                    kind='logical'
                else:raise p1.ContractError('Unexpected or anonymous actual delta: '+path+' '+str(predicate))
                counts[kind+'_'+direction]+=1
    p1.require(dict(counts)=={'header_added':51,'header_removed':47,'annotation_added':17,
                               'annotation_removed':17,'logical_removed':1},
               'Cumulative actual transition classification mismatch')
    return counts

def expected_graphs():
    """Construct frozen -> issue 9 -> issue 12 -> approved version headers."""
    base=p1.baseline_graphs()
    issue9=p1.issue9_transitions()
    result=p1.build_expected(base,issue9)
    previous={(e.graph,s,p):e for e in issue9 for s,p,o in e.remove|e.add}
    entries=list(issue9)
    counts=Counter()
    for path,(rem,add) in ISSUE12.items():
        for s,p,o in rem|add:
            p1.require((path,s,p) not in previous, 'Issue 9/12 subject-predicate overlap requires explicit reconciliation')
            if p==RDFS.subClassOf: counts['logical_removed' if (s,p,o) in rem else 'logical_added']+=1
            elif p in (RDFS.comment,C.modellingNote):counts['annotation_removed' if (s,p,o) in rem else 'annotation_added']+=1
            else:raise p1.ContractError('Unclassified issue 12 predicate')
        # Separate reviewed logical and annotation categories.
        for category in ('annotation','logical'):
            rr={t for t in rem if (t[1]==RDFS.subClassOf)==(category=='logical')}
            aa={t for t in add if (t[1]==RDFS.subClassOf)==(category=='logical')}
            if rr or aa:
                entries.append(p1.Transition('issue12-'+Path(path).stem+'-'+category,path,'#12',
                    SOURCE,DECISIONS,'Owner-approved issue 12 transition','Exact prior triples',
                    category,frozenset(rr),frozenset(aa)))
        result[path]=apply_changes(result[path],rem,add)
    p1.require(dict(counts)=={'annotation_added':3,'annotation_removed':3,'logical_removed':1},'Issue 12 classification mismatch')
    header_add=header_remove=0
    for path in sorted(result):
        rem,add=version_transition(result[path],path)
        for s,p,o in rem|add:
            p1.require((path,s,p) not in previous, 'Version overlap requires explicit reconciliation')
        header_remove+=len(rem);header_add+=len(add)
        entries.append(p1.Transition('phase2b-version-'+Path(path).stem,path,'phase2b',
             'owner-approved-phase2b-pending-commit',('migration/PHASE2B_IMPLEMENTATION.md',
             'migration/phase2b_contract.py'),'Owner-approved development identity',
             'Exact prior header','header',frozenset(rem),frozenset(add)))
        result[path]=apply_changes(result[path],rem,add)
    p1.require((header_remove,header_add)==(47,51),'Header transition count mismatch')
    check_subject_predicate_overlaps(entries)
    reconstructed=p1.build_expected(base,entries)
    p1.require(all(isomorphic(result[path],reconstructed[path]) for path in result),'Ordered transition reconstruction mismatch')
    return base,result

@lru_cache(maxsize=2)
def _restoration_templates(evidence_key):
    _,expected=expected_graphs()
    previous=p1.build_expected(p1.baseline_graphs(),p1.issue9_transitions())
    return expected,previous

def restore_phase1(graph,path):
    """Verify whole Phase 2 graph, then reconstruct exact Phase 1 graph."""
    p1.issue9_transitions()  # Recheck pinned evidence and attribution every time.
    evidence_key=hashlib.sha256((ROOT/p1.EVIDENCE).read_bytes()+p1.CONTRACT.read_bytes()).hexdigest()
    expected,previous=_restoration_templates(evidence_key)
    p1.require(isomorphic(graph,expected[path]),'Unauthorized canonical RDF difference: '+path)
    return previous[path]+Graph()

def expected_catalogue():
    raw=subprocess.check_output(['git','show',p1.BASELINE+':catalog-v001.xml'],cwd=ROOT).decode('utf8')
    for path in sorted(p1.APPROVED_FILES):
        iri='https://w3id.org/eudpp/'+Path(path).stem
        old='name="'+iri+'/2.0.0"';new='name="'+iri+SUFFIX+'"'
        p1.require(raw.count(old)==1,'Historical catalogue precondition: '+iri)
        raw=raw.replace(old,new)
    return raw.encode('utf8')

def check_frozen(frozen=None):
    """Verify immutable baseline bytes and single-catalogue offline resolution."""
    from scripts.validate_public import catalogue_import_closure
    frozen = Path(frozen) if frozen is not None else FROZEN
    p1.require(frozen.is_dir(),'Frozen 2.0.0 package missing')
    sha=subprocess.check_output(['git','show',p1.BASELINE+':SHA256SUMS'],cwd=ROOT)
    p1.require((frozen/'SHA256SUMS').read_bytes()==sha,'Frozen checksum file changed')
    records=[row.split('  ',1) for row in sha.decode().splitlines() if row]
    for digest,path in records:
        p1.require(hashlib.sha256((frozen/path).read_bytes()).hexdigest()==digest,'Frozen byte mismatch: '+path)
    expected={p for _,p in records}|{'SHA256SUMS'}
    actual={p.relative_to(frozen).as_posix() for p in frozen.rglob('*') if p.is_file()}
    p1.require(actual==expected,'Frozen package inventory changed')
    closure=catalogue_import_closure(frozen/'catalog-v001.xml',
                                      'https://w3id.org/eudpp/textile-ontology/2.0.0')
    p1.require(len(closure)==20,'Frozen closure changed')
    p1.require(all(p.is_relative_to(frozen.resolve()) for p in closure),'Frozen closure escaped')
    return len(records),len(closure)

def validate():
    if not __debug__:raise p1.ContractError('Optimized Python disables required historical assertions')
    verify_source()
    baseline,expected=expected_graphs()
    p1.require((ROOT/'VERSION').read_bytes()==(VERSION+'\n').encode(),'Package version changed')
    historical='migration/legacy-soc-attribution.json'
    original=subprocess.check_output(['git','show',p1.BASELINE+':'+historical],cwd=ROOT)
    p1.require((ROOT/historical).read_bytes()==original,'Protected file changed: '+historical)
    p1.require((ROOT/'catalog-v001.xml').read_bytes()==expected_catalogue(),'Catalogue transition mismatch')
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'ontology').glob('textile-*.ttl')}
    p1.require(actual==set(expected),'Canonical document inventory changed')
    from migration import mat_alignment
    protected=mat_alignment.protected_hashes()
    rows=[]; actual_graphs={}
    for path in sorted(expected):
        graph=p1.parse_turtle((ROOT/path).read_text(encoding='utf8'),path)
        p1.require(isomorphic(graph,expected[path]),'Unauthorized canonical RDF difference: '+path)
        rows.append(path);actual_graphs[path]=graph
    actual_counts=classify_actual(baseline,actual_graphs)
    frozen,closure=check_frozen()
    return dict(canonical_graphs=len(rows),issue9_annotation_added=14,issue9_annotation_removed=14,
                issue12_annotation_added=3,issue12_annotation_removed=3,
                issue12_logical_added=0,issue12_logical_removed=1,
                header_added=51,header_removed=47,imports_changed=0,
                protected_files=len(protected),frozen_checksums=frozen,frozen_closure=closure,
                package_version=VERSION, actual_cumulative_counts=dict(actual_counts))

if __name__=='__main__':
    import json
    print(json.dumps(validate(),indent=2))
