"""Issue 12: preserve composition and constrain packaging inference."""
import subprocess
import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.namespace import SH
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from pyshacl import validate
from scripts import validate_public as v
from migration import mat_alignment as m

T = Namespace("https://w3id.org/eudpp/textile-core#")
A = Namespace("https://w3id.org/eudpp/textile-associated-materials#")
D = Namespace("https://w3id.org/eudpp#")
E = Namespace("https://example.org/issue12#")
C = Namespace("https://w3id.org/eudpp/textile-connector#")

@pytest.fixture(scope="module", params=[RDFS_Semantics, OWLRL_Semantics], ids=["rdfs", "owlrl"])
def inferred(request):
    graph = m.closure()
    data = [(E.shirt,T.hasFibreCompositionComponent,E.entry),
            (E.entry,T.hasFibreType,E.cotton),
            (E.shirt,T.hasFibreComponent,E.cotton),
            (E.shirt,A.hasNonTextileComponent,E.button),
            (E.shirt,A.hasPackagingMaterial,E.wrapper)]
    for triple in data: graph.add(triple)
    DeductiveClosure(request.param).expand(graph)
    return graph

def test_fibre_alignment_and_deferred_bridge(inferred):
    assert (E.entry,RDF.type,D.MaterialOfComposition) in inferred
    assert (E.cotton,RDF.type,D.MaterialType) in inferred
    assert (E.entry,D.hasMaterialType,E.cotton) in inferred
    assert (E.shirt,D.hasMaterial,E.entry) not in inferred
    assert (T.hasFibreCompositionComponent,RDFS.subPropertyOf,D.hasMaterial) not in inferred
    assert (E.shirt,T.hasFibreComponent,E.cotton) in inferred

def test_non_textile_part_is_not_automatically_product_or_material(inferred):
    assert (E.button,RDF.type,A.TextileProductPart) in inferred
    assert (E.button,RDF.type,D.Product) not in inferred
    assert (E.button,RDF.type,D.MaterialOfComposition) not in inferred
    assert (E.shirt,D.isComponentOf,E.button) not in inferred

def test_packaging_is_not_automatically_material_of_composition(inferred):
    assert (E.wrapper,RDF.type,A.PackagingMaterial) in inferred
    assert (E.wrapper,RDF.type,D.MaterialOfComposition) not in inferred
    assert (A.PackagingMaterial,OWL.disjointWith,D.MaterialOfComposition) not in inferred
    assert (D.MaterialOfComposition,OWL.disjointWith,A.PackagingMaterial) not in inferred

def test_explicit_packaging_product_material_remains_possible():
    # The bounded Textile closure does not define CORE hasMaterial. An
    # explicit CORE edge and type can still be stated without importing CON.
    graph = m.closure()
    graph.add((E.shirt, A.hasPackagingMaterial, E.wrapper))
    graph.add((E.packagingProduct, RDF.type, D.Product))
    graph.add((E.packagingProduct, D.hasMaterial, E.wrapper))
    graph.add((E.wrapper, RDF.type, A.PackagingMaterial))
    initial = graph + Graph()
    DeductiveClosure(OWLRL_Semantics).expand(initial)
    assert (E.wrapper, RDF.type, D.MaterialOfComposition) not in initial
    assert (E.shirt, D.hasMaterial, E.wrapper) not in initial

    graph.add((E.wrapper, RDF.type, D.MaterialOfComposition))
    reasoner = OWLRL_Semantics(graph, False, False)
    reasoner.closure(); reasoner.flush_stored_triples()
    assert not reasoner.error_messages
    assert (E.packagingProduct, D.hasMaterial, E.wrapper) in graph
    assert (E.wrapper, RDF.type, A.PackagingMaterial) in graph
    assert (E.wrapper, RDF.type, D.MaterialOfComposition) in graph
    assert (E.shirt, D.hasMaterial, E.wrapper) not in graph
    assert (E.shirt, RDF.type, D.MaterialOfComposition) not in graph
    assert (A.PackagingMaterial, OWL.disjointWith, D.MaterialOfComposition) not in graph
    assert (D.MaterialOfComposition, OWL.disjointWith, A.PackagingMaterial) not in graph
    # OWL RL on this example is not a complete OWL DL consistency proof.


def test_packaging_product_with_selected_full_core_connector():
    # Supplemental semantic check: CON 2.4.0 is a reference snapshot, not
    # part of the bounded Textile import closure; no dependency is changed.
    graph = m.closure()
    graph.parse(m.ROOT / "dependencies/current-core/connector.owl")
    graph.add((E.shirt, A.hasPackagingMaterial, E.wrapper))
    graph.add((E.packagingProduct, RDF.type, D.Product))
    graph.add((E.packagingProduct, D.hasMaterial, E.wrapper))
    graph.add((E.wrapper, RDF.type, A.PackagingMaterial))
    reasoner = OWLRL_Semantics(graph, False, False)
    reasoner.closure(); reasoner.flush_stored_triples()
    assert not reasoner.error_messages
    assert (E.wrapper, RDF.type, D.MaterialOfComposition) in graph  # CON range
    assert (E.shirt, D.hasMaterial, E.wrapper) not in graph
    assert (E.shirt, RDF.type, D.MaterialOfComposition) not in graph
    assert (A.PackagingMaterial, OWL.disjointWith, D.MaterialOfComposition) not in graph
    assert (D.MaterialOfComposition, OWL.disjointWith, A.PackagingMaterial) not in graph
    # This checks a selected example under OWL RL, not all OWL DL models.


def test_packaging_baseline_and_current_exact_axiom():
    baseline=Graph().parse(data=subprocess.check_output(["git","show",'40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b'+":ontology/textile-associated-materials.ttl"],cwd=m.ROOT),format="turtle")
    triple=(A.PackagingMaterial,RDFS.subClassOf,D.MaterialOfComposition)
    assert triple in baseline and triple not in m.closure()
    assert (A.NonTextileComponent,RDFS.subClassOf,A.TextileProductPart) in m.closure()

def test_existing_fraction_profile_positive_and_negative():
    shapes=Graph().parse(m.ROOT/"shacl/textile-quantitative-shapes.ttl")
    for name,expected in [("valid/V01-core-mass-fraction.ttl",True),("invalid/I01-core-mass-fraction.ttl",False)]:
        data=Graph().parse(m.ROOT/"tests/abox_corpus/fixtures"/name)
        conforms, report, _ = validate(m.closure()+data,shacl_graph=shapes,inference="rdfs",advanced=True)
        assert conforms is expected
        if not expected:
            focus = Namespace("https://example.org/eu-dpp-textile/")["value-cotton-fraction"]
            matching = [result for result in report.subjects(RDF.type, SH.ValidationResult)
                        if (result, SH.focusNode, focus) in report
                        and (result, SH.resultPath, C.numericValue) in report
                        and (result, SH.sourceConstraintComponent, SH.MaxInclusiveConstraintComponent) in report]
            assert matching, "Expected mass-fraction maximum violation was not reported"
    assert (T.hasFibreMassFraction,RDFS.subPropertyOf,D.materialPercentage) not in m.closure()
    assert (T.hasFibreMassFraction,OWL.equivalentProperty,D.materialPercentage) not in m.closure()
