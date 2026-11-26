"""Phase 4 source and cumulative-contract regression checks."""
import pytest
from rdflib import BNode, Graph, Literal, OWL, RDF, RDFS, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import SH
from migration import phase4_contract as p4
from migration.integration_contract import ContractError, parse_turtle


def test_committed_phase3_graphs_are_source_of_expected_graphs():
    expected=p4.expected_graphs()
    assert len(expected)==13
    assert len(p4.subgraph(expected[p4.ASSESS],URIRef(p4.PREFIX+'resultForAssessedAspect')))==18
    assert isomorphic(p4.source_graph(p4.PROFILE),parse_turtle((p4.ROOT/p4.PROFILE).read_text(encoding='utf8'),p4.PROFILE))
    assert not list(p4.source_graph(p4.PROFILE).subjects(RDF.type,OWL.Ontology))


@pytest.mark.parametrize('fault',['range','union','import','header','annotation'])
def test_cumulative_restoration_rejects_unauthorized_graphs(fault):
    g=p4.expected_graphs()[p4.ASSESS]+Graph()
    prop=URIRef(p4.PREFIX+'resultForAssessedAspect')
    if fault=='range':g.add((prop,RDFS.range,URIRef('urn:bad')))
    elif fault=='union':
        node=next(g.objects(prop,RDFS.range));g.add((node,OWL.hasValue,BNode()))
    elif fault=='import':g.add((p4.ASS,OWL.imports,URIRef('urn:bad')))
    elif fault=='header':g.add((p4.ASS,OWL.deprecated,Literal(True)))
    else:g.add((URIRef(p4.PREFIX+'AssessmentExecution'),RDFS.seeAlso,URIRef('urn:bad')))
    with pytest.raises(ContractError,match='Unauthorized Phase 4 graph'):
        p4.restore_phase3(g,p4.ASSESS)


def test_expected_shapes_preserve_reference_duration_and_reject_mutation():
    graph=p4.expected_shapes()
    actual=parse_turtle((p4.ROOT/p4.SHAPES).read_text(encoding='utf8'),p4.SHAPES)
    assert isomorphic(actual,graph)
    ref=URIRef('https://w3id.org/eudpp/textile-shacl#ReferencePeriodShape')
    assert isomorphic(p4.subgraph(p4.old_graph(p4.SHAPES),ref),p4.subgraph(graph,ref))
    altered=graph+Graph();altered.add((p4.AWARD,SH.maxCount,Literal(1)))
    assert not isomorphic(altered,graph)


def test_optional_profile_is_not_in_default_loader():
    from scripts import validate_public as public
    assert (p4.ROOT/p4.PROFILE).parent.name=='profiles'
    assert p4.ROOT/p4.PROFILE not in set((p4.ROOT/'shacl').glob('*.ttl'))


@pytest.mark.parametrize('fault',['property','anonymous','import','header','shape'])
def test_production_contract_rejects_mutated_actual_graph(monkeypatch,fault):
    p4.expected_graphs(); p4.expected_shapes()
    target=p4.SHAPES if fault=='shape' else p4.ASSESS
    actual=(p4.ROOT/target).read_text(encoding='utf8')
    parse=p4.p1.parse_turtle
    def mutated(data,path):
        graph=parse(data,path)
        if path==target and data==actual:
            if fault=='property':graph.add((URIRef(p4.PREFIX+'awardedScoreValue'),RDFS.range,URIRef('urn:bad')))
            elif fault=='anonymous':
                node=next(graph.objects(URIRef(p4.PREFIX+'resultForAssessedAspect'),RDFS.range))
                graph.add((node,OWL.hasValue,BNode()))
            elif fault=='import':graph.add((p4.ASS,OWL.imports,URIRef('urn:bad')))
            elif fault=='header':graph.add((p4.ASS,OWL.deprecated,Literal(True)))
            else:graph.add((p4.AWARD,SH.maxCount,Literal(1)))
        return graph
    monkeypatch.setattr(p4.p1,'parse_turtle',mutated)
    with pytest.raises(ContractError,match='Unauthorized'):
        p4.validate()


@pytest.mark.parametrize('path,message', [('catalog-v001.xml','Catalogue transition mismatch'),
                                          (p4.PROFILE,'Optional profile changed'),
                                          ('scripts/validate_public.py','Public profile selection changed')])
def test_production_contract_rejects_catalogue_and_profile_mutation(monkeypatch,path,message):
    from pathlib import Path
    read=Path.read_bytes;target=p4.ROOT/path
    def altered(self):
        data=read(self)
        return data+b'\n# unauthorized\n' if self==target else data
    monkeypatch.setattr(Path,'read_bytes',altered)
    with pytest.raises(ContractError,match=message):p4.validate()
