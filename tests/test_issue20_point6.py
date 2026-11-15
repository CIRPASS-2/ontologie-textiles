"""Instance-level temporal reuse: precision, optionality and unchanged schema."""
import subprocess
from datetime import datetime

import pytest
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.namespace import DCTERMS, XSD, SH

from scripts import validate_public as v

ROOT = v.ROOT
BASELINE = '5a0e76a39b543ef09f52d915e6215bd98bc6ea8e'
A = Namespace('https://w3id.org/eudpp/textile-assessment#')
P = Namespace('http://www.w3.org/ns/prov#')
D = Namespace('https://w3id.org/eudpp#')
EPCIS = Namespace('https://ref.gs1.org/epcis/')
PROCESS = Namespace('https://w3id.org/eudpp/textile-process#')
E = Namespace('https://example.org/textile-assessment/issue20-point6/')
EXAMPLE = 'examples/example-17-assessment-times-v2.1.0-dev.ttl'
EXECUTIONS = {E.completed, E.longRunning, E.eventLinked, E.dateOnly, E.undated}

# Test-only projection, checked against the authoritative W3C PROV-O graph
# during focused implementation validation. Not imported by production modules.
# The complete authoritative graph is also exercised in memory separately;
# normal regression tests remain offline and do not fetch remote imports.
PROV_TIME_AXIOMS = '''
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
prov:startedAtTime a owl:DatatypeProperty ;
    rdfs:domain prov:Activity ; rdfs:range xsd:dateTime .
prov:endedAtTime a owl:DatatypeProperty ;
    rdfs:domain prov:Activity ; rdfs:range xsd:dateTime .
prov:Activity owl:disjointWith prov:Entity .
'''


def test_all_schema_profiles_dependencies_and_prior_evidence_are_byte_preserved():
    paths = subprocess.check_output([
        'git', 'ls-tree', '-r', '--name-only', BASELINE, '--',
        'ontology', 'mireot', 'dependencies', 'shacl', 'catalog-v001.xml', 'VERSION',
        'migration', 'scripts', 'examples', 'traceability', 'docs/widoco', 'widoco',
        'docs/decisions', 'tests/abox_corpus',
        *['tests/test_issue20_point' + str(n) + '.py' for n in range(1, 6)],
        'tests/issue20_support.py',
        *['docs/ISSUE20_POINT' + str(n) + '_IMPLEMENTATION.md' for n in range(1, 6)],
    ], cwd=ROOT, text=True).splitlines()
    for path in paths:
        current = (ROOT / path).read_bytes()
        before = subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)
        # These three reference files are outside the byte-owned package and
        # already have mixed checkout EOLs. Preserve their full text; every
        # owned source/profile/dependency retains a strict byte comparison.
        if path in v.PRESERVED_REFERENCE_MATERIAL:
            assert current.replace(b'\r\n', b'\n') == before.replace(b'\r\n', b'\n'), path
        else:
            assert current == before, path
    paths = v.catalogue_import_closure(ROOT / 'catalog-v001.xml',
                                      'https://w3id.org/eudpp/textile-ontology')
    assert len(paths) == 20
    for path in paths:
        assert not list(Graph().parse(path).subjects(RDF.type, P.Activity))
        assert not list(Graph().parse(path).triples((None, OWL.imports,
                                                   URIRef('http://www.w3.org/ns/prov-o'))))


@pytest.fixture(scope='module')
def example():
    return Graph().parse(ROOT / EXAMPLE)


@pytest.fixture(scope='module')
def runtime():
    return sum((Graph().parse(p) for p in v.catalogue_import_closure(
        ROOT / 'catalog-v001.xml', 'https://w3id.org/eudpp/textile-ontology')), Graph())


def temporal_guard():
    # Guard applies only to supplied values on AssessmentExecution instances.
    # It is not part of any production SHACL profile or the public validator.
    return Graph().parse(data='''
      @prefix sh: <http://www.w3.org/ns/shacl#> .
      @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
      @prefix a: <https://w3id.org/eudpp/textile-assessment#> .
      @prefix prov: <http://www.w3.org/ns/prov#> .
      @prefix dcterms: <http://purl.org/dc/terms/> .
      [] a sh:NodeShape ; sh:targetClass a:AssessmentExecution ;
         sh:property [ sh:path prov:startedAtTime ; sh:datatype xsd:dateTime ; sh:pattern "T[0-9]{2}:[0-9]{2}:[0-9]{2}" ],
                     [ sh:path prov:endedAtTime ; sh:datatype xsd:dateTime ; sh:pattern "T[0-9]{2}:[0-9]{2}:[0-9]{2}" ],
                     [ sh:path dcterms:date ; sh:datatype xsd:date ] .
    ''', format='turtle')


def test_example_context_optional_times_and_result_query(example):
    assert set(example.subjects(RDF.type, A.AssessmentExecution)) == EXECUTIONS
    for execution in EXECUTIONS:
        assert (execution, RDF.type, P.Activity) in example
        assert set(example.objects(execution, A.assessesProduct)) == {E.product}
        assert set(example.objects(execution, A.appliesMethod)) == {E.method}
    assert not list(example.objects(E.completed, A.isRepresentedByProductEvent))
    assert not list(example.objects(E.completed, P.startedAtTime))
    assert not any(list(example.objects(E.undated, p)) for p in
                   [P.startedAtTime, P.endedAtTime, DCTERMS.date])
    assert set(example.objects(E.dateOnly, DCTERMS.date)) == {
        Literal('2026-11-14', datatype=XSD.date)}
    assert not any(list(example.objects(E.dateOnly, p)) for p in
                   [P.startedAtTime, P.endedAtTime])
    assert example.value(E.longRunning, P.startedAtTime) != example.value(E.longRunning, P.endedAtTime)
    rows = list(example.query('''
      SELECT ?time WHERE {
        <https://example.org/textile-assessment/issue20-point6/result>
        <https://w3id.org/eudpp/textile-assessment#resultOfAssessment>/
        <http://www.w3.org/ns/prov#endedAtTime> ?time .
      }
    '''))
    assert [r.time for r in rows] == [example.value(E.longRunning, P.endedAtTime)]
    assert not list(example.objects(E.result, P.endedAtTime))


@pytest.mark.parametrize('inference', ['none', 'rdfs'])
def test_example_passes_test_only_guard(example, inference):
    shapes = temporal_guard()
    assert not list(shapes.triples((None, SH.minCount, None)))
    assert not list(shapes.triples((None, SH.maxCount, None)))
    assert validate(example, shacl_graph=shapes, inference=inference)[0]


CASES = [
    (P.endedAtTime, Literal('2026-11-15T10:00:00Z', datatype=XSD.dateTime), True),
    (P.startedAtTime, Literal('2026-11-15T10:00:00+01:00', datatype=XSD.dateTime), True),
    (P.endedAtTime, Literal('2026-11-15T10:00:00', datatype=XSD.dateTime), True),
    (DCTERMS.date, Literal('2026-11-15', datatype=XSD.date), True),
    (P.endedAtTime, Literal('2026-11-15', datatype=XSD.date), False),
    (DCTERMS.date, Literal('2026-11-15T10:00:00Z', datatype=XSD.dateTime), False),
    (P.endedAtTime, Literal('2026-11-15T10:00:00Z', datatype=XSD.dateTimeStamp), False),
    (P.endedAtTime, Literal('2026-11-15T10:00:00Z'), False),
    (P.endedAtTime, E.notALiteral, False),
    (DCTERMS.date, E.notALiteral, False),
    (P.endedAtTime, Literal('not-a-time', datatype=XSD.dateTime, normalize=False), False),
    (P.startedAtTime, Literal('2026-11-15', datatype=XSD.dateTime, normalize=False), False),
    (DCTERMS.date, Literal('2026-02-30', datatype=XSD.date, normalize=False), False),
    (DCTERMS.date, Literal('2026-11-15'), False),
]


@pytest.mark.parametrize('inference', ['none', 'rdfs'])
@pytest.mark.parametrize('predicate,value,expected', CASES)
def test_supplied_value_precision_and_datatypes(predicate, value, expected, inference):
    graph = Graph()
    graph.add((E.probe, RDF.type, A.AssessmentExecution))
    graph.add((E.probe, predicate, value))
    assert bool(validate(graph, shacl_graph=temporal_guard(), inference=inference)[0]) == expected


def test_multiple_values_allowed_and_bad_values_cannot_hide(example):
    graph = example + Graph()
    graph.add((E.completed, P.endedAtTime, Literal('2026-11-10T15:00:00', datatype=XSD.dateTime)))
    assert validate(graph, shacl_graph=temporal_guard())[0]
    graph.add((E.completed, P.endedAtTime, E.notALiteral))
    assert not validate(graph, shacl_graph=temporal_guard())[0]


def test_guard_does_not_apply_to_unrelated_prov_activities():
    graph = Graph()
    graph.add((E.other, RDF.type, P.Activity))
    graph.add((E.other, P.endedAtTime, Literal('invalid')))
    assert validate(graph, shacl_graph=temporal_guard())[0]


def test_production_profiles_do_not_claim_temporal_validation(runtime, example):
    graph = runtime + example
    graph.add((E.completed, P.endedAtTime, E.notALiteral))
    shapes = sum((Graph().parse(p) for p in (ROOT / 'shacl').glob('*.ttl')), Graph())
    assert validate(graph, shacl_graph=shapes, inference='rdfs', do_owl_imports=False)[0]
    assert not validate(graph, shacl_graph=temporal_guard(), inference='rdfs')[0]


def assert_temporal_roles(graph):
    for execution in EXECUTIONS | {E.inferred}:
        assert (execution, RDF.type, P.Activity) in graph
        for cls in [A.AssessmentResult, PROCESS.TextileProcessExecution, D.ProductEvent, EPCIS.EPCISEvent]:
            assert (execution, RDF.type, cls) not in graph
    assert not any(list(graph.objects(E.dateOnly, p)) for p in [P.startedAtTime, P.endedAtTime])
    assert not any(list(graph.objects(E.undated, p)) for p in [P.startedAtTime, P.endedAtTime, DCTERMS.date])
    assert not list(graph.objects(E.result, P.endedAtTime))
    assert not list(graph.objects(E.result, P.generatedAtTime))
    assert set(graph.objects(E.eventLinked, P.endedAtTime)) == {
        Literal('2026-11-13T10:15:00Z', datatype=XSD.dateTime)}
    # OWL-RL installs datatype converters globally: parsing before or after
    # another reasoning test can preserve Z or normalize it to +00:00.
    # Require the same single typed instant, not one lexical spelling of UTC.
    for predicate, expected in [(EPCIS.eventTime, '2026-11-13T10:05:00Z'),
                                (EPCIS.recordTime, '2026-11-14T08:00:00Z')]:
        values = set(graph.objects(E.observation, predicate))
        assert len(values) == 1
        value = next(iter(values))
        assert value.datatype == XSD.dateTimeStamp
        assert datetime.fromisoformat(str(value)) == datetime.fromisoformat(expected)
    assert not list(graph.objects(E.eventLinked, EPCIS.eventTime))
    assert not list(graph.objects(E.observation, P.endedAtTime))
    assert not [o for _, p, o in graph if str(p) == 'http://www.daml.org/2002/03/agents/agent-ont#error']
    assert not list(graph.subjects(RDF.type, OWL.Nothing))


@pytest.mark.parametrize('semantics', [RDFS_Semantics, OWLRL_Semantics])
def test_optional_prov_axioms_and_event_mapping_preserve_roles(runtime, example, semantics):
    graph = runtime + example + Graph().parse(ROOT / 'dependencies/current-core/event.owl')
    graph.add((E.inferred, RDF.type, A.AssessmentExecution))
    graph.add((E.inferred, P.endedAtTime, Literal('2026-11-15T10:00:00', datatype=XSD.dateTime)))
    assert (E.inferred, RDF.type, P.Activity) not in graph
    graph += Graph().parse(data=PROV_TIME_AXIOMS, format='turtle')
    DeductiveClosure(semantics).expand(graph)
    assert_temporal_roles(graph)
