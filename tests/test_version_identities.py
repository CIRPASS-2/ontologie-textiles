"""Option B keeps current version identity separate from preserved history."""
import hashlib
from pathlib import Path
import json
from xml.etree import ElementTree as ET
import pytest
from rdflib import Graph, RDF, OWL, URIRef, Literal
from rdflib.namespace import DCTERMS, XSD
from migration.correct_version_identities import MODULES, PREDICATES, REVISION_DATE, project
from migration.update_creators import semantic_digest
from scripts import validate_public as v

ROOT=v.ROOT
REPORT=json.loads((ROOT/'migration/version-identity-results.json').read_text('utf8'))


@pytest.mark.parametrize('row',REPORT['modules'],ids=lambda row:row['file'])
def test_exact_header_revision_and_catalogue_identity(row):
    from migration.mat_alignment import restore_frozen_graph
    original_ontology=URIRef(row['ontology_iri'])
    current_file=('ontology/textile-common.ttl' if row['file']=='ontology/textile-connector.ttl' else row['file'])
    graph=Graph().parse(ROOT/current_file)
    ontology=URIRef('https://w3id.org/eudpp/'+Path(current_file).stem)
    assert set(graph.subjects(RDF.type,OWL.Ontology))=={ontology}
    assert set(graph.objects(ontology,OWL.versionIRI))=={URIRef(str(ontology)+'/dev/integration-2026-11.2')}
    frozen=restore_frozen_graph(graph,current_file)
    assert semantic_digest(project(frozen,original_ontology))==row['non_metadata_graph_sha256']
    assert set(REPORT['allowed_predicates'])==set(map(str,PREDICATES))
    for field in ('added','removed'):
        for subject,predicate,_ in Graph().parse(data='\n'.join(row[field]),format='turtle'):
            assert subject==original_ontology and predicate in PREDICATES
    changed=row['file'].removeprefix('ontology/textile-').removesuffix('.ttl') in MODULES
    if changed:
        assert set(frozen.objects(original_ontology,DCTERMS.modified))=={Literal(REVISION_DATE,datatype=XSD.date)}
        old_catalog=ROOT/'migration/historical/1.1.2/catalog-v001.xml'
        old={entry.attrib['name']:entry.attrib['uri'] for entry in ET.parse(old_catalog).getroot()}
        rel=old[str(original_ontology)+'/1.1.2']
        expected=json.loads((old_catalog.parent.parent/'inventory.json').read_text('utf8'))['files'][rel]
        assert hashlib.sha256((old_catalog.parent/rel).read_bytes()).hexdigest()==expected
    else:
        assert not row['added'] and not row['removed']
    if current_file.endswith('textile-common.ttl'):
        assert not list(graph.objects(ontology,OWL.priorVersion))
    else:
        assert set(graph.objects(ontology,OWL.priorVersion))=={URIRef(str(ontology)+'/dev/integration-2026-11.1')}
    catalog={entry.attrib['name']:entry.attrib['uri'] for entry in ET.parse(ROOT/'catalog-v001.xml').getroot()}
    assert catalog[str(ontology)+'/dev/integration-2026-11.2']==current_file
    assert str(ontology)+'/2.0.0' not in catalog
    assert str(ontology)+'/dev/integration-2026-11.1' not in catalog
    assert catalog[str(ontology)]==current_file


def test_si_mireot_retains_unchanged_identity_and_bytes():
    path=ROOT/'mireot/si-textile-mireot.ttl';graph=Graph().parse(path)
    ontology=URIRef('https://w3id.org/eudpp/textile-si-mireot')
    assert set(graph.objects(ontology,OWL.versionIRI))=={URIRef(str(ontology)+'/1.1.2')}
    historical=ROOT/'migration/historical/1.1.2/mireot/si-textile-mireot.ttl'
    assert path.read_bytes()==historical.read_bytes()


def test_all_runtime_version_iris_have_unique_catalogue_targets():
    identities={};versions={}
    catalog={entry.attrib['name']:entry.attrib['uri'] for entry in ET.parse(ROOT/'catalog-v001.xml').getroot()}
    for area in ('ontology','mireot'):
        for path in (ROOT/area).glob('*.ttl'):
            graph=Graph().parse(path);ontology=next(graph.subjects(RDF.type,OWL.Ontology))
            version=graph.value(ontology,OWL.versionIRI)
            assert ontology not in identities and version not in versions
            identities[ontology]=path;versions[version]=path
            if path.name!='si-textile-mireot.ttl':
                assert str(version)==str(ontology)+('/dev/integration-2026-11.2' if area=='ontology' else '/2.0.0')
                assert catalog[str(version)]==path.relative_to(ROOT).as_posix()
    assert len(identities)==len(versions)==20
