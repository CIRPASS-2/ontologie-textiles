"""Issue #10 reference data and narrowly authorized offline routes."""
import hashlib
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL, URIRef
from migration import phase4_contract as contract

ROOT = Path(__file__).resolve().parents[1]
EX = Namespace("https://example.org/textile/issue10#")
EUDPP = Namespace("https://w3id.org/eudpp#")
ASS = Namespace("https://w3id.org/eudpp/textile-assessment#")

def test_catalogue_has_only_the_two_authorized_additions():
    old = contract.blob(contract.BASE, "catalog-v001.xml").replace(
        ("/dev/" + contract.OLD).encode(), ("/dev/" + contract.VERSION).encode())
    actual = contract.expected_catalogue()
    from xml.etree import ElementTree as ET
    def routes(raw):
        elements = list(ET.fromstring(raw))
        result = {e.attrib["name"]: e.attrib["uri"] for e in elements}
        assert len(result) == len(elements)
        return result
    before, after = routes(old), routes(actual)
    assert after == before | {
        "https://w3id.org/eudpp/LCA": "dependencies/current-core/lca.owl",
        "https://w3id.org/eudpp/LCA/3.1": "dependencies/current-core/lca.owl",
    }
    assert (ROOT / "catalog-v001.xml").read_bytes() == actual

def test_reference_data_and_pinned_lca():
    raw = (ROOT / "dependencies/current-core/lca.owl").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == "39a523d6ef6202a1247359a4cf4c151e4b0aee42046c1b5c3b6bcef7a2b3c71b"
    lca = Graph().parse(data=raw, format="xml")
    assert (URIRef("https://w3id.org/eudpp/LCA"), OWL.versionIRI, URIRef("https://w3id.org/eudpp/LCA/3.1")) in lca
    assert not list(lca.triples((None, OWL.imports, None)))
    g = Graph().parse(ROOT / "examples/issue10-textile-reference-individuals.ttl")
    assert set(g.subjects()) == {EX.PEFCRApparelFootwearV31, EX.ISO4484Part1_2023, EX.ISO4484Part3_2023}
    assert (EX.PEFCRApparelFootwearV31, RDF.type, EUDPP.PEFCR) in g
    for subject in (EX.ISO4484Part1_2023, EX.ISO4484Part3_2023):
        assert (subject, RDF.type, ASS.TestingStandard) in g
    assert not list(g.triples((None, OWL.imports, None)))
