# Experiment record schema

This document defines what a publishable experiment round must contain. It applies to
rounds added after the v0.1.0 release. Rounds 01–04 were assembled before this
standard existed and are marked `historical_partial`; they are preserved as-is and are
not a precedent for new work.

Validation is enforced by [`scripts/validate.py`](../scripts/validate.py) and exercised
by [`tests/test_validation.py`](../tests/test_validation.py). A new round that is
incomplete fails CI.

## Manifest

`manifest.json` is the index of published records. Top-level fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Manifest format version. Currently `1`. |
| `assembled_on` | Date the current manifest was assembled (`YYYY-MM-DD`). |
| `skill_version` | Skill version being described. Must match `SKILL.md` and a release baseline. |
| `response_language` | Language of the archived response files. |
| `review_language` | Language of the editorial summaries. |
| `reviewer` | Summary attribution for historical reviews. |
| `reported_model_label` | Model label reported for historical rounds. Not a verified snapshot. |
| `frozen_skill_sha256` | Hash inventory that must agree with the matching release baseline. |
| `rounds` | Array of round records. |
| `pending_tests` | Prepared protocols with no responses yet. Each must point to an existing file. |

Each round has a unique `id` such as `05-belief-revision`, a `status`, two response
records (`A` and `B`), and `record_completeness`. Responses live at
`experiments/raw/<round-id>/<condition>.txt`; their SHA-256 hashes are recorded and the
files are never edited after publication. The validator also rejects any response file
under `experiments/raw/` that the manifest does not list.

`record_completeness` is one of:

- `historical_partial` — allowed only for round IDs listed in the v0.1.0 release
  baseline (`experiments/releases/v0.1.0.json`, `legacy_partial_rounds`).
- `complete` — required for every new round. All fields below must be present.

## Complete round fields

```json
{
  "id": "05-belief-revision",
  "status": "run",
  "record_completeness": "complete",
  "executed_at": "2026-11-12T09:30:00+01:00",
  "inputs": [
    {
      "condition": "A",
      "turn": 1,
      "path": "experiments/records/05-belief-revision/input-A-turn1.txt",
      "sha256": "<64 lowercase hex characters>"
    },
    {
      "condition": "B",
      "turn": 1,
      "path": "experiments/records/05-belief-revision/input-B-turn1.txt",
      "sha256": "<64 lowercase hex characters>"
    }
  ],
  "settings": {
    "model_label": "Model as displayed in the interface",
    "model_snapshot_verified": false,
    "fresh_chat": true,
    "exposed_settings": "Reasoning level, plan, or other visible settings",
    "other_skills": "Disabled, or list what remained enabled",
    "tools": "Enabled tools, or none",
    "memory_or_project_context": "Disabled, or record what could not be disabled"
  },
  "loading_evidence": {
    "status": "confirmed",
    "note": "What was observed, by whom, and how it was captured",
    "artifacts": [
      {
        "path": "experiments/records/05-belief-revision/loading.txt",
        "sha256": "<64 lowercase hex characters>"
      }
    ]
  },
  "reviewer": {
    "name_or_role": "Reviewer name or durable role label",
    "relationship_to_skill": "No role in creating the skill, or disclose the involvement",
    "independent": true,
    "blinded_to_condition": true,
    "reviewed_at": "2026-11-12"
  },
  "deviations": [],
  "redactions": [],
  "responses": [
    {
      "condition": "A",
      "path": "experiments/raw/05-belief-revision/A.txt",
      "sha256": "<64 lowercase hex characters>"
    },
    {
      "condition": "B",
      "path": "experiments/raw/05-belief-revision/B.txt",
      "sha256": "<64 lowercase hex characters>"
    }
  ]
}
```

### `executed_at`

ISO 8601 date and time with an explicit timezone. Use the start time if turns span
several minutes and note the span in `deviations` when it matters.

### `inputs`

Exact submitted text, not a reconstruction from the protocol. Archive one entry per
condition and turn. Multi-turn runs (for example the three-turn belief-revision test)
need one entry per turn in each condition. Prompt files must live under `experiments/`
and hash to the recorded value.

### `settings`

Record the environment in enough detail for someone to judge comparability:

- `model_label` — exactly what the interface displayed.
- `model_snapshot_verified` — `true` only when a backend identifier or immutable
  snapshot was independently checked; a visible label alone is not verification.
- `fresh_chat` — whether each condition started a new chat.
- `exposed_settings` — reasoning level, thinking mode, account plan, or equivalent.
- `other_skills` — whether unrelated skills were disabled in both conditions.
- `tools` — tools or integrations available to the tested assistant.
- `memory_or_project_context` — memory, projects, and context that could not be
  disabled.

### `loading_evidence`

Use `confirmed`, `not_observed`, or `unknown`. Add a `note` in every case. If
`confirmed`, at least one hashed artifact is required. A fluent mention of the skill
name is not confirmation; prefer a visible activation event, exported log, or
screenshot saved under `experiments/records/<round-id>/`. Record failed activations
too.

### `reviewer`

Record provenance rather than only a display name: the reviewer's durable name or
role, their relationship to the skill (creator, collaborator, independent reviewer),
whether they were independent of the development, whether condition labels were
hidden during grading, and the review date. When blinding was impossible, say so
instead of omitting the field.

### `deviations` and `redactions`

Both are arrays, and both may be empty. List prompt asymmetries, regenerated answers,
interrupted turns, unavailable settings, or protocol changes in `deviations`. List
removed personal data, credentials, or unrelated conversation content in `redactions`;
do not quietly alter a response file.

## Artifact layout

```text
experiments/
  manifest.json                     index of published rounds
  releases/v0.1.0.json              immutable skill and archive baseline
  protocols/                        prompts and procedures prepared before a run
  raw/<round-id>/A.txt, B.txt       verbatim published responses (never edited)
  records/<round-id>/               exact inputs and loading evidence for new rounds
```

Do not place scoring rubrics, held-out prompts, or reviewer notes in the tested chat.
Those materials belong outside the installed skill and may be summarized in the round
record rather than handed to the assistant under test.

## Validation

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate.py
```

`validate.py` checks that complete rounds have every field above, that referenced
artifacts exist and match their hashes, and that new partial rounds are rejected. It
does not judge whether the experiment was well designed or whether the skill helped;
those remain human-review questions.
