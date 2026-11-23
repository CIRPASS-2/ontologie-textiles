"""Option B compatibility generator checks against the approved source graph."""
import subprocess
from rdflib import Graph, OWL, URIRef
from rdflib.compare import isomorphic
from scripts import generate_common_connector as gen

SOURCE = 'b05927c3e32ff0d0b82ce6d5a55dc60665f9168f'


def source_common():
    raw = subprocess.check_output(['git', 'show', SOURCE + ':ontology/textile-common.ttl'], cwd=gen.ROOT)
    return Graph().parse(data=raw.decode('utf8'), format='turtle')


def test_complete_option_b_source_projection():
    common = source_common()
    payload, terms = gen.payload(common)
    assert len(terms) == 37
    assert len(payload) == 395
    assert sum(subject not in terms for subject, _, _ in payload) == 33
    connector, _ = gen.compatibility(common)
    assert gen.verify(common, connector) == (37, 395)
    assert (gen.CONNECTOR, OWL.imports, gen.COMMON) not in connector
    assert set(connector.objects(gen.CONNECTOR, OWL.imports)) == {gen.SI}
    assert isomorphic(connector, Graph().parse(data=gen.render(common), format='turtle'))
    assert gen.render(common) == gen.render(common)


def test_supporting_triple_omission_is_rejected():
    import pytest
    common = source_common()
    connector, terms = gen.compatibility(common)
    supporting = next(t for t in connector if t[0] not in terms and t[0] != gen.CONNECTOR)
    connector.remove(supporting)
    with pytest.raises(ValueError, match='complete Common projection'):
        gen.verify(common, connector)


def test_lexical_literal_mutation_is_rejected_without_global_normalization():
    import pytest
    from migration.integration_contract import parse_turtle
    common = source_common()
    extra = parse_turtle('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> . <urn:test:lexical> <urn:test:value> "01"^^xsd:integer .', 'ontology/textile-common.ttl')
    common += extra
    connector, _ = gen.compatibility(common)
    rendered = gen.render(common)
    roundtrip = parse_turtle(rendered, 'compat/textile-connector.ttl')
    assert gen.verify(common, roundtrip) == (37, 396)
    mutated = parse_turtle(rendered.replace('"01"^^<http://www.w3.org/2001/XMLSchema#integer>', '"1"^^<http://www.w3.org/2001/XMLSchema#integer>'), 'compat/textile-connector.ttl')
    with pytest.raises(ValueError, match='complete Common projection'):
        gen.verify(common, mutated)
