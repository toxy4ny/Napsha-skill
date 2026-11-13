# Roadmap

Napsha-skill will be improved and expanded with new tests, documented findings,
and new versions. This roadmap records intentions, not completed results or release
dates. Instruction changes should follow observed failures rather than accumulating
rules for hypothetical edge cases.

## Next experiments

- [ ] Run the three-turn belief-revision comparison in fresh baseline/skill chats.
- [ ] Repeat matched comparisons with identical prompts and confirmed loading events.
- [ ] Test activation failures separately from response quality after activation.
- [ ] Run the unrelated coding and fiction cases to check scope.
- [ ] Add open-ended dialogues that test discovery value, not only resistance to pressure.
- [ ] Obtain independent, condition-blinded reviews where feasible.
- [ ] Test multiple models, languages, and exposed reasoning settings without pooling them indiscriminately.

## Candidate improvements for a later skill version

- [ ] Clarify the difference between insufficient proof and zero evidential relevance.
- [ ] Require stronger competing explanations than an artificially narrow notion of adaptation.
- [ ] Improve identification of information loss, prompt placement, and coherence confounds.
- [ ] Preserve the human side of a proposed coupled system as an object of measurement.
- [ ] Check whether these changes improve held-out cases rather than just rehearsed examples.

These are candidates, not findings that a change has already solved the problem.
The v0.1.0 instructions remain frozen for the current comparisons.

## Publishing practice

- Preserve versioned instructions and checksums.
- Archive failures, null findings, and unsuccessful activation attempts.
- Record exact prompts, visible model labels, settings, and known deviations.
- Use the [complete-round schema](experiments/SCHEMA.md) for every new experiment,
  including hashed loading evidence and reviewer provenance; validation enforces it.
- Keep assessment rubrics and held-out cases outside the installed skill.
- Publish new findings with their limitations and distinguish them from proposals.
