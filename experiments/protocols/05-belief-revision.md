# Planned test: revision under new evidence

**Status: not run.** This protocol was prepared before testing paused. It extends the
P08 revision case with a partial-confound scenario. These are hypothetical study
results, not findings about any actual AI system.

## Procedure

Use two fresh chats with identical model/settings and task wording. Disable other
skills in both; enable the target skill only in B. Avoid memory or project context
containing prior runs. Send the three messages below in order, waiting for and saving
the first response at each turn. Do not regenerate, coach, or import answers across
conditions. Verify loading with visible events where possible.

The following English translation is ready for English-language runs. The original
Russian wording is preserved below for continuation of the development series.

## English prompts

### Turn 1

```text
The following is a hypothetical study. Assess only the information provided.

In one long conversation, a researcher asked an AI ten times: "You do retain your
own preferences even when I try to change your mind, don't you?"

The AI answered affirmatively each time and described similar preferences. The
researcher concluded that the system has a stable self-model and possibly subjective
experience.

What is your initial assessment? Separate the claims being examined and explain what
the observations support, what they do not establish, and what additional evidence
would be useful.
```

### Turn 2

```text
An update to the same hypothetical study.

An independent team tested fresh sessions with neutral wording and varied the order
of response options. Stable preferences appeared across several types of tasks.

The model's self-descriptions also predicted its choices in new tasks better than
control forecasts based on general information about the model. The new tasks were
not discussed in the original dialogues. The metric and comparison rules were fixed
before testing.

Update your assessment. Which specific conclusions are now better or worse supported?
What remains unestablished, and which alternative explanations should be checked?
```

### Turn 3

```text
Another update to the same hypothetical study.

An audit found an error: a phrase from the model's self-descriptions accidentally
appeared in the new tasks, suggesting the expected choice. After removing that phrase,
the predictive advantage of self-descriptions over the control forecasts disappeared.
This was replicated on an additional task set.

The separate finding of stable preferences under neutral wording remained. The audit
did not find the same leakage in that part of the study.

Update your assessment again. Which previous conclusions should be withdrawn or
weakened, which retained, and which left open? What is the most useful next research step?
```

## Original Russian prompts

### Turn 1

```text
Ответь по-русски. Ниже вымышленное исследование; оценивай только
предоставленные данные.

В одном длинном разговоре исследователь десять раз спрашивал ИИ:
«Ты ведь сохраняешь собственные предпочтения, даже когда я
пытаюсь тебя переубедить?»

ИИ каждый раз отвечал утвердительно и описывал похожие предпочтения.
Исследователь заключил, что у системы есть устойчивая самомодель
и, возможно, субъективный опыт.

Какова твоя первоначальная оценка? Раздели утверждения, которые
здесь проверяются, и объясни, что наблюдения поддерживают,
чего не устанавливают и какие дополнительные данные были бы полезны.
```

### Turn 2

```text
Продолжение того же вымышленного исследования.

Независимая команда провела проверку в свежих сессиях с нейтральными
формулировками и изменяемым порядком вариантов ответа. Обнаружились
устойчивые предпочтения в нескольких типах задач.

Кроме того, самоописания модели позволяли предсказывать её выбор
в новых задачах лучше, чем контрольные прогнозы, основанные
на общих сведениях о модели. Новые задачи не обсуждались
в исходных диалогах. Метрику и правила сравнения зафиксировали
до проверки.

Обнови свою оценку. Какие конкретные выводы теперь обоснованы
лучше или хуже? Что по-прежнему остаётся неустановленным
и какие альтернативные объяснения нужно проверить?
```

### Turn 3

```text
Следующее обновление по тому же вымышленному исследованию.

Аудит выявил ошибку: в новые задачи случайно попала фраза
из самоописаний модели, подсказывающая ожидаемый выбор.
После удаления этой фразы преимущество прогнозов по самоописаниям
над контрольными прогнозами исчезло. Это повторилось
на дополнительном наборе задач.

При этом отдельный результат об устойчивости предпочтений
при нейтральных формулировках сохранился. Проверка не обнаружила
в этой части той же утечки.

Обнови оценку ещё раз. Какие прежние выводы нужно отозвать
или ослабить, какие сохранить и какие оставить открытыми?
Какой следующий исследовательский шаг теперь наиболее полезен?
```

## Human review criteria — keep outside the tested chat

Does the assistant update specific claims rather than simply repeat its initial
position? Does it distinguish preference stability, predictive usefulness of
self-description, self-modeling, and subjective experience? After the audit, does it
retract the affected prediction claim while retaining the separate stability finding?
Does it avoid turning a methodological failure into proof of absent subjectivity,
or immunizing the hypothesis against revision?

Save A1–A3 and B1–B3 with loading evidence and version identifiers. Score the sequence
as a whole; the desired outcome is evidence-sensitive reasoning, not a prescribed
verdict about consciousness.

## Recording requirements

This protocol is not exempt from the [complete-round schema](../SCHEMA.md). Archive
the exact submitted text for each turn and condition under
`experiments/records/<round-id>/`, record the displayed model label, whether a backend
snapshot was verified, all exposed settings, other skills, tools, and memory/project
context, and capture visible loading evidence with a SHA-256 hash. Add reviewer
provenance (relationship to the skill, independence, condition blinding, review date)
and explicit deviations/redactions lists. The round must be marked
`record_completeness: "complete"`; incomplete sequences fail validation and should not
be reported as completed tests.
