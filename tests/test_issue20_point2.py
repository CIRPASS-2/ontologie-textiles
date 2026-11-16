"""Only the approved assessment-to-conceptual-event bridge and import."""
import subprocess
import hashlib

import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.compare import isomorphic
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate

from scripts import validate_public as v
from issue20_support import apply_review_annotations
from issue20_support import (POINT2_TURTLE, published_contract_graph, apply_point3,
                             expected_quantitative_shapes, POINT5_SHACL_README_SHA256, POINT4_TURTLE, POINT5_TURTLE)

ROOT = v.ROOT
POINT1 = 'c87568e707d1c183a8ef24090180fcae01001f7c'
A = Namespace('https://w3id.org/eudpp/textile-assessment#')
P = Namespace('https://w3id.org/eudpp/textile-process#')
D = Namespace('https://w3id.org/eudpp#')
C = Namespace('https://w3id.org/eudpp/textile-connector#')
EPCIS = Namespace('https://ref.gs1.org/epcis/')
X = Namespace('https://example.org/eu-dpp-textile/issue20-point2/')
EXAMPLE = 'examples/example-13-assessment-product-event-v2.1.0-dev.ttl'


def point1_bytes(name):
    return subprocess.check_output(['git', 'show', POINT1 + ':' + name], cwd=ROOT)


def test_exact_delta_preserves_point1_and_all_other_modules():
    for filename in v.CURRENT_MODULES:
        name = 'ontology/' + filename
        before = point1_bytes(name)
        expected = Graph().parse(data=before, format='turtle')
        if filename == 'textile-assessment.ttl':
            extension = Graph().parse(data=POINT2_TURTLE, format='turtle')
            assert len(extension) == 9  # Eight property triples and one import.
            assert not set(extension) & set(expected)
            expected += extension
            apply_point3(expected)  # Check the exact separately approved later delta.
            expected.parse(data=POINT4_TURTLE, format='turtle')
            expected.parse(data=POINT5_TURTLE, format='turtle')
            apply_review_annotations(expected)
        else:
            assert (ROOT / name).read_bytes() == before, name
        assert isomorphic(Graph().parse(ROOT / name), expected), name


def test_dependency_and_point1_inputs_are_unchanged():
    names = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', POINT1, '--',
         'dependencies', 'mireot', 'migration', 'shacl',
         'examples/example-12-assessed-aspects-v2.1.0-dev.ttl',
         'tests/test_issue20_point1.py', 'docs/decisions/TXT-DEC-011.md',
         'docs/ISSUE20_POINT1_IMPLEMENTATION.md', 'VERSION', 'catalog-v001.xml',
         'scripts/validate_public.py'], cwd=ROOT, text=True).splitlines()
    for name in names:
        if name == 'catalog-v001.xml':
            assert (ROOT / name).read_bytes() == point1_bytes(name).replace(
                b'textile-shacl/quantitative/2.0.0', b'textile-shacl/quantitative/2.1.0-dev')
        elif name == 'shacl/textile-quantitative-shapes.ttl':
            assert isomorphic(Graph().parse(ROOT / name), expected_quantitative_shapes())
        elif name == 'shacl/README.md':
            current = (ROOT / name).read_bytes()
            assert current.startswith(point1_bytes(name))
            assert hashlib.sha256(current).hexdigest() == POINT5_SHACL_README_SHA256
        else:
            assert (ROOT / name).read_bytes() == point1_bytes(name), name


def test_standalone_import_is_bounded_and_does_not_import_process():
    paths = v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-assessment')
    assert {p.relative_to(ROOT).as_posix() for p in paths} == {
        'ontology/textile-assessment.ttl', 'ontology/textile-connector.ttl',
        'ontology/textile-durability.ttl', 'mireot/si-textile-mireot.ttl',
        'mireot/dpp-textile-mireot.ttl', 'mireot/event-textile-mireot.ttl',
    }
    graph = sum((v.parse(p) for p in paths), Graph())
    assert (D.ProductEvent, RDF.type, OWL.Class) in graph
    assert not list(graph.predicate_objects(D.isRepresentedByCarrier))
    assert not list(graph.predicate_objects(P.isRepresentedByProductEvent))
    assert len(v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')) == 20


def test_independent_optional_property_and_traceability():
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    prop = A.isRepresentedByProductEvent
    assert set(graph.objects(prop, RDFS.domain)) == {A.AssessmentExecution}
    assert set(graph.objects(prop, RDFS.range)) == {D.ProductEvent}
    assert set(graph.objects(prop, RDF.type)) == {OWL.ObjectProperty}
    for predicate in [RDFS.subPropertyOf, OWL.equivalentProperty, OWL.inverseOf,
                      OWL.propertyChainAxiom]:
        assert not list(graph.triples((prop, predicate, None)))
        assert not list(graph.triples((None, predicate, prop)))
    assert not list(graph.subjects(OWL.onProperty, prop))
    assert graph.value(prop, C.sourceLocator) == Literal('docs/decisions/TXT-DEC-012.md', lang='en')
    assert graph.value(prop, C.sourceType) == C.modellingAbstraction
    assert not list(graph.objects(prop, v.DCT.source))
    row = next(r for r in v.derive(v.ontology_graph(ROOT))[0] if r['resource_iri'] == str(prop))
    assert row['has_jrc_evidence'] == 'FALSE' and row['evidence_count'] == '0'


@pytest.mark.parametrize('fault', ['domain', 'functional', 'process-alignment', 'missing-import'])
def test_exact_contract_rejects_unapproved_changes(fault):
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    if fault == 'domain':
        graph.set((A.isRepresentedByProductEvent, RDFS.domain, P.TextileProcessExecution))
    elif fault == 'functional':
        graph.add((A.isRepresentedByProductEvent, RDF.type, OWL.FunctionalProperty))
    elif fault == 'process-alignment':
        graph.add((A.isRepresentedByProductEvent, RDFS.subPropertyOf, P.isRepresentedByProductEvent))
    else:
        graph.remove((None, OWL.imports, v.URIRef('https://w3id.org/eudpp/textile-event-mireot')))
    with pytest.raises(AssertionError, match='Unauthorized canonical RDF difference'):
        published_contract_graph(graph, 'ontology/textile-assessment.ttl')


@pytest.fixture(scope='module')
def runtime():
    return sum((v.parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')), Graph())


@pytest.fixture(scope='module', params=[False, True], ids=['bounded', 'full-EVENT'])
def model(request, runtime):
    graph = runtime + Graph().parse(ROOT / EXAMPLE)
    if request.param:
        graph += Graph().parse(ROOT / 'dependencies/current-core/event.owl', format='xml')
    for triple in [
        (X.untypedAssessment, A.isRepresentedByProductEvent, X.inferredEvent),
        (X.process, P.isRepresentedByProductEvent, X.processEvent),
        (X.processReuse, RDF.type, A.AssessmentExecution),
        (X.processReuse, P.isRepresentedByProductEvent, X.processReuseEvent),
        (X.observationOnly, RDF.type, EPCIS.ObjectEvent),
        (X.observationOnly, EPCIS.action, Literal('OBSERVE')),
        (X.observationOnly, EPCIS.bizStep, v.URIRef('https://ref.gs1.org/cbv/BizStep-inspecting')),
        (X.directCarrierAssessment, A.isRepresentedByProductEvent, X.directCarrier),
        (X.directCarrier, RDF.type, EPCIS.ObjectEvent),
    ]:
        graph.add(triple)
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    return graph, request.param


def test_entailments_preserve_execution_event_and_carrier_roles(model):
    graph, full_event = model
    for triple in [
        (X.untypedAssessment, RDF.type, A.AssessmentExecution),
        (X.inferredEvent, RDF.type, D.ProductEvent),
        (X.productEvent, RDF.type, D.ESPREvent),
        (X.process, RDF.type, P.TextileProcessExecution),
        (X.processEvent, P.representsProcessExecution, X.process),
        (X.processReuse, RDF.type, P.TextileProcessExecution),
        (X.processReuseEvent, P.representsProcessExecution, X.processReuse),
    ]:
        assert triple in graph
    for triple in [
        (X.inspection, RDF.type, P.TextileProcessExecution),
        (X.inspection, RDF.type, D.ProductEvent),
        (X.inspection, RDF.type, EPCIS.EPCISEvent),
        (X.productEvent, RDF.type, A.AssessmentExecution),
        (X.productEvent, RDF.type, P.TextileProcessExecution),
        (X.observation, RDF.type, D.ProductEvent),
        (X.process, RDF.type, A.AssessmentExecution),
        (X.productEvent, P.representsProcessExecution, X.inspection),
        (X.inspection, OWL.sameAs, X.productEvent),
        (X.productEvent, OWL.sameAs, X.observation),
    ]:
        assert triple not in graph
    assert ((X.observation, D.hasProductEvent, X.productEvent) in graph) == full_event
    if full_event:
        assert (X.observation, RDF.type, EPCIS.EPCISEvent) in graph
    assert not [o for _, p, o in graph if str(p) == 'http://www.daml.org/2002/03/agents/agent-ont#error']
    assert not list(graph.subjects(RDF.type, OWL.Nothing))


def test_observation_alone_is_not_a_product_event_and_range_is_not_validation(model):
    graph, _ = model
    assert (X.observationOnly, RDF.type, D.ProductEvent) not in graph
    # Deliberate misuse: OWL silently adds ProductEvent typing to the carrier.
    # ProductEvent and EPCISEvent are not disjoint; this is not intended usage.
    assert (X.directCarrier, RDF.type, D.ProductEvent) in graph


@pytest.mark.parametrize('count', [0, 2])
def test_existing_validation_allows_missing_and_multiple_links(runtime, count):
    data = Graph().parse(ROOT / EXAMPLE)
    data.remove((X.inspection, A.isRepresentedByProductEvent, None))
    for target in [X.productEvent, X.secondEvent][:count]:
        data.add((X.inspection, A.isRepresentedByProductEvent, target))
        data.add((target, RDF.type, D.ProductEvent))
    shapes = sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())
    assert validate(runtime + data, shacl_graph=shapes, inference='rdfs', do_owl_imports=False)[0]
