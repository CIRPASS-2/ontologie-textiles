"""Issue 17 care-symbol modelling and compatibility checks."""
import subprocess
import pytest
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL, SKOS
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from pyshacl import validate
from migration import phase4_contract as p4
from migration import mat_alignment as m

ROOT = m.ROOT
BASE = '637b937481ccdfb87ca9798cb66549183453c167'
P = Namespace('https://w3id.org/eudpp/textile-process#')
D = Namespace('https://w3id.org/eudpp#')
E = Namespace('https://example.org/issue17/')

def base(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)

def test_exact_approved_graph_and_unchanged_prior_resources():
    old = Graph().parse(data=base('ontology/textile-process.ttl').decode('utf8'), format='turtle')
    g = Graph().parse(ROOT/'ontology/textile-process.ttl')
    assert isomorphic(g, p4.issue17_expected_graph(old))
    for term in (P.TextileCareInstruction, P.DigitalTextileCareInstruction, P.CareMethodConcept, P.hasCareInstruction, P.hasProcessMethod):
        assert isomorphic(p4.subgraph(g, term), p4.subgraph(old, term))
    assert (P.CareSymbolConcept, RDF.type, OWL.Class) in g
    assert (P.CareSymbolConcept, RDFS.subClassOf, SKOS.Concept) in g
    assert (P.hasCareSymbol, RDF.type, OWL.ObjectProperty) in g
    assert (P.hasCareSymbol, RDFS.domain, P.TextileCareInstruction) in g
    assert (P.hasCareSymbol, RDFS.range, P.CareSymbolConcept) in g
    assert not list(g.objects(P.hasCareSymbol, RDFS.subPropertyOf))
    assert not list(g.objects(P.CareSymbolConcept, OWL.equivalentClass))
    assert (P.CareSymbolConcept, RDFS.subClassOf, P.CareMethodConcept) not in g
    assert (P.CareSymbolConcept, RDFS.subClassOf, P.ProcessMethodConcept) not in g
    assert (P.hasCareSymbol, RDF.type, OWL.FunctionalProperty) not in g

def test_scheme_and_provenance():
    g = Graph().parse(ROOT/'ontology/textile-process.ttl')
    assert (P.CareSymbolScheme, RDF.type, SKOS.ConceptScheme) in g
    for concept,num in ((P.normalWashMaximum70C,'3096'),(P.flatDripDrying,'3101')):
        assert (concept,RDF.type,P.CareSymbolConcept) in g
        assert (concept,RDF.type,SKOS.Concept) in g
        assert (concept,SKOS.inScheme,P.CareSymbolScheme) in g
        assert (P.CareSymbolScheme,SKOS.hasTopConcept,concept) in g
        assert (concept,DCTERMS.references,URIRef('https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Agrs%3A7000%3A'+num)) in g
        assert not list(g.objects(concept,SKOS.notation))
        for pred in (SKOS.exactMatch,SKOS.closeMatch,OWL.sameAs): assert not list(g.objects(concept,pred))

@pytest.mark.parametrize('semantics',[RDFS_Semantics, OWLRL_Semantics])
def test_symbol_inference_does_not_assert_executions(semantics):
    g=m.closure();g.parse(ROOT/'examples/example-20-care-symbols.ttl')
    DeductiveClosure(semantics).expand(g)
    assert (E.instruction,RDF.type,P.TextileCareInstruction) in g
    assert (E.instruction,RDF.type,D.DigitalInstruction) in g
    assert len(set(g.objects(E.instruction,P.hasCareSymbol))) == 2
    assert (E.instruction,RDF.type,P.TextileProcessExecution) not in g
    assert (E.instruction,RDF.type,P.TextileProcess) not in g
    for c in (P.normalWashMaximum70C,P.flatDripDrying):
        assert (c,RDF.type,P.CareSymbolConcept) in g
        assert (c,RDF.type,P.ProcessMethodConcept) not in g

def test_existing_and_new_examples_conform():
    shapes=Graph()
    for path in (ROOT/'shacl').glob('*.ttl'): shapes.parse(path)
    g=m.closure()
    for name in ('example-03-process-v1.1.2.ttl','example-20-care-symbols.ttl'): g.parse(ROOT/'examples'/name)
    ok,_,report=validate(g,shacl_graph=shapes,inference='rdfs',advanced=True)
    assert ok,report

def assert_shacl_snapshot(expected, actual):
    assert actual == expected


def test_dependencies_shapes_and_unrelated_modules_unchanged():
    for directory in ('mireot','dependencies/current-core','ontology'):
        for path in (ROOT/directory).glob('*'):
            if not path.is_file() or path.name=='textile-process.ttl': continue
            assert path.read_bytes() == base(path.relative_to(ROOT).as_posix())
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, '--', 'shacl/'], cwd=ROOT, text=True).splitlines()
    expected = {name: base(name) for name in names}
    actual = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in (ROOT/'shacl').rglob('*') if path.is_file()}
    assert_shacl_snapshot(expected, actual)
    assert 'shacl/profiles/textile-assessed-aspect-targets.ttl' in expected


def test_recursive_shacl_comparison_detects_inventory_and_content_changes():
    expected = {'shacl/a.ttl': b'a', 'shacl/profiles/b.ttl': b'b'}
    assert_shacl_snapshot(expected, expected.copy())
    for changed in ({'shacl/a.ttl': b'a'},
                    {**expected, 'shacl/profiles/new.ttl': b'new'},
                    {**expected, 'shacl/profiles/b.ttl': b'changed'}):
        with pytest.raises(AssertionError):
            assert_shacl_snapshot(expected, changed)


def test_traceability_notes_are_narrow_and_reproducible():
    from scripts import validate_public as v
    resources, evidence, sources, _ = v.derive(v.ontology_graph(ROOT), ROOT)
    targets = {str(P[name]) for name in ('CareSymbolConcept', 'CareSymbolScheme', 'hasCareSymbol', 'normalWashMaximum70C', 'flatDripDrying')}
    rows = {r['resource_iri']: r for r in resources}
    assert targets <= rows.keys()
    for iri in targets:
        assert rows[iri]['provenance_category'] == 'projectDecision'
        assert rows[iri]['traceability_status'] == 'PARTIAL'
        assert rows[iri]['evidence_count'] == '0'
        assert rows[iri]['notes'].startswith('Issue 17 project modelling decision;')
    assert all(not r['notes'].startswith('Issue 17 project modelling decision;') for iri, r in rows.items() if iri not in targets)
    assert (ROOT/'traceability/textile-resource-traceability.csv').read_bytes() == v.csv_bytes(v.RESOURCE_FIELDS, resources)
    assert (ROOT/'traceability/textile-resource-evidence.csv').read_bytes() == v.csv_bytes(v.EVIDENCE_FIELDS, evidence)
    assert (ROOT/'traceability/source-documents.csv').read_bytes() == v.csv_bytes(v.SOURCE_FIELDS, sources)
