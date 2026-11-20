"""Phase 1 cumulative contract: exact graphs, preconditions and mutations."""
from dataclasses import replace

import pytest
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.compare import graph_diff, isomorphic, to_isomorphic

from migration import integration_contract as contract

EX = Namespace('urn:integration-test:')
CORE = 'ontology/textile-core.ttl'
DUR = 'ontology/textile-durability.ttl'


@pytest.fixture(scope='module')
def approved():
    baseline = contract.baseline_graphs()
    entries = contract.issue9_transitions()
    actual = {p: contract.parse_turtle((contract.ROOT / p).read_text(encoding='utf8'), p) for p in baseline}
    return baseline, entries, actual


def test_exact_issue9_transition(approved, monkeypatch):
    baseline, entries, actual = approved
    monkeypatch.setattr(contract, 'baseline_graphs', lambda: baseline)
    report = contract.validate(actual, entries)
    assert (report['canonical_graphs'], report['annotation_added'],
            report['annotation_removed']) == (13, 14, 14)
    assert all(report[name] == 0 for name in
               ('logical_changes', 'header_changes', 'version_changes', 'import_changes', 'shacl_changes'))


@pytest.mark.parametrize('fault', ['extra_axiom', 'missing_axiom', 'annotation',
                                   'version', 'import', 'restriction', 'list'])
def test_unauthorized_graph_mutations_rejected(approved, monkeypatch, fault):
    baseline, entries, actual = approved
    monkeypatch.setattr(contract, 'baseline_graphs', lambda: baseline)
    mutated = dict(actual)
    target = 'ontology/textile-assessment.ttl' if fault == 'list' else CORE
    graph = actual[target] + Graph()
    mutated[target] = graph
    if fault == 'extra_axiom':
        graph.add((EX.classA, RDFS.subClassOf, EX.classB))
    elif fault == 'missing_axiom':
        triple = next(graph.triples((None, RDFS.subClassOf, None)))
        graph.remove(triple)
    elif fault == 'annotation':
        graph.add((EX.classA, RDFS.comment, Literal('unapproved', lang='en')))
    elif fault == 'version':
        triple = next(graph.triples((None, OWL.versionIRI, None)))
        graph.remove(triple)
        graph.add((triple[0], OWL.versionIRI, EX.unapprovedVersion))
    elif fault == 'import':
        triple = next(graph.triples((None, OWL.imports, None)))
        graph.remove(triple)
        graph.add((triple[0], OWL.imports, EX.unapprovedImport))
    elif fault == 'restriction':
        node = next(graph.subjects(RDF.type, OWL.Restriction))
        graph.add((node, OWL.hasValue, EX.unapproved))
    else:
        node, _, old = next(graph.triples((None, RDF.first, None)))
        graph.remove((node, RDF.first, old))
        graph.add((node, RDF.first, EX.unapproved))
    with pytest.raises(contract.ContractError, match='Unauthorized canonical RDF difference'):
        contract.validate(mutated, entries)


def test_incomplete_transition_does_not_accept_full_candidate(approved, monkeypatch):
    baseline, entries, actual = approved
    monkeypatch.setattr(contract, 'baseline_graphs', lambda: baseline)
    with pytest.raises(contract.ContractError, match='Unapproved transition sequence'):
        contract.validate(actual, entries[:1])


def test_unmet_precondition_rejected(approved):
    baseline, entries, _ = approved
    bad = replace(entries[0], remove=frozenset({(EX.missing, RDF.type, OWL.Class)}))
    with pytest.raises(contract.ContractError, match='Missing removal precondition'):
        contract.build_expected(baseline, [bad])


def test_duplicate_and_contradictory_entries_rejected(approved):
    baseline, entries, _ = approved
    with pytest.raises(contract.ContractError, match='Duplicate transition id'):
        contract.build_expected(baseline, [entries[0], entries[0]])
    triple = next(iter(entries[0].add))
    bad = replace(entries[0], add=frozenset({triple}), remove=frozenset({triple}))
    with pytest.raises(contract.ContractError, match='Contradictory'):
        contract.build_expected(baseline, [bad])


def test_overlap_requires_explicit_contributing_decisions_and_issues():
    path = 'ontology/example.ttl'
    old = (EX.s, RDFS.comment, Literal('old'))
    middle = (EX.s, RDFS.comment, Literal('middle'))
    final = (EX.s, RDFS.comment, Literal('final'))
    base = Graph(); base.add(old)
    first = contract.Transition('a', path, '#9', 'commit9', ('decision9',),
                                'first', 'old exists', 'annotation',
                                frozenset({old}), frozenset({middle}))
    second = contract.Transition('b', path, '#12', 'commit12', ('decision12',),
                                 'reconciled', 'middle exists', 'annotation',
                                 frozenset({middle}), frozenset({final}))
    with pytest.raises(contract.ContractError, match='Overlapping'):
        contract.build_expected({path: base}, [first, second])
    second = replace(second, reconciles=('a',), decisions=('decision9', 'decision12'),
                     contributing_issues=('#9', '#12'))
    result = contract.build_expected({path: base}, [first, second])[path]
    assert final in result and old not in result and middle not in result


def test_anonymous_change_needs_reviewed_complete_snapshots():
    path = 'ontology/example.ttl'
    before = Graph().parse(data='@prefix e: <urn:ex:> . e:x e:p [ e:q e:a ] .', format='turtle')
    after = Graph().parse(data='@prefix e: <urn:ex:> . e:x e:p [ e:q e:b ] .', format='turtle')
    _, removed, added = graph_diff(to_isomorphic(before), to_isomorphic(after))
    transition = contract.Transition('snapshot', path, '#future', 'source', ('decision',),
                                    'approved blank-node change', 'exact previous graph', 'logical',
                                    before=before, after=after,
                                    removed_graph=removed, added_graph=added)
    assert isomorphic(contract.build_expected({path: before}, [transition])[path], after)
    incomplete = replace(transition, added_graph=Graph())
    with pytest.raises(contract.ContractError, match='Snapshot diff mismatch'):
        contract.build_expected({path: before}, [incomplete])
    wrong = Graph() + before
    wrong.add((EX.unapproved, RDF.type, OWL.Class))
    with pytest.raises(contract.ContractError, match='Snapshot precondition'):
        contract.build_expected({path: wrong}, [transition])
    bn = next(n for n in before.all_nodes() if isinstance(n, BNode))
    bad = replace(transition, before=None, after=None, removed_graph=None, added_graph=None,
                  add=frozenset({(bn, RDF.type, OWL.Class)}))
    with pytest.raises(contract.ContractError, match='Blank-node changes require'):
        contract.build_expected({path: before}, [bad])


def test_issue9_evidence_is_pinned_to_approved_commit(monkeypatch):
    from pathlib import Path
    original = Path.read_bytes
    def altered(path):
        data = original(path)
        if path == contract.ROOT / contract.EVIDENCE:
            return data + b' '
        return data
    monkeypatch.setattr(Path, 'read_bytes', altered)
    with pytest.raises(contract.ContractError, match='Issue 9 evidence changed'):
        contract.issue9_transitions()


def test_validator_rejects_changed_protected_catalogue(monkeypatch):
    from pathlib import Path
    original = Path.read_bytes
    target = contract.ROOT / 'catalog-v001.xml'
    def altered(path):
        data = original(path)
        return data + b' ' if path == target else data
    monkeypatch.setattr(Path, 'read_bytes', altered)
    with pytest.raises(AssertionError):
        contract.validate()



def test_production_validate_current_worktree():
    report = contract.validate()
    assert report['canonical_graphs'] == 13
    assert report['annotation_added'] == report['annotation_removed'] == 14


@pytest.mark.parametrize('relative', ['VERSION', 'migration/legacy-soc-attribution.json'])
def test_production_validate_rejects_mutated_protected_bytes(monkeypatch, relative):
    from pathlib import Path
    original = Path.read_bytes
    target = contract.ROOT / relative
    def altered(path):
        data = original(path)
        return data + b' ' if path == target else data
    monkeypatch.setattr(Path, 'read_bytes', altered)
    with pytest.raises(contract.ContractError, match='Protected file changed'):
        contract.validate()


def test_production_validate_rejects_extra_ontology_file(monkeypatch):
    from pathlib import Path
    original = Path.glob
    def altered(path, pattern, *args, **kwargs):
        found = list(original(path, pattern, *args, **kwargs))
        if path == contract.ROOT / 'ontology' and pattern == 'textile-*.ttl':
            found.append(path / 'textile-x.ttl')
        return iter(found)
    monkeypatch.setattr(Path, 'glob', altered)
    with pytest.raises(contract.ContractError, match='Canonical document inventory changed'):
        contract.validate()


@pytest.mark.parametrize('fault', ['swap', 'duplicate', 'unrelated_decision', 'wrong_issue', 'wrong_commit'])
def test_production_validate_rejects_false_attribution(monkeypatch, fault):
    import json
    from pathlib import Path
    original = Path.read_text
    def altered(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        if path != contract.CONTRACT:
            return text
        data = json.loads(text)
        first, second = data['entries']
        if fault == 'swap':
            first['graph'], second['graph'] = second['graph'], first['graph']
        elif fault == 'duplicate':
            second['id'] = first['id']
        elif fault == 'unrelated_decision':
            first['decisions'] = ['docs/decisions/TXT-DEC-010.md']
        elif fault == 'wrong_issue':
            first['issue'] = '#12'
        else:
            first['source_commit'] = contract.BASELINE
        return json.dumps(data)
    monkeypatch.setattr(Path, 'read_text', altered)
    with pytest.raises(contract.ContractError, match='issue 9 entry identity|transition attribution'):
        contract.validate()


def test_production_validate_rejects_lexical_date_change(monkeypatch):
    from pathlib import Path
    from rdflib.namespace import XSD
    # RDFLib's default normalization collapses these distinct RDF terms.
    assert Literal('2026-03-06', datatype=XSD.date) == Literal('2026-03-06Z', datatype=XSD.date)
    original = Path.read_text
    target = contract.ROOT / CORE
    def altered(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        if path == target:
            old = '"2026-03-06"^^xsd:date'
            assert old in text
            return text.replace(old, '"2026-03-06Z"^^xsd:date', 1)
        return text
    monkeypatch.setattr(Path, 'read_text', altered)
    with pytest.raises(contract.ContractError, match='Unauthorized canonical RDF difference'):
        contract.validate()


def test_lexical_parser_preserves_numeric_and_token_literals_without_global_mutation():
    import rdflib
    from concurrent.futures import ThreadPoolExecutor
    from rdflib.namespace import XSD
    before = rdflib.NORMALIZE_LITERALS
    source = ('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> . '
              '<urn:s> <urn:p> "01"^^xsd:integer, 01, 1.00, 1.0e+0, '
              '"2026-03-06Z"^^xsd:date, " a  b "^^xsd:token .')
    def parse(_):
        graph = contract.parse_turtle(source, CORE)
        return {(str(o), o.datatype) for o in graph.objects()}
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(parse, range(8)))
    expected = {('01', XSD.integer), ('1.00', XSD.decimal),
                ('1.0e+0', XSD.double), ('2026-03-06Z', XSD.date),
                (' a  b ', XSD.token)}
    assert all(result == expected for result in results)
    assert rdflib.NORMALIZE_LITERALS == before


def test_production_validate_rejects_optimized_python():
    import subprocess
    import sys
    result = subprocess.run([sys.executable, '-B', '-O', '-m', 'migration.integration_contract'],
                            cwd=contract.ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert 'Optimized Python disables required historical assertions' in result.stderr


def test_snapshot_after_delta_requires_reconciled_decisions():
    path = 'ontology/example.ttl'
    old = (EX.s, RDFS.comment, Literal('old'))
    middle = (EX.s, RDFS.comment, Literal('middle'))
    before = Graph(); before.add(old)
    interim = Graph(); interim.add(middle)
    after = Graph() + interim
    after.add((EX.s, RDF.type, OWL.Class))
    first = contract.Transition('a', path, '#9', 'source9', ('decision9',),
                                'approved delta', 'old exists', 'annotation',
                                frozenset({old}), frozenset({middle}))
    _, removed, added = graph_diff(to_isomorphic(interim), to_isomorphic(after))
    snapshot = contract.Transition('b', path, '#future', 'source2', ('decision2',),
                                   'test snapshot', 'exact interim graph', 'logical',
                                   before=interim, after=after,
                                   removed_graph=removed, added_graph=added)
    with pytest.raises(contract.ContractError, match='Snapshot overlap'):
        contract.build_expected({path: before}, [first, snapshot])
    snapshot = replace(snapshot, reconciles=('a',), decisions=('decision9', 'decision2'),
                       contributing_issues=('#9', '#future'))
    assert isomorphic(contract.build_expected({path: before}, [first, snapshot])[path], after)



def test_missing_approved_decision_record_is_rejected(monkeypatch):
    import subprocess
    original = subprocess.run
    def altered(args, *pos, **kwargs):
        if (args[:3] == ['git', 'cat-file', '-e'] and
                args[3].endswith('docs/decisions/TXT-DEC-016.md')):
            return subprocess.CompletedProcess(args, 1, b'', b'not found')
        return original(args, *pos, **kwargs)
    monkeypatch.setattr(subprocess, 'run', altered)
    with pytest.raises(contract.ContractError, match='Decision record absent'):
        contract.validate()


def test_frozen_inventory_does_not_depend_on_mutable_current_modules(monkeypatch):
    monkeypatch.setattr(contract.mat_alignment.v, 'CURRENT_MODULES', ('textile-x.ttl',))
    assert set(contract.baseline_graphs()) == contract.APPROVED_FILES
