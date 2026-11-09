"""Coded protocol values, inclusive presence and preserved quantitative checks."""
import subprocess

import pytest
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import SH, SKOS, XSD

from scripts import validate_public as v
from issue20_support import (
    POINT3_TURTLE, POINT3_SETTING_SHAPE, apply_point3,
    expected_quantitative_shapes, published_contract_graph,
)

ROOT = v.ROOT
POINT2 = '97304854623b9bc669ba8778bfed2c57c1023e2a'
A = Namespace('https://w3id.org/eudpp/textile-assessment#')
C = Namespace('https://w3id.org/eudpp/textile-connector#')
D = Namespace('https://w3id.org/eudpp/textile-durability#')
T = Namespace('https://w3id.org/eudpp/textile-shacl#')
X = Namespace('https://example.org/eu-dpp-textile/issue20-point3/')
U = Namespace('https://si-digital-framework.org/SI/units/')
EXAMPLE = 'examples/example-14-parameter-values-v2.1.0-dev.ttl'
QUANT = 'shacl/textile-quantitative-shapes.ttl'


def point2_bytes(name):
    return subprocess.check_output(['git', 'show', POINT2 + ':' + name], cwd=ROOT)


def test_exact_ontology_delta_preserves_points1_and2_and_all_imports():
    for filename in v.CURRENT_MODULES:
        name = 'ontology/' + filename
        old = point2_bytes(name)
        before = Graph().parse(data=old, format='turtle')
        expected = before + Graph()
        if filename == 'textile-assessment.ttl':
            prop = Graph().parse(data=POINT3_TURTLE, format='turtle')
            assert len(prop) == 8 and not set(prop) & set(before)
            apply_point3(expected)
            assert len(set(expected) - set(before)) == 9
            assert len(set(before) - set(expected)) == 1  # Header guidance only.
            assert set(expected.triples((None, OWL.imports, None))) == set(before.triples((None, OWL.imports, None)))
        else:
            assert (ROOT / name).read_bytes() == old, name
        assert isomorphic(Graph().parse(ROOT / name), expected), name
    for entry, count in [('textile-assessment', 6), ('textile-ontology', 20)]:
        assert len(v.catalogue_import_closure(
            ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/' + entry)) == count


def test_exact_shape_edit_and_approved_single_version_iri_change():
    graph = Graph().parse(ROOT / QUANT)
    assert isomorphic(graph, expected_quantitative_shapes())
    old = point2_bytes(QUANT).decode('utf8')
    start = old.index('tsh:MeasurementParameterSettingShape a sh:NodeShape ;')
    end = old.index('\ntsh:NoQuantitativeValueSubclassShape', start)
    body = POINT3_SETTING_SHAPE[POINT3_SETTING_SHAPE.index('tsh:MeasurementParameterSettingShape'):]
    expected = old[:start] + body + old[end:]
    expected = expected.replace(
        '@prefix sh: <http://www.w3.org/ns/shacl#> .',
        '@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .')
    expected = expected.replace('quantitative/2.0.0>', 'quantitative/2.1.0-dev>')
    assert (ROOT / QUANT).read_bytes() == expected.encode('utf8')
    catalogue = {entry.attrib['name']: entry.attrib['uri'] for entry in v.ET.parse(ROOT / 'catalog-v001.xml').getroot()}
    assert 'https://w3id.org/eudpp/textile-shacl/quantitative/2.0.0' not in catalogue
    assert catalogue['https://w3id.org/eudpp/textile-shacl/quantitative/2.1.0-dev'] == QUANT
    guards = {graph.value(p, SH.path): p for p in graph.objects(T.MeasurementParameterSettingShape, SH.property)}
    assert graph.value(guards[A.hasParameterValue], SH['class']) == C.QuantitativeValue
    assert graph.value(guards[A.hasParameterValue], SH.maxCount) == Literal(1)
    assert graph.value(guards[A.hasParameterConcept], SH['class']) == SKOS.Concept
    assert graph.value(guards[A.hasParameterConcept], SH.maxCount) is None
    assert not list(graph.objects(T.MeasurementParameterSettingShape, SH.xone))


def test_frozen_sources_and_committed_evidence_are_preserved():
    names = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', POINT2, '--', 'dependencies',
         'mireot', 'migration', 'scripts', 'catalog-v001.xml', 'VERSION',
         'examples/example-12-assessed-aspects-v2.1.0-dev.ttl',
         'examples/example-13-assessment-product-event-v2.1.0-dev.ttl',
         'tests/test_issue20_point1.py', 'docs/decisions/TXT-DEC-011.md',
         'docs/decisions/TXT-DEC-012.md', 'docs/ISSUE20_POINT1_IMPLEMENTATION.md',
         'docs/ISSUE20_POINT2_IMPLEMENTATION.md'], cwd=ROOT, text=True).splitlines()
    for name in names:
        expected = point2_bytes(name)
        if name == 'catalog-v001.xml':
            expected = expected.replace(b'textile-shacl/quantitative/2.0.0', b'textile-shacl/quantitative/2.1.0-dev')
        assert (ROOT / name).read_bytes() == expected, name
    for name in ['shacl/textile-soc-shapes.ttl', 'shacl/textile-recyclability-shapes.ttl',
                 'shacl/profiles/textile-soc-complete-report.ttl',
                 'shacl/profiles/textile-assessed-aspect-targets.ttl']:
        assert (ROOT / name).read_bytes() == point2_bytes(name), name


def test_property_has_no_new_restrictions_or_jrc_evidence():
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    prop = A.hasParameterConcept
    assert set(graph.objects(prop, RDF.type)) == {OWL.ObjectProperty}
    assert set(graph.objects(prop, RDFS.domain)) == {A.MeasurementParameterSetting}
    assert set(graph.objects(prop, RDFS.range)) == {SKOS.Concept}
    assert not list(graph.subjects(OWL.onProperty, prop))
    for predicate in [RDFS.subPropertyOf, OWL.inverseOf, OWL.equivalentProperty, OWL.propertyChainAxiom]:
        assert not list(graph.triples((prop, predicate, None)))
        assert not list(graph.triples((None, predicate, prop)))
    assert graph.value(prop, C.sourceLocator) == Literal('docs/decisions/TXT-DEC-013.md', lang='en')
    assert graph.value(prop, C.sourceType) == C.modellingAbstraction
    assert not list(graph.objects(prop, v.DCT.source))
    row = next(r for r in v.derive(v.ontology_graph(ROOT))[0] if r['resource_iri'] == str(prop))
    assert row['has_jrc_evidence'] == 'FALSE' and row['evidence_count'] == '0'


@pytest.mark.parametrize('fault', ['wrong-range', 'functional', 'quantitative-alignment'])
def test_exact_contract_rejects_unapproved_ontology_changes(fault):
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    if fault == 'wrong-range':
        graph.set((A.hasParameterConcept, RDFS.range, C.QuantitativeValue))
    elif fault == 'functional':
        graph.add((A.hasParameterConcept, RDF.type, OWL.FunctionalProperty))
    else:
        graph.add((A.hasParameterConcept, RDFS.subPropertyOf, A.hasParameterValue))
    with pytest.raises(AssertionError, match='Unauthorized canonical RDF difference'):
        published_contract_graph(graph, 'ontology/textile-assessment.ttl')


@pytest.fixture(scope='module')
def runtime():
    return sum((Graph().parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')), Graph())


@pytest.fixture(scope='module')
def shapes():
    return sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())


def setting_data(q, c, fault=None):
    graph = Graph()
    graph.add((X.setting, RDF.type, A.MeasurementParameterSetting))
    graph.add((X.setting, A.settingForParameter, X.parameter))
    graph.add((X.parameter, RDF.type, A.MeasurementParameter))
    for i in range(q):
        value = X['quantity' + str(i)]
        graph.add((X.setting, A.hasParameterValue, value))
        graph.add((value, RDF.type, C.QuantitativeValue))
        graph.add((value, C.numericValue, Literal('5', datatype=XSD.decimal)))
        graph.add((value, C.hasMeasurementUnit, U.one))
    for i in range(c):
        code = X['code' + str(i)]
        graph.add((X.setting, A.hasParameterConcept, code))
        graph.add((code, RDF.type, SKOS.Concept))
    if fault in ['untyped-code', 'wrong-code']:
        graph.remove((X.code0, RDF.type, SKOS.Concept))
        if fault == 'wrong-code':
            graph.add((X.code0, RDF.type, OWL.Class))
    elif fault == 'literal-code':
        graph.set((X.setting, A.hasParameterConcept, Literal('illustrative-code')))
    elif fault == 'wrong-numeric-type':
        graph.set((X.quantity0, RDF.type, OWL.Class))
    elif fault == 'integer':
        graph.set((X.quantity0, C.numericValue, Literal('5', datatype=XSD.integer)))
    elif fault == 'missing-unit':
        graph.remove((X.quantity0, C.hasMeasurementUnit, None))
    elif fault == 'multiple-units':
        graph.add((X.quantity0, C.hasMeasurementUnit, U.metre))
    elif fault == 'literal-quantity-kind':
        graph.add((X.quantity0, C.hasQuantityKind, Literal('kind')))
    elif fault == 'missing-number':
        graph.remove((X.quantity0, C.numericValue, None))
    return graph


CASES = [
    ('numerical', 1, 0, None, True, True, None),
    ('categorical', 0, 1, None, True, True, None),
    ('both', 1, 1, None, True, True, None),
    ('neither', 0, 0, None, False, False, SH.OrConstraintComponent),
    ('multiple-codes', 0, 2, None, True, True, None),
    ('numeric-and-multiple-codes', 1, 2, None, True, True, None),
    ('multiple-numbers', 2, 0, None, False, False, SH.MaxCountConstraintComponent),
    ('multiple-numbers-with-code', 2, 1, None, False, False, SH.MaxCountConstraintComponent),
    ('untyped-code', 0, 1, 'untyped-code', False, True, SH.ClassConstraintComponent),
    ('wrong-code', 0, 1, 'wrong-code', False, True, SH.ClassConstraintComponent),
    ('wrong-code-with-number', 1, 1, 'wrong-code', False, True, SH.ClassConstraintComponent),
    ('literal-code', 0, 1, 'literal-code', False, False, SH.ClassConstraintComponent),
    ('literal-code-with-number', 1, 1, 'literal-code', False, False, SH.ClassConstraintComponent),
    ('wrong-numeric-type-with-code', 1, 1, 'wrong-numeric-type', False, True, SH.ClassConstraintComponent),
    ('integer-with-code', 1, 1, 'integer', False, False, SH.DatatypeConstraintComponent),
    ('missing-unit-with-code', 1, 1, 'missing-unit', False, False, SH.MinCountConstraintComponent),
    ('multiple-units-with-code', 1, 1, 'multiple-units', False, False, SH.MaxCountConstraintComponent),
    ('literal-quantity-kind-with-code', 1, 1, 'literal-quantity-kind', False, False, SH.NodeKindConstraintComponent),
    ('missing-number-with-code', 1, 1, 'missing-number', False, False, SH.OrConstraintComponent),
]


@pytest.mark.parametrize('inference', ['none', 'rdfs'])
@pytest.mark.parametrize('name,q,c,fault,before,after,component', CASES, ids=[c[0] for c in CASES])
def test_value_forms_and_non_bypassable_validation(runtime, shapes, inference, name, q, c, fault, before, after, component):
    ok, report, _ = validate(runtime + setting_data(q, c, fault), shacl_graph=shapes,
                             inference=inference, do_owl_imports=False)
    assert bool(ok) == (before if inference == 'none' else after), name
    if not ok:
        assert component in set(report.objects(None, SH.sourceConstraintComponent)), name


def test_example_and_existing_numeric_examples_remain_valid(runtime, shapes):
    for example in [EXAMPLE, 'examples/example-06-assessment-v1.1.2.ttl',
                    'examples/example-12-assessed-aspects-v2.1.0-dev.ttl']:
        data = Graph().parse(ROOT / example if example.startswith('examples/') else ROOT / 'examples' / example)
        for inference in ['none', 'rdfs']:
            assert validate(runtime + data, shacl_graph=shapes, inference=inference, do_owl_imports=False)[0]


def test_xone_would_impose_unapproved_exclusivity(runtime, shapes):
    exclusive = Graph() + shapes
    alternatives = exclusive.value(T.MeasurementParameterSettingShape, SH['or'])
    exclusive.remove((T.MeasurementParameterSettingShape, SH['or'], alternatives))
    exclusive.add((T.MeasurementParameterSettingShape, SH.xone, alternatives))
    assert not validate(runtime + setting_data(1, 1), shacl_graph=exclusive,
                        inference='none', do_owl_imports=False)[0]


def test_domain_range_and_role_separation(runtime):
    graph = runtime + Graph().parse(ROOT / EXAMPLE)
    graph.add((X.inferredSetting, A.hasParameterConcept, X.inferredConcept))
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    assert (X.inferredSetting, RDF.type, A.MeasurementParameterSetting) in graph
    assert (X.inferredConcept, RDF.type, SKOS.Concept) in graph
    for cls in [A.AssessmentExecution, A.AssessmentCondition, A.MeasurementResult]:
        assert (X.inferredSetting, RDF.type, cls) not in graph
    assert (X.inferredConcept, RDF.type, C.QuantitativeValue) not in graph
    assert (X.cycleType, RDF.type, D.ObservedPerformanceParameter) not in graph
    assert (X.condition, RDF.type, A.AssessmentExecution) not in graph
    assert not [o for _, p, o in graph if str(p) == 'http://www.daml.org/2002/03/agents/agent-ont#error']
    assert not list(graph.subjects(RDF.type, OWL.Nothing))
