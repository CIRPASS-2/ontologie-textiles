"""Issue 13: declaration scope, source pairing and compatibility."""
import subprocess
import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.collection import Collection
from rdflib.compare import isomorphic
from rdflib.namespace import SH, XSD
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from pyshacl import validate
from migration import mat_alignment as m
from migration import phase4_contract as p4

R = Namespace("https://w3id.org/eudpp/textile-recyclability#")
D = Namespace("https://w3id.org/eudpp#")
C = Namespace("https://w3id.org/eudpp/textile-connector#")
E = Namespace("https://example.org/issue13/")
ROOT = m.ROOT


def test_exact_approved_delta_and_domain():
    old = p4.expected_graphs()['ontology/textile-recyclability.ttl']
    expected = p4.issue13_expected_graph(old)
    actual = Graph().parse(ROOT / 'ontology/textile-recyclability.ttl')
    assert isomorphic(actual, expected)
    domains = list(actual.objects(R.hasRecycledContentDeclaration, RDFS.domain))
    assert len(domains) == 1
    assert list(Collection(actual, actual.value(domains[0], OWL.unionOf))) == [D.Product, D.MaterialOfComposition]
    assert (R.hasRecycledContentDeclaration, RDFS.range, R.RecycledContentDeclaration) in actual
    assert (D.MaterialOfComposition, RDFS.subClassOf, D.Product) not in actual
    for p in (D.materialRecycledContent, D.materialRecycledContentType):
        assert not list(actual.triples((None, OWL.equivalentProperty, p)))
    assert (R.verifiesRecycledContentDeclaration, RDFS.range, R.RecycledContentDeclaration) in actual
    assert (R.hasReferenceMaterialMassValue, RDF.type, OWL.ObjectProperty) in actual
    assert (R.hasReferenceMaterialMassValue, RDFS.domain, R.RecycledContentDeclaration) in actual
    assert (R.hasReferenceMaterialMassValue, RDFS.range, C.QuantitativeValue) in actual
    original = Graph().parse(data=subprocess.check_output(['git', 'show', '455d8e363148043d365919ea5a2c3051bc2c283c:ontology/textile-recyclability.ttl']).decode('utf8'), format='turtle')
    assert set(original.predicate_objects(R.hasReferenceProductMassValue)) == set(actual.predicate_objects(R.hasReferenceProductMassValue))


@pytest.mark.parametrize('semantics', [RDFS_Semantics, OWLRL_Semantics])
def test_material_and_product_inference(semantics):
    g = m.closure()
    g.parse(ROOT / 'examples/example-18-recycled-content-constituent.ttl')
    g.parse(ROOT / 'examples/example-11-textile-recyclability-v1.1.2.ttl')
    g.add((E.bareMaterial, RDF.type, D.MaterialOfComposition))
    g.add((E.bareMaterial, R.hasRecycledContentDeclaration, E.bareDeclaration))
    DeductiveClosure(semantics).expand(g)
    assert (E.polyester, RDF.type, D.Product) not in g
    assert (E.bareMaterial, RDF.type, D.Product) not in g
    assert (E.bareDeclaration, RDF.type, R.RecycledContentDeclaration) in g
    original = Namespace('https://example.org/textile-recyclability/')
    assert (original.shirt123, RDF.type, D.Product) in g
    assert (original.recycledContentAssessmentResult, R.verifiesRecycledContentDeclaration, original.recycledContentDeclaration) in g


@pytest.fixture(scope='module')
def shapes():
    g = Graph()
    for name in ('textile-recyclability-shapes.ttl', 'textile-quantitative-shapes.ttl'):
        g.parse(ROOT / 'shacl' / name)
    return g


def check(data, shapes):
    return validate(m.closure() + data, shacl_graph=shapes, inference='rdfs', advanced=True)


def test_valid_material_and_original_product(shapes):
    data = Graph().parse(ROOT / 'examples/example-18-recycled-content-constituent.ttl')
    data.parse(ROOT / 'examples/example-11-textile-recyclability-v1.1.2.ttl')
    conforms, _, report = check(data, shapes)
    assert conforms, report
    for decl, origin, fraction, mass in ((E.preDeclaration, R.preConsumerRecycledContent, '0.20', '0.08'), (E.postDeclaration, R.postConsumerRecycledContent, '0.30', '0.12')):
        assert set(data.objects(decl, R.hasRecycledContentSource)) == {origin}
        f = data.value(decl, R.hasRecycledContentMassFractionValue)
        ref = data.value(decl, R.hasReferenceMaterialMassValue)
        recycled = data.value(decl, R.hasRecycledMaterialMassValue)
        assert data.value(f, C.numericValue) == Literal(fraction, datatype=XSD.decimal)
        assert data.value(ref, C.numericValue) == Literal('0.40', datatype=XSD.decimal)
        assert data.value(recycled, C.numericValue) == Literal(mass, datatype=XSD.decimal)


@pytest.mark.parametrize('fault', ['mass', 'source', 'fraction'])
def test_invalid_material_declarations_fail_at_expected_constraint(shapes, fault):
    data = Graph().parse(ROOT / 'examples/example-18-recycled-content-constituent.ttl')
    if fault == 'mass': data.set((E.preMass, C.numericValue, Literal('0.09', datatype=XSD.decimal)))
    elif fault == 'source': data.add((E.preDeclaration, R.hasRecycledContentSource, R.postConsumerRecycledContent))
    else: data.add((E.preDeclaration, R.hasRecycledContentMassFractionValue, E.postFraction))
    conforms, report, _ = check(data, shapes)
    assert not conforms
    results = list(report.subjects(SH.focusNode, E.preDeclaration))
    if fault == 'mass':
        assert any('consistent with recycled mass' in str(report.value(x, SH.resultMessage)) for x in results)
    else:
        path = R.hasRecycledContentSource if fault == 'source' else R.hasRecycledContentMassFractionValue
        assert any((x, SH.resultPath, path) in report and (x, SH.sourceConstraintComponent, SH.MaxCountConstraintComponent) in report for x in results)


def test_cumulative_contract_rejects_unapproved_recyclability_change():
    expected = p4.issue13_expected_graph(p4.expected_graphs()['ontology/textile-recyclability.ttl'])
    expected.add((R.preConsumerRecycledContent, RDFS.comment, Literal('unapproved', lang='en')))
    actual = Graph().parse(ROOT / 'ontology/textile-recyclability.ttl')
    assert not isomorphic(actual, expected)


@pytest.mark.parametrize('case', ['material_wrong', 'product_wrong', 'both_same_node', 'negative_reference', 'wrong_units', 'missing_reference', 'negative_recycled'])
def test_reference_mass_errors(shapes, case):
    if case == 'product_wrong':
        data = Graph().parse(ROOT / 'examples/example-11-textile-recyclability-v1.1.2.ttl')
        x = Namespace('https://example.org/textile-recyclability/')
        value = data.value(x.recycledContentDeclaration, R.hasReferenceProductMassValue)
        data.remove((x.recycledContentDeclaration, R.hasReferenceProductMassValue, value))
        data.add((x.recycledContentDeclaration, R.hasReferenceMaterialMassValue, value))
    else:
        data = Graph().parse(ROOT / 'examples/example-18-recycled-content-constituent.ttl')
        if case == 'material_wrong':
            data.remove((E.preDeclaration, R.hasReferenceMaterialMassValue, E.polyesterMass))
            data.add((E.preDeclaration, R.hasReferenceProductMassValue, E.polyesterMass))
        elif case == 'both_same_node':
            data.add((E.preDeclaration, R.hasReferenceProductMassValue, E.polyesterMass))
        elif case == 'negative_reference': data.set((E.polyesterMass, C.numericValue, Literal('-0.4', datatype=XSD.decimal)))
        elif case == 'wrong_units': data.set((E.preMass, C.hasMeasurementUnit, Namespace('https://si-digital-framework.org/SI/units/').gram))
        elif case == 'missing_reference': data.remove((E.preDeclaration, R.hasReferenceMaterialMassValue, E.polyesterMass))
        elif case == 'negative_recycled': data.set((E.preMass, C.numericValue, Literal('-0.08', datatype=XSD.decimal)))
    conforms, _, report = check(data, shapes)
    assert not conforms, report
    if case in ('material_wrong', 'product_wrong', 'both_same_node'):
        assert 'match it to an unambiguously typed' in report


def test_dual_typed_and_unowned_subjects_do_not_assume_disjoint_classes(shapes):
    data = Graph().parse(ROOT / 'examples/example-18-recycled-content-constituent.ttl')
    data.add((E.polyester, RDF.type, D.Product))
    assert check(data, shapes)[0]
    data.remove((E.polyester, R.hasRecycledContentDeclaration, E.preDeclaration))
    assert check(data, shapes)[0]
