"""Regression checks for Common documentation migration and Git attributes."""
from pathlib import Path
import subprocess
from rdflib import Graph, Namespace, URIRef
from scripts import fix_widoco_common_provenance as fix

ROOT = Path(__file__).resolve().parents[1]


def test_common_replacement_provenance_is_not_a_prior_version():
    text = (ROOT/'docs/widoco/common/index-en.html').read_text(encoding='utf8')
    assert '<dt>Replaces ontology:</dt>' in text
    assert '<dt>Previous version:</dt>' not in text
    provenance = Graph().parse(ROOT/'docs/widoco/common/provenance/provenance-en.ttl')
    prov = Namespace('http://www.w3.org/ns/prov#')
    assert not list(provenance.objects(URIRef(fix.CURRENT), prov.wasRevisionOf))
    assert 'replaces the former Connector ontology' in (ROOT/'docs/widoco/common/provenance/provenance-en.html').read_text(encoding='utf8')
    assert '<dt>Previous version:</dt>' in (ROOT/'docs/widoco/connector/index-en.html').read_text(encoding='utf8')


def test_git_attributes_preserve_new_rdf_bytes():
    result = subprocess.check_output(['git', 'check-attr', 'text', '--',
        'ontology/textile-common.ttl', 'compat/textile-connector.ttl'], cwd=ROOT, text=True)
    assert result.count('text: unset') == 2
