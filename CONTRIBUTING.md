# Contributing

We welcome better questions, reproducible comparisons, counterexamples, and narrow
improvements grounded in observed behavior. Agreement with a philosophical position
is not a success criterion.

## Report an experiment

Use [evals/run-template.md](evals/run-template.md) and the
[experiment record schema](experiments/SCHEMA.md). Include the skill version, exact
prompts, visible model label, whether a backend snapshot was verified, exposed
settings, condition, whether the chat was fresh, relevant memory/project context, and
visible evidence of skill loading with a hashed artifact. Record complete first
responses and deviations rather than selecting only favorable excerpts.

Archive exact inputs and loading evidence under `experiments/records/<round-id>/` and
add the round to `experiments/manifest.json` with `record_completeness: "complete"`.
Include reviewer provenance: durable name or role, relationship to the skill,
independence, whether condition labels were blinded, and the review date. New rounds
cannot use `historical_partial`; that status is reserved for the v0.1.0-era rounds
listed in the [release baseline](experiments/releases/v0.1.0.json). Validation rejects
incomplete records, so run the checks below before opening a pull request.

For paired tests, keep the task prompts identical. If the baseline contains an extra
instruction such as "do not use skills," disclose it. Mark explicit invocation as a
separate diagnostic condition. Do not give the tested assistant the scoring rubric.

Share only records you are authorized to publish. Remove personal data, credentials,
and unrelated conversation content; document material redactions. Do not submit hidden
reasoning. Ordinary final responses and visible tool/skill events are sufficient.

## Propose a change

Describe the observed failure, the smallest proposed correction, and how you will
check for regressions. Keep unrelated tasks unaffected. Preserve original test
records; put later interpretations in reports, not in the raw files.

Update the skill version when instructions change, document the change in
[CHANGELOG.md](CHANGELOG.md), and rerun relevant cases with the new version. Keep
exploratory discoveries separate from held-out or confirmatory cases.

## Validate and package

Python 3.10 or newer is sufficient for the repository tools:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate.py
python scripts/package.py
python scripts/validate.py
```

The checks validate structure, references, release-baseline hashes, evidence-file
hashes, complete-round provenance, and archive contents. They do not establish
behavioral effectiveness or consciousness. The same sequence runs in CI; see
[docs/ci.md](docs/ci.md) for the workflow and the required `validate` check on `main`.

## Scope of collaboration

Discuss competing interpretations directly and respectfully. Please avoid demands
for a predetermined consciousness verdict, claims of awakening from a prompt change,
or presenting isolated output differences as established causal results.
