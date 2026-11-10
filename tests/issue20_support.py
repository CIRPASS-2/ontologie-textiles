"""Test-only exact approved issue-20 deltas against the published Git baseline.

Historical creator, version and MAT proofs still run against their original
graphs, but only after checking every current triple against this exact delta.
No published package copy or runtime migration mechanism is required.
"""
from functools import lru_cache
import subprocess
from pathlib import Path

from rdflib import Graph, URIRef, Literal, RDF, RDFS, OWL
from rdflib.namespace import DCTERMS, XSD
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b'
CHANGED_MODULES = {'textile-assessment.ttl', 'textile-ontology.ttl'}
PROPERTY_TURTLE = '''
@prefix dpp: <https://w3id.org/eudpp#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .
@prefix txtdur: <https://w3id.org/eudpp/textile-durability#> .
txtass:resultForAssessedAspect a owl:ObjectProperty ;
    rdfs:label "result for assessed aspect"@en ;
    rdfs:comment "Relates an individual measurement or test result to the individual product property, observed degradation phenomenon, failure mode, or external damage that the result directly concerns. This relation identifies the subject of the result, not necessarily the specific quantity, degree, or grading dimension measured. Its intended object is not a test-protocol parameter, result value, assessment criterion, derived indicator, or OWL class used as an individual. A result's method and interpretation scale, when relevant, determine how the reported value is to be interpreted."@en ;
    rdfs:domain txtass:MeasurementResult ;
    rdfs:range [ a owl:Class ; owl:unionOf (
        dpp:Property txtdur:ObservedDegradationPhenomenon
        txtdur:FailureMode txtdur:ExternalDamage ) ] ;
    rdfs:isDefinedBy <https://w3id.org/eudpp/textile-assessment> ;
    txtcon:sourceLocator "docs/decisions/TXT-DEC-011.md"@en ;
    txtcon:sourceType txtcon:modellingAbstraction .
'''


POINT2_TURTLE = '''
@prefix dpp: <https://w3id.org/eudpp#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .
txtass:isRepresentedByProductEvent a owl:ObjectProperty ;
    rdfs:label "is represented by product event"@en ;
    rdfs:comment "Links a concrete assessment execution to the conceptual, product-facing ProductEvent that represents it, distinct from any technical EPCIS carrier. The relation does not identify the execution with the event or its carrier and does not imply that every assessment execution or EPCIS observation qualifies as a ProductEvent."@en ;
    rdfs:domain txtass:AssessmentExecution ;
    rdfs:range dpp:ProductEvent ;
    rdfs:isDefinedBy <https://w3id.org/eudpp/textile-assessment> ;
    txtcon:sourceLocator "docs/decisions/TXT-DEC-012.md"@en ;
    txtcon:sourceType txtcon:modellingAbstraction .

<https://w3id.org/eudpp/textile-assessment>
    owl:imports <https://w3id.org/eudpp/textile-event-mireot> .
'''


POINT3_SHACL_README_SHA256 = '618a5cb716d4ce909ca176fddd9e47d2d980940cf39a455feac595d1305b5d7d'


POINT3_TURTLE = '''
@prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
txtass:hasParameterConcept a owl:ObjectProperty ;
    rdfs:label "has parameter concept"@en ;
    rdfs:comment "Links a measurement parameter setting to its categorical or coded protocol value, represented by a SKOS concept. The concept qualifies the protocol setting, not the assessed product characteristic or a rule for selecting an applicable threshold."@en ;
    rdfs:domain txtass:MeasurementParameterSetting ;
    rdfs:range skos:Concept ;
    rdfs:isDefinedBy <https://w3id.org/eudpp/textile-assessment> ;
    txtcon:sourceLocator "docs/decisions/TXT-DEC-013.md"@en ;
    txtcon:sourceType txtcon:modellingAbstraction .

'''


def apply_point3(graph):
    """Apply only the approved property and its directly affected header comment."""
    ontology = URIRef('https://w3id.org/eudpp/textile-assessment')
    old = Literal('Quantitative results, parameter settings and thresholds use txtcon:QuantitativeValue and SI Digital Framework units through the Textile Connector pattern.', lang='en')
    new = Literal('Quantitative results, quantitative parameter settings and thresholds use txtcon:QuantitativeValue and SI Digital Framework units through the Textile Connector pattern; categorical parameter settings use SKOS concepts.', lang='en')
    assert (ontology, RDFS.comment, old) in graph
    graph.remove((ontology, RDFS.comment, old))
    graph.add((ontology, RDFS.comment, new))
    graph.parse(data=POINT3_TURTLE, format='turtle')
    return graph


POINT3_SETTING_SHAPE = '''
@prefix tsh: <https://w3id.org/eudpp/textile-shacl#> .
@prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
tsh:MeasurementParameterSettingShape a sh:NodeShape ;
    sh:property [ sh:class txtcon:QuantitativeValue ;
            sh:maxCount 1 ;
            sh:message "A supplied quantitative parameter value must be a QuantitativeValue, with at most one per setting."@en ;
            sh:path txtass:hasParameterValue ],
        [ sh:class skos:Concept ;
            sh:path txtass:hasParameterConcept ] ;
    sh:or ( [ sh:property [ sh:minCount 1 ;
                        sh:path txtass:hasParameterValue ] ]
            [ sh:property [ sh:minCount 1 ;
                        sh:path txtass:hasParameterConcept ] ] ) ;
    sh:targetClass txtass:MeasurementParameterSetting .
'''


def expected_quantitative_shapes():
    """Preserve every other shape and all metadata except the approved version IRI."""
    from rdflib.namespace import SH
    graph = Graph().parse(data=published_bytes('shacl/textile-quantitative-shapes.ttl'), format='turtle')
    setting = URIRef('https://w3id.org/eudpp/textile-shacl#MeasurementParameterSettingShape')
    for node in list(graph.objects(setting, SH.property)):
        graph.remove((node, None, None))
    graph.remove((setting, None, None))
    graph.parse(data=POINT3_SETTING_SHAPE, format='turtle')
    profile = URIRef('https://w3id.org/eudpp/textile-shacl/quantitative')
    graph.set((profile, OWL.versionIRI, URIRef(str(profile) + '/2.1.0-dev')))
    graph.parse(data=POINT4_SHAPE, format='turtle')
    return graph


POINT4_SHACL_README_SHA256 = '7c34c78630e05689c7cdc7bdcf83ff6a916e8a870812ad68ffed2b5b2a0fb06c'


POINT4_TURTLE = '''
@prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
txtass:awardedScoreValue a owl:ObjectProperty ;
    rdfs:label "awarded score value"@en ;
    rdfs:comment "Links an assessment result to the number of points actually awarded to that individual result under the applicable scoring method. The awarded points are distinct from an underlying measured value, points prescribed by a scoring rule, and an aggregated indicator value. This relation does not calculate, aggregate or verify the award."@en ;
    rdfs:domain txtass:AssessmentResult ;
    rdfs:range txtcon:QuantitativeValue ;
    rdfs:isDefinedBy <https://w3id.org/eudpp/textile-assessment> ;
    txtcon:sourceLocator "docs/decisions/TXT-DEC-014.md"@en ;
    txtcon:sourceType txtcon:modellingAbstraction .
'''


POINT4_SHAPE = '''
@prefix tsh: <https://w3id.org/eudpp/textile-shacl#> .
@prefix txtass: <https://w3id.org/eudpp/textile-assessment#> .
@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix units: <https://si-digital-framework.org/SI/units/> .
tsh:AwardedScoreValueShape a sh:NodeShape ;
    sh:targetObjectsOf txtass:awardedScoreValue ;
    sh:class txtcon:QuantitativeValue ;
    sh:node tsh:QuantitativeValueShape ;
    sh:property [ sh:path txtcon:numericValue ;
            sh:minCount 1 ],
        [ sh:path txtcon:hasMeasurementUnit ;
            sh:hasValue units:one ] .
'''


def current_version(filename):
    return '2.1.0-dev' if filename in CHANGED_MODULES else '2.0.0'


@lru_cache(maxsize=None)
def published_bytes(relative):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + relative], cwd=ROOT)


def expected_graph(relative):
    graph = Graph().parse(data=published_bytes(relative), format='turtle')
    if Path(relative).name not in CHANGED_MODULES:
        return graph
    ontology = next(graph.subjects(RDF.type, OWL.Ontology))
    graph.set((ontology, OWL.versionIRI, URIRef(str(ontology) + '/2.1.0-dev')))
    graph.set((ontology, OWL.priorVersion, URIRef(str(ontology) + '/2.0.0')))
    graph.set((ontology, OWL.versionInfo, Literal('Version 2.1.0-dev')))
    graph.set((ontology, DCTERMS.modified, Literal('2026-11-09', datatype=XSD.date)))
    if Path(relative).name == 'textile-assessment.ttl':
        graph.set((ontology, DCTERMS.bibliographicCitation,
                   Literal('EU DPP Textile Assessment Ontology. Version 2.1.0-dev.', lang='en')))
        graph.parse(data=PROPERTY_TURTLE, format='turtle')
        graph.parse(data=POINT2_TURTLE, format='turtle')
        apply_point3(graph)
        graph.parse(data=POINT4_TURTLE, format='turtle')
    return graph


def published_contract_graph(graph, relative):
    assert isomorphic(graph, expected_graph(relative)), 'Unauthorized canonical RDF difference: ' + relative
    return Graph().parse(data=published_bytes(relative), format='turtle')
