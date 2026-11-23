"""Focused checks for the optional issue #11 legal-name reference dataset."""
import csv
import subprocess
from pathlib import Path
from xml.etree import ElementTree

from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, OWL, URIRef

ROOT = Path(__file__).resolve().parents[1]
BASE = "f161127a20e661eaf7add48754bc0e3174f12b3f"
DIR = ROOT / "docs/vocabularies"
A = Namespace("https://w3id.org/eudpp/textile-fibre-annex-i#")
TXT = Namespace("https://w3id.org/eudpp/textile-core#")
DPP = Namespace("https://w3id.org/eudpp#")
DCT = Namespace("http://purl.org/dc/terms/")
SOURCE = URIRef("https://eur-lex.europa.eu/eli/reg/2011/1007/2018-02-15/eng")

def graph():
    return Graph().parse(DIR / "eu-annex-i-fibre-names.ttl")

def test_annex_source_coverage_and_critical_entries():
    g = graph()
    concepts = set(g.subjects(SKOS.inScheme, A.FibreNamesScheme))
    assert len(concepts) == 61
    entries = {}
    for s in concepts:
        assert (s, RDF.type, SKOS.Concept) in g and (s, DCT.source, SOURCE) in g
        ids = list(g.objects(s, DCT.identifier))
        assert len(ids) == 1 and str(ids[0]).startswith("Annex I entry ")
        entries.setdefault(int(str(ids[0]).rsplit(" ", 1)[1]), set()).add(s)
        labels = list(g.objects(s, SKOS.prefLabel))
        assert len(labels) == 1 and labels[0].language == "en"
        assert not set(g.objects(s, SKOS.prefLabel)) & set(g.objects(s, SKOS.altLabel))
    assert set(entries) == set(range(1, 51))
    assert entries[2] == {A[x] for x in ("alpaca llama camel cashmere mohair angora vicuna yak guanaco cashgora beaver otter").split()}
    assert entries[3] == {A["animal-or-horsehair"]}
    assert entries[48] == {A["other-material-rule"]}
    assert (A["other-material-rule"], RDF.type, TXT.FibreTypeConcept) not in g
    assert all((s, RDF.type, TXT.FibreTypeConcept) in g for s in concepts - entries[48])
    assert entries[50] == {A.polyacrylate}
    for s, alt in ((A.flax, "linen"), (A.abaca, "Manila hemp"), (A.polyamide, "nylon")):
        assert (s, SKOS.altLabel, Literal(alt, lang="en")) in g
    assert not list(g.triples((None, OWL.imports, None)))
    assert not list(g.triples((None, OWL.equivalentClass, None)))
    for predicate in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch, SKOS.narrowMatch, SKOS.relatedMatch):
        assert not list(g.triples((None, predicate, None)))

# Independent transcription of the Annex I Name column, consolidated 2018-02-15.
# Entries 3 and 48 use the dataset's explicit general wording, not an exhaustive list.
ANNEX_NAMES = {
    1: ("wool",),
    2: ("alpaca", "llama", "camel", "cashmere", "mohair", "angora",
        "vicuna", "yak", "guanaco", "cashgora", "beaver", "otter"),
    3: ("animal or horsehair",), 4: ("silk",), 5: ("cotton",),
    6: ("kapok",), 7: ("flax",), 8: ("true hemp",), 9: ("jute",),
    10: ("abaca",), 11: ("alfa",), 12: ("coir",), 13: ("broom",),
    14: ("ramie",), 15: ("sisal",), 16: ("sunn",), 17: ("henequen",),
    18: ("maguey",), 19: ("acetate",), 20: ("alginate",), 21: ("cupro",),
    22: ("modal",), 23: ("protein",), 24: ("triacetate",), 25: ("viscose",),
    26: ("acrylic",), 27: ("chlorofibre",), 28: ("fluorofibre",),
    29: ("modacrylic",), 30: ("polyamide",), 31: ("aramid",),
    32: ("polyimide",), 33: ("lyocell",), 34: ("polylactide",),
    35: ("polyester",), 36: ("polyethylene",), 37: ("polypropylene",),
    38: ("polycarbamide",), 39: ("polyurethane",), 40: ("vinylal",),
    41: ("trivinyl",), 42: ("elastodiene",), 43: ("elastane",),
    44: ("glass fibre",), 45: ("elastomultiester",), 46: ("elastolefin",),
    47: ("melamine",), 48: ("Other material naming rule",),
    49: ("polypropylene/polyamide bicomponent",), 50: ("polyacrylate",),
}


def test_independent_annex_preferred_names_and_entries():
    g = graph()
    actual = {}
    for subject in g.subjects(SKOS.inScheme, A.FibreNamesScheme):
        entry = int(str(g.value(subject, DCT.identifier)).rsplit(" ", 1)[1])
        actual.setdefault(entry, []).append(str(g.value(subject, SKOS.prefLabel)))
    assert {entry: sorted(names) for entry, names in actual.items()} == {
        entry: sorted(names) for entry, names in ANNEX_NAMES.items()
    }
    assert (A.vinylal, SKOS.prefLabel, Literal("vinylal", lang="en")) in g


def test_coverage_and_t19_inventory_trace_to_sources():
    g = graph()
    with (DIR / "eu-annex-i-coverage.csv").open(encoding="utf8", newline="") as f: coverage = list(csv.DictReader(f))
    assert len(coverage) == 61
    assert {URIRef(row["concept_iri"]) for row in coverage} == set(g.subjects(SKOS.inScheme, A.FibreNamesScheme))
    for row in coverage:
        s = URIRef(row["concept_iri"])
        assert (s, DCT.identifier, Literal("Annex I entry " + row["annex_entry"])) in g
        assert (s, SKOS.prefLabel, Literal(row["preferred_name_en"], lang="en")) in g
    source = ElementTree.parse(ROOT / "ref-data/eBiz/eBiz_T19.xml").getroot()
    codes = {}
    for row in source.findall(".//Row"):
        values = {v.attrib["ColumnRef"]: "".join(v.itertext()).strip() for v in row.findall("Value")}
        codes[values["code"]] = values
    with (DIR / "ebiz-t19-mapping-evidence.csv").open(encoding="utf8", newline="") as f: inventory = list(csv.DictReader(f))
    assert len(inventory) == len(codes) == 61
    assert {x["t19_code"] for x in inventory} == set(codes)
    for row in inventory:
        assert row["source_label_en"] == codes[row["t19_code"]]["EN"]
        assert row["source_description_en"] == codes[row["t19_code"]]["Description"]
        assert row["candidate_predicate"] == "undetermined"
        assert row["status"] in {"candidate", "unresolved"}
        if row["annex_candidate_iri"]:
            assert (URIRef(row["annex_candidate_iri"]), SKOS.inScheme, A.FibreNamesScheme) in g
    by_code = {r["t19_code"]: r for r in inventory}
    assert not by_code["HA"]["annex_candidate_iri"]
    assert by_code["CU"]["status"] == "candidate"
    assert not by_code["WT"]["annex_candidate_iri"]

def test_existing_ontology_and_shapes_are_byte_preserved():
    for area in ("ontology", "compat", "mireot", "shacl"):
        names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE, "--", area], cwd=ROOT, text=True).splitlines()
        for name in names:
            if name.startswith("ontology/graphwise-ontology/"):
                continue
            assert (ROOT / name).read_bytes() == subprocess.check_output(["git", "show", BASE + ":" + name], cwd=ROOT), name
    core = Graph().parse(ROOT / "ontology/textile-core.ttl")
    assert (TXT.FibreTypeConcept, RDFS.subClassOf, DPP.MaterialType) in core
    assert (TXT.hasFibreType, RDFS.subPropertyOf, DPP.hasMaterialType) in core
    scheme = URIRef("https://w3id.org/eudpp/textile-codelists#FibreTypeScheme")
    members = set(core.subjects(SKOS.inScheme, scheme))
    assert len(members) == 22 and all(list(core.objects(s, SKOS.notation)) for s in members)
