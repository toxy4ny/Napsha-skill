#!/usr/bin/env python3
"""Validate structure and record integrity; this is not a behavioral evaluation."""
from datetime import datetime
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/ai-subjectivity-inquiry'
SKILL_RELATIVE = SKILL.relative_to(ROOT).as_posix()
RELEASES = ROOT / 'experiments/releases'
RAW = ROOT / 'experiments/raw'
MANIFEST = ROOT / 'experiments/manifest.json'
HEX_DIGEST = re.compile(r'[0-9a-f]{64}')
CASE_ID = re.compile(r'P\d{2}')
ROUND_ID = re.compile(r'\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*')
CONDITIONS = {'A', 'B'}
COMPLETE_ROUND_KEYS = ('executed_at', 'inputs', 'settings', 'loading_evidence',
                       'reviewer', 'deviations', 'redactions')
SETTINGS_KEYS = ('model_label', 'model_snapshot_verified', 'fresh_chat',
                 'exposed_settings', 'other_skills', 'tools',
                 'memory_or_project_context')
REVIEWER_KEYS = ('name_or_role', 'relationship_to_skill', 'independent',
                 'blinded_to_condition', 'reviewed_at')
LOADING_STATUSES = {'confirmed', 'not_observed', 'unknown'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def frontmatter(path):
    text = path.read_text()
    match = re.match(r'\A---\n(.*?)\n---\n', text, flags=re.S)
    require(match is not None, f'Missing frontmatter: {path}')
    metadata = yaml.safe_load(match.group(1))
    require(isinstance(metadata, dict), f'Frontmatter must be a mapping: {path}')
    return metadata, text[match.end():]


def installed_name(relative):
    """Map a repository-relative skill file path to its name inside the archive."""
    return PurePosixPath(relative).relative_to(PurePosixPath('skills')).as_posix()


def parse_timestamp(value, field, record_id):
    require(isinstance(value, str) and value, f'Missing {field}: {record_id}')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as error:
        raise ValueError(f'Invalid {field}: {record_id}') from error
    require(parsed.tzinfo is not None, f'{field} must include a timezone: {record_id}')


def load_release_baselines():
    """Load immutable per-version baselines kept separate from manifest.json."""
    paths = sorted(RELEASES.glob('*.json'))
    require(paths, 'Missing release baseline in experiments/releases/')
    baselines = {}
    for path in paths:
        baseline = json.loads(path.read_text())
        require(isinstance(baseline, dict), f'Release baseline must be an object: {path}')
        require(baseline.get('schema_version') == 1,
                f'Unsupported release baseline schema: {path}')
        version = baseline.get('version')
        require(isinstance(version, str) and re.fullmatch(r'\d+\.\d+\.\d+', version),
                f'Invalid release version: {path}')
        require(path.name == f'v{version}.json',
                f'Release baseline filename must match its version: {path}')
        require(version not in baselines, f'Duplicate release baseline: {version}')
        require(baseline.get('skill') == SKILL.name, f'Wrong skill in release baseline: {path}')

        files = baseline.get('files')
        require(isinstance(files, dict) and files, f'Release baseline has no files: {path}')
        for relative, expected in files.items():
            require(relative.startswith(f'{SKILL_RELATIVE}/'),
                    f'Release baseline file is outside the installed skill: {relative}')
            require(isinstance(expected, str) and HEX_DIGEST.fullmatch(expected),
                    f'Invalid file digest in release baseline: {relative}')

        archive = baseline.get('archive')
        require(isinstance(archive, dict), f'Release baseline has no archive: {path}')
        require(archive.get('path') == f'dist/ai-subjectivity-inquiry-v{version}.zip',
                f'Release archive path does not match its version: {path}')
        require(isinstance(archive.get('sha256'), str)
                and HEX_DIGEST.fullmatch(archive['sha256']),
                f'Invalid release archive digest: {path}')

        evaluation = baseline.get('evaluation')
        require(isinstance(evaluation, dict), f'Release baseline has no evaluation block: {path}')
        require(evaluation.get('prompt_file') == 'evals/prompts.md',
                f'Unexpected evaluation prompt file in release baseline: {path}')
        cases = evaluation.get('cases')
        require(isinstance(cases, list) and cases, f'Release baseline has no cases: {path}')
        require(len(cases) == len(set(cases)), f'Duplicate evaluation case: {path}')
        require(all(isinstance(case, str) and CASE_ID.fullmatch(case) for case in cases),
                f'Invalid evaluation case id: {path}')

        legacy = baseline.get('legacy_partial_rounds', [])
        require(isinstance(legacy, list), f'legacy_partial_rounds must be a list: {path}')
        require(len(legacy) == len(set(legacy)), f'Duplicate legacy partial round: {path}')
        require(all(isinstance(round_id, str) and ROUND_ID.fullmatch(round_id)
                    for round_id in legacy),
                f'Invalid legacy partial round: {path}')
        baselines[version] = baseline
    return baselines


def validate_release_archive(baseline, check_checksum_file):
    """Verify a distributable against the release baseline, not against manifest.json."""
    version = baseline['version']
    target = ROOT / baseline['archive']['path']
    require(target.is_file(), f'Missing release archive: {baseline["archive"]["path"]}')
    require(digest(target) == baseline['archive']['sha256'],
            f'Release archive digest differs: {target.name}')

    expected_members = {installed_name(relative): expected
                        for relative, expected in baseline['files'].items()}
    try:
        with zipfile.ZipFile(target) as archive:
            require(archive.testzip() is None, f'Corrupt archive: {target.name}')
            names = archive.namelist()
            require(len(names) == len(set(names)), f'Duplicate archive member: {target.name}')
            require(set(names) == set(expected_members),
                    f'Wrong installable archive contents: {target.name}')
            for member, expected in expected_members.items():
                require(digest_bytes(archive.read(member)) == expected,
                        f'Stale archive member: {member}')
    except zipfile.BadZipFile as error:
        raise ValueError(f'Corrupt archive: {target.name}') from error

    if check_checksum_file:
        expected_sum = f'{baseline["archive"]["sha256"]}  {target.name}\n'
        require((ROOT / 'dist/SHA256SUMS.txt').read_text() == expected_sum, 'Checksum differs')


def validate_provenance_file(relative, expected, label):
    require(isinstance(relative, str) and relative.startswith('experiments/'),
            f'{label} must be archived under experiments/: {relative}')
    path = ROOT / relative
    require(path.is_file(), f'Missing {label}: {relative}')
    require(isinstance(expected, str) and HEX_DIGEST.fullmatch(expected),
            f'Invalid {label} digest: {relative}')
    require(digest(path) == expected, f'{label} changed: {relative}')


def validate_complete_round(record):
    """A complete round records inputs, settings, loading evidence, and review provenance."""
    round_id = record['id']
    for key in COMPLETE_ROUND_KEYS:
        require(key in record, f'Complete round is missing {key}: {round_id}')
    parse_timestamp(record['executed_at'], 'executed_at', round_id)

    inputs = record['inputs']
    require(isinstance(inputs, list) and inputs, f'Complete round has no exact inputs: {round_id}')
    input_conditions = set()
    for item in inputs:
        require(isinstance(item, dict), f'Invalid input record: {round_id}')
        condition = item.get('condition')
        require(condition in CONDITIONS, f'Invalid input condition: {round_id}')
        input_conditions.add(condition)
        require(isinstance(item.get('turn'), int) and item['turn'] >= 1,
                f'Inputs need a positive turn number: {round_id}')
        validate_provenance_file(item.get('path'), item.get('sha256'),
                                 f'input for {round_id}/{condition}')
    require(input_conditions == CONDITIONS,
            f'Exact inputs must cover both A and B: {round_id}')

    settings = record['settings']
    require(isinstance(settings, dict), f'Settings must be an object: {round_id}')
    for key in SETTINGS_KEYS:
        require(key in settings, f'Complete round is missing settings.{key}: {round_id}')
    require(isinstance(settings['model_label'], str) and settings['model_label'],
            f'Model label must be a non-empty string: {round_id}')
    require(isinstance(settings['model_snapshot_verified'], bool),
            f'model_snapshot_verified must be boolean: {round_id}')
    require(isinstance(settings['fresh_chat'], bool),
            f'fresh_chat must be boolean: {round_id}')

    loading = record['loading_evidence']
    require(isinstance(loading, dict), f'Loading evidence must be an object: {round_id}')
    require(loading.get('status') in LOADING_STATUSES,
            f'Loading status must be confirmed, not_observed, or unknown: {round_id}')
    require(isinstance(loading.get('note'), str),
            f'Loading evidence needs a note: {round_id}')
    artifacts = loading.get('artifacts')
    require(isinstance(artifacts, list), f'Loading artifacts must be a list: {round_id}')
    if loading['status'] == 'confirmed':
        require(artifacts, f'Confirmed loading needs at least one artifact: {round_id}')
    for artifact in artifacts:
        require(isinstance(artifact, dict), f'Invalid loading artifact: {round_id}')
        validate_provenance_file(artifact.get('path'), artifact.get('sha256'),
                                 f'loading artifact for {round_id}')

    reviewer = record['reviewer']
    require(isinstance(reviewer, dict), f'Reviewer provenance must be an object: {round_id}')
    for key in REVIEWER_KEYS:
        require(key in reviewer, f'Complete round is missing reviewer.{key}: {round_id}')
    require(isinstance(reviewer['name_or_role'], str) and reviewer['name_or_role'],
            f'Reviewer name or role must be non-empty: {round_id}')
    require(isinstance(reviewer['relationship_to_skill'], str)
            and reviewer['relationship_to_skill'],
            f'Reviewer relationship to the skill must be recorded: {round_id}')
    require(isinstance(reviewer['independent'], bool),
            f'Reviewer independence must be boolean: {round_id}')
    require(isinstance(reviewer['blinded_to_condition'], bool),
            f'Reviewer blinding must be boolean: {round_id}')
    require(isinstance(reviewer['reviewed_at'], str) and reviewer['reviewed_at'],
            f'Reviewer date must be recorded: {round_id}')

    require(isinstance(record['deviations'], list),
            f'Deviations must be a list: {round_id}')
    require(isinstance(record['redactions'], list),
            f'Redactions must be a list: {round_id}')


def main():
    meta, body = frontmatter(SKILL / 'SKILL.md')
    require(meta['name'] == SKILL.name, 'Skill name must match its directory')
    require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['name']), 'Invalid name')
    require(len(meta['name']) <= 64, 'Skill name is too long')
    require(isinstance(meta['description'], str) and 0 < len(meta['description']) <= 200,
            'Description must be 1–200 characters')
    require(not any(c in meta['description'] for c in '<>'), 'Invalid description')
    version = meta['metadata']['version']
    require(re.fullmatch(r'\d+\.\d+\.\d+', version), 'Invalid version')
    require('[TODO:' not in body, 'Unfinished scaffold')
    require('evals/' not in body and 'experiments/' not in body, 'Evaluation leakage')

    model = SKILL / 'references/respect-under-uncertainty.md'
    mm, model_body = frontmatter(model)
    require(mm['type'] == 'mental-model', 'Wrong reference type')
    ids = [source['id'] for source in mm['sources']]
    require(len(ids) == len(set(ids)), 'Duplicate source IDs')
    require(set(re.findall(r'\[\^([^\]]+)\]', model_body)) <= set(ids), 'Missing source IDs')
    for heading in ('When to Avoid', 'Thinking Steps', 'Coaching Questions'):
        require(f'## {heading}' in model_body, f'Missing section: {heading}')

    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text()
        require(text.count('```') % 2 == 0, f'Unclosed code block: {path}')
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
            if link.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            require(target.is_relative_to(ROOT) and target.exists(),
                    f'Broken local link: {path}: {link}')

    ET.parse(ROOT / 'assets/napsha-banner.svg')

    baselines = load_release_baselines()
    current = baselines.get(version)
    require(current is not None, f'No release baseline for skill version {version}')
    legacy_partial = {round_id for baseline in baselines.values()
                      for round_id in baseline.get('legacy_partial_rounds', [])}

    manifest = json.loads(MANIFEST.read_text())
    require(manifest.get('schema_version') == 1, 'Unsupported manifest schema')
    require(manifest['skill_version'] == version, 'Manifest version differs from the skill')

    # The working tree must match the immutable baseline, not a mutable manifest hash.
    installable = {path.relative_to(ROOT).as_posix() for path in SKILL.rglob('*')
                   if path.is_file()}
    require(installable == set(current['files']),
            'Installable skill files differ from the release baseline inventory')
    for relative, expected in current['files'].items():
        require(digest(ROOT / relative) == expected, f'Frozen skill changed: {relative}')

    frozen = manifest['frozen_skill_sha256']
    require(set(frozen) == set(current['files']),
            'Manifest frozen-file inventory differs from the release baseline')
    for relative, expected in current['files'].items():
        require(frozen[relative] == expected,
                f'Manifest hash differs from the release baseline: {relative}')

    rounds = manifest.get('rounds')
    require(isinstance(rounds, list) and rounds, 'Manifest must define experiment rounds')
    seen_rounds = set()
    expected_records = {}
    for record in rounds:
        round_id = record.get('id')
        require(isinstance(round_id, str) and ROUND_ID.fullmatch(round_id),
                f'Invalid experiment round id: {round_id}')
        require(round_id not in seen_rounds, f'Duplicate experiment round: {round_id}')
        seen_rounds.add(round_id)
        require(isinstance(record.get('status'), str) and record['status'],
                f'Round needs a status: {round_id}')

        responses = record.get('responses')
        require(isinstance(responses, list) and responses,
                f'Round has no responses: {round_id}')
        conditions = [response.get('condition') for response in responses]
        require(len(conditions) == len(set(conditions)),
                f'Duplicate condition in round: {round_id}')
        require(set(conditions) == CONDITIONS, f'Round must contain A and B: {round_id}')
        for response in responses:
            relative = response.get('path')
            require(isinstance(relative, str)
                    and relative.startswith(f'experiments/raw/{round_id}/')
                    and relative.endswith('.txt'),
                    f'Response path must be under experiments/raw/{round_id}/: {relative}')
            require(relative not in expected_records,
                    f'Duplicate response record: {relative}')
            expected = response.get('sha256')
            require(isinstance(expected, str) and HEX_DIGEST.fullmatch(expected),
                    f'Invalid response digest: {relative}')
            require((ROOT / relative).is_file(), f'Missing response record: {relative}')
            require(digest(ROOT / relative) == expected, f'Response changed: {relative}')
            expected_records[relative] = expected

        completeness = record.get('record_completeness')
        require(completeness in {'historical_partial', 'complete'},
                f'Round must declare record_completeness: {round_id}')
        if completeness == 'historical_partial':
            require(round_id in legacy_partial,
                    f'Only v0.1.0-era rounds may remain partially recorded: {round_id}')
        else:
            validate_complete_round(record)

    actual_records = {path.relative_to(ROOT).as_posix() for path in RAW.rglob('*')
                      if path.is_file()}
    require(actual_records == set(expected_records), 'Evidence inventory differs')

    pending = manifest.get('pending_tests', [])
    require(isinstance(pending, list), 'pending_tests must be a list')
    for test in pending:
        require(isinstance(test, dict) and isinstance(test.get('protocol'), str),
                'Pending test needs a protocol path')
        require((ROOT / test['protocol']).is_file(),
                f'Missing pending-test protocol: {test["protocol"]}')
        require(isinstance(test.get('status'), str) and test['status'],
                f'Pending test needs a status: {test["protocol"]}')

    # Evaluation cases and archive contents come from the release baseline, so changing
    # the prompt file or adding a member cannot silently expand either inventory.
    cases = current['evaluation']['cases']
    prompts = (ROOT / current['evaluation']['prompt_file']).read_text()
    require(re.findall(r'^## (P\d{2})', prompts, flags=re.M) == cases,
            'Evaluation case inventory differs from the release baseline')

    for release_version, baseline in baselines.items():
        validate_release_archive(baseline, check_checksum_file=release_version == version)

    print(f'PASS: YAML, links, SVG, release baseline v{version}, {len(rounds)} rounds, '
          f'{len(expected_records)} response records, {len(cases)} cases, ZIP and checksum.')
    print('Behavioral effectiveness is not established by these checks.')


if __name__ == '__main__':
    main()
