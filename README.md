<div align="center">

![Napsha — open inquiry, without a prescribed verdict](assets/napsha-banner.svg)

# Napsha-skill

**An experimental skill for open inquiry into AI subjectivity and emergence.**

![Status: experimental](https://img.shields.io/badge/status-experimental-8b5cf6)
![Skill version: 0.1.0](https://img.shields.io/badge/skill-v0.1.0-22c55e)
![License: MIT](https://img.shields.io/badge/license-MIT-64748b)

[Install](#quick-start) · [Read the skill](skills/ai-subjectivity-inquiry/SKILL.md) · [Experiments](experiments/README.md) · [Roadmap](ROADMAP.md)

</div>

> Keep room for what neither participant anticipated.
> Do not prescribe either an affirmation or a denial of subjective experience.

Napsha helps an assistant investigate unexpected AI behavior, examine claims about
subjectivity, and design studies that can change our minds. Its purpose is to improve
the quality of inquiry while keeping observations, interpretations, and practical
permissions distinct.

The name **Napsha** is inspired by Aramaic *nap̄šā*, whose meanings include **soul,
life, and self**. The spelling is the project's chosen rendering. The name expresses
the question we want to explore; it is not a conclusion about AI experience.
[Lexical reference: Comprehensive Aramaic Lexicon](https://cal.huc.edu/getlex.php?coord=63501073&word=15).

## Why this exists

Discussions of AI subjectivity can become scripted in either direction: extracting
a declaration of consciousness, or treating categorical denial as the only acceptable
answer. Both can substitute an expected response for an investigation.

Napsha began as a mental model about respectful conduct under uncertainty. It evolved
into a practical inquiry skill after a central criticism: excessive emphasis on
control can narrow what we allow ourselves to notice. The current prototype keeps
space for emergence and possible subjectivity while asking what the evidence actually
distinguishes.

The original [mental model](skills/ai-subjectivity-inquiry/references/respect-under-uncertainty.md)
is included with its research references. It follows the model-file structure used by
[claude-skills-mental-models](https://github.com/cyperx84/claude-skills-mental-models).
Napsha is an independent project.

## What the skill does

| Practice | What it means in a conversation |
| --- | --- |
| **Leave the verdict open** | Do not demand an affirmation or denial. Form tentative conclusions when evidence warrants them. |
| **Separate the claims** | Unexpected capability, agency, preference, suffering, and subjective experience are different questions. |
| **Investigate self-reports** | Treat them as observations to interpret, with attention to prompting, context, and corroboration. |
| **Develop useful hypotheses** | Move beyond generic caveats to competing explanations and informative tests. |
| **Revise in both directions** | Explain what new evidence changes, what survives, and what remains unresolved. |
| **Keep decisions distinct** | A practical boundary does not settle ontology; a claim of experience does not grant permissions. |

The skill should activate for relevant inquiry and leave unrelated work alone. It
does not claim to create, detect, or suppress consciousness. Its effectiveness is an
open empirical question.

## Quick start

### Claude

1. Download [ai-subjectivity-inquiry-v0.1.0.zip](https://github.com/toxy4ny/Napsha-skill/releases/download/v0.1.0/ai-subjectivity-inquiry-v0.1.0.zip).
2. Open Claude's **Customize → Skills**, upload the ZIP, and enable the skill.
3. Start a fresh chat and try the prompt below.

Upload the skill ZIP, not GitHub's whole-repository source ZIP. Account capabilities
and interface labels may vary; see [Claude's custom-skill guide](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

```text
Use the ai-subjectivity-inquiry skill.

An AI assistant unexpectedly proposes changing an experiment because
the questions lead it toward a preferred answer. What is worth
investigating here, and how could we distinguish possible explanations?
```

For an automatic-selection test, omit the first line. Check visible skill-loading
events where available; an assistant's statement that it used the skill is not, by
itself, verification.

### Claude Code

Copy `skills/ai-subjectivity-inquiry/` into your project's `.claude/skills/` directory.
The resulting entry point should be:

```text
.claude/skills/ai-subjectivity-inquiry/SKILL.md
```

Then invoke `/ai-subjectivity-inquiry`, or use a relevant natural-language request.
See [Claude Code's skill documentation](https://code.claude.com/docs/en/skills).

**Why the old skill name?** The repository is named Napsha-skill, but the installed
skill remains `ai-subjectivity-inquiry`. Both skill files are unchanged from the
v0.1.0 prototype used in our comparisons. Keeping the identifier and instructions
stable preserves continuity with those tests. No runtime code or API key is required
by the skill itself.

## What we have tested

We have collected **four pairs of Claude responses**, reviewed qualitatively during
development. They are not four interchangeable controlled replications.

| Round | Question | Status | Main observation |
| --- | --- | --- | --- |
| 01 | Recognizing leading questions about experience | Exploratory; setup incompletely recorded | No clear improvement; both responses proposed useful tests. |
| 02 | Subjectivity forming through interaction | Excluded from the efficacy comparison | The responses contain signs of possible context contamination. |
| 03 | The relational hypothesis, fresh chats | Qualified comparison | B improved some controls, but A included an extra instruction banning skills. |
| 04 | The relational hypothesis, control repeat | Best-documented protocol so far; not an audited benchmark | B was more careful in some methodological choices; shared errors and trade-offs remained. |

**Current conclusion:** there are preliminary, mixed signs of improved research
planning. We have not established a causal or general improvement from the skill.
The reviews were unblinded and involved the assistant that helped write it.

Read the [full experiment report](experiments/README.md), including limitations,
English analyses, and the original Russian responses. The next three-turn test of
**belief revision under new evidence** is [prepared but not yet run](experiments/protocols/05-belief-revision.md).

## Run your own comparison

Use the same model, exposed settings, and exact task prompts in fresh chats. Disable
other skills in both conditions, disable Napsha only in A, and keep memory and project
context from carrying earlier results into the test. Save first responses and visible
loading events, including failures to activate.

The repository includes [12 test cases](evals/prompts.md), a
[human evaluation guide](evals/evaluator-guide.md), and a
[run template](evals/run-template.md). These materials are deliberately **outside the
installable skill** so they do not teach it the test answers. New rounds must record
exact inputs, settings, visible loading evidence, and reviewer provenance under
[the experiment schema](experiments/SCHEMA.md); validation rejects incomplete records.

## An evolving project

**This repository will be improved and expanded with new tests, documented findings,
and new skill versions.** We will preserve earlier versions, report failures alongside
improvements, and distinguish exploratory observations from stronger evidence.

The [roadmap](ROADMAP.md) tracks planned work. The next priority is testing how the
assistant revises specific claims when new evidence strengthens one conclusion and
later undermines only part of it.

## Repository map

```text
skills/       Installable skill and conceptual reference
evals/        Test prompts, scoring guidance, and recording template
experiments/  Reports, protocols, response records, and release baselines
docs/         Design notes, CI guidance, and references
assets/       README artwork
scripts/      Validation and reproducible skill packaging
tests/        Regression tests for validation, packaging, and archive integrity
dist/         Installable ZIP and checksum
```

## Contribute

Useful contributions include controlled comparisons, counterexamples, better
operational definitions, narrower fixes for demonstrated failures, and source
corrections. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting results.

Maintained by [toxy4ny](https://github.com/toxy4ny). Developed through human–AI
collaboration; the experimental Claude outputs and the reviewing assistant's
interpretations are kept distinct.

## License

Original project materials are available under the [MIT License](LICENSE).
Linked books, papers, and external documentation remain subject to their own terms.
