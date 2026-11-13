"""Shared fixtures for the repository regression tests."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]

# Validation and packaging operate on repository-relative paths, so every test gets
# a disposable copy of the published tree.
COPY_ENTRIES = (
    '.github',
    'assets',
    'dist',
    'docs',
    'evals',
    'experiments',
    'scripts',
    'skills',
    'tests',
    'CHANGELOG.md',
    'CONTRIBUTING.md',
    'LICENSE',
    'README.md',
    'ROADMAP.md',
    'requirements-dev.txt',
)


@pytest.fixture
def repo(tmp_path):
    target = tmp_path / 'repo'
    target.mkdir()
    for entry in COPY_ENTRIES:
        source = ROOT / entry
        destination = target / entry
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    return target


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_script(repo, script, *arguments):
    return subprocess.run(
        [sys.executable, str(Path(repo) / 'scripts' / script), *arguments],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def load_manifest(repo):
    return json.loads((Path(repo) / 'experiments/manifest.json').read_text())


def save_manifest(repo, manifest):
    (Path(repo) / 'experiments/manifest.json').write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    )


def load_baseline(repo, version='0.1.0'):
    return json.loads((Path(repo) / f'experiments/releases/v{version}.json').read_text())


def save_baseline(repo, baseline, version='0.1.0'):
    (Path(repo) / f'experiments/releases/v{version}.json').write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False) + '\n'
    )


def append_round(repo, record):
    manifest = load_manifest(repo)
    manifest['rounds'].append(record)
    save_manifest(repo, manifest)
    return manifest


def add_response_pair(repo, round_id, contents=('baseline response\n', 'skill response\n')):
    """Create the two response records a manifest round points at."""
    directory = Path(repo) / 'experiments/raw' / round_id
    directory.mkdir(parents=True)
    records = []
    for condition, body in zip(('A', 'B'), contents):
        path = directory / f'{condition}.txt'
        path.write_text(body)
        records.append({
            'condition': condition,
            'path': f'experiments/raw/{round_id}/{condition}.txt',
            'sha256': sha256(path),
        })
    return records


def rewrite_archive(repo, transform):
    """Rewrite the distributable archive in place, preserving deterministic metadata."""
    import zipfile

    target = next((Path(repo) / 'dist').glob('*.zip'))
    with zipfile.ZipFile(target) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    transform(members)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, data in members.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return target


def refresh_archive_reference(repo, target=None):
    """Update the baseline and checksum file to match a deliberately rewritten ZIP."""
    target = target or next((Path(repo) / 'dist').glob('*.zip'))
    baseline = load_baseline(repo)
    digest = sha256(target)
    baseline['archive']['sha256'] = digest
    save_baseline(repo, baseline)
    (Path(repo) / 'dist/SHA256SUMS.txt').write_text(f'{digest}  {target.name}\n')
    return digest
