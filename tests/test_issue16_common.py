"""Issue 16 compatibility and reference-period regression tests."""
from pathlib import Path
from collections import defaultdict, Counter
from xml.etree import ElementTree as ET
from rdflib import Graph, Namespace, RDF, OWL, URIRef
from rdflib.namespace import SH
from pyshacl import validate
from scripts import validate_public as v

ROOT=Path(__file__).resolve().parents[1]
EX=Namespace("https://example.org/issue16/")
C=Namespace("https://w3id.org/eudpp/textile-connector#")
OLD=URIRef("https://w3id.org/eudpp/textile-connector")
NEW=URIRef("https://w3id.org/eudpp/textile-common")

def test_common_identity_and_complete_legacy_representation():
    from scripts.generate_common_connector import verify
    common=Graph().parse(ROOT/"ontology/textile-common.ttl")
    connector=Graph().parse(ROOT/"compat/textile-connector.ttl")
    assert set(common.subjects(RDF.type,OWL.Ontology))=={NEW}
    assert set(connector.subjects(RDF.type,OWL.Ontology))=={OLD}
    assert (OLD,OWL.imports,NEW) not in connector
    assert verify(common,connector)==(37,395)
    assert (C.QuantitativeValue,RDF.type,OWL.Class) in connector
    cat=ROOT/"catalog-v001.xml"
    assert len(v.catalogue_import_closure(cat,OLD))==2
    assert ROOT/"ontology/textile-common.ttl" in v.catalogue_import_closure(cat,NEW)

def test_reference_period_cases():
    ont=Graph();shapes=Graph()
    for p in (ROOT/"ontology").glob("textile-*.ttl"): ont.parse(p)
    for p in (ROOT/"mireot").glob("*.ttl"): ont.parse(p)
    for p in (ROOT/"shacl").glob("*.ttl"): shapes.parse(p)
    prefix="""@prefix e: <https://example.org/issue16/> . @prefix c: <https://w3id.org/eudpp/textile-connector#> . @prefix t: <https://w3id.org/eudpp/textile-soc#> . @prefix d: <https://w3id.org/eudpp#> . @prefix u: <https://si-digital-framework.org/SI/units/> . @prefix xsd: <http://www.w3.org/2001/XMLSchema#> . """
    cases={
      'boundaries':'c:periodStart "2025-01-01T00:00:00Z"^^xsd:dateTime; c:periodEnd "2025-01-03T00:00:00Z"^^xsd:dateTime',
      'start_duration':'c:periodStart "2025-01-01T00:00:00Z"^^xsd:dateTime; c:hasReferenceDuration e:v_start_duration',
      'end_duration':'c:periodEnd "2025-01-03T00:00:00Z"^^xsd:dateTime; c:hasReferenceDuration e:v_end_duration',
      'duration_only':'c:hasReferenceDuration e:v_duration_only',
      'second':'c:hasReferenceDuration e:v_second', 'hour':'c:hasReferenceDuration e:v_hour',
      'celsius':'c:hasReferenceDuration e:v_celsius', 'negative':'c:hasReferenceDuration e:v_negative',
      'zero':'c:hasReferenceDuration e:v_zero', 'unknown':'c:hasReferenceDuration e:v_unknown',
      'time_kind':'c:hasReferenceDuration e:v_time_kind', 'length_kind':'c:hasReferenceDuration e:v_length_kind', 'missing_number':'c:hasReferenceDuration e:v_missing_number', 'wrong_datatype':'c:hasReferenceDuration e:v_wrong_datatype', 'blank_unit':'c:hasReferenceDuration e:v_blank_unit', 'missing_unit':'c:hasReferenceDuration e:v_missing_unit',
      'single_start':'c:periodStart "2025-01-01T00:00:00Z"^^xsd:dateTime',
      'reversed':'c:periodStart "2025-01-03T00:00:00Z"^^xsd:dateTime; c:periodEnd "2025-01-01T00:00:00Z"^^xsd:dateTime',
      'equal':'c:periodStart "2025-01-01T00:00:00Z"^^xsd:dateTime; c:periodEnd "2025-01-01T00:00:00Z"^^xsd:dateTime',
      'incomparable':'c:periodStart "2025-01-03T00:00:00"^^xsd:dateTime; c:periodEnd "2025-01-01T00:00:00Z"^^xsd:dateTime',
      'offset_order':'c:periodStart "2025-01-01T10:00:00+01:00"^^xsd:dateTime; c:periodEnd "2025-01-01T09:00:00+02:00"^^xsd:dateTime',
      'inconsistent':'c:periodStart "2025-01-01T00:00:00Z"^^xsd:dateTime; c:periodEnd "2025-01-03T00:00:00Z"^^xsd:dateTime; c:hasReferenceDuration e:v_inconsistent',
    }
    for name,body in cases.items():ont.parse(data=prefix+f"e:{name} a c:ReferencePeriod; {body} .",format="turtle")
    values={'start_duration':('2','u:day'),'end_duration':('2','u:day'),'duration_only':('2','u:minute'),'second':('2','u:second'),'hour':('2','u:hour'),'celsius':('2','u:degreeCelsius'),'negative':('-1','u:day'),'zero':('0','u:day'),'unknown':('2','e:unknownUnit'),'inconsistent':('99','u:day')}
    for name,(number,unit) in values.items():ont.parse(data=prefix+f'e:v_{name} a c:QuantitativeValue; c:numericValue "{number}"^^xsd:decimal; c:hasMeasurementUnit {unit} .',format='turtle')
    ont.parse(data=prefix+'e:v_wrong_datatype a c:QuantitativeValue; c:numericValue \"2\"^^xsd:integer; c:hasMeasurementUnit u:day . e:v_blank_unit a c:QuantitativeValue; c:numericValue \"2\"^^xsd:decimal; c:hasMeasurementUnit [] . e:v_missing_unit a c:QuantitativeValue; c:numericValue \"2\"^^xsd:decimal .',format='turtle')
    ont.parse(data=prefix+'e:v_time_kind a c:QuantitativeValue; c:numericValue "2"^^xsd:decimal; c:hasMeasurementUnit u:day; c:hasQuantityKind <https://si-digital-framework.org/quantities/TIME> . e:v_length_kind a c:QuantitativeValue; c:numericValue "2"^^xsd:decimal; c:hasMeasurementUnit u:day; c:hasQuantityKind <https://si-digital-framework.org/quantities/LENG> .',format='turtle')
    ont.parse(data=prefix+'e:v_missing_number a t:MaximumThresholdValue; t:maximumValue "0.5"^^xsd:decimal; c:hasMeasurementUnit d:massFractionUnit .',format='turtle')
    _,report,_=validate(ont,shacl_graph=shapes,inference='rdfs',advanced=True,do_owl_imports=False)
    results=defaultdict(Counter)
    T=Namespace("https://w3id.org/eudpp/textile-shacl#")
    for node in report.subjects(RDF.type,SH.ValidationResult):
        focus=report.value(node,SH.focusNode)
        if not str(focus).startswith(str(EX)):continue
        key=str(focus).removeprefix(str(EX)).removeprefix('v_')
        source=report.value(node,SH.sourceShape)
        owners=set(shapes.subjects(SH.property,source)) or {source}
        assert len(owners)==1
        owner=next(iter(owners))
        path=report.value(node,SH.resultPath)
        component=report.value(node,SH.sourceConstraintComponent)
        assert report.value(node,SH.resultSeverity)==SH.Violation
        if component==SH.SPARQLConstraintComponent:
            assert report.value(node,SH.sourceConstraint) in set(shapes.objects(T.ReferencePeriodShape,SH.sparql))
        results[key][(owner,component,path)]+=1
    def one(owner,component,path):return Counter({(T[owner],SH[component],C[path] if path else None):1})
    expected={
      'celsius':one('ReferenceDurationShape','InConstraintComponent','hasMeasurementUnit'),
      'unknown':one('ReferenceDurationShape','InConstraintComponent','hasMeasurementUnit'),
      'blank_unit':one('ReferenceDurationShape','InConstraintComponent','hasMeasurementUnit'),
      'missing_unit':one('QuantitativeValueShape','MinCountConstraintComponent','hasMeasurementUnit'),
      'missing_number':one('ReferenceDurationShape','MinCountConstraintComponent','numericValue')+one('ReferenceDurationShape','InConstraintComponent','hasMeasurementUnit'),
      'wrong_datatype':one('QuantitativeValueShape','DatatypeConstraintComponent','numericValue')+one('ReferenceDurationShape','DatatypeConstraintComponent','numericValue'),
      'length_kind':one('ReferenceDurationShape','InConstraintComponent','hasQuantityKind'),
      'negative':one('PositiveValueShape','MinExclusiveConstraintComponent','numericValue'),
      'zero':one('PositiveValueShape','MinExclusiveConstraintComponent','numericValue'),
      'single_start':one('ReferencePeriodShape','OrConstraintComponent',None),
      'reversed':one('ReferencePeriodShape','LessThanConstraintComponent','periodStart'),
      'equal':one('ReferencePeriodShape','LessThanConstraintComponent','periodStart'),
      'offset_order':one('ReferencePeriodShape','LessThanConstraintComponent','periodStart'),
      'incomparable':one('ReferencePeriodShape','SPARQLConstraintComponent',None),
    }
    assert dict(results)==expected


def test_generated_legacy_candidate_has_complete_term_parity():
    from scripts import generate_common_connector as gen
    from rdflib.compare import isomorphic
    source=Graph().parse(ROOT/'ontology/textile-common.ttl')
    actual=Graph().parse(ROOT/'compat/textile-connector.ttl')
    expected,terms=gen.payload(source)
    projected=Graph()
    for triple in actual:
        if triple[0] != OLD: projected.add(triple)
    assert len(terms)==37 and len(expected)==395
    assert isomorphic(expected,projected)
    for term in terms:
        assert set(actual.predicate_objects(term))==set(source.predicate_objects(term)),term
    changed=Graph()+actual
    label=next(changed.triples((C.QuantitativeValue,Namespace('http://www.w3.org/2000/01/rdf-schema#').label,None)))
    changed.remove(label)
    assert set(changed.predicate_objects(C.QuantitativeValue))!=set(source.predicate_objects(C.QuantitativeValue))
    assert set(actual.subjects(RDF.type,OWL.Ontology))=={OLD}
    assert set(actual.objects(OLD,OWL.imports))=={gen.SI}
    assert (C.QuantitativeValue,RDF.type,OWL.Class) in actual
    assert (ROOT/'compat/textile-connector.ttl').read_text(encoding='utf8')==gen.render(source)
    catalog={x.attrib['name']:x.attrib['uri'] for x in ET.parse(ROOT/'catalog-v001.xml').getroot()}
    assert catalog[str(OLD)]=='compat/textile-connector.ttl'
    closure=v.catalogue_import_closure(ROOT/'catalog-v001.xml',OLD)
    assert ROOT/'compat/textile-connector.ttl' in closure
    assert ROOT/'mireot/si-textile-mireot.ttl' in closure
    assert ROOT/'ontology/textile-common.ttl' not in closure
