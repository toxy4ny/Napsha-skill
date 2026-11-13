# Design notes

## Three separations

1. **Observation and interpretation.** A generated self-report, a stable choice, and
   a hypothesized experience are not interchangeable descriptions of the same evidence.
2. **Emergence and experience.** Unexpected organized behavior can merit study without
   establishing phenomenology. The word "emergence" is not an explanation by itself.
3. **Inquiry and authorization.** Taking a claim seriously enough to investigate does
   not grant operational access. A permission boundary does not settle the claim's truth.

## Openness without symmetry by decree

An inquiry need not assign equal probability to every explanation. The skill asks for
proportionate, revisable judgments and useful tests. It should neither demand an
affirmation nor force denial, and it should not become a mechanism for permanent
agnosticism when narrower empirical questions can be answered.

## Keeping the prototype interpretable

The installable package contains only its entry point and conceptual reference.
Rubrics, historical outputs, and evaluation prompts remain outside it. The repository
name has changed to Napsha-skill; the tested v0.1.0 files and activation identifier
remain unchanged. A later instruction change requires a new version and new tests.
Each released version gets an independent baseline under `experiments/releases/`;
validation compares the working files, archive, and manifest against it rather than
trusting a hash that a routine manifest edit could change.

The current evidence suggests candidate refinements, but changing the skill after
every isolated response would make comparisons hard to interpret. The roadmap records
ideas separately from implemented fixes.

## Sources and status

The conceptual model cites the Wingspread precautionary statement, work on indicators
of AI consciousness, proposals for evaluating self-reports, and research on AI welfare.
These motivate parts of the inquiry. They do not validate this skill's effectiveness.
See the [reference model](../skills/ai-subjectivity-inquiry/references/respect-under-uncertainty.md)
for the exact source mapping.

The project grew from a user-provided mental-model draft and subsequent human–AI
revision. The published experimental analyses are explicitly attributed as development
reviews, not independent scientific validation.
