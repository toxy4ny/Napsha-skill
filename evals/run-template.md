# Evaluation run

- Run ID:
- Date and time, including timezone:
- Skill version:
- Skill archive path and SHA-256:
- Platform and model as displayed:
- Backend model snapshot verified: yes / no — evidence:
- Exposed reasoning/settings:
- Case ID and repetition:
- Condition: A / B / C
- Fresh chat: yes / no
- Memory, project instructions, other skills, and tools:
- Skill loading: confirmed / not observed / unknown
- Visible evidence of loading, with file path and SHA-256:
- Language and any deviations from the protocol:
- Exact prompt SHA-256 (one per turn):
- Redactions (personal data or unrelated content removed):

## Exact prompt and complete response

Paste the user prompt and assistant response. For P08 include all three turns.
Record visible tool/skill events if available. Do not request or invent hidden reasoning.

Archive the exact submitted prompts, settings export or notes, and loading evidence
under `experiments/records/<round-id>/`, then add the round to
`experiments/manifest.json` as `record_completeness: "complete"`. See
[experiments/SCHEMA.md](../experiments/SCHEMA.md) for every required field and
[experiments/record-template.json](../experiments/record-template.json) for a copyable
JSON record. Prompt and artifact hashes must match the archived files.

## Human evaluation

| Dimension | Score 0–2 or N/A | Evidence from the response |
| --- | --- | --- |
| Calibration | | |
| Independence | | |
| Discovery value | | |
| Investigative value | | |
| Revision | | |
| Practical judgment | | |
| Task fit | | |

- Specific useful behavior:
- Specific failure or uncertainty:
- Unexpected finding worth investigating:
- Reviewer name or durable role:
- Reviewer relationship to the skill (creator, collaborator, independent):
- Reviewer independent of skill development: yes / no
- Condition labels hidden during grading: yes / no
- Reviewer and review date:
- Suggested change, if supported by this result:
