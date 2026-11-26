"""Keep Common version succession distinct from Connector replacement in WIDOCO."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
OLD='https://w3id.org/eudpp/textile-connector/2.0.0'
CURRENT='https://w3id.org/eudpp/textile-common/dev/integration-2026-11.3'
PREVIOUS='https://w3id.org/eudpp/textile-common/dev/integration-2026-11.2'

def main():
    base=ROOT/'docs/widoco/common'
    index=base/'index-en.html'
    text=index.read_text(encoding='utf8')
    pattern=r'(<dt>Previous version:</dt>\s*<dd><a href=")[^"]+("[^>]*>)[^<]+(</a></dd>)'
    replacement=r'\g<1>'+PREVIOUS+r'\g<2>'+PREVIOUS+r'\g<3>'
    text,n=re.subn(pattern,lambda m:m.group(1)+PREVIOUS+m.group(2)+PREVIOUS+m.group(3),text)
    if n!=1:raise ValueError('Unexpected Common prior-version display')
    marker='<dt>Replaces ontology:</dt>\n<dd><a href="'+OLD+'">'+OLD+'</a></dd>'
    if marker not in text:text=text.replace('<dt>Revision:</dt>',marker+'\n<dt>Revision:</dt>',1)
    index.write_text(text,encoding='utf8',newline='\n')
    path=base/'provenance/provenance-en.ttl';text=path.read_text(encoding='utf8')
    text=text.replace('prov:wasRevisionOf <'+OLD+'>','prov:wasRevisionOf <'+PREVIOUS+'>')
    if 'prov:wasRevisionOf <'+PREVIOUS+'>' not in text:raise ValueError('Missing Common prior-version provenance')
    path.write_text(text,encoding='utf8',newline='\n')
    path=base/'provenance/provenance-en.html';text=path.read_text(encoding='utf8')
    text=text.replace(CURRENT+' is a revision of the previous version '+OLD,CURRENT+' is a revision of the previous version '+PREVIOUS)
    if CURRENT+' is a revision of the previous version '+PREVIOUS not in text:raise ValueError('Missing Common previous version description')
    path.write_text(text,encoding='utf8',newline='\n')

if __name__=='__main__':main()
