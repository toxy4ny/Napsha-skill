# Continuous integration

The repository publishes one workflow, [Validate skill and records](../.github/workflows/validate.yml).
It runs on every push and pull request, and can be started manually with
`workflow_dispatch`.

## What it checks

1. `python -m pytest -q` — regression tests for validation, release-baseline
   independence, reproducible packaging, and archive integrity.
2. `python scripts/validate.py` — structure, links, frozen skill files, release
   baseline, evidence hashes, complete-round provenance, evaluation inventory, ZIP
   contents, and checksum.
3. `python scripts/package.py` followed by validation again and
   `git diff --exit-code -- dist/` — proves the committed archive is reproducible and
   not stale.

The job is named `validate`. A successful run creates a check run with that exact
name, so it can be required on `main`.

## Require the check on `main`

A repository administrator can enable the requirement in **Settings → Rules → Rulesets**
(or **Settings → Branches** for classic protection):

- target the `main` branch;
- require the status check `validate`;
- optionally require branches to be up to date before merging.

The equivalent API call, using a token with repository administration permission:

```bash
gh api -X POST repos/OWNER/REPO/rulesets --input - <<'JSON'
{
  "name": "Require validation on main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
  "rules": [
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [{"context": "validate"}]
      }
    }
  ]
}
JSON
```

For classic branch protection, `PUT /repos/OWNER/REPO/branches/main/protection` with
`required_status_checks.contexts` set to `["validate"]` has the same effect. Only a
token with administration permission can make either change; the repository's default
CI token cannot, by design.

## Run the workflow manually

```bash
gh workflow run validate.yml --ref main
gh run list --workflow validate.yml --limit 5
gh run watch <run-id> --exit-status
```

To diagnose a failure locally, run the same sequence from
[CONTRIBUTING.md](../CONTRIBUTING.md#validate-and-package).
