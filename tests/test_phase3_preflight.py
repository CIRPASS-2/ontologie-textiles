"""Source-pinned Phase 3 preflight, without altering canonical graphs."""
from rdflib import OWL
from migration import phase3_preflight as phase3
from scripts import generate_common_connector as compat


def test_issue16_source_payload_matches_approved_phase2b():
    assert phase3.check_source_payload() == (37, 395)


def test_expected_phase3_graphs_preserve_common_and_explicit_imports():
    graphs = phase3.expected_graphs()
    assert len(graphs) == 13
    assert phase3.OLD_PATH not in graphs
    assert phase3.COMMON_PATH in graphs
    for path, graph in graphs.items():
        if path != phase3.COMMON_PATH:
            assert compat.COMMON in set(graph.objects(None, OWL.imports))
            assert compat.CONNECTOR not in set(graph.objects(None, OWL.imports))
    assert b'/dev/integration-2026-11.2' in phase3.expected_shapes_bytes()


def test_source_domain_transitions_and_phase2b_commit_are_pinned():
    assert phase3.verify_issue16_source() == 12
    assert phase3.verify_phase2b_commit() == 13


def test_phase3_prior_decisions_have_explicit_overlap_check():
    assert phase3.verify_reconciliation() == 47


def test_proposed_catalogue_keeps_historical_version_routes_separate():
    from xml.etree import ElementTree as ET
    root = ET.fromstring(phase3.expected_catalogue())
    routes = {item.attrib['name']: item.attrib['uri'] for item in root}
    for name in ('textile-common', 'textile-connector'):
        iri = 'https://w3id.org/eudpp/' + name
        assert iri + '/dev/integration-2026-11.2' in routes
        assert iri + '/2.0.0' not in routes
        assert iri + '/dev/integration-2026-11.1' not in routes
    assert routes[str(compat.COMMON)] == 'ontology/textile-common.ttl'
    assert routes[str(compat.CONNECTOR)] == 'compat/textile-connector.ttl'
    assert 'https://w3id.org/eudpp/textile-shacl/quantitative/2.0.0' not in routes
    assert 'https://w3id.org/eudpp/textile-shacl/quantitative/dev/integration-2026-11.2' in routes


def test_version_history_does_not_invent_common_2_0():
    from rdflib import Graph, URIRef
    from rdflib.namespace import DCTERMS
    graphs = phase3.expected_graphs()
    common = graphs[phase3.COMMON_PATH]
    assert not list(common.objects(compat.COMMON, OWL.priorVersion))
    assert (compat.COMMON, DCTERMS.replaces, URIRef(str(compat.CONNECTOR) + '/2.0.0')) in common
    for path, graph in graphs.items():
        if path == phase3.COMMON_PATH: continue
        iri = URIRef('https://w3id.org/eudpp/' + __import__('pathlib').Path(path).stem)
        assert set(graph.objects(iri, OWL.priorVersion)) == {URIRef(str(iri) + '/dev/integration-2026-11.1')}
    connector, _ = compat.compatibility(common)
    assert set(connector.objects(compat.CONNECTOR, OWL.priorVersion)) == {URIRef(str(compat.CONNECTOR) + '/dev/integration-2026-11.1')}
    shape = Graph().parse(data=phase3.expected_shapes_bytes().decode('utf8'), format='turtle')
    shape_iri = URIRef('https://w3id.org/eudpp/textile-shacl/quantitative')
    assert set(shape.objects(shape_iri, OWL.priorVersion)) == {URIRef(str(shape_iri) + '/2.0.0')}


def test_actual_delta_categories_reject_unapproved_logical_and_blank_nodes():
    import pytest
    from rdflib import BNode, Graph, RDFS, URIRef
    from migration import phase2b_contract as phase2
    from migration.integration_contract import ContractError
    _, previous = phase2.expected_graphs()
    expected = phase3.expected_graphs()
    report = phase3.classify_actual(previous, expected)
    assert len(report) == 13
    path = 'ontology/textile-core.ttl'
    mutated = dict(expected)
    mutated[path] = expected[path] + Graph()
    mutated[path].add((URIRef('urn:unexpected'), RDFS.subClassOf, BNode()))
    with pytest.raises(ContractError, match='Unexpected logical or anonymous'):
        phase3.classify_actual(previous, mutated)


def test_phase3_restoration_rejects_unapproved_anonymous_changes():
    import pytest
    from rdflib import BNode, Graph, OWL
    from migration.integration_contract import ContractError
    expected = phase3.expected_graphs()
    path = 'ontology/textile-core.ttl'
    mutated = expected[path] + Graph()
    node = next(mutated.subjects(None, OWL.Restriction))
    mutated.add((node, OWL.hasValue, BNode()))
    with pytest.raises(ContractError, match='Unauthorized canonical RDF difference'):
        phase3.restore_phase2(mutated, path)


def test_production_contract_checks_complete_actual_candidate(tmp_path, monkeypatch):
    import shutil
    import pytest
    from rdflib import Graph, RDFS, URIRef
    from migration import phase2b_contract as phase2
    from migration.integration_contract import ContractError
    graphs = phase3.expected_graphs()
    for path, graph in graphs.items():
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(graph.serialize(format='turtle'), encoding='utf8')
    common = graphs[phase3.COMMON_PATH]
    connector = tmp_path / 'compat/textile-connector.ttl'
    connector.parent.mkdir()
    connector.write_text(compat.render(common), encoding='utf8', newline='\n')
    (tmp_path/'VERSION').write_text(phase3.VERSION + '\n', encoding='utf8', newline='\n')
    (tmp_path/'catalog-v001.xml').write_bytes(phase3.expected_catalogue())
    shapes = tmp_path/phase3.SHAPES
    shapes.parent.mkdir(parents=True, exist_ok=True)
    shapes.write_bytes(phase3.expected_shapes_bytes())
    shutil.copytree(phase3.ROOT/'mireot', tmp_path/'mireot')
    source_blobs = {phase3.COMMON_PATH: phase3.source_blob(phase3.COMMON_PATH, phase3.COMMON_SHA256),
                    phase3.SHAPES: phase3.source_blob(phase3.SHAPES, phase3.SHAPES_SHA256)}
    monkeypatch.setattr(phase3, 'source_blob', lambda path, digest: source_blobs[path])
    monkeypatch.setattr(phase3, 'ROOT', tmp_path)
    monkeypatch.setattr(phase3, 'verify_issue16_source', lambda: 12)
    monkeypatch.setattr(phase3, 'verify_phase2b_commit', lambda: 13)
    monkeypatch.setattr(phase3, 'verify_protected', lambda: 1)
    monkeypatch.setattr(phase2, 'verify_source', lambda: None)
    monkeypatch.setattr(phase2, 'check_frozen', lambda: (799, 20))
    report = phase3.validate()
    assert (report['canonical_closure'], report['common_closure'], report['compatibility_closure']) == (20, 2, 2)
    assert (report['compatibility_terms'], report['compatibility_payload_triples']) == (37, 395)
    # Mutate the generator as well as its output: production authorization must
    # remain independent when an unapproved header is deterministically regenerated.
    original = compat.compatibility
    mutations = (
        (OWL.priorVersion, URIRef('urn:unapproved:prior'), True),
        (OWL.deprecated, __import__('rdflib').Literal(True), False),
        (RDFS.seeAlso, URIRef('urn:unapproved:reference'), False),
    )
    for predicate, value, replace_existing in mutations:
        def altered(source):
            graph, terms = original(source)
            if replace_existing:
                graph.remove((compat.CONNECTOR, predicate, None))
            graph.add((compat.CONNECTOR, predicate, value))
            return graph, terms
        with monkeypatch.context() as patch:
            patch.setattr(compat, 'compatibility', altered)
            connector.write_text(compat.render(common), encoding='utf8', newline='\n')
            with pytest.raises(ContractError, match='Unauthorized Connector ontology header'):
                phase3.validate()
    connector.write_text(compat.render(common), encoding='utf8', newline='\n')
    target = tmp_path/'ontology/textile-core.ttl'
    target.write_text(target.read_text(encoding='utf8') + '\n<urn:bad> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <urn:bad2> .\n', encoding='utf8')
    with pytest.raises(ContractError, match='Unauthorized canonical RDF difference'):
        phase3.validate()
