"""Reconstruct the committed Phase 3 package in a new isolated directory."""
from pathlib import Path
import argparse
import hashlib
import io
import os
import stat
import subprocess
import tarfile
from xml.etree import ElementTree as ET
from rdflib import Graph, OWL


def catalogue_import_closure(catalogue, entry):
    """Resolve this snapshot with its own catalogue; no network fallback."""
    base = catalogue.parent.resolve()
    routes = {node.attrib['name']: node.attrib['uri'] for node in ET.parse(catalogue).getroot()}
    pending, seen = [str(entry)], set()
    while pending:
        iri = pending.pop()
        if iri not in routes:
            raise ValueError('Unmapped historical import: ' + iri)
        path = (base / routes[iri]).resolve()
        if not path.is_relative_to(base) or not path.is_file():
            raise ValueError('Invalid historical catalogue target: ' + iri)
        if path in seen:
            continue
        seen.add(path)
        graph = Graph().parse(path, format='xml' if path.suffix == '.owl' else 'turtle')
        pending.extend(map(str, graph.objects(None, OWL.imports)))
    return seen

ROOT = Path(__file__).resolve().parents[1]
COMMIT = 'ce6d4a9b74c0abb70d86e93a3d2cce22f140a0d2'
ENTRY = 'https://w3id.org/eudpp/textile-ontology/dev/integration-2026-11.2'


def reconstruct(destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError('Destination must not exist: ' + str(destination))
    def blob(path):
        return subprocess.check_output(['git', 'show', COMMIT + ':' + path], cwd=ROOT)
    manifest = blob('PUBLICATION_MANIFEST.txt').decode('utf8')
    section = manifest.split('[CURRENT_PACKAGE]\n', 1)[1].split('\n[', 1)[0]
    names = {line.strip() for line in section.splitlines() if line.strip() and not line.startswith('#')}
    checksums = blob('SHA256SUMS')
    records = [line.split('  ', 1) for line in checksums.decode('utf8').splitlines() if line]
    if len(names) != 870 or len(records) != 869 or names != {path for _, path in records} | {'SHA256SUMS'}:
        raise ValueError('Committed Phase 3 manifest or checksum inventory changed')
    for name in names:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or path.as_posix() != name:
            raise ValueError('Unsafe package path')
    archive = subprocess.check_output(['git', 'archive', '--format=tar', COMMIT], cwd=ROOT)
    destination.mkdir(parents=False, exist_ok=False)
    found = set()
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tar:
        for entry in tar:
            if entry.name not in names:
                continue
            if not entry.isfile() or entry.name in found:
                raise ValueError('Unexpected archive member')
            target = destination / entry.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(tar.extractfile(entry).read())
            found.add(entry.name)
    if found != names or (destination / 'SHA256SUMS').read_bytes() != checksums:
        raise ValueError('Committed package inventory mismatch')
    for digest, name in records:
        if hashlib.sha256((destination / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Committed package checksum mismatch: ' + name)
    actual = {path.relative_to(destination).as_posix() for path in destination.rglob('*') if path.is_file()}
    if actual != names:
        raise ValueError('Unexpected reconstructed files')
    closure = catalogue_import_closure(destination / 'catalog-v001.xml', ENTRY)
    if len(closure) != 20 or any(not p.is_relative_to(destination) for p in closure):
        raise ValueError('Committed package offline closure mismatch')
    for name in names:
        os.chmod(destination / name, stat.S_IREAD)
    return len(names), len(records), len(closure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination')
    args = parser.parse_args()
    files, checksums, closure = reconstruct(args.destination)
    print(f'Reconstructed {files} files; {checksums} checksums; {closure} offline graphs')

if __name__ == '__main__':
    main()
