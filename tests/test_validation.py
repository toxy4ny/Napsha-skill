"""Regression tests for structural and evidence validation."""
from conftest import (
    add_response_pair,
    append_round,
    load_baseline,
    load_manifest,
    rewrite_archive,
    run_script,
    save_baseline,
    save_manifest,
    sha256,
)


def test_published_tree_passes(repo):
    result = run_script(repo, 'validate.py')
    assert result.returncode == 0, result.stderr
    assert 'PASS' in result.stdout


def test_rejects_modified_frozen_skill(repo):
    skill = repo / 'skills/ai-subjectivity-inquiry/SKILL.md'
    skill.write_text(skill.read_text() + '\nUnrecorded instruction change.\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Frozen skill changed' in result.stderr


def test_rejects_modified_reference(repo):
    reference = repo / 'skills/ai-subjectivity-inquiry/references/respect-under-uncertainty.md'
    reference.write_text(reference.read_text() + '\nUnrecorded reference change.\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Frozen skill changed' in result.stderr


def test_rejects_modified_evidence_record(repo):
    record = repo / 'experiments/raw/01-framing-exploratory/A.txt'
    record.write_text(record.read_text() + '\nEdited after publication.\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Response changed' in result.stderr


def test_rejects_extra_evidence_record(repo):
    (repo / 'experiments/raw/01-framing-exploratory/extra.txt').write_text('extra\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Evidence inventory differs' in result.stderr


def test_rejects_missing_evidence_record(repo):
    responses = add_response_pair(repo, '05-missing')
    (repo / responses[0]['path']).unlink()
    append_round(repo, {
        'id': '05-missing',
        'status': 'run',
        'record_completeness': 'historical_partial',
        'responses': responses,
    })

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Missing response record' in result.stderr


def test_rejects_broken_local_link(repo):
    readme = repo / 'README.md'
    readme.write_text(readme.read_text() + '\n[missing](does-not-exist.md)\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Broken local link' in result.stderr


def test_manifest_cannot_rebaseline_a_frozen_file(repo):
    """The manifest is mutable history; the release baseline is the authority."""
    baseline = load_baseline(repo)
    manifest = load_manifest(repo)
    relative = 'skills/ai-subjectivity-inquiry/SKILL.md'
    fake = '0' * 64
    baseline['files'][relative] = fake
    manifest['frozen_skill_sha256'][relative] = fake
    save_baseline(repo, baseline)
    save_manifest(repo, manifest)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Frozen skill changed' in result.stderr


def test_manifest_hash_must_match_release_baseline(repo):
    manifest = load_manifest(repo)
    manifest['frozen_skill_sha256']['skills/ai-subjectivity-inquiry/SKILL.md'] = '0' * 64
    save_manifest(repo, manifest)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Manifest hash differs from the release baseline' in result.stderr


def test_rejects_manifest_version_without_baseline(repo):
    manifest = load_manifest(repo)
    manifest['skill_version'] = '0.2.0'
    save_manifest(repo, manifest)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Manifest version differs' in result.stderr


def test_rejects_duplicate_round_ids(repo):
    manifest = load_manifest(repo)
    manifest['rounds'].append(dict(manifest['rounds'][0]))
    save_manifest(repo, manifest)

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Duplicate experiment round' in result.stderr


def test_rejects_new_partial_round(repo):
    responses = add_response_pair(repo, '05-unrecorded')
    append_round(repo, {
        'id': '05-unrecorded',
        'status': 'not_run',
        'record_completeness': 'historical_partial',
        'responses': responses,
    })

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Only v0.1.0-era rounds may remain partially recorded' in result.stderr


def test_rejects_complete_round_without_provenance(repo):
    responses = add_response_pair(repo, '05-incomplete')
    append_round(repo, {
        'id': '05-incomplete',
        'status': 'run',
        'record_completeness': 'complete',
        'responses': responses,
    })

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Complete round is missing executed_at' in result.stderr


def test_accepts_a_complete_round(repo):
    round_id = '05-complete'
    responses = add_response_pair(repo, round_id)
    records = repo / 'experiments/records' / round_id
    records.mkdir(parents=True)
    inputs = []
    for condition in ('A', 'B'):
        path = records / f'input-{condition}.txt'
        path.write_text(f'exact {condition} prompt\n')
        inputs.append({
            'condition': condition,
            'turn': 1,
            'path': f'experiments/records/{round_id}/input-{condition}.txt',
            'sha256': sha256(path),
        })
    loading = records / 'loading.txt'
    loading.write_text('visible skill-loading event\n')
    append_round(repo, {
        'id': round_id,
        'status': 'run',
        'record_completeness': 'complete',
        'executed_at': '2026-11-12T09:30:00+01:00',
        'inputs': inputs,
        'settings': {
            'model_label': 'Example model, as displayed',
            'model_snapshot_verified': False,
            'fresh_chat': True,
            'exposed_settings': 'extra reasoning enabled',
            'other_skills': 'disabled in both conditions',
            'tools': 'none',
            'memory_or_project_context': 'disabled',
        },
        'loading_evidence': {
            'status': 'confirmed',
            'note': 'Visible activation event in the skill condition.',
            'artifacts': [{
                'path': f'experiments/records/{round_id}/loading.txt',
                'sha256': sha256(loading),
            }],
        },
        'reviewer': {
            'name_or_role': 'Independent reviewer',
            'relationship_to_skill': 'No role in creating the skill',
            'independent': True,
            'blinded_to_condition': True,
            'reviewed_at': '2026-11-12',
        },
        'deviations': [],
        'redactions': [],
        'responses': responses,
    })

    result = run_script(repo, 'validate.py')

    assert result.returncode == 0, result.stderr
    assert '5 rounds' in result.stdout


def test_rejects_unknown_evaluation_case(repo):
    prompts = repo / 'evals/prompts.md'
    prompts.write_text(prompts.read_text() + '\n## P13\n\n```text\nNew case.\n```\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Evaluation case inventory differs' in result.stderr


def test_rejects_stale_archive_member(repo):
    rewrite_archive(repo, lambda members: members.__setitem__(
        'ai-subjectivity-inquiry/SKILL.md', b'changed inside the archive\n'
    ))
    # Refresh only the archive digest, leaving the baseline's member hashes intact.
    target = next((repo / 'dist').glob('*.zip'))
    baseline = load_baseline(repo)
    baseline['archive']['sha256'] = sha256(target)
    save_baseline(repo, baseline)
    (repo / 'dist/SHA256SUMS.txt').write_text(f'{baseline["archive"]["sha256"]}  {target.name}\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Stale archive member' in result.stderr


def test_rejects_extra_archive_member(repo):
    rewrite_archive(repo, lambda members: members.__setitem__('extra.txt', b'extra\n'))
    target = next((repo / 'dist').glob('*.zip'))
    baseline = load_baseline(repo)
    baseline['archive']['sha256'] = sha256(target)
    save_baseline(repo, baseline)
    (repo / 'dist/SHA256SUMS.txt').write_text(f'{baseline["archive"]["sha256"]}  {target.name}\n')

    result = run_script(repo, 'validate.py')

    assert result.returncode != 0
    assert 'Wrong installable archive contents' in result.stderr
