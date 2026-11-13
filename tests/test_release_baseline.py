"""Regression tests for the independent, per-version release baseline."""
from pathlib import Path
import json
import re

from conftest import (
    load_baseline,
    load_manifest,
    run_script,
    save_baseline,
    save_manifest,
    sha256,
)


def test_baseline_covers_every_installable_file(repo):
    baseline = load_baseline(repo)
    installable = {
        path.relative_to(repo).as_posix()
        for path in (repo / 'skills').rglob('*')
        if path.is_file()
    }

    assert set(baseline['files']) == installable
    for relative, expected in baseline['files'].items():
        assert sha256(repo / relative) == expected


def test_baseline_archive_path_is_versioned(repo):
    baseline = load_baseline(repo)
    version = baseline['version']

    assert baseline['archive']['path'] == f'dist/ai-subjectivity-inquiry-v{version}.zip'
    assert re.fullmatch(r'[0-9a-f]{64}', baseline['archive']['sha256'])


def test_baseline_evaluation_cases_match_prompt_headings(repo):
    baseline = load_baseline(repo)
    prompts = (repo / baseline['evaluation']['prompt_file']).read_text()

    assert re.findall(r'^## (P\d{2})', prompts, flags=re.M) == baseline['evaluation']['cases']


def test_baseline_filename_matches_its_version(repo):
    for path in (repo / 'experiments/releases').glob('*.json'):
        baseline = json.loads(path.read_text())
        assert path.name == f"v{baseline['version']}.json"


def test_working_tree_and_manifest_changes_cannot_bypass_baseline(repo):
    """Editing both the skill and its manifest hash still trips the baseline."""
    relative = 'skills/ai-subjectivity-inquiry/SKILL.md'
    skill = repo / relative
    skill.write_text(skill.read_text() + '\nCoordinated edit.\n')
    manifest = load_manifest(repo)
    manifest['frozen_skill_sha256'][relative] = sha256(skill)
    save_manifest(repo, manifest)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Frozen skill changed' in result.stderr


def test_legacy_partial_rounds_are_declared_in_the_baseline(repo):
    baseline = load_baseline(repo)
    manifest = load_manifest(repo)
    partial = {record['id'] for record in manifest['rounds']
               if record['record_completeness'] == 'historical_partial'}

    assert partial
    assert partial == set(baseline['legacy_partial_rounds'])


def test_baseline_cannot_be_replaced_with_a_different_skill(repo):
    baseline = load_baseline(repo)
    baseline['skill'] = 'some-other-skill'
    save_baseline(repo, baseline)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Wrong skill in release baseline' in result.stderr


def test_release_archives_are_preserved_for_every_baseline(repo):
    for path in (repo / 'experiments/releases').glob('*.json'):
        baseline = json.loads(path.read_text())
        target = Path(repo) / baseline['archive']['path']
        assert target.is_file()
        assert sha256(target) == baseline['archive']['sha256']
