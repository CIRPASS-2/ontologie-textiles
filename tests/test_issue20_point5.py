"""Controlled aggregate conclusions with explicit vocabulary and validation limits."""
import subprocess

import pytest
from owlrl import DeductiveClosure, OWLRL_Semantics, RDFS_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import SH, SKOS

from scripts import validate_public as v
from issue20_support import POINT5_TURTLE, published_contract_graph

ROOT = v.ROOT
POINT4 = '77dfddbe8bc509a65fec0037617506dc34072d36'
A = Namespace('https://w3id.org/eudpp/textile-assessment#')
C = Namespace('https://w3id.org/eudpp/textile-connector#')
R = Namespace('https://w3id.org/eudpp/textile-recyclability#')
I = Namespace('https://w3id.org/eudpp/textile-indicator#')
REFERENCE_E = Namespace('https://example.org/textile-recyclability/')
E = Namespace('https://example.org/textile-recyclability/issue20-point5/')
APP = Namespace('https://example.org/application/recyclability-outcomes/')
EXAMPLE = 'examples/example-16-assessment-outcomes-v2.1.0-dev.ttl'
REFERENCE = 'tests/abox_corpus/fixtures/valid/V06-recyclability-overall-result.ttl'


def baseline(name):
    return subprocess.check_output(['git', 'show', POINT4 + ':' + name], cwd=ROOT)


def renamed_reference():
    """Apply only the approved instance-IRI renaming to the unchanged V06 graph."""
    reference = Graph().parse(ROOT / REFERENCE)
    renamed = Graph()
    for triple in reference:
        renamed.add(tuple(
            URIRef(str(E) + str(term)[len(str(REFERENCE_E)):])
            if isinstance(term, URIRef) and str(term).startswith(str(REFERENCE_E))
            else term for term in triple))
    assert len(renamed) == len(reference)
    return renamed


def test_only_eight_property_triples_are_added_to_ontology_sources():
    addition = Graph().parse(data=POINT5_TURTLE, format='turtle')
    assert len(addition) == 8
    for filename in v.CURRENT_MODULES:
        name = 'ontology/' + filename
        old = baseline(name)
        expected = Graph().parse(data=old, format='turtle')
        if filename == 'textile-assessment.ttl':
            assert not set(addition) & set(expected)
            expected += addition
        else:
            assert (ROOT / name).read_bytes() == old, name
        assert isomorphic(Graph().parse(ROOT / name), expected), name


def test_production_profiles_and_all_protected_inputs_are_byte_preserved():
    names = subprocess.check_output([
        'git', 'ls-tree', '-r', '--name-only', POINT4, '--',
        'dependencies', 'mireot', 'migration', 'scripts', 'catalog-v001.xml', 'VERSION',
        'examples', 'docs/decisions', 'tests/abox_corpus', 'tests/test_issue20_point1.py',
        'docs/ISSUE20_POINT1_IMPLEMENTATION.md', 'docs/ISSUE20_POINT2_IMPLEMENTATION.md',
        'docs/ISSUE20_POINT3_IMPLEMENTATION.md', 'docs/ISSUE20_POINT4_IMPLEMENTATION.md',
    ], cwd=ROOT, text=True).splitlines()
    names += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'shacl').rglob('*.ttl')]
    for name in names:
        assert (ROOT / name).read_bytes() == baseline(name), name
    assert (ROOT / 'shacl/README.md').read_bytes().startswith(baseline('shacl/README.md'))
    for entry, count in [('textile-assessment', 6), ('textile-ontology', 20)]:
        paths = v.catalogue_import_closure(ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/' + entry)
        assert len(paths) == count
        if entry == 'textile-assessment':
            assert (SKOS.Concept, RDF.type, OWL.Class) in sum((Graph().parse(p) for p in paths), Graph())


def test_property_is_independent_optional_and_has_issue_traceability():
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    prop = A.hasAssessmentOutcome
    assert set(graph.objects(prop, RDF.type)) == {OWL.ObjectProperty}
    assert set(graph.objects(prop, RDFS.domain)) == {A.AssessmentResult}
    assert set(graph.objects(prop, RDFS.range)) == {SKOS.Concept}
    assert not list(graph.subjects(OWL.onProperty, prop))
    for predicate in [RDFS.subPropertyOf, OWL.equivalentProperty, OWL.inverseOf, OWL.propertyChainAxiom]:
        assert not list(graph.triples((prop, predicate, None)))
        assert not list(graph.triples((None, predicate, prop)))
    assert graph.value(prop, C.sourceLocator) == Literal('docs/decisions/TXT-DEC-015.md', lang='en')
    assert graph.value(prop, C.sourceType) == C.modellingAbstraction
    assert not list(graph.objects(prop, v.DCT.source))
    row = next(r for r in v.derive(v.ontology_graph(ROOT))[0] if r['resource_iri'] == str(prop))
    assert row['evidence_count'] == '0' and row['has_jrc_evidence'] == 'FALSE'


@pytest.mark.parametrize('fault', ['criterion-range', 'functional', 'indicator-alignment'])
def test_exact_contract_rejects_unapproved_changes(fault):
    graph = Graph().parse(ROOT / 'ontology/textile-assessment.ttl')
    if fault == 'criterion-range':
        graph.set((A.hasAssessmentOutcome, RDFS.range, R.RecyclabilityOutcomeConcept))
    elif fault == 'functional':
        graph.add((A.hasAssessmentOutcome, RDF.type, OWL.FunctionalProperty))
    else:
        graph.add((A.hasAssessmentOutcome, RDFS.subPropertyOf, I.hasCategoricalValue))
    with pytest.raises(AssertionError, match='Unauthorized canonical RDF difference'):
        published_contract_graph(graph, 'ontology/textile-assessment.ttl')


@pytest.fixture(scope='module')
def runtime():
    return sum((Graph().parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')), Graph())


@pytest.fixture(scope='module')
def assessment():
    return sum((Graph().parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-assessment')), Graph())


@pytest.fixture
def guard():
    # Test-only supplied-value checking; no production profile is added or changed.
    return Graph().parse(data='''
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
        [] a sh:NodeShape ; sh:targetObjectsOf txtass:hasAssessmentOutcome ; sh:class skos:Concept .
    ''', format='turtle')


def outcome_data(case):
    graph = Graph().parse(ROOT / EXAMPLE)
    graph.remove((E.mechanicalRouteResult, A.hasAssessmentOutcome, None))
    if case == 'absent':
        return graph
    code = {'positive': APP.recyclableUnderMethod, 'negative': APP.notRecyclableUnderMethod,
            'inconclusive': APP.inconclusiveUnderMethod}.get(case, APP.inconclusiveUnderMethod)
    if case in ['untyped', 'wrong-type']:
        code = APP.untyped
        if case == 'wrong-type':
            graph.add((code, RDF.type, OWL.Class))
    elif case == 'literal':
        code = Literal('recyclable')
    elif case == 'criterion-code':
        code = R.criterionSatisfied  # Deliberate semantic misuse; generic typing cannot reject it.
    graph.add((E.mechanicalRouteResult, A.hasAssessmentOutcome, code))
    if case == 'multiple':
        graph.add((E.mechanicalRouteResult, A.hasAssessmentOutcome, APP.recyclableUnderMethod))
    return graph


CASES = [
    ('positive', True, True), ('negative', True, True), ('inconclusive', True, True),
    ('absent', True, True), ('multiple', True, True), ('untyped', False, True),
    ('wrong-type', False, True), ('literal', False, False), ('criterion-code', True, True),
]


@pytest.mark.parametrize('inference', ['none', 'rdfs'])
@pytest.mark.parametrize('case,before,after', CASES, ids=[c[0] for c in CASES])
def test_optional_value_guard_and_its_limits(assessment, guard, inference, case, before, after):
    # Add the existing criterion concept declaration to isolate typing from module loading.
    data = outcome_data(case)
    data.add((R.criterionSatisfied, RDF.type, SKOS.Concept))
    assert len(guard) == 3 and not list(guard.triples((None, SH.minCount, None)))
    ok, _, report = validate(assessment + data, shacl_graph=guard,
                              inference=inference, do_owl_imports=False)
    assert bool(ok) == (before if inference == 'none' else after), report


def test_example_preserves_reference_context_and_uses_only_application_verdicts():
    reference = renamed_reference()
    example = Graph().parse(ROOT / EXAMPLE)
    assert set(reference) <= set(example)
    assert not list(reference.triples((None, A.hasAssessmentOutcome, None)))
    assert set(example.objects(E.mechanicalRouteResult, A.hasAssessmentOutcome)) == {APP.inconclusiveUnderMethod}
    for code in [APP.recyclableUnderMethod, APP.notRecyclableUnderMethod, APP.inconclusiveUnderMethod]:
        assert set(example.objects(code, RDF.type)) == {SKOS.Concept}
        assert example.value(code, SKOS.definition) and example.value(code, SKOS.prefLabel)
        assert not list(example.objects(code, SKOS.inScheme))
    assert not list(example.subjects(RDF.type, OWL.Class))
    assert not list(example.subjects(RDF.type, SKOS.ConceptScheme))


@pytest.mark.parametrize('case', ['positive', 'negative', 'inconclusive', 'absent'])
def test_complete_route_specific_reports_with_all_current_profiles(runtime, guard, case):
    shapes = sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())
    ok, _, report = validate(runtime + outcome_data(case), shacl_graph=shapes + guard,
                              inference='rdfs', do_owl_imports=False)
    assert ok, report


def test_production_validation_does_not_claim_the_test_only_guard(runtime, guard):
    shapes = sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())
    data = runtime + outcome_data('literal')
    assert validate(data, shacl_graph=shapes, inference='rdfs', do_owl_imports=False)[0]
    assert not validate(data, shacl_graph=shapes + guard, inference='rdfs', do_owl_imports=False)[0]


@pytest.fixture(scope='module', params=[RDFS_Semantics, OWLRL_Semantics], ids=['RDFS', 'OWL-RL'])
def model(request, runtime):
    reference = runtime + renamed_reference()
    candidate = runtime + outcome_data('positive')
    candidate.add((E.inferredResult, A.hasAssessmentOutcome, APP.inferredConcept))
    for graph in [reference, candidate]:
        DeductiveClosure(request.param).expand(graph)
    return reference, candidate


def test_context_and_expected_classifications_without_unintended_roles(model):
    _, graph = model
    assert (E.inferredResult, RDF.type, A.AssessmentResult) in graph
    assert (APP.inferredConcept, RDF.type, SKOS.Concept) in graph
    for result in [E.inferredResult, E.mechanicalRouteResult]:
        for cls in [A.MeasurementResult, R.RecyclabilityCriterionResult, I.Indicator]:
            assert (result, RDF.type, cls) not in graph
    assert (APP.recyclableUnderMethod, RDF.type, R.RecyclabilityOutcomeConcept) not in graph
    assert set(graph.objects(E.mechanicalRouteAssessment, A.appliesMethod)) == {E.method}
    assert set(graph.objects(E.mechanicalRouteAssessment, A.assessesProduct)) == {E.product}
    assert set(graph.objects(E.mechanicalRouteResult, R.resultForRecyclingRoute)) == {E.route}
    assert not [o for _, p, o in graph if str(p) == 'http://www.daml.org/2002/03/agents/agent-ont#error']
    assert not list(graph.subjects(RDF.type, OWL.Nothing))


def test_criterion_outcomes_do_not_entail_an_overall_verdict(model):
    reference, candidate = model
    assert list(reference.triples((None, R.hasCriterionOutcome, None)))
    assert not list(reference.triples((None, A.hasAssessmentOutcome, None)))
    criteria = set(reference.objects(E.mechanicalRouteResult, R.hasCriterionResult))
    assert len(criteria) == 7
    for criterion in criteria:
        assert set(reference.objects(criterion, R.hasCriterionOutcome)) == set(candidate.objects(criterion, R.hasCriterionOutcome))
        assert not list(candidate.objects(criterion, A.hasAssessmentOutcome))
