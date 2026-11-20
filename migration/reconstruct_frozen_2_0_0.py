"""Reconstruct the isolated historical package from the approved Git tree."""
from pathlib import Path
import argparse
import io
import os
import stat
import subprocess
import tarfile
from migration import integration_contract as contract
from migration.phase2b_contract import check_frozen

ROOT = Path(__file__).resolve().parents[1]

def reconstruct(destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError('Destination must not already exist: ' + str(destination))
    baseline = contract.BASELINE
    def git_blob(name):
        return subprocess.check_output(['git', 'show', baseline + ':' + name], cwd=ROOT)
    sha = git_blob('SHA256SUMS')
    manifest = git_blob('PUBLICATION_MANIFEST.txt').decode('utf8')
    section = manifest.split('[CURRENT_PACKAGE]\n', 1)[1].split('\n[', 1)[0]
    names = {line.strip() for line in section.splitlines() if line.strip() and not line.startswith('#')}
    records = [line.split('  ', 1) for line in sha.decode('utf8').splitlines() if line]
    checksum_names = {name for _, name in records}
    contract.require(len(records) == 799 and len(checksum_names) == 799 and
                     names == checksum_names | {'SHA256SUMS'} and len(names) == 800,
                     'Historical manifest and checksum inventory mismatch')
    for name in names:
        path = Path(name)
        contract.require(not path.is_absolute() and '..' not in path.parts and
                         path.as_posix() == name, 'Unsafe historical path')
    archive = subprocess.check_output(['git', 'archive', '--format=tar', baseline], cwd=ROOT)
    destination.mkdir(parents=False, exist_ok=False)
    found = set()
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tar:
        for member in tar:
            if member.name not in names:
                continue
            contract.require(member.isfile() and member.name not in found,
                             'Unexpected historical archive member')
            data = tar.extractfile(member).read()
            target = destination / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            found.add(member.name)
    contract.require(found == names, 'Historical archive missing package files')
    checksums, closure = check_frozen(destination)
    for name in sorted(names):
        os.chmod(destination / name, stat.S_IREAD)
    return len(found), checksums, closure

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', help='new, absent destination directory')
    args = parser.parse_args()
    files, checksums, closure = reconstruct(args.destination)
    print(f'Reconstructed {files} files; {checksums} checksums; {closure} offline graphs')

if __name__ == '__main__':
    main()
