"""Exact issue #9 annotation-only transition and discriminating mutation controls."""
import subprocess
import pytest
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL
from migration import issue9_annotations as m

EX = Namespace('urn:issue9:')


def test_all_canonical_graphs_have_only_the_exact_approved_annotation_delta():
    rows = m.canonical_differences()
    assert len(rows) == 13
    assert sum(len(r['added']) for r in rows) == 14
    assert sum(len(r['removed']) for r in rows) == 14
    for row in rows:
        before = m.baseline_graph(row['file'])
        from migration.phase4_contract import restore_phase3
        from migration.phase3_preflight import restore_phase2
        from migration.phase2b_contract import restore_phase1
        after = restore_phase3(Graph().parse(m.ROOT / row['file']), row['file'])
        after, prior_path = restore_phase2(after, row['file'])
        after = restore_phase1(after, prior_path)
        # Entity declarations are compared, not filtered as annotations.
        declarations = [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty]
        for kind in declarations:
            assert {s for s in before.subjects(RDF.type, kind) if isinstance(s, URIRef)} == {s for s in after.subjects(RDF.type, kind) if isinstance(s, URIRef)}


@pytest.mark.parametrize('fault', ['class', 'property', 'subclass', 'domain', 'note', 'remove-annotation'])
def test_unapproved_logical_and_annotation_changes_are_rejected(fault):
    relative = 'ontology/textile-durability.ttl'
    graph = Graph().parse(m.ROOT / relative)
    if fault == 'class': graph.add((EX['term'], RDF.type, OWL.Class))
    elif fault == 'property': graph.add((EX['term'], RDF.type, OWL.ObjectProperty))
    elif fault == 'subclass': graph.add((EX['term'], RDFS.subClassOf, OWL.Thing))
    elif fault == 'domain': graph.add((EX.relation, RDFS.domain, EX['term']))
    elif fault == 'note': graph.add((EX['term'], RDFS.comment, Literal('Unapproved annotation')))
    else: graph.remove(next(graph.triples((None, RDFS.comment, None))))
    with pytest.raises(AssertionError, match='Unauthorized canonical RDF difference'):
        m.restore_issue9_graph(graph, relative)


def test_all_non_annotation_runtime_inputs_and_traceability_stay_byte_identical():
    areas = ['catalog-v001.xml', 'VERSION', 'mireot', 'dependencies', 'shacl', 'examples',
             'traceability', 'migration/historical', 'migration/legacy-soc-attribution.json']
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', m.BASELINE, '--', *areas],
                                    cwd=m.ROOT, text=True).splitlines()
    for relative in paths:
        raw = subprocess.check_output(['git', 'show', m.BASELINE + ':' + relative], cwd=m.ROOT)
        actual = (m.ROOT / relative).read_bytes()
        if relative == 'catalog-v001.xml':
            from migration.phase4_contract import expected_catalogue
            assert actual == expected_catalogue(), relative
        elif relative == 'VERSION':
            assert actual == b'integration-2026-11.3\n', relative
        elif relative == 'shacl/textile-quantitative-shapes.ttl':
            from migration.phase4_contract import expected_shapes
            from rdflib.compare import isomorphic
            assert isomorphic(Graph().parse(data=actual.decode(),format="turtle"), expected_shapes()), relative
        elif relative == 'shacl/README.md':
            from migration.phase3_preflight import source_blob, SHACL_README_SHA256
            assert actual.startswith(source_blob(relative, SHACL_README_SHA256).rstrip()+b"\n\n## Issue #20 Assessment profiles\n"), relative
        elif relative == 'traceability/textile-resource-traceability.csv':
            from scripts import validate_public as v
            resources,_,_,_=v.derive(v.ontology_graph(m.ROOT),m.ROOT)
            assert actual == v.csv_bytes(v.RESOURCE_FIELDS,resources), relative
        else:
            assert actual == raw, relative


def test_documentation_generation_preserves_content_and_tracks_inputs(monkeypatch):
    import json
    import re
    from pathlib import Path
    from migration import refresh_publication as refresh

    paths = [
        'README.md', 'docs/MODELLING_GUIDE.md', 'docs/ARCHITECTURE.md',
        'docs/DEPENDENCIES.md', 'docs/SOURCE_TRACEABILITY.md',
        'docs/governance/upstream-dependency-governance.md',
    ]
    expected = {p: (m.ROOT / p).read_text(encoding='utf8') for p in paths}
    resources, evidence, sources, other = refresh.v.derive(refresh.v.ontology_graph(m.ROOT))
    scopes = json.loads((m.ROOT / 'migration/extraction-scopes.json').read_text('utf8'))
    original_count = scopes['soc']['copied_triples']
    changed_scopes = json.loads(json.dumps(scopes))
    changed_scopes['soc']['copied_triples'] = original_count + 17
    original_read = Path.read_text
    original_baseline = refresh.baseline_text
    outputs = {}
    state = {'perturbed': False}

    def read(path, *args, **kwargs):
        if state['perturbed'] and path == m.ROOT / 'migration/extraction-scopes.json':
            return json.dumps(changed_scopes)
        text = original_read(path, *args, **kwargs)
        if state['perturbed'] and path == m.ROOT / 'docs/MODELLING_GUIDE.md':
            text += '\nAn independently maintained guide section.\n'
        return text

    def baseline(path):
        text = original_baseline(path)
        if state['perturbed'] and str(path).replace('\\', '/') == 'docs/ARCHITECTURE.md':
            text = text.replace('## Modelling principles',
                                'Independently maintained baseline material.\n\n## Modelling principles')
        return text

    def derive(graph):
        if state['perturbed']:
            return resources + [resources[0]], evidence + [evidence[0]], sources, other
        return resources, evidence, sources, other

    def capture(path, text):
        outputs[str(path).replace('\\', '/')] = text.replace('\r\n', '\n').rstrip('\r\n') + '\n'

    monkeypatch.setattr(Path, 'read_text', read)
    monkeypatch.setattr(Path, 'write_bytes', lambda self, data: len(data))
    monkeypatch.setattr(refresh, 'baseline_text', baseline)
    monkeypatch.setattr(refresh.v, 'derive', derive)
    monkeypatch.setattr(refresh, 'write', capture)

    for _ in range(2):
        outputs.clear()
        refresh.documentation()
        assert {p: outputs[p] for p in paths} == expected

    # Links in all inserted fragments resolve from the generated destination.
    fragments = {
        'README.md': [refresh.README_CREATORS, refresh.README_ISSUE9],
        'docs/MODELLING_GUIDE.md': [refresh.GUIDE_ISSUE9],
        'docs/ARCHITECTURE.md': [refresh.ARCHITECTURE_ISSUE9],
        'docs/DEPENDENCIES.md': [refresh.DEPENDENCIES_ISSUE9],
        'docs/SOURCE_TRACEABILITY.md': [refresh.TRACEABILITY_ISSUE9],
        'docs/governance/upstream-dependency-governance.md': [refresh.GOVERNANCE_19, refresh.GOVERNANCE_21],
    }
    for path, parts in fragments.items():
        for part in parts:
            for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', part):
                if not link.startswith(('http:', 'https:', '#')):
                    assert ((m.ROOT / path).parent / link.split('#')[0]).exists(), (path, link)

    # Check every relative Markdown destination in all six generated documents.
    from urllib.parse import unquote
    for path in paths:
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', outputs[path]):
            if link.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            local = unquote(link.split('#')[0].split('?')[0])
            if local:
                assert ((m.ROOT / path).parent / local).exists(), (path, link)

    state['perturbed'] = True
    outputs.clear()
    refresh.documentation()
    assert f'| {original_count + 17} |' in outputs['docs/DEPENDENCIES.md']
    assert f'The projection contains {len(resources) + 1} resources and {len(evidence) + 1} evidence rows:' in outputs['docs/SOURCE_TRACEABILITY.md']
    assert 'Independently maintained baseline material.' in outputs['docs/ARCHITECTURE.md']
    assert 'An independently maintained guide section.' in outputs['docs/MODELLING_GUIDE.md']
    for path, parts in fragments.items():
        for part in parts:
            assert part.strip() in outputs[path]


def test_documentation_generation_rejects_changed_or_duplicate_anchors():
    from migration import refresh_publication as refresh
    for text in ('missing', 'anchor anchor'):
        with pytest.raises(ValueError, match='expected exactly one anchor'):
            refresh.insert_before(text, 'anchor', 'fragment', 'test document')
    with pytest.raises(ValueError, match='already present'):
        refresh.insert_before('fragment anchor', 'anchor', 'fragment', 'test document')


def test_core_con_property_boundary_and_local_relationships():
    from scripts import validate_public as v

    dpp = Namespace('https://w3id.org/eudpp#')
    ind = Namespace('https://w3id.org/eudpp/textile-indicator#')
    proc = Namespace('https://w3id.org/eudpp/textile-process#')
    textile = Namespace('https://w3id.org/eudpp/textile-core#')
    source = Graph().parse(m.ROOT / 'dependencies/current-core/connector.owl')
    runtime = v.ontology_graph(m.ROOT)
    assert (dpp.concernsProduct, RDFS.domain, dpp.ProductEvent) in source
    assert (dpp.concernsProduct, RDFS.range, dpp.Product) in source
    assert not list(runtime.triples((dpp.concernsProduct, None, None)))
    assert (ind.concernsProduct, RDFS.domain, ind.Indicator) in runtime
    assert (ind.concernsProduct, RDFS.range, dpp.Product) in runtime
    assert (proc.concernsProduct, RDFS.domain, proc.TextileProcessExecution) in runtime
    assert (proc.concernsProduct, RDFS.range, textile.TextileProduct) in runtime
    assert (ind.isIndicatorOf, RDFS.subPropertyOf, ind.concernsProduct) in runtime
    assert (ind.hasIndicator, OWL.inverseOf, ind.isIndicatorOf) in runtime
    assert (proc.concernsProduct, OWL.inverseOf, proc.hasProcessExecution) in runtime
    assert not list(runtime.triples((ind.concernsProduct, OWL.inverseOf, None)))
    assert not list(runtime.triples((None, OWL.inverseOf, ind.concernsProduct)))
    from owlrl import DeductiveClosure, RDFS_Semantics
    for local in (ind.concernsProduct, proc.concernsProduct):
        hypothetical = Graph()
        hypothetical.add((local, RDFS.subPropertyOf, dpp.concernsProduct))
        hypothetical.add((dpp.concernsProduct, RDFS.domain, dpp.ProductEvent))
        hypothetical.add((EX.subject, local, EX.product))
        DeductiveClosure(RDFS_Semantics).expand(hypothetical)
        assert (EX.subject, RDF.type, dpp.ProductEvent) in hypothetical
