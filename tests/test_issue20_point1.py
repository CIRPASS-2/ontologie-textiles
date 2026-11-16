"""Point 1: result identity, category boundaries and optional target validation."""
from pathlib import Path

import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal
from rdflib.collection import Collection
from rdflib.compare import isomorphic
from rdflib.namespace import SH
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate

from scripts import validate_public as v
import issue20_support as change

ROOT = v.ROOT
A = Namespace('https://w3id.org/eudpp/textile-assessment#')
D = Namespace('https://w3id.org/eudpp/textile-durability#')
C = Namespace('https://w3id.org/eudpp/textile-connector#')
S = Namespace('https://w3id.org/eudpp/textile-structure#')
E = Namespace('https://example.org/eu-dpp-textile/issue20-point1/')
SI = Namespace('https://si-digital-framework.org/SI#')
UNITS = Namespace('https://si-digital-framework.org/SI/units/')
EXAMPLE = 'examples/example-12-assessed-aspects-v2.1.0-dev.ttl'
TARGETS = 'shacl/profiles/textile-assessed-aspect-targets.ttl'


@pytest.fixture(scope='module')
def ontology():
    return sum((v.parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')), Graph())


@pytest.fixture(scope='module')
def data():
    return Graph().parse(ROOT / EXAMPLE)


@pytest.fixture(scope='module')
def model(ontology, data):
    graph = ontology + data
    graph.add((E.inferredResult, A.resultForAssessedAspect, E['colour-fastness-001']))
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    return graph


def optional_report(ontology, data):
    shapes = Graph().parse(ROOT / TARGETS)
    return validate(ontology + data, shacl_graph=shapes, inference='none', do_owl_imports=False)


def test_exact_reviewed_extension_and_unchanged_hierarchies():
    for filename in v.CURRENT_MODULES:
        rel = 'ontology/' + filename
        change.published_contract_graph(Graph().parse(ROOT / rel), rel)
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    assert graph.value(A.resultForAssessedAspect, RDFS.domain) == A.MeasurementResult
    union = graph.value(graph.value(A.resultForAssessedAspect, RDFS.range), OWL.unionOf)
    assert set(Collection(graph, union)) == {
        Namespace('https://w3id.org/eudpp#').Property,
        D.ObservedDegradationPhenomenon, D.FailureMode, D.ExternalDamage,
    }
    assert (A.resultForAssessedAspect, RDF.type, OWL.FunctionalProperty) not in graph
    assert not list(graph.subjects(OWL.onProperty, A.resultForAssessedAspect))


@pytest.mark.parametrize('fault', ['domain', 'functional', 'unrelated-class', 'disjointness'])
def test_exact_transition_rejects_unapproved_mutations(fault):
    rel = 'ontology/textile-assessment.ttl'
    graph = Graph().parse(ROOT / rel)
    if fault == 'domain':
        graph.set((A.resultForAssessedAspect, RDFS.domain, A.AssessmentExecution))
    elif fault == 'functional':
        graph.add((A.resultForAssessedAspect, RDF.type, OWL.FunctionalProperty))
    elif fault == 'unrelated-class':
        graph.add((E.unapproved, RDF.type, OWL.Class))
    else:
        graph.add((D.ObservedPerformanceParameter, OWL.disjointWith, D.ExternalDamage))
    with pytest.raises(AssertionError, match='Unauthorized canonical RDF difference'):
        change.published_contract_graph(graph, rel)


def test_multi_result_bindings_and_protocol_separation(data):
    expected = {
        E['colour-result-001']: E['colour-fastness-001'],
        E['dimension-result-001']: E['dimensional-stability-001'],
        E['pilling-result-001']: E['pilling-001'],
        E['surface-density-result-001']: E['surface-density-001'],
    }
    assert dict(data.subject_objects(A.resultForAssessedAspect)) == expected
    assert set(data.objects(E['wash-test-001'], A.producesResult)) == set(list(expected)[:2])
    assert not set(expected.values()) & {E['cycle-count-parameter'], E['five-cycles-setting']}
    assert (E['five-cycles-setting'], A.settingForParameter, E['cycle-count-parameter']) in data


def test_inference_preserves_result_and_aspect_categories(model):
    assert (E.inferredResult, RDF.type, A.MeasurementResult) in model
    for node in ['inferredResult', 'colour-result-001', 'dimension-result-001',
                 'pilling-result-001', 'surface-density-result-001']:
        assert (E[node], RDF.type, A.AssessmentResult) in model
        assert (E[node], RDF.type, A.AssessmentExecution) not in model
    for node in ['pilling-001', 'surface-density-001']:
        assert (E[node], RDF.type, D.ObservedPerformanceParameter) not in model
    assert (E['surface-density-001'], RDF.type, S.TextileStructureCharacteristic) in model
    assert (E['pilling-001'], RDF.type, D.ObservedDegradationPhenomenon) in model
    assert (E['pilling-001'], RDF.type, Namespace('https://w3id.org/eudpp#').Property) not in model
    assert (E['cycle-count-parameter'], RDF.type, D.ObservedPerformanceParameter) not in model
    assert not [o for _, p, o in model if str(p).endswith('agent-ont#error')]
    assert not list(model.subjects(RDF.type, OWL.Nothing))


def test_mass_per_area_and_numeric_datatypes(data):
    assert data.value(E['surface-density-value-001'], C.numericValue) == Literal('0.145', datatype=XSD.decimal)
    for value in data.objects(None, C.numericValue):
        assert value.datatype == XSD.decimal and not value.ill_typed
    unit = data.value(E['surface-density-value-001'], C.hasMeasurementUnit)
    assert data.value(unit, SI.hasLeftUnitTerm) == UNITS.kilogram
    power = data.value(unit, SI.hasRightUnitTerm)
    assert data.value(power, SI.hasUnitBase) == UNITS.metre
    assert data.value(power, SI.hasNumericExponent) == Literal('-2', datatype=XSD.short)


def test_positive_example_in_baseline_and_optional_target_profile(ontology, data):
    baseline = sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())
    assert not list(baseline.triples((None, SH.path, A.resultForAssessedAspect)))
    assert validate(ontology + data, shacl_graph=baseline, inference='rdfs', do_owl_imports=False)[0]
    assert optional_report(ontology, data)[0]


@pytest.mark.parametrize('fault,components', [
    ('setting', {SH.OrConstraintComponent, SH.NotConstraintComponent}),
    ('parameter', {SH.OrConstraintComponent, SH.NotConstraintComponent}),
    ('class', {SH.OrConstraintComponent, SH.NotConstraintComponent}),
    ('value', {SH.OrConstraintComponent, SH.NotConstraintComponent}),
    ('literal', {SH.NodeKindConstraintComponent, SH.OrConstraintComponent}),
    ('untyped', {SH.OrConstraintComponent}),
])
def test_negative_targets(ontology, data, fault, components):
    broken = Graph() + data
    targets = {'setting': E['five-cycles-setting'],
               'parameter': E['cycle-count-parameter'], 'class': D.ColourFastness,
               'value': E['relative-dimension-change-001'], 'literal': Literal('3', datatype=XSD.decimal),
               'untyped': E.unknown}
    broken.set((E['colour-result-001'], A.resultForAssessedAspect, targets[fault]))
    ok, report, _ = optional_report(ontology, broken)
    assert not ok
    results = list(report.subjects(RDF.type, SH.ValidationResult))
    assert {report.value(r, SH.sourceConstraintComponent) for r in results} == components
    assert {report.value(r, SH.focusNode) for r in results} == {E['colour-result-001']}
    assert {report.value(r, SH.resultPath) for r in results} == {A.resultForAssessedAspect}


@pytest.mark.parametrize('example', ['example-06-assessment-v1.1.2.ttl',
                                   'example-07-indicator-v1.1.2.ttl'])
def test_legacy_results_remain_valid(ontology, example):
    assert optional_report(ontology, Graph().parse(ROOT / 'examples' / example))[0]


@pytest.mark.parametrize('count', [0, 2])
def test_no_cardinality_requirement(ontology, data, count):
    graph = Graph() + data
    graph.remove((E['colour-result-001'], A.resultForAssessedAspect, None))
    if count:
        graph.add((E['colour-result-001'], A.resultForAssessedAspect, E['colour-fastness-001']))
        graph.add((E['colour-result-001'], A.resultForAssessedAspect, E['dimensional-stability-001']))
    assert optional_report(ontology, graph)[0]


def test_published_version_is_not_redirected_to_development():
    catalog = {x.attrib['name']: x.attrib['uri'] for x in v.ET.parse(ROOT / 'catalog-v001.xml').getroot()}
    for module in ['assessment', 'ontology']:
        assert 'https://w3id.org/eudpp/textile-' + module + '/2.0.0' not in catalog


def test_no_direct_jrc_attribution_and_public_traceability():
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    assert graph.value(A.resultForAssessedAspect, C.sourceLocator) == Literal('docs/decisions/TXT-DEC-011.md', lang='en')
    assert graph.value(A.resultForAssessedAspect, C.sourceType) == C.modellingAbstraction
    assert not list(graph.objects(A.resultForAssessedAspect, v.DCT.source))
    row = next(r for r in v.derive(v.ontology_graph(ROOT))[0]
               if r['resource_iri'] == str(A.resultForAssessedAspect))
    assert row['has_jrc_evidence'] == 'FALSE' and row['evidence_count'] == '0'
