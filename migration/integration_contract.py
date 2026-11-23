"""Ordered, explicit RDF transition validation for the integration worktree.

Phase 1 uses the independently committed issue-9 manifest. Later phases must
supply reviewed entries and evidence; a source branch is not an authorization.
All complete candidate graphs are compared by isomorphism, including blank
nodes. Snapshot operations are experimental preparation only; matching snapshots
and graph differences are not independent approval evidence.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import io
import json
from pathlib import Path
import subprocess

from rdflib import BNode, Graph, Literal, OWL, RDFS, SKOS, URIRef
from rdflib.namespace import XSD
from rdflib.plugins.parsers.notation3 import (
    RDFSink, SinkParser, numberCharsPlus, exponent_syntax,
    decimal_syntax, integer_syntax,
)
from rdflib.compare import graph_diff, isomorphic, to_isomorphic

from migration import issue9_annotations as issue9
from migration import mat_alignment

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '40b08bff9316ba47b0b8b0c2b5265ef2ddbdfe6b'
START = '384d3dece18c9804839d47c0a21aec545f17d47c'
CONTRACT = ROOT / 'migration/integration-transition-contract.json'
EVIDENCE = 'migration/issue9-annotation-delta.json'
APPROVED_FILES = frozenset('ontology/textile-' + name + '.ttl' for name in (
    'assessment', 'associated-materials', 'connector', 'context', 'core',
    'durability', 'indicator', 'ontology', 'process', 'recyclability',
    'repairability', 'soc', 'structure'))
APPROVED_ENTRIES = {
    'issue9-durability': 'ontology/textile-durability.ttl',
    'issue9-soc': 'ontology/textile-soc.ttl',
}
APPROVED_DECISIONS = (
    'docs/decisions/TXT-DEC-016.md',
    'migration/ISSUE_9_IMPLEMENTATION_REPORT.md',
)
CATEGORIES = frozenset({'annotation', 'logical', 'header', 'import',
                        'document', 'shacl', 'dependency'})


class ContractError(ValueError):
    """An authorization, precondition, or graph comparison failed."""


def require(condition, message):
    if not condition:
        raise ContractError(message)


class _LexicalSink(RDFSink):
    """Construct RDFLib literals with the original lexical string."""
    def newLiteral(self, text, datatype, lang):
        literal = Literal(text, lang=lang, datatype=datatype, normalize=False)
        # RDFLib 7.6 normalizes xsd:token and xsd:normalizedString even when
        # normalize=False. Retain the parser-decoded RDF lexical form, while
        # keeping RDFLib's datatype validation and cached value.
        if str(literal) != text:
            exact = str.__new__(Literal, text)
            exact._language = literal.language
            exact._datatype = literal.datatype
            exact._value = literal.value
            exact._ill_typed = literal.ill_typed
            return exact
        return literal


class _LexicalTurtleParser(SinkParser):
    """Keep bare numeric tokens as lexical RDF literals, not Python numbers."""
    def nodeOrLiteral(self, text, offset, result):
        j = self.node(text, offset, result)
        if j >= 0:
            return j
        j = self.skipSpace(text, offset)
        if j < 0:
            return -1
        if text[j] in numberCharsPlus:
            for syntax, datatype in ((exponent_syntax, XSD.double),
                                     (decimal_syntax, XSD.decimal),
                                     (integer_syntax, XSD.integer)):
                match = syntax.match(text, j)
                if match:
                    result.append(self._store.newLiteral(text[j:match.end()], datatype, None))
                    return match.end()
        return super().nodeOrLiteral(text, offset, result)


def parse_turtle(data, relative):
    """Parse Turtle without changing process-global RDFLib configuration."""
    graph = Graph()
    sink = _LexicalSink(graph)
    base = (ROOT / relative).resolve().as_uri()
    parser = _LexicalTurtleParser(sink, baseURI=base, turtle=True)
    parser.loadStream(io.StringIO(data))
    for prefix, namespace in parser._bindings.items():
        graph.bind(prefix, namespace)
    return graph


@dataclass(frozen=True)
class Transition:
    id: str
    graph: str
    issue: str
    source_commit: str
    decisions: tuple[str, ...]
    rationale: str
    precondition: str
    category: str
    remove: frozenset = field(default_factory=frozenset)
    add: frozenset = field(default_factory=frozenset)
    reconciles: tuple[str, ...] = ()
    contributing_issues: tuple[str, ...] = ()
    # Snapshot structures support experiments with anonymous changes. The
    # production validator does not authorize them; future use requires
    # independently reviewed and pinned source evidence.
    before: Graph | None = None
    after: Graph | None = None
    removed_graph: Graph | None = None
    added_graph: Graph | None = None


def build_expected(baselines, transitions):
    """Apply supplied transitions; this function does not confer approval."""
    expected = {name: graph + Graph() for name, graph in baselines.items()}
    seen_ids = {}
    touched = {}
    for entry in transitions:
        require(entry.id and entry.id not in seen_ids, 'Duplicate transition id')
        require(entry.graph in expected, 'Unknown graph: ' + entry.graph)
        require(entry.issue and entry.source_commit and entry.decisions and
                entry.rationale and entry.precondition, 'Incomplete transition metadata')
        require(entry.category in CATEGORIES, 'Unknown transition category')
        require(not (entry.add & entry.remove), 'Contradictory transition')
        require(all(x in seen_ids for x in entry.reconciles),
                'Reconciliation must identify earlier transitions')
        graph = expected[entry.graph]
        if entry.before is not None or entry.after is not None:
            require(all(x is not None for x in
                        (entry.before, entry.after, entry.removed_graph, entry.added_graph)),
                    'Snapshots require complete before, after, added and removed graphs')
            require(not entry.add and not entry.remove, 'Snapshot and triple delta cannot be mixed')
            require(isomorphic(graph, entry.before), 'Snapshot precondition failed: ' + entry.id)
            _, removed, added = graph_diff(to_isomorphic(entry.before),
                                           to_isomorphic(entry.after))
            require(isomorphic(removed, entry.removed_graph) and
                    isomorphic(added, entry.added_graph), 'Snapshot diff mismatch: ' + entry.id)
            # Snapshot overlaps are not inferred from unstable blank-node ids.
            # Any subsequent change to this graph must explicitly reconcile it.
            for old in seen_ids.values():
                if old.graph == entry.graph:
                    require(old.id in entry.reconciles and
                            set(old.decisions) <= set(entry.decisions) and
                            ({old.issue, entry.issue} | set(old.contributing_issues)) <= set(entry.contributing_issues),
                            'Snapshot overlap requires all contributing decisions')
            expected[entry.graph] = entry.after + Graph()
            touched[(entry.graph, None)] = entry
        else:
            require(entry.add or entry.remove, 'Empty transition')
            require(not any(isinstance(term, BNode)
                            for triple in entry.add | entry.remove for term in triple),
                    'Blank-node changes require reviewed snapshots')
            snapshot = touched.get((entry.graph, None))
            if snapshot:
                require(snapshot.id in entry.reconciles and
                        set(snapshot.decisions) <= set(entry.decisions) and
                        ({snapshot.issue, entry.issue} | set(snapshot.contributing_issues)) <= set(entry.contributing_issues),
                        'Snapshot overlap requires all contributing decisions')
            for triple in entry.add | entry.remove:
                old = touched.get((entry.graph, triple))
                if old:
                    require(old.id in entry.reconciles and
                            set(old.decisions) <= set(entry.decisions) and
                            ({old.issue, entry.issue} | set(old.contributing_issues)) <= set(entry.contributing_issues),
                            'Overlapping transition requires all contributing decisions')
            require(entry.remove <= set(graph), 'Missing removal precondition: ' + entry.id)
            require(not (entry.add & set(graph)), 'Addition already present: ' + entry.id)
            for triple in entry.remove:
                graph.remove(triple)
            for triple in entry.add:
                graph.add(triple)
            for triple in entry.add | entry.remove:
                touched[(entry.graph, triple)] = entry
        seen_ids[entry.id] = entry
    return expected


def issue9_transitions():
    """Read exact approved records, also pinning evidence to the approved commit."""
    data = json.loads(CONTRACT.read_text(encoding='utf8'))
    require(data['schema'] == 1 and data['phase'] == 1 and
            data['baseline_commit'] == BASELINE and data['starting_commit'] == START and
            data['evidence'] == EVIDENCE, 'Unexpected contract identity')
    pinned = subprocess.check_output(['git', 'show', START + ':' + EVIDENCE], cwd=ROOT)
    require((ROOT / EVIDENCE).read_bytes() == pinned, 'Issue 9 evidence changed')
    require(len(data['entries']) == 2, 'Unexpected issue 9 entry count')
    for document in APPROVED_DECISIONS:
        result = subprocess.run(['git', 'cat-file', '-e', START + ':' + document],
                                cwd=ROOT, capture_output=True)
        require(result.returncode == 0, 'Decision record absent from approved commit: ' + document)
    require({row['id'] for row in data['entries']} == set(APPROVED_ENTRIES),
            'Unexpected or duplicate issue 9 entry identity')
    transitions = []
    for row in data['entries']:
        require(row['issue'] == '#9' and row['source_commit'] == START and
                row['category'] == 'annotation' and
                row['graph'] == APPROVED_ENTRIES.get(row['id']) and
                tuple(row['decisions']) == APPROVED_DECISIONS,
                'Unapproved phase 1 transition attribution')
        added, removed = issue9.expected_delta(row['graph'], parser=parse_turtle)
        transitions.append(Transition(
            id=row['id'], graph=row['graph'], issue=row['issue'],
            source_commit=row['source_commit'], decisions=tuple(row['decisions']),
            rationale=row['rationale'], precondition=row['precondition'],
            category=row['category'], remove=frozenset(removed), add=frozenset(added)))
    require({x.graph for x in transitions} ==
            {'ontology/textile-durability.ttl', 'ontology/textile-soc.ttl'},
            'Unexpected issue 9 graph inventory')
    counts = Counter(t[1] for entry in transitions for t in entry.add)
    require(sum(counts.values()) == 14 and counts ==
            {RDFS.comment: 5, SKOS.definition: 3,
             issue9.Namespace('https://w3id.org/eudpp/textile-connector#').modellingNote: 6},
            'Unexpected issue 9 predicate counts')
    require(sum(len(x.remove) for x in transitions) == 14,
            'Unexpected issue 9 removal count')
    return transitions


def baseline_graphs():
    paths = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', BASELINE, '--', 'ontology'],
        cwd=ROOT, text=True).splitlines()
    historical = {p for p in paths if p.startswith('ontology/textile-')
                  and p.endswith('.ttl') and '/' not in p[len('ontology/'):]}
    require(historical == APPROVED_FILES, 'Frozen canonical graph inventory changed')
    return {path: issue9.baseline_graph(path, parser=parse_turtle) for path in sorted(historical)}


def validate(candidate_graphs=None, transitions=None):
    """Compare each entire current ontology with its independently built expectation."""
    if not __debug__:
        raise ContractError('Optimized Python disables required historical assertions')
    require(candidate_graphs is None and transitions is None,
            'Injected candidates are not accepted by current Phase 2B validation')
    if (ROOT / 'VERSION').read_text(encoding='utf8').strip() == 'integration-2026-11.2':
        from migration.phase3_preflight import validate as validate_phase3
        return validate_phase3()
    from migration.phase2b_contract import validate as validate_phase2
    return validate_phase2()


def _validate_phase1_fixture(candidate_graphs, transitions=None):
    """Validate a synthetic Phase 1 fixture, never the current integration."""
    # Reuse the existing strict byte and inventory proof; never replace it
    # with graph equivalence or a newly computed allowlist.
    protected = mat_alignment.protected_hashes()
    for name in ('VERSION', 'migration/legacy-soc-attribution.json'):
        frozen = (b'integration-2026-11.2\n' if name == 'VERSION' else
                  subprocess.check_output(['git', 'show', BASELINE + ':' + name], cwd=ROOT))
        require((ROOT / name).read_bytes() == frozen, 'Protected file changed: ' + name)
    baseline = baseline_graphs()
    approved = issue9_transitions()
    if transitions is not None:
        require(transitions == approved, 'Unapproved transition sequence')
    transitions = approved
    expected = build_expected(baseline, transitions)
    if candidate_graphs is None:
        actual_files = {p.relative_to(ROOT).as_posix()
                        for p in (ROOT / 'ontology').glob('textile-*.ttl')}
        require(actual_files == set(baseline), 'Canonical document inventory changed')
        candidate_graphs = {path: parse_turtle((ROOT / path).read_text(encoding='utf8'), path)
                            for path in baseline}
    require(set(candidate_graphs) == set(expected), 'Candidate graph inventory changed')
    for path in expected:
        require(isomorphic(expected[path], candidate_graphs[path]),
                'Unauthorized canonical RDF difference: ' + path)
    categories = Counter(e.category for e in transitions)
    require(set(categories) <= {'annotation'},
            'The Phase 1 report accepts annotation transitions only')
    return {
        'baseline_commit': BASELINE, 'starting_commit': START,
        'canonical_graphs': len(expected), 'transition_ids': [e.id for e in transitions],
        'annotation_added': sum(len(e.add) for e in transitions if e.category == 'annotation'),
        'annotation_removed': sum(len(e.remove) for e in transitions if e.category == 'annotation'),
        'logical_changes': 0, 'header_changes': 0, 'version_changes': 0,
        'import_changes': 0, 'shacl_changes': 0,
        'evidence': EVIDENCE, 'protected_files': len(protected) + 2,
    }


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
