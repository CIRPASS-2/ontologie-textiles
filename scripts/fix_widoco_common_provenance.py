"""Correct WIDOCO's Common replacement/version conflation, deterministically."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = 'https://w3id.org/eudpp/textile-connector/2.0.0'
CURRENT = 'https://w3id.org/eudpp/textile-common/dev/integration-2026-11.2'


def update(path, before, after):
    text = path.read_text(encoding='utf8')
    if before in text:
        if text.count(before) != 1:
            raise ValueError('Unexpected repeated WIDOCO statement: ' + str(path))
        path.write_text(text.replace(before, after), encoding='utf8', newline='\n')
    elif after not in text:
        raise ValueError('Expected WIDOCO statement missing: ' + str(path))


def main():
    base = ROOT / 'docs/widoco/common'
    update(base / 'index-en.html', '<dt>Previous version:</dt>\n<dd><a href="' + OLD + '">',
           '<dt>Replaces ontology:</dt>\n<dd><a href="' + OLD + '">')
    update(base / 'provenance/provenance-en.html',
           CURRENT + ' is a revision of the previous version ' + OLD,
           CURRENT + ' replaces the former Connector ontology ' + OLD)
    path = base / 'provenance/provenance-en.ttl'
    text = path.read_text(encoding='utf8')
    bad = '\t prov:wasRevisionOf <' + OLD + '>;\n'
    if bad in text:
        if text.count(bad) != 1:
            raise ValueError('Unexpected repeated revision statement')
        path.write_text(text.replace(bad, ''), encoding='utf8', newline='\n')
    elif 'prov:wasRevisionOf' in text:
        raise ValueError('Unexpected Common revision statement')


if __name__ == '__main__':
    main()
