"""Regression tests for reproducible packaging and archive integrity."""
from pathlib import Path
import hashlib
import zipfile

from conftest import (
    load_baseline,
    refresh_archive_reference,
    rewrite_archive,
    run_script,
    sha256,
)

INSTALLABLE_MEMBERS = {
    'ai-subjectivity-inquiry/SKILL.md',
    'ai-subjectivity-inquiry/references/respect-under-uncertainty.md',
}


def archive_path(repo):
    return next((Path(repo) / 'dist').glob('ai-subjectivity-inquiry-v*.zip'))


def test_packaging_is_byte_for_byte_reproducible(repo):
    first = run_script(repo, 'package.py')
    assert first.returncode == 0, first.stderr
    first_digest = sha256(archive_path(repo))

    second = run_script(repo, 'package.py')
    assert second.returncode == 0, second.stderr

    assert sha256(archive_path(repo)) == first_digest
    assert run_script(repo, 'validate.py').returncode == 0


def test_committed_dist_matches_a_fresh_build(repo):
    """CI's committed-dist check should never hide behind a stale checkout."""
    before = sha256(archive_path(repo))
    result = run_script(repo, 'package.py')

    assert result.returncode == 0, result.stderr
    assert sha256(archive_path(repo)) == before


def test_archive_contains_only_the_installable_skill(repo):
    target = archive_path(repo)
    with zipfile.ZipFile(target) as archive:
        assert set(archive.namelist()) == INSTALLABLE_MEMBERS
        assert archive.testzip() is None
        assert not any(name.startswith(('evals/', 'experiments/')) for name in archive.namelist())


def test_checksum_file_matches_archive(repo):
    target = archive_path(repo)
    digest = sha256(target)
    checksum = (repo / 'dist/SHA256SUMS.txt').read_text()

    assert checksum == f'{digest}  {target.name}\n'
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest


def test_archive_members_match_working_skill_files(repo):
    target = archive_path(repo)
    skills = repo / 'skills'
    with zipfile.ZipFile(target) as archive:
        for member in INSTALLABLE_MEMBERS:
            assert archive.read(member) == (skills / member).read_bytes()


def test_validate_rejects_deliberately_corrupted_archive(repo):
    target = archive_path(repo)
    target.write_bytes(target.read_bytes()[:64])
    refresh_archive_reference(repo, target)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Corrupt archive' in result.stderr


def test_validate_rejects_archive_member_from_different_bytes(repo):
    rewrite_archive(repo, lambda members: members.__setitem__(
        'ai-subjectivity-inquiry/references/respect-under-uncertainty.md',
        b'different reference bytes\n',
    ))
    refresh_archive_reference(repo)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Stale archive member' in result.stderr


def test_release_baseline_matches_the_committed_archive(repo):
    baseline = load_baseline(repo)
    target = repo / baseline['archive']['path']

    assert target.is_file()
    assert sha256(target) == baseline['archive']['sha256']
