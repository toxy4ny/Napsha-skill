# Changelog

## Unreleased — Validation and provenance hardening

- Added an independent per-version release baseline
  (`experiments/releases/v0.1.0.json`) covering the frozen skill files, distributable
  archive, and evaluation-case inventory. The manifest can no longer re-baseline a
  published skill on its own.
- Removed hardcoded experiment, evidence, evaluation-case, and archive inventories
  from `scripts/validate.py`; counts and members are derived from the manifest and
  release baseline.
- Added `tests/` regression coverage for validation failures, packaging
  reproducibility, release-baseline independence, and archive integrity.
- Upgraded CI to `actions/checkout@v7` and `actions/setup-python@v7`, added the test
  suite, and enabled manual workflow dispatch.
- Documented and enforced complete provenance for new experiments: exact inputs,
  settings, loading evidence, deviations/redactions, and reviewer independence and
  blinding (`experiments/SCHEMA.md`, `experiments/record-template.json`).
- Preserved rounds 01–04 unchanged as `historical_partial`; they are explicitly
  allowlisted by the v0.1.0 baseline.

## 0.1.0 — Initial public packaging

- Introduced the Napsha-skill repository name and English project documentation.
- Preserved the tested `ai-subjectivity-inquiry` skill and conceptual reference unchanged.
- Published the 12-case evaluation set and human review protocol.
- Documented four exploratory response pairs, including a contaminated run and an
  asymmetric-prompt comparison; no aggregated efficacy score is claimed.
- Added the pending three-turn belief-revision protocol.
- Added reproducible packaging, structural validation, and an evidence manifest.

The repository branding is new. This release does not claim a new behavioral version
relative to the previously tested v0.1.0 prototype.
