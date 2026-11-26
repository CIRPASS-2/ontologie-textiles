"""Phase 3 source-pinned preflight and explicit graph transition definitions.

This module prepares expectations only. It does not modify ontology files.
"""
import hashlib
from functools import lru_cache
import subprocess
from pathlib import Path
from rdflib import Graph, Literal, OWL, RDF, RDFS, URIRef
from rdflib.compare import graph_diff, isomorphic, to_isomorphic
from rdflib.namespace import DCTERMS
from migration import phase2b_contract as phase2
from migration import integration_contract as p1
from scripts import generate_common_connector as compat

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'b05927c3e32ff0d0b82ce6d5a55dc60665f9168f'
COMMON_PATH = 'ontology/textile-common.ttl'
OLD_PATH = 'ontology/textile-connector.ttl'
SHAPES = 'shacl/textile-quantitative-shapes.ttl'
COMMON_SHA256 = 'a184d24165f04a19d486e83f454d11ae0bada420a662963d5519674107fea683'
SHAPES_SHA256 = '114ebb8b5bb51de1ccceb4fdcf713403514254e8a8ced7cb09f020c15e194c01'
SHACL_README_SHA256 = 'bc55ab558b2042d80a1e42f38a4ba1868a5919c237a947ab1973427eed8b1149'
OLD_VERSION = 'integration-2026-11.1'
VERSION = 'integration-2026-11.2'
SOURCE_VERSION = '2.1.0-issue16-dev'

COMMENTS = {
 'ontology/textile-assessment.ttl': {
  URIRef('https://w3id.org/eudpp/textile-assessment'): 'Quantitative results, parameter settings and thresholds use txtcon:QuantitativeValue and SI Digital Framework units through the Textile Connector pattern.',
 },
 'ontology/textile-recyclability.ttl': {
  URIRef('https://w3id.org/eudpp/textile-recyclability#hasRecyclabilityTechnologyLevel'): 'Classifies a recyclability assessment result using the shared product-technology-level vocabulary defined in Textile Connector.',
  URIRef('https://w3id.org/eudpp/textile-recyclability#hasRecycledContentTechnologyLevel'): 'Classifies a recycled-content assessment result using the shared product-technology-level vocabulary defined in Textile Connector.',
 },
}


def source_blob(path, digest):
    raw = subprocess.check_output(['git', 'show', SOURCE + ':' + path], cwd=ROOT)
    p1.require(hashlib.sha256(raw).hexdigest() == digest, 'Approved issue 16 source bytes changed: ' + path)
    return raw


def common_source():
    raw = source_blob(COMMON_PATH, COMMON_SHA256)
    return p1.parse_turtle(raw.decode('utf8'), COMMON_PATH)


def check_source_payload():
    """Verify exact source against Phase 2B with only 37 defining-module changes."""
    _, previous = phase2.expected_graphs()
    old = previous[OLD_PATH]
    source = common_source()
    old_payload = Graph()
    for triple in old:
        if triple[0] != compat.CONNECTOR:
            old_payload.add(triple)
    terms = {s for s in old_payload.subjects(RDFS.isDefinedBy, compat.CONNECTOR)
             if isinstance(s, URIRef) and str(s).startswith(str(compat.NS))}
    p1.require(len(terms) == 37, 'Phase 2B Connector term inventory changed')
    for term in terms:
        old_payload.remove((term, RDFS.isDefinedBy, compat.CONNECTOR))
        old_payload.add((term, RDFS.isDefinedBy, compat.COMMON))
    source_payload, source_terms = compat.payload(source)
    p1.require(terms == source_terms and isomorphic(old_payload, source_payload),
               'Issue 16 source changes more than approved defining-module assertions')
    p1.require(len(source_payload) == 395 and sum(s not in terms for s,p,o in source_payload) == 33,
               'Unexpected Common supporting triple inventory')
    p1.require(set(source.objects(compat.COMMON, OWL.imports)) == {compat.SI},
               'Common source import changed')
    return len(terms), len(source_payload)


def replace_literal(graph, subject, predicate, old, new):
    before = (subject, predicate, old)
    p1.require(before in graph, 'Phase 3 transition precondition failed: ' + str(predicate))
    graph.remove(before)
    graph.add((subject, predicate, new))



def verify_issue16_source():
    """Prove each source domain graph contains only the enumerated decisions."""
    baseline = p1.baseline_graphs()
    for path, original in baseline.items():
        if path == OLD_PATH:
            continue
        expected = original + Graph()
        removed, added = phase2.version_transition(expected, path, '/' + SOURCE_VERSION, SOURCE_VERSION)
        expected = phase2.apply_changes(expected, removed, added)
        ontology = URIRef('https://w3id.org/eudpp/' + Path(path).stem)
        replace_literal(expected, ontology, OWL.imports, compat.CONNECTOR, compat.COMMON)
        for subject, old in COMMENTS.get(path, {}).items():
            replace_literal(expected, subject, RDFS.comment, Literal(old, lang='en'),
                            Literal(old.replace('Textile Connector', 'Textile Common'), lang='en'))
        raw = subprocess.check_output(['git', 'show', SOURCE + ':' + path], cwd=ROOT)
        actual = p1.parse_turtle(raw.decode('utf8'), path)
        p1.require(isomorphic(expected, actual), 'Unexpected issue 16 source transition: ' + path)
    check_source_payload()
    source_blob(SHAPES, SHAPES_SHA256)
    source_blob('shacl/README.md', SHACL_README_SHA256)
    return 12


def verify_phase2b_commit():
    """Prove the pinned committed .1 graphs are reconstructed by the prior contract."""
    phase2.verify_source()
    _, expected = phase2.expected_graphs()
    commit = '6e2c2034e90a6883aaf99f18df2504b5f2136376'
    for path, graph in expected.items():
        raw = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=ROOT)
        p1.require(isomorphic(graph, p1.parse_turtle(raw.decode('utf8'), path)),
                   'Committed Phase 2B graph differs from cumulative proof: ' + path)
    return len(expected)


def verify_reconciliation():
    """Detect subject/predicate overlap with earlier issue decisions and headers."""
    earlier = set()
    for entry in p1.issue9_transitions():
        earlier.update((entry.graph, subject, predicate) for subject, predicate, _ in entry.remove | entry.add)
    for path, (removed, added) in phase2.ISSUE12.items():
        earlier.update((path, subject, predicate) for subject, predicate, _ in removed | added)
    overlap = {(path, subject, RDFS.comment) for path, entries in COMMENTS.items()
               for subject in entries} & earlier
    p1.require(not overlap, 'Issue 16 comment overlaps an earlier decision without reconciliation')
    _, previous = phase2.expected_graphs()
    reconciled = set()
    for path, graph in previous.items():
        if path == OLD_PATH:
            continue
        ontology = URIRef('https://w3id.org/eudpp/' + Path(path).stem)
        for predicate in (OWL.versionIRI, OWL.versionInfo, OWL.priorVersion, DCTERMS.bibliographicCitation):
            if list(graph.objects(ontology, predicate)):
                reconciled.add((path, ontology, predicate))
        p1.require((path, ontology, OWL.imports) not in earlier,
                   'Import transition overlaps an earlier issue decision')
    p1.require(len(reconciled) == 47, 'Unexpected owner-approved development-header overlap')
    return len(reconciled)

@lru_cache(maxsize=2)
def _expected_graphs(evidence_key):
    """Build from the exact Phase 2B graphs, applying explicit issue 16 changes."""
    check_source_payload()
    verify_reconciliation()
    _, previous = phase2.expected_graphs()
    result = {}
    for path, original in previous.items():
        if path == OLD_PATH:
            continue
        graph = original + Graph()
        ontology = URIRef('https://w3id.org/eudpp/' + Path(path).stem)
        replace_literal(graph, ontology, OWL.versionIRI,
                        URIRef(str(ontology) + '/dev/' + OLD_VERSION),
                        URIRef(str(ontology) + '/dev/' + VERSION))
        replace_literal(graph, ontology, OWL.priorVersion,
                        URIRef(str(ontology) + '/2.0.0'),
                        URIRef(str(ontology) + '/dev/' + OLD_VERSION))
        replace_literal(graph, ontology, OWL.versionInfo,
                        Literal('Version ' + OLD_VERSION), Literal('Version ' + VERSION))
        for old in list(graph.objects(ontology, DCTERMS.bibliographicCitation)):
            p1.require(str(old).endswith('Version ' + OLD_VERSION + '.'), 'Unexpected citation')
            replace_literal(graph, ontology, DCTERMS.bibliographicCitation, old,
                            Literal(str(old).replace(OLD_VERSION, VERSION), lang=old.language))
        replace_literal(graph, ontology, OWL.imports, compat.CONNECTOR, compat.COMMON)
        for subject, old in COMMENTS.get(path, {}).items():
            replace_literal(graph, subject, RDFS.comment, Literal(old, lang='en'),
                            Literal(old.replace('Textile Connector', 'Textile Common'), lang='en'))
        result[path] = graph
    common = common_source()
    # Common is a new ontology identity; Connector is its migration source,
    # not a prior version of the Common identity.
    historical = URIRef(str(compat.CONNECTOR) + '/2.0.0')
    p1.require((compat.COMMON, OWL.priorVersion, historical) in common, 'Common migration provenance precondition')
    common.remove((compat.COMMON, OWL.priorVersion, historical))
    common.add((compat.COMMON, DCTERMS.replaces, historical))
    replace_literal(common, compat.COMMON, OWL.versionIRI,
                    URIRef(str(compat.COMMON) + '/' + SOURCE_VERSION),
                    URIRef(str(compat.COMMON) + '/dev/' + VERSION))
    replace_literal(common, compat.COMMON, OWL.versionInfo,
                    Literal('Version ' + SOURCE_VERSION), Literal('Version ' + VERSION))
    old_citation = next(common.objects(compat.COMMON, DCTERMS.bibliographicCitation))
    replace_literal(common, compat.COMMON, DCTERMS.bibliographicCitation, old_citation,
                    Literal(str(old_citation).replace(SOURCE_VERSION, VERSION), lang=old_citation.language))
    result[COMMON_PATH] = common
    return result



def expected_graphs():
    # Recheck issue-9 attribution on every call; cached graphs are keyed by both
    # reviewed local evidence files and never derive from candidate graphs.
    p1.issue9_transitions()
    evidence_key = hashlib.sha256((p1.ROOT / p1.EVIDENCE).read_bytes() + p1.CONTRACT.read_bytes()).hexdigest()
    return _expected_graphs(evidence_key)

def expected_shapes_bytes():
    raw = source_blob(SHAPES, SHAPES_SHA256)
    old = b'https://w3id.org/eudpp/textile-shacl/quantitative/2.1.0-issue16-dev'
    new = b'https://w3id.org/eudpp/textile-shacl/quantitative/dev/integration-2026-11.2'
    p1.require(raw.count(old) == 1, 'Unexpected quantitative SHACL version precondition')
    raw = raw.replace(old, new)
    target = b'owl:versionIRI <' + new + b'> ;'
    p1.require(raw.count(target) == 1, 'Quantitative SHACL header precondition')
    return raw.replace(target, target + b'\n    owl:priorVersion <https://w3id.org/eudpp/textile-shacl/quantitative/2.0.0> ;')


def expected_catalogue():
    """Apply only owner-approved version, document and shape routing changes."""
    raw = phase2.expected_catalogue().decode('utf8')
    p1.require(raw.count('/dev/' + OLD_VERSION) == 13, 'Phase 2B catalogue version inventory')
    raw = raw.replace('/dev/' + OLD_VERSION, '/dev/' + VERSION)
    p1.require(raw.count('uri="ontology/textile-connector.ttl"') == 2, 'Legacy catalogue route inventory')
    raw = raw.replace('uri="ontology/textile-connector.ttl"', 'uri="compat/textile-connector.ttl"')
    marker = '  <uri name="https://w3id.org/eudpp/textile-connector"'
    p1.require(raw.count(marker) == 1, 'Common catalogue insertion precondition')
    common = ('  <uri name="https://w3id.org/eudpp/textile-common" uri="ontology/textile-common.ttl" />\n'
              '  <uri name="https://w3id.org/eudpp/textile-common/dev/' + VERSION + '" uri="ontology/textile-common.ttl" />\n')
    raw = raw.replace(marker, common + marker)
    old = 'https://w3id.org/eudpp/textile-shacl/quantitative/2.0.0'
    p1.require(raw.count(old) == 1, 'Quantitative catalogue precondition')
    raw = raw.replace(old, 'https://w3id.org/eudpp/textile-shacl/quantitative/dev/' + VERSION)
    return raw.encode('utf8')


def verify_protected():
    """Verify upstream, MIREOT and historical inputs against frozen Git blobs."""
    areas = ['dependencies', 'mireot', 'migration/core-sources', 'migration/historical', 'migration/legacy-soc-attribution.json', 'shacl', 'examples', 'traceability']
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', p1.BASELINE, '--', *areas],
                                    cwd=ROOT, text=True).splitlines()
    from scripts.validate_public import package_files
    packaged = {name for name in package_files(ROOT)
                if any(name == area or name.startswith(area + '/') for area in areas)}
    p1.require(packaged == set(names), 'Protected input inventory changed')
    batch = ''.join(p1.BASELINE + ':' + name + '\n' for name in names).encode()
    raw = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=batch,
                         capture_output=True, check=True).stdout
    position = 0
    for name in names:
        end = raw.index(b'\n', position)
        header = raw[position:end].split()
        p1.require(len(header) == 3 and header[1] == b'blob', 'Missing protected Git object')
        size = int(header[2]); data = raw[end+1:end+1+size]; position = end+size+2
        if name == SHAPES:
            data = expected_shapes_bytes()
        elif name == 'shacl/README.md':
            data = source_blob(name, SHACL_README_SHA256)
        elif name == 'traceability/textile-resource-traceability.csv':
            p1.require(data.count(b',textile-connector,') == 37, 'Traceability migration precondition')
            data = data.replace(b',textile-connector,', b',textile-common,')
        p1.require((ROOT/name).read_bytes() == data, 'Protected file changed: ' + name)
    return len(names)


def restore_phase2(graph, path):
    """Accept an exact Phase 3 canonical graph and recover its Phase 2B graph."""
    expected = expected_graphs()
    p1.require(path in expected and isomorphic(graph, expected[path]),
               'Unauthorized canonical RDF difference (Phase 3): ' + path)
    previous_path = OLD_PATH if path == COMMON_PATH else path
    _, previous = phase2.expected_graphs()
    return previous[previous_path] + Graph(), previous_path



def classify_actual(previous, actual):
    """Classify real complete-graph differences, rejecting unapproved categories."""
    from collections import Counter
    result = {}
    for path, graph in actual.items():
        old_path = OLD_PATH if path == COMMON_PATH else path
        _, removed, added = graph_diff(to_isomorphic(previous[old_path]), to_isomorphic(graph))
        counts = Counter()
        old_iri = URIRef('https://w3id.org/eudpp/' + Path(old_path).stem)
        new_iri = URIRef('https://w3id.org/eudpp/' + Path(path).stem)
        for direction, triples in (('removed', removed), ('added', added)):
            for subject, predicate, obj in triples:
                if subject in COMMENTS.get(path, {}) and predicate == RDFS.comment:
                    category = 'annotation'
                elif subject in (old_iri, new_iri):
                    category = 'import' if predicate == OWL.imports else 'header'
                elif path == COMMON_PATH and predicate == RDFS.isDefinedBy:
                    category = 'annotation'
                else:
                    raise p1.ContractError('Unexpected logical or anonymous Phase 3 delta: ' + path + ' ' + str(predicate))
                counts[category + '_' + direction] += 1
        result[path] = dict(counts)
    return result

def verify_connector_header(graph):
    """Authorize the complete ontology-subject header independently of generation."""
    connector = URIRef('https://w3id.org/eudpp/textile-connector')
    common = URIRef('https://w3id.org/eudpp/textile-common')
    expected = {
        (connector, RDF.type, OWL.Ontology),
        (connector, RDFS.label, Literal('Textile Connector compatibility ontology', lang='en')),
        (connector, RDFS.comment, Literal('Complete compatibility representation of Textile Common using the retained Connector term IRIs.', lang='en')),
        (connector, OWL.versionIRI, URIRef('https://w3id.org/eudpp/textile-connector/dev/integration-2026-11.2')),
        (connector, OWL.versionInfo, Literal('Version integration-2026-11.2')),
        (connector, OWL.priorVersion, URIRef('https://w3id.org/eudpp/textile-connector/dev/integration-2026-11.1')),
        (connector, OWL.imports, URIRef('https://w3id.org/eudpp/textile-si-mireot')),
        (connector, DCTERMS.source, common),
    }
    for name in ('Andreas Schneider', 'BOUGACHA Racem', 'Elio Hbeich',
                 'Ivo Ladenius', 'Jan Merckx', 'Piero de Sabbata'):
        expected.add((connector, DCTERMS.creator, Literal(name, lang='en')))
    p1.require(set(graph.triples((connector, None, None))) == expected,
               'Unauthorized Connector ontology header')
    p1.require(set(graph.subjects(RDF.type, OWL.Ontology)) == {connector},
               'Unexpected Connector ontology identity')


def validate():
    """Validate actual cumulative graphs, isolated compatibility and protected bytes."""
    if not __debug__:
        raise p1.ContractError('Optimized Python disables required historical assertions')
    from scripts.validate_public import catalogue_import_closure
    phase2.verify_source()
    verify_issue16_source()
    verify_phase2b_commit()
    expected = expected_graphs()
    p1.require((ROOT/'VERSION').read_bytes() == (VERSION+'\n').encode(), 'Package version changed (Phase 3)')
    p1.require((ROOT/'catalog-v001.xml').read_bytes() == expected_catalogue(), 'Catalogue transition mismatch (Phase 3)')
    p1.require((ROOT/SHAPES).read_bytes() == expected_shapes_bytes(), 'Unapproved quantitative SHACL change')
    paths = {p.relative_to(ROOT).as_posix() for p in (ROOT/'ontology').glob('textile-*.ttl')}
    p1.require(paths == set(expected), 'Canonical document inventory changed (Phase 3)')
    actual_graphs = {}
    for path, graph in expected.items():
        actual = p1.parse_turtle((ROOT/path).read_text(encoding='utf8'), path)
        p1.require(isomorphic(actual, graph), 'Unauthorized canonical RDF difference (Phase 3): ' + path)
        actual_graphs[path] = actual
    _, previous = phase2.expected_graphs()
    categories = classify_actual(previous, actual_graphs)
    common = p1.parse_turtle((ROOT/COMMON_PATH).read_text(encoding='utf8'), COMMON_PATH)
    connector_path = ROOT/'compat/textile-connector.ttl'
    connector = p1.parse_turtle(connector_path.read_text(encoding='utf8'), 'compat/textile-connector.ttl')
    p1.require(connector_path.read_text(encoding='utf8') == compat.render(common),
               'Compatibility representation is not deterministically generated')
    verify_connector_header(connector)
    terms, triples = compat.verify(common, connector)
    canonical = catalogue_import_closure(ROOT/'catalog-v001.xml',
                   'https://w3id.org/eudpp/textile-ontology/dev/' + VERSION)
    common_closure = catalogue_import_closure(ROOT/'catalog-v001.xml',
                   'https://w3id.org/eudpp/textile-common/dev/' + VERSION)
    legacy = catalogue_import_closure(ROOT/'catalog-v001.xml',
                   'https://w3id.org/eudpp/textile-connector/dev/' + VERSION)
    p1.require(len(canonical) == 20 and len(common_closure) == 2 and len(legacy) == 2,
               'Offline closure changed')
    p1.require(ROOT/COMMON_PATH in canonical and ROOT/COMMON_PATH in common_closure
               and connector_path in legacy and ROOT/COMMON_PATH not in legacy,
               'Unexpected canonical or compatibility closure')
    protected = verify_protected()
    frozen, historical = phase2.check_frozen()
    return dict(version=VERSION, canonical_graphs=len(paths), issue9_annotation_added=14,
                issue9_annotation_removed=14, issue12_logical_removed=1, compatibility_terms=terms,
                compatibility_payload_triples=triples, canonical_closure=len(canonical),
                common_closure=len(common_closure),
                compatibility_closure=len(legacy), protected_files=protected,
                frozen_checksums=frozen, historical_closure=historical,
                graph_transition_categories=categories)
