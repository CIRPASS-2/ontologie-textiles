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
    # The old assertion compared all dependencies with main before approved
    # issues #10/#13/#15. Use the shared exact cumulative inventory/byte proof;
    # its source is the pinned approved commit, never candidate checksums.
    from migration import mat_alignment
    assert len(mat_alignment.protected_hashes()) == 76
    assert (m.ROOT/'VERSION').read_bytes() == b'integration-2026-11.3\n'


def test_documentation_generation_preserves_content_and_tracks_inputs(monkeypatch):
    import json
    import re
    from pathlib import Path
    from migration import refresh_publication as refresh

    paths = [
        'README.md', 'docs/MODELLING_GUIDE.md', 'docs/ARCHITECTURE.md',
        'docs/DEPENDENCIES.md', 'docs/SOURCE_TRACEABILITY.md',
        'docs/governance/upstream-dependency-governance.md',
        'shacl/README.md', 'examples/README.md', 'CHANGELOG.md',
        'traceability/README.md', 'docs/PUBLICATION_SCOPE.md',
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


@pytest.mark.parametrize('relative', [
    'dependencies/current-core/lca.owl', 'mireot/dpp-textile-mireot.ttl',
    'shacl/textile-recyclability-shapes.ttl', 'migration/historical/inventory.json',
])
def test_cumulative_protection_rejects_changed_approved_bytes(monkeypatch, relative):
    from pathlib import Path
    from migration import mat_alignment
    read=Path.read_bytes
    def changed(path):
        data=read(path)
        return data+b'\n# unauthorized\n' if path==m.ROOT/relative else data
    monkeypatch.setattr(Path,'read_bytes',changed)
    with pytest.raises(AssertionError,match=relative.replace('.',r'\.')):
        mat_alignment.protected_hashes()


def test_cumulative_protection_rejects_unapproved_inventory(monkeypatch):
    from migration import mat_alignment
    packaged=mat_alignment.v.package_files
    monkeypatch.setattr(mat_alignment.v,'package_files',lambda root:packaged(root)+['examples/unapproved.ttl'])
    with pytest.raises(AssertionError,match='Protected file inventory changed'):
        mat_alignment.protected_hashes()


@pytest.mark.parametrize('fault', ['technical', 'profile_link'])
def test_documentation_guide_checks_reject_lost_content(fault):
    from migration.refresh_publication import check_shacl_guide
    text=(m.ROOT/'shacl/README.md').read_text('utf8')
    if fault=='technical':
        text=text.replace('A MeasurementParameterSetting may have a quantitative value',
                          'An unauthorized replacement',1)
    else:
        text=text.replace('](profiles/textile-soc-complete-report.ttl)','](missing.ttl)')
    with pytest.raises(AssertionError):check_shacl_guide(text)
