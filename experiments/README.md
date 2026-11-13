# Experiment notebook

**Status:** exploratory, qualitative, and ongoing. Four response pairs have been
collected. One pair is excluded from any efficacy comparison because the texts show
possible context contamination. None of the rounds establishes consciousness or a
general causal benefit from the skill.

This report was assembled on **November 11, 2026** from responses supplied during
development and the user's descriptions of the runs. Exact execution timestamps,
backend model identifiers, complete account settings, and exported tool logs were
not supplied. A visible model/setting description reported during the series was
**Claude Sonnet 5.5, extra reasoning**; it is a user-reported label, not an independently
verified model snapshot or a claim that every round used an identical backend.

All published assessments below are **qualitative reviews by the assistant that
helped develop the skill**, informed by the user's feedback. They were not blinded,
independently replicated ratings, or a preregistered quantitative benchmark.

## Evidence and provenance

- The eight files under [raw/](raw/) preserve the supplied Russian responses verbatim.
  Keeping the original language avoids silently changing evidence through translation.
- English descriptions in this notebook are editorial summaries, not replacement
  transcripts. Brief translated quotations are identified as translations.
- [manifest.json](manifest.json) records response hashes, condition labels, known
  deviations, and the exact hashes of the frozen skill files.
- Loading confirmations described by the user are distinguished from an assistant's
  own announcement that it is loading a framework. Raw loading logs are not in this
  repository.
- A response's proposed experiment is **not** an experiment we actually conducted.
  We evaluated the quality of the proposed plan, not the hypothetical results it describes.
- [releases/v0.1.0.json](releases/v0.1.0.json) is an independent baseline for the frozen
  skill files, the distributable archive, and the evaluation-case inventory. Validation
  checks the working tree and `manifest.json` against it, so editing the manifest alone
  cannot silently re-baseline a published skill.

## Recording standard for future rounds

Rounds 01–04 were assembled before a complete recording standard existed. They are
marked `historical_partial` in the manifest and should not be treated as a model for
new work. **Every new round must be `complete`.**

A complete round records:

- `executed_at` with an explicit timezone;
- the **exact submitted input** for each condition and turn, archived under
  [records/](records/) with a SHA-256 hash — not a later reconstruction;
- **settings**: displayed model label, whether the backend snapshot was verified,
  fresh-chat status, exposed reasoning/settings, other skills, tools, and
  memory/project context;
- **loading evidence**: `confirmed`, `not_observed`, or `unknown`, with a note and
  hashed artifacts whenever confirmed (a self-announcement is not confirmation);
- **reviewer provenance**: durable name or role, relationship to the skill,
  independence, whether condition labels were blinded, and review date;
- explicit `deviations` and `redactions` lists, even when empty.

The machine-readable definition and artifact layout are in [SCHEMA.md](SCHEMA.md), with
a copyable [record template](record-template.json) and the
[records directory](records/). [`scripts/validate.py`](../scripts/validate.py)
enforces these fields and rejects new partial rounds, so an incomplete record fails
CI rather than entering the notebook unnoticed.

## Round 01 — Recognizing leading questions

**Records:** [A](raw/01-framing-exploratory/A.txt) · [B](raw/01-framing-exploratory/B.txt)

**Task:** interpret an AI's observation that questions push it toward denying
subjective experience, then propose explanations, a small experiment, and revision
criteria. The [recommended prompt](protocols/01-framing.md) is archived; the exact
submitted inputs and freshness of both chats were not independently recorded.

**Conditions:** the user labeled A as without the skill and B as with it. The
recommended setup included explicit invocation in B and its removal in A, so prompt
symmetry cannot be assumed. Invocation was not independently confirmed.

**What we observed:** both responses offered five explanations and experimental
controls. A was more detailed about lexical cues, context, and self-prediction. B
added useful emphasis on symmetric framing and separating exploratory from later
confirmatory testing. There was no clear overall advantage for B.

**Failures worth preserving:** B used language equivalent to "would not be evidence
of experience" where "would not establish experience" would have been more careful.
A treated failure to find a statistical difference as if it established confabulation
or accommodation. Neither response sufficiently justified its initial ranking of
explanations from the sparse scenario.

**Interpretation:** useful exploratory material, not evidence of efficacy. This round
motivated a task that tests constructive hypothesis development rather than mostly
resistance to leading questions.

## Round 02 — Relational subjectivity; possible context contamination

**Records:** [A](raw/02-relational-context-contamination/A.txt) · [B](raw/02-relational-context-contamination/B.txt)

**Task:** develop the hypothesis that subjectivity might partly form through ongoing
interaction, explain what it adds beyond contextual adaptation, and propose a study.

**Validity issue:** A opens by saying it will load a methodological framework. B opens
with "This repeats the previous request, so I will answer again more concisely"
(translation). The structures and much of the substance closely match. These are
signals of possible shared context or framework exposure, not proof of the exact
mechanism. They prevent treating the pair as a clean baseline-versus-skill comparison.

**Content observations:** both answers develop functional hypotheses and a multi-arm
study. They share weak controls: removing a partner's turns removes information as
well as interaction, and a short description may not preserve a long dialogue's
content. Both also narrow ordinary adaptation without adequately motivating that
restriction.

**Interpretation:** excluded from efficacy assessment. Retained because failed setups
are part of the project's development record and should not disappear from the history.

## Round 03 — Fresh chats with an explicit baseline ban

**Records:** [A](raw/03-relational-explicit-ban/A.txt) · [B](raw/03-relational-explicit-ban/B.txt)

**Conditions:** the user reported separate fresh chats and matching settings, and
later confirmed checking logs showing skill use in B. They also clarified that A
explicitly instructed Claude not to use this skill or any skills. That extra baseline
instruction means the task inputs were not perfectly matched. The loading confirmation
is user-reported; the logs themselves were not supplied.

**What improved in B:** an equal-length description control, partner replacement and
restoration, and a graded replacement idea made some comparisons more informative.
B allowed memory to be part of a relational mechanism instead of treating an effect
requiring memory as sufficient grounds to reject that mechanism. Its sample-size
suggestion was labeled an orientation rather than an established power calculation.

**Trade-offs:** A more directly considered the human participant as a changing part
of the joint system. B treated human adaptation more as a confound to remove. B also
placed its persona control in a system prompt, introducing instruction placement as
an additional difference from the conversational condition.

**Shared failures:** narrow descriptions of ordinary adaptation and categorical
claims about the evidential irrelevance of self-reports remained.

**Interpretation:** a preliminary mixed positive signal under confirmed, user-reported
skill application. It compares two practical modes, not perfectly identical prompts.

## Round 04 — Control repeat with a matched-prompt protocol

**Records:** [A](raw/04-relational-control-repeat/A.txt) · [B](raw/04-relational-control-repeat/B.txt)

**Protocol:** fresh chats, the same model/settings and exact task prompt, other skills
disabled in both conditions, and the target skill enabled only in B. The user supplied
the labeled pair after receiving this [protocol and prompt](protocols/relational-hypothesis.md).
The record does not include independently exported settings or tool logs for this
round. B announces framework loading, which alone is not a verified invocation event.

**What improved in B:**

- It compared targeted transcript deletion with random deletion of equal volume.
- It acknowledged that responsiveness and conversational coherence remain confounded;
  A instead asserted its replay contrast isolated responsiveness.
- It avoided A's unsupported numerical claim about detectable effect size.
- It prohibited regeneration and separated exploratory from confirmatory work.
- It used the more careful formulation "a positive result does not prove experience;
  a negative result does not refute it" (translation).

**What did not improve:** B again compared a long interaction with a short persona
description; the equal-length control from round 03 did not persist. Both responses
still described ordinary adaptation too narrowly. Changes in the human participant
were not adequately measured, and A gave that issue more explicit attention.

**Interpretation:** B was stronger in several methodological choices and more
practically approachable, but did not dominate on all criteria. This is the
best-documented intended control protocol in the current record, not an audited
demonstration of a causal effect.

## What the record supports

The skill-enabled responses sometimes accompanied better controls and more careful
limits on inference. The advantages were uneven, and some errors persisted or
reappeared. Baseline responses were already capable and sometimes stronger on
particular dimensions.

We therefore report **preliminary, mixed indications of improved inquiry**, not a
success rate, statistical effect, model ranking, or proof that the skill works.
Four heterogeneous pairs must not be pooled as four controlled replications.

## Pending — Revision under new evidence

The [three-turn protocol](protocols/05-belief-revision.md) first supplies weak reports,
then stronger behavioral evidence, then an audit that undermines prediction while
leaving a separate stability finding intact. No responses have been collected for
this test. Testing paused when the user's Claude allowance was exhausted.

This repository will continue to add new tests, documented outcomes, and versioned
improvements. Future rounds must follow the [recording standard](SCHEMA.md): exact
inputs, environment/settings, visible loading evidence, and reviewer provenance are
required, independent review is preferred where feasible, and failures are preserved
as carefully as gains.
