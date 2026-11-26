"""Issue 15: bounded CORE reuse and scope clarification regressions."""
import subprocess
import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.compare import isomorphic
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from migration import phase4_contract as p4
from migration import mat_alignment as m

ROOT = m.ROOT
BASE = 'a1d5de600c4f3a216ae7d277404f707e6d3c6715'
D = Namespace('https://w3id.org/eudpp#')
T = Namespace('https://w3id.org/eudpp/textile-core#')
C = Namespace('https://w3id.org/eudpp/textile-codelists#')
E = Namespace('https://example.org/issue15-synthetic/')

def baseline(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)

def test_core_mireot_preserves_complete_authoritative_declaration():
    src = Graph().parse(ROOT / 'dependencies/current-core/p_dpp.owl')
    ext = Graph().parse(ROOT / 'mireot/dpp-textile-mireot.ttl')
    assert set(src.triples((D.commodityCode, None, None))) == set(ext.triples((D.commodityCode, None, None)))
    assert len(list(ext.triples((D.commodityCode, None, None)))) == 7
    assert (D.commodityCode, RDF.type, OWL.DatatypeProperty) in ext
    assert (D.commodityCode, RDFS.domain, D.Product) in ext
    assert (D.commodityCode, RDFS.range, URIRef('http://www.w3.org/2001/XMLSchema#string')) in ext
    assert (ROOT / 'dependencies/current-core/p_dpp.owl').read_bytes() == baseline('dependencies/current-core/p_dpp.owl')

def test_only_approved_core_comments_changed():
    g = Graph().parse(ROOT / 'ontology/textile-core.ttl')
    old = Graph().parse(data=baseline('ontology/textile-core.ttl').decode('utf8'), format='turtle')
    assert isomorphic(g, p4.issue15_expected_graph(old))
    for term in (T.ReusableTextileAbsorbentHygieneProduct, T.TextileCleaningProduct):
        assert (term, RDFS.subClassOf, T.TextileProduct) in g
        assert 'JRC Textile Preparatory Study scope' in str(g.value(term, RDFS.comment))
    for term in (T.defaultStudyScopeStatus, T.StudyScopeStatusConcept):
        assert 'JRC Textile Preparatory Study scope' in str(g.value(term, RDFS.comment))

def test_no_classification_equivalence_or_mapping_added():
    for path in list((ROOT/'ontology').glob('*.ttl')) + list((ROOT/'mireot').glob('*.ttl')):
        actual = Graph().parse(path)
        old = Graph().parse(data=baseline(path.relative_to(ROOT).as_posix()).decode('utf8'), format='turtle')
        forbidden = {OWL.equivalentProperty, RDFS.subPropertyOf, URIRef('http://www.w3.org/2004/02/skos/core#exactMatch'), URIRef('http://www.w3.org/2004/02/skos/core#closeMatch'), URIRef('http://www.w3.org/2004/02/skos/core#broadMatch'), URIRef('http://www.w3.org/2004/02/skos/core#narrowMatch')}
        assert not {t for t in actual if t[1] in forbidden} - set(old)

@pytest.mark.parametrize('semantics', [RDFS_Semantics, OWLRL_Semantics])
def test_synthetic_commodity_code_inferences(semantics):
    g = m.closure()
    g.add((E.product, D.commodityCode, Literal('synthetic-code')))
    DeductiveClosure(semantics).expand(g)
    assert (E.product, RDF.type, D.Product) in g
    assert not list(g.objects(E.product, D.hasProductGroup))
    assert not list(g.objects(E.product, T.hasTextileApparelProductType))

def test_unrelated_graphs_and_examples_unchanged():
    for directory in ('ontology', 'shacl', 'examples'):
        for path in (ROOT / directory).glob('*.ttl'):
            if path.name in ('textile-core.ttl', 'textile-process.ttl', 'example-20-care-symbols.ttl'): continue
            assert path.read_bytes() == baseline(path.relative_to(ROOT).as_posix())
