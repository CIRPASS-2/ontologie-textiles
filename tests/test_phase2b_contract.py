"""Phase 2B approved transition and offline historic package controls."""
from dataclasses import replace
import pytest
from pathlib import Path
from rdflib import Graph,Literal,Namespace,RDF,RDFS,OWL,URIRef
from rdflib.compare import isomorphic
from migration import phase2b_contract as phase2
from migration import integration_contract as p1

EX=Namespace('urn:phase2b-test:')

def test_source_commit_matches_explicit_approved_changes():
    phase2.verify_source()

def test_cumulative_expected_graphs_and_actual_category_counts():
    base,graphs=phase2.expected_graphs()
    assert len(graphs)==13
    assert phase2.classify_actual(base,graphs)=={
      'annotation_added':17,'annotation_removed':17,'logical_removed':1,
      'header_added':51,'header_removed':47}

def test_frozen_package_byte_and_offline_closure():
    assert phase2.check_frozen()==(799,20)

def test_subject_predicate_overlap_demands_reconciliation_without_single_value_assumption():
    path='ontology/test.ttl'; triple=(EX.s,RDFS.comment,Literal('old'))
    a=p1.Transition('a',path,'#9','commit9',('decision9',),'why','pre','annotation',
                    frozenset(),frozenset({triple}))
    b=p1.Transition('b',path,'#12','commit12',('decision12',),'why','pre','annotation',
                    frozenset(),frozenset({(EX.s,RDFS.comment,Literal('other'))}))
    with pytest.raises(p1.ContractError,match='Subject-predicate overlap'):
        phase2.check_subject_predicate_overlaps([a,b])
    b=replace(b,reconciles=('a',),decisions=('decision9','decision12'),
              contributing_issues=('#9','#12'))
    phase2.check_subject_predicate_overlaps([a,b])
    built=p1.build_expected({path:Graph()},[a,b])[path]
    assert len(list(built.objects(EX.s,RDFS.comment)))==2

def test_unapproved_and_blank_node_changes_are_rejected():
    base,expected=phase2.expected_graphs()
    graph=expected[phase2.CORE]+Graph()
    graph.add((EX.x,RDFS.subClassOf,EX.y))
    altered=dict(expected);altered[phase2.CORE]=graph
    with pytest.raises(p1.ContractError,match='Unexpected or anonymous'):
        phase2.classify_actual(base,altered)
    graph=expected[phase2.CORE]+Graph()
    node=next(graph.subjects(RDF.type,OWL.Restriction))
    graph.add((node,OWL.hasValue,EX.extra))
    altered[phase2.CORE]=graph
    with pytest.raises(p1.ContractError):
        phase2.classify_actual(base,altered)


@pytest.mark.parametrize('fault',['extra_axiom','missing_axiom','annotation','version','import','restriction','list'])
def test_cumulative_actual_graph_mutations_are_rejected(fault):
    path='ontology/textile-assessment.ttl' if fault=='list' else phase2.CORE
    graph=p1.parse_turtle((phase2.ROOT/path).read_text(encoding='utf8'),path)
    if fault=='extra_axiom':
        graph.add((EX.x,RDFS.subClassOf,EX.y))
    elif fault=='missing_axiom':
        graph.remove((phase2.T.FibreCompositionComponent,RDFS.subClassOf,phase2.D.MaterialOfComposition))
    elif fault=='annotation':
        graph.add((EX.x,RDFS.comment,Literal('unapproved',lang='en')))
    elif fault=='version':
        old=next(graph.triples((None,OWL.versionIRI,None)));graph.remove(old)
        graph.add((old[0],OWL.versionIRI,EX.unapproved))
    elif fault=='import':
        old=next(graph.triples((None,OWL.imports,None)));graph.remove(old)
        graph.add((old[0],OWL.imports,EX.unapproved))
    elif fault=='restriction':
        node=next(graph.subjects(RDF.type,OWL.Restriction));graph.add((node,OWL.hasValue,EX.unapproved))
    else:
        node,_,old=next(graph.triples((None,RDF.first,None)))
        graph.remove((node,RDF.first,old));graph.add((node,RDF.first,EX.unapproved))
    with pytest.raises(p1.ContractError,match='Unauthorized canonical RDF difference'):
        phase2.restore_phase1(graph,path)


def test_active_and_frozen_catalogue_versions_are_separate():
    import xml.etree.ElementTree as ET
    active={x.attrib['name']:x.attrib['uri'] for x in ET.parse(phase2.ROOT/'catalog-v001.xml').getroot()}
    old={x.attrib['name']:x.attrib['uri'] for x in ET.parse(phase2.FROZEN/'catalog-v001.xml').getroot()}
    for path in p1.APPROVED_FILES:
        iri='https://w3id.org/eudpp/'+Path(path).stem
        assert active[iri]==active[iri+phase2.SUFFIX]==path
        assert iri+'/2.0.0' not in active
        assert old[iri]==old[iri+'/2.0.0']==path
        graph=p1.parse_turtle((phase2.FROZEN/path).read_text(encoding='utf8'),path)
        assert (URIRef(iri),OWL.versionIRI,URIRef(iri+'/2.0.0')) in graph


def test_altered_source_decision_record_is_rejected(monkeypatch):
    original = Path.read_bytes
    def mutated(path):
        data = original(path)
        return data + b"altered" if path == phase2.ROOT / phase2.DECISIONS[0] else data
    monkeypatch.setattr(Path, 'read_bytes', mutated)
    with pytest.raises(p1.ContractError, match='decision record differs'):
        phase2.verify_source()


def test_phase1_fixture_cannot_validate_current_phase2():
    graphs = p1.build_expected(p1.baseline_graphs(), p1.issue9_transitions())
    with pytest.raises(p1.ContractError, match='Injected candidates'):
        p1.validate(graphs, p1.issue9_transitions())


def test_reconstruct_frozen_package_in_isolated_directory(tmp_path):
    from migration.reconstruct_frozen_2_0_0 import reconstruct
    destination = tmp_path / 'reconstructed'
    assert reconstruct(destination) == (800, 799, 20)
    with pytest.raises(FileExistsError):
        reconstruct(destination)
