"""Actual awarded points: exact additive correction and existing role boundaries."""
import subprocess

import pytest
from owlrl import DeductiveClosure, OWLRL_Semantics, RDFS_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.compare import isomorphic
from rdflib.namespace import SH, XSD

from scripts import validate_public as v
from issue20_support import POINT4_TURTLE, POINT4_SHAPE, published_contract_graph

ROOT = v.ROOT
POINT3 = '8a2bef637477a7fa9e77068dc8322d3d1e3ccff6'
A = Namespace('https://w3id.org/eudpp/textile-assessment#')
C = Namespace('https://w3id.org/eudpp/textile-connector#')
R = Namespace('https://w3id.org/eudpp/textile-recyclability#')
I = Namespace('https://w3id.org/eudpp/textile-indicator#')
S = Namespace('https://w3id.org/eudpp/textile-soc#')
T = Namespace('https://w3id.org/eudpp/textile-shacl#')
U = Namespace('https://si-digital-framework.org/SI/units/')
E = Namespace('https://example.org/eu-dpp-textile/issue20-point4/')
EXAMPLE = 'examples/example-15-awarded-points-v2.1.0-dev.ttl'
QUANT = 'shacl/textile-quantitative-shapes.ttl'


def baseline(name):
    return subprocess.check_output(['git', 'show', POINT3 + ':' + name], cwd=ROOT)


def test_exact_additive_source_delta_preserves_all_prior_axioms():
    addition = Graph().parse(data=POINT4_TURTLE, format='turtle')
    assert len(addition) == 8
    for filename in v.CURRENT_MODULES:
        name = 'ontology/' + filename
        old = baseline(name)
        before = Graph().parse(data=old, format='turtle')
        expected = before + Graph()
        if filename == 'textile-assessment.ttl':
            assert not set(addition) & set(before)
            expected += addition
            assert len(expected) - len(before) == 8
        else:
            assert (ROOT / name).read_bytes() == old, name
        assert isomorphic(Graph().parse(ROOT / name), expected), name


def test_exact_shape_addition_preserves_all_existing_shapes_and_metadata():
    old = baseline(QUANT)
    addition = Graph().parse(data=POINT4_SHAPE, format='turtle')
    assert len(addition) == 10
    assert isomorphic(Graph().parse(ROOT / QUANT),
                      Graph().parse(data=old, format='turtle') + addition)
    marker = '<https://w3id.org/eudpp/textile-shacl/quantitative> a owl:Ontology ;'
    body = POINT4_SHAPE[POINT4_SHAPE.index('tsh:AwardedScoreValueShape'):]
    assert (ROOT / QUANT).read_bytes() == old.decode('utf8').replace(
        marker, body + '\n' + marker).encode('utf8')
    shape = T.AwardedScoreValueShape
    assert set(addition.objects(shape, SH.targetObjectsOf)) == {A.awardedScoreValue}
    assert not list(addition.objects(shape, SH.targetClass))
    assert not list(addition.triples((None, SH.maxCount, None)))
    assert not list(addition.triples((None, SH.minInclusive, None)))


def test_frozen_inputs_and_prior_committed_evidence_are_byte_preserved():
    names = subprocess.check_output([
        'git', 'ls-tree', '-r', '--name-only', POINT3, '--',
        'dependencies', 'mireot', 'migration', 'scripts', 'catalog-v001.xml', 'VERSION',
        'examples', 'docs/decisions', 'docs/ISSUE20_POINT1_IMPLEMENTATION.md',
        'docs/ISSUE20_POINT2_IMPLEMENTATION.md', 'docs/ISSUE20_POINT3_IMPLEMENTATION.md',
        'tests/abox_corpus', 'tests/test_issue20_point1.py', 'shacl/profiles',
        'shacl/textile-soc-shapes.ttl', 'shacl/textile-recyclability-shapes.ttl',
    ], cwd=ROOT, text=True).splitlines()
    for name in names:
        assert (ROOT / name).read_bytes() == baseline(name), name
    for entry, count in [('textile-assessment', 6), ('textile-ontology', 20)]:
        assert len(v.catalogue_import_closure(
            ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/' + entry)) == count


def test_property_is_independent_optional_and_has_issue_traceability():
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    prop = A.awardedScoreValue
    assert set(graph.objects(prop, RDF.type)) == {OWL.ObjectProperty}
    assert set(graph.objects(prop, RDFS.domain)) == {A.AssessmentResult}
    assert set(graph.objects(prop, RDFS.range)) == {C.QuantitativeValue}
    assert not list(graph.subjects(OWL.onProperty, prop))
    for predicate in [RDFS.subPropertyOf, OWL.equivalentProperty, OWL.inverseOf, OWL.propertyChainAxiom]:
        assert not list(graph.triples((prop, predicate, None)))
        assert not list(graph.triples((None, predicate, prop)))
    assert graph.value(prop, C.sourceLocator) == Literal('docs/decisions/TXT-DEC-014.md', lang='en')
    assert graph.value(prop, C.sourceType) == C.modellingAbstraction
    assert not list(graph.objects(prop, v.DCT.source))
    row = next(r for r in v.derive(v.ontology_graph(ROOT))[0] if r['resource_iri'] == str(prop))
    assert row['evidence_count'] == '0' and row['has_jrc_evidence'] == 'FALSE'


@pytest.mark.parametrize('fault', ['wrong-domain', 'functional', 'rule-alignment'])
def test_exact_contract_rejects_unapproved_extensions(fault):
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    if fault == 'wrong-domain':
        graph.set((A.awardedScoreValue, RDFS.domain, A.MeasurementResult))
    elif fault == 'functional':
        graph.add((A.awardedScoreValue, RDF.type, OWL.FunctionalProperty))
    else:
        graph.add((A.awardedScoreValue, RDFS.subPropertyOf, R.awardsScoreValue))
    with pytest.raises(AssertionError, match='Unauthorized canonical RDF difference'):
        published_contract_graph(graph, 'ontology/textile-assessment.ttl')


@pytest.fixture(scope='module')
def runtime():
    return sum((Graph().parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')), Graph())


@pytest.fixture(scope='module')
def shapes():
    return Graph().parse(ROOT / QUANT)


def score_data(case):
    graph = Graph()
    kind = R.RecyclabilityCriterionResult if case == 'criterion' else A.MeasurementResult
    graph.add((E.result, RDF.type, kind))
    if case == 'absent':
        return graph
    graph.add((E.result, A.awardedScoreValue, E.points))
    graph.add((E.points, RDF.type, C.QuantitativeValue))
    graph.add((E.points, C.numericValue, Literal('3', datatype=XSD.decimal)))
    graph.add((E.points, C.hasMeasurementUnit, U.one))
    if case == 'multiple-links':
        graph.add((E.result, A.awardedScoreValue, E.otherPoints))
        graph.add((E.otherPoints, RDF.type, C.QuantitativeValue))
        graph.add((E.otherPoints, C.numericValue, Literal('4', datatype=XSD.decimal)))
        graph.add((E.otherPoints, C.hasMeasurementUnit, U.one))
    elif case in ['zero', 'negative']:
        graph.set((E.points, C.numericValue, Literal('0' if case == 'zero' else '-2', datatype=XSD.decimal)))
    elif case == 'wrong-type':
        graph.set((E.points, RDF.type, OWL.Class))
    elif case == 'literal-target':
        graph.set((E.result, A.awardedScoreValue, Literal('3')))
    elif case == 'empty-untyped-target':
        graph.remove((E.points, None, None))
    elif case == 'missing-number':
        graph.remove((E.points, C.numericValue, None))
    elif case in ['integer', 'string']:
        graph.set((E.points, C.numericValue, Literal('3', datatype=XSD.integer if case == 'integer' else XSD.string)))
    elif case == 'missing-unit':
        graph.remove((E.points, C.hasMeasurementUnit, None))
    elif case == 'wrong-unit':
        graph.set((E.points, C.hasMeasurementUnit, U.metre))
    elif case == 'multiple-units':
        graph.add((E.points, C.hasMeasurementUnit, U.metre))
    elif case == 'multiple-numbers':
        graph.add((E.points, C.numericValue, Literal('4', datatype=XSD.decimal)))
    elif case == 'literal-kind':
        graph.add((E.points, C.hasQuantityKind, Literal('points')))
    elif case == 'threshold-expression':
        graph.set((E.points, RDF.type, S.MaximumThresholdValue))
        graph.remove((E.points, C.numericValue, None))
        graph.add((E.points, S.maximumValue, Literal('0.3', datatype=XSD.decimal)))
    elif case == 'multiple-with-invalid':
        graph.add((E.result, A.awardedScoreValue, E.empty))
    return graph


CASES = [
    ('measurement', True, True), ('criterion', True, True), ('absent', True, True),
    ('multiple-links', True, True), ('zero', True, True), ('negative', True, True),
    ('wrong-type', False, True), ('literal-target', False, False),
    ('empty-untyped-target', False, False), ('missing-number', False, False),
    ('integer', False, False), ('string', False, False), ('missing-unit', False, False),
    ('wrong-unit', False, False), ('multiple-units', False, False),
    ('multiple-numbers', False, False), ('literal-kind', False, False),
    ('threshold-expression', False, False), ('multiple-with-invalid', False, False),
]


@pytest.mark.parametrize('inference', ['none', 'rdfs'])
@pytest.mark.parametrize('case,before,after', CASES, ids=[c[0] for c in CASES])
def test_supplied_awards_without_new_score_bounds(runtime, shapes, inference, case, before, after):
    ok, _, report = validate(runtime + score_data(case), shacl_graph=shapes,
                              inference=inference, do_owl_imports=False)
    assert bool(ok) == (before if inference == 'none' else after), report


@pytest.fixture(scope='module', params=[RDFS_Semantics, OWLRL_Semantics], ids=['RDFS', 'OWL-RL'])
def model(request, runtime):
    graph = runtime + Graph().parse(ROOT / EXAMPLE)
    graph.add((E.inferredResult, A.awardedScoreValue, E.inferredPoints))
    graph.add((E.rule, R.awardsScoreValue, E.prescribedPoints))
    graph.add((E.indicator, I.derivedFrom, E.measurementResult))
    graph.add((E.indicator, I.hasQuantitativeValue, E.aggregateValue))
    DeductiveClosure(request.param).expand(graph)
    return graph


def test_entailments_preserve_result_rule_measurement_and_indicator_roles(model):
    assert (E.inferredResult, RDF.type, A.AssessmentResult) in model
    assert (E.inferredPoints, RDF.type, C.QuantitativeValue) in model
    for result in [E.measurementResult, E.criterionResult]:
        assert (result, RDF.type, A.AssessmentResult) in model
        for cls in [I.Indicator, R.RecyclabilityScoringRule, A.AssessmentMethod, A.AssessmentExecution]:
            assert (result, RDF.type, cls) not in model
    assert (E.criterionResult, RDF.type, A.MeasurementResult) not in model
    assert (E.inferredResult, RDF.type, A.MeasurementResult) not in model
    assert (E.rule, RDF.type, R.RecyclabilityScoringRule) in model
    assert (E.rule, RDF.type, A.AssessmentResult) not in model
    assert (E.indicator, RDF.type, I.Indicator) in model
    assert (E.indicator, RDF.type, A.AssessmentResult) not in model
    assert set(model.objects(E.measurementResult, A.hasMeasuredValue)) == {E.measuredValue}
    assert set(model.objects(E.measurementResult, A.awardedScoreValue)) == {E.robustPoints}
    assert not list(model.triples((E.rule, A.awardedScoreValue, None)))
    assert not list(model.triples((E.indicator, A.awardedScoreValue, None)))
    assert not list(model.triples((E.unscoredResult, A.awardedScoreValue, None)))
    assert (E.robustPoints, OWL.sameAs, E.measuredValue) not in model
    assert not [o for _, p, o in model if str(p) == 'http://www.daml.org/2002/03/agents/agent-ont#error']
    assert not list(model.subjects(RDF.type, OWL.Nothing))


@pytest.mark.parametrize('inference', ['none', 'rdfs'])
def test_example_and_existing_scoring_fixtures_with_all_profiles(runtime, inference):
    all_shapes = sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())
    for name in [EXAMPLE, 'tests/abox_corpus/fixtures/valid/V05-recyclability-scoring.ttl',
                 'tests/abox_corpus/fixtures/valid/V06-recyclability-overall-result.ttl']:
        ok, _, report = validate(runtime + Graph().parse(ROOT / name), shacl_graph=all_shapes,
                                 inference=inference, do_owl_imports=False)
        # Existing recyclability fixtures intentionally rely on RDFS inference.
        if name == EXAMPLE or inference == 'rdfs':
            assert ok, report
