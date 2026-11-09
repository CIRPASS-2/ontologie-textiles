"""Test-only exact point-1 and point-2 deltas against the published Git baseline.

Historical creator, version and MAT proofs still run against their original
graphs, but only after checking every current triple against this exact delta.
No published package copy or runtime migration mechanism is required.
"""
from functools import lru_cache
import subprocess
from pathlib import Path

from rdflib import Graph, URIRef, Literal, RDF, OWL
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
    return graph


def published_contract_graph(graph, relative):
    assert isomorphic(graph, expected_graph(relative)), 'Unauthorized canonical RDF difference: ' + relative
    return Graph().parse(data=published_bytes(relative), format='turtle')
