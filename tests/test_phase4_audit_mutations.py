"""Production-path audit mutations in isolated, rechecksummed packages."""
from pathlib import Path
import hashlib
import shutil
import pytest
from migration import integration_contract as entry
from migration import phase4_contract as phase4
from scripts import validate_public as public


@pytest.fixture
def scratch(tmp_path, monkeypatch):
    source=phase4.ROOT
    for name in (*public.package_files(source), *public.PRESERVED_REFERENCE_MATERIAL):
        target=tmp_path/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source/name,target)
    # Git reads the shared object database; no source worktree is modified.
    shutil.copyfile(source/'.git',tmp_path/'.git')
    monkeypatch.setattr(entry,'ROOT',tmp_path)
    monkeypatch.setattr(phase4,'ROOT',tmp_path)
    return tmp_path


def loader_paths(module, root, monkeypatch, complete_report=False):
    from rdflib import Graph
    selected=[]
    class StopAfterLoading(Exception):
        pass
    monkeypatch.setattr(module,'ontology_graph',lambda root:Graph())
    monkeypatch.setattr(module,'parse',lambda path:(selected.append(path) or Graph()))
    def stop(*args):
        raise StopAfterLoading
    monkeypatch.setattr(module,'reject_legacy_soc',stop)
    with pytest.raises(StopAfterLoading):
        module.runtime_checks(root,complete_report=complete_report)
    return selected


def test_actual_default_loader_excludes_assessed_aspect(monkeypatch):
    selected=loader_paths(public,phase4.ROOT,monkeypatch)
    assert phase4.ROOT/phase4.PROFILE not in selected
    assert {p.relative_to(phase4.ROOT).as_posix() for p in selected if p.is_relative_to(phase4.ROOT/'shacl')} == {
        'shacl/textile-quantitative-shapes.ttl',
        'shacl/textile-recyclability-shapes.ttl',
        'shacl/textile-soc-shapes.ttl',
    }


def refresh_integrity(root):
    files=public.package_files(root)
    manifest=('# Current Textile package integrity and separate reference inventory.\n'
              '# Only CURRENT_PACKAGE participates in SHA256SUMS (except SHA256SUMS itself).\n'
              '[CURRENT_PACKAGE]\n'+'\n'.join(files)+'\n\n[PRESERVED_REFERENCE_MATERIAL]\n'
              +'\n'.join(public.PRESERVED_REFERENCE_MATERIAL)+'\n')
    (root/'PUBLICATION_MANIFEST.txt').write_text(manifest,encoding='utf8',newline='\n')
    checks=''.join(hashlib.sha256((root/name).read_bytes()).hexdigest()+'  '+name+'\n'
                   for name in files if name!='SHA256SUMS')
    (root/'SHA256SUMS').write_text(checks,encoding='utf8',newline='\n')


@pytest.mark.parametrize('fault,message',[
    ('outcome','Unauthorized SHACL document inventory'),
    ('optional_copy','Unauthorized SHACL document inventory'),
    ('recyclability','Unauthorized recyclability SHACL bytes'),
    ('soc','Protected SHACL bytes changed'),
    ('complete_report','Protected SHACL bytes changed'),
    ('decision','Approved issue 20 source record changed'),
    ('example','Approved issue 20 source record changed'),
    ('loader','Public profile selection changed'),
])
def test_rechecksummed_mutations_are_rejected_by_production(scratch,fault,message,monkeypatch):
    if fault=='outcome':
        (scratch/'shacl/textile-outcome-shapes.ttl').write_text(
            '@prefix sh: <http://www.w3.org/ns/shacl#> .\n'
            '<urn:audit:outcome> a sh:NodeShape ; sh:targetObjectsOf <https://w3id.org/eudpp/textile-assessment#hasAssessmentOutcome> .\n',
            encoding='utf8',newline='\n')
    elif fault=='optional_copy':
        shutil.copyfile(scratch/phase4.PROFILE,scratch/'shacl/textile-assessed-aspect-targets.ttl')
    elif fault in ('recyclability','soc','complete_report'):
        path={'recyclability':'shacl/textile-recyclability-shapes.ttl',
              'soc':'shacl/textile-soc-shapes.ttl',
              'complete_report':'shacl/profiles/textile-soc-complete-report.ttl'}[fault]
        with (scratch/path).open('ab') as stream:stream.write(b'\n# unauthorized mutation\n')
    elif fault=='decision':
        with (scratch/'docs/decisions/TXT-DEC-014.md').open('ab') as stream:
            stream.write(b'\nUnauthorized decision alteration.\n')
    elif fault=='example':
        with (scratch/'examples/example-15-awarded-points-v2.1.0-dev.ttl').open('ab') as stream:
            stream.write(b'\n# unauthorized example alteration\n')
    else:
        path=scratch/'scripts/validate_public.py'
        text=path.read_text(encoding='utf8')
        old=" for p in sorted((root/'shacl').glob('*.ttl')):shapes+=parse(p)"
        new=old+"\n shapes+=parse(root/'shacl/profiles/textile-assessed-aspect-targets.ttl')"
        assert text.count(old)==1
        path.write_text(text.replace(old,new),encoding='utf8',newline='\n')
        # Exercise the changed loader, not just the modified source text.
        import importlib.util
        spec=importlib.util.spec_from_file_location('audit_mutated_loader',path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert scratch/phase4.PROFILE in loader_paths(module,scratch,monkeypatch)
    refresh_integrity(scratch)
    # The ordinary public structural validator accepts the rechecksummed package;
    # independent authorization must still reject the actual mutation.
    assert public.structural_checks(scratch)['structural_checks']=='passed'
    with pytest.raises(entry.ContractError,match=message):
        entry.validate()
