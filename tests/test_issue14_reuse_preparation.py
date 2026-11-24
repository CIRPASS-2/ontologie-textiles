"""Issue 14: distinguish reuse and preparing waste for reuse."""
import subprocess
import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from pyshacl import validate
from migration import mat_alignment as m
from migration import phase4_contract as p4

P = Namespace('https://w3id.org/eudpp/textile-process#')
R = Namespace('https://w3id.org/eudpp/textile-recyclability#')
T = Namespace('https://w3id.org/eudpp/textile-core#')
D = Namespace('https://w3id.org/eudpp#')
E = Namespace('https://example.org/issue14/')
BASE = '5d54ad8081f7e4bc6cd6109a87de7725cd745084'
ROOT = m.ROOT


def test_exact_approved_change_and_class_definitions():
    g = Graph().parse(ROOT / 'ontology/textile-process.ttl')
    assert isomorphic(g, p4.issue14_expected_graph(p4.expected_graphs()['ontology/textile-process.ttl']))
    for t in (P.ReuseProcess, P.PreparingForReuseProcess):
        assert (t, RDF.type, OWL.Class) in g
        assert (t, RDFS.subClassOf, P.EndOfLifeProcess) in g
    reuse = str(g.value(P.ReuseProcess, RDFS.comment))
    prep = str(g.value(P.PreparingForReuseProcess, RDFS.comment))
    assert 'not waste' in reuse and 'same purpose' in reuse
    assert any('Article 3(13)' in str(x) for x in g.objects(P.ReuseProcess, DCTERMS.bibliographicCitation))
    common = Namespace('https://w3id.org/eudpp/textile-connector#')
    assert (P.ReuseProcess, common.sourceType, common.adaptedDefinition) in g
    assert any('JRC' in str(x) and '3(13)' in str(x) for x in g.objects(P.ReuseProcess, common.modellingNote))
    assert any('JRC' in str(x) for x in g.objects(P.ReuseProcess, common.sourceLocator))
    assert 'become waste' in prep and 'checking, cleaning or repairing' in prep and 'without any other pre-processing' in prep
    for a, b in ((P.ReuseProcess, P.PreparingForReuseProcess), (P.PreparingForReuseProcess, P.ReuseProcess), (P.PreparingForReuseProcess, P.RepairProcess)):
        assert (a, RDFS.subClassOf, b) not in g
        assert (a, OWL.equivalentClass, b) not in g
        assert (a, OWL.disjointWith, b) not in g
        assert (b, OWL.disjointWith, a) not in g


def test_prior_cumulative_graph_can_be_restored():
    for path in ('ontology/textile-process.ttl', 'ontology/textile-recyclability.ttl'):
        graph = Graph().parse(ROOT / path)
        assert isomorphic(p4.restore_phase3(graph, path), p4.old_graph(path))


def test_other_ontologies_and_shapes_are_unchanged():
    for name in ('ontology/textile-recyclability.ttl', 'ontology/textile-repairability.ttl', 'shacl/textile-recyclability-shapes.ttl', 'shacl/textile-quantitative-shapes.ttl'):
        assert (ROOT / name).read_bytes() == subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=ROOT)
    assert (R.TextileWaste, RDFS.subClassOf, T.TextileProduct) in Graph().parse(ROOT / 'ontology/textile-recyclability.ttl')


@pytest.mark.parametrize('semantics', [RDFS_Semantics, OWLRL_Semantics])
def test_process_and_waste_inference(semantics):
    g = m.closure()
    g.parse(ROOT / 'examples/example-19-reuse-preparation.ttl')
    DeductiveClosure(semantics).expand(g)
    assert (E.reuseType, RDF.type, P.EndOfLifeProcess) in g
    assert (E.preparationType, RDF.type, P.EndOfLifeProcess) in g
    assert (E.preparationType, RDF.type, P.ReuseProcess) not in g
    assert (E.reuseType, RDF.type, P.PreparingForReuseProcess) not in g
    assert (E.preparationType, RDF.type, P.RepairProcess) not in g
    assert (E.discardedJacket, RDF.type, T.TextileProduct) in g
    assert (E.discardedJacket, RDF.type, D.Product) in g
    assert (E.reusedShirt, RDF.type, R.TextileWaste) not in g


def test_new_and_existing_public_examples_conform():
    shapes = Graph()
    for path in (ROOT / 'shacl').glob('*.ttl'): shapes.parse(path)
    data = m.closure()
    for name in ('example-19-reuse-preparation.ttl', 'example-11-textile-recyclability-v1.1.2.ttl'):
        data.parse(ROOT / 'examples' / name)
    conforms, _, report = validate(data, shacl_graph=shapes, inference='rdfs', advanced=True)
    assert conforms, report
