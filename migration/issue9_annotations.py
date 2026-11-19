"""Verify the exact approved issue #9 annotation delta without predicate exclusions."""
import json
import subprocess
from pathlib import Path
from rdflib import Graph, Literal, RDFS, SKOS, Namespace
from rdflib.compare import isomorphic, graph_diff, to_isomorphic

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b'
MANIFEST = ROOT / 'migration/issue9-annotation-delta.json'
ANNOTATIONS = {RDFS.comment, SKOS.definition,
               Namespace('https://w3id.org/eudpp/textile-connector#').modellingNote}


def baseline_graph(relative):
    raw = subprocess.check_output(['git', 'show', BASELINE + ':' + relative], cwd=ROOT)
    return Graph().parse(data=raw.decode('utf8'), format='turtle')


def expected_delta(relative):
    record = json.loads(MANIFEST.read_text('utf8'))
    assert record['baseline_commit'] == BASELINE
    assert record['metadata_changes'] == []
    assert sum(len(r['added']) for r in record['modules']) == 14
    assert sum(len(r['removed']) for r in record['modules']) == 14
    assert {r['file'] for r in record['modules']} == {
        'ontology/textile-durability.ttl', 'ontology/textile-soc.ttl'}
    row = next((r for r in record['modules'] if r['file'] == relative), None)
    parse = lambda field: set(Graph().parse(data='\n'.join(row[field]), format='turtle')) if row else set()
    added, removed = parse('added'), parse('removed')
    assert len(added) == len(removed)
    assert {(s, p) for s, p, o in added} == {(s, p) for s, p, o in removed}
    for s, p, o in added | removed:
        assert p in ANNOTATIONS and isinstance(o, Literal), (relative, s, p, o)
    return added, removed


def restore_issue9_graph(graph, relative):
    """Check the entire candidate against its frozen baseline before reversing edits."""
    baseline = baseline_graph(relative)
    added, removed = expected_delta(relative)
    assert removed <= set(baseline) and not (added & set(baseline)), relative
    expected = baseline + Graph()
    for triple in removed:
        expected.remove(triple)
    for triple in added:
        expected.add(triple)
    assert isomorphic(graph, expected), 'Unauthorized canonical RDF difference: ' + relative
    return baseline


def canonical_differences():
    rows = []
    for path in sorted((ROOT / 'ontology').glob('*.ttl')):
        relative = path.relative_to(ROOT).as_posix()
        graph = Graph().parse(path)
        baseline = restore_issue9_graph(graph, relative)
        _, added, removed = graph_diff(to_isomorphic(graph), to_isomorphic(baseline))
        assert set(added) == expected_delta(relative)[0]
        assert set(removed) == expected_delta(relative)[1]
        fmt = lambda triples: sorted(' '.join(t.n3() for t in triple) + ' .' for triple in triples)
        rows.append(dict(file=relative, added=fmt(added), removed=fmt(removed)))
    return rows


if __name__ == '__main__':
    rows = canonical_differences()
    print(json.dumps(dict(baseline_commit=BASELINE, canonical_graphs=len(rows),
                         logical_added=0, logical_removed=0,
                         annotations_added=sum(len(r['added']) for r in rows),
                         annotations_removed=sum(len(r['removed']) for r in rows),
                         metadata_added=0, metadata_removed=0, modules=rows), indent=2))
