"""Generate the complete Option B Connector representation from Textile Common."""
from __future__ import annotations
import argparse
from pathlib import Path
from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.compare import isomorphic, to_canonical_graph
from rdflib.namespace import DCTERMS
import sys
if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from migration.integration_contract import parse_turtle

ROOT = Path(__file__).resolve().parents[1]
COMMON = URIRef('https://w3id.org/eudpp/textile-common')
CONNECTOR = URIRef('https://w3id.org/eudpp/textile-connector')
SI = URIRef('https://w3id.org/eudpp/textile-si-mireot')
NS = Namespace('https://w3id.org/eudpp/textile-connector#')
VERSION = 'integration-2026-11.2'
OUTPUT = ROOT / 'compat/textile-connector.ttl'


def payload(graph):
    """Return every triple except the canonical ontology subject header."""
    if set(graph.subjects(RDF.type, OWL.Ontology)) != {COMMON}:
        raise ValueError('Expected exactly the canonical Common ontology header')
    terms = {s for s in graph.subjects(RDFS.isDefinedBy, COMMON)
             if isinstance(s, URIRef) and str(s).startswith(str(NS))}
    if len(terms) != 37:
        raise ValueError(f'Expected 37 defined terms, found {len(terms)}')
    result = Graph()
    for triple in graph:
        if triple[0] != COMMON:
            result.add(triple)
    return result, terms


def compatibility(common):
    body, terms = payload(common)
    result = body + Graph()
    header = (
        (CONNECTOR, RDF.type, OWL.Ontology),
        (CONNECTOR, RDFS.label, Literal('Textile Connector compatibility ontology', lang='en')),
        (CONNECTOR, RDFS.comment, Literal('Complete compatibility representation of Textile Common using the retained Connector term IRIs.', lang='en')),
        (CONNECTOR, OWL.versionIRI, URIRef(str(CONNECTOR) + '/dev/' + VERSION)),
        (CONNECTOR, OWL.versionInfo, Literal('Version ' + VERSION)),
        (CONNECTOR, OWL.priorVersion, URIRef(str(CONNECTOR) + '/dev/integration-2026-11.1')),
        (CONNECTOR, OWL.imports, SI),
        (CONNECTOR, DCTERMS.source, COMMON),
    )
    for triple in header:
        result.add(triple)
    # The compatibility document retains the approved authorship metadata;
    # ontology identity and version headers remain separate from Common.
    for creator in common.objects(COMMON, DCTERMS.creator):
        result.add((CONNECTOR, DCTERMS.creator, creator))
    return result, terms


def render(common):
    graph, _ = compatibility(common)
    canonical = to_canonical_graph(graph)
    return ('# Generated complete Option B compatibility representation.\n'
            '@prefix txtcon: <https://w3id.org/eudpp/textile-connector#> .\n') + ''.join(
        ' '.join(term.n3() for term in triple) + ' .\n'
        for triple in sorted(canonical, key=lambda row: tuple(term.n3() for term in row)))


def verify(common, actual):
    expected, terms = compatibility(common)
    if not isomorphic(actual, expected):
        raise ValueError('Connector graph differs from complete Common projection and approved header')
    old_body = Graph()
    for triple in actual:
        if triple[0] != CONNECTOR:
            old_body.add(triple)
    new_body, _ = payload(common)
    if not isomorphic(old_body, new_body):
        raise ValueError('Connector does not reproduce complete Common payload')
    if set(actual.objects(CONNECTOR, OWL.imports)) != {SI}:
        raise ValueError('Connector imports must contain only the approved SI module')
    return len(terms), len(new_body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    common = parse_turtle((ROOT / 'ontology/textile-common.ttl').read_text(encoding='utf8'), 'ontology/textile-common.ttl')
    text = render(common)
    if args.check:
        if OUTPUT.read_text(encoding='utf8') != text:
            raise ValueError('Connector representation differs from deterministic generator')
        terms, triples = verify(common, parse_turtle(OUTPUT.read_text(encoding='utf8'), 'compat/textile-connector.ttl'))
        print(f'Compatibility verified: {terms} terms, {triples} non-header triples')
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding='utf8', newline='\n')
        verify(common, parse_turtle(OUTPUT.read_text(encoding='utf8'), 'compat/textile-connector.ttl'))


if __name__ == '__main__':
    main()
