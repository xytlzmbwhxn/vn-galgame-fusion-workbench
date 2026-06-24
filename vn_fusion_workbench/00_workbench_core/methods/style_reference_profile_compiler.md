# Style Reference Profile Compiler

Use this after learning a batch of tutorial texts or VN scripts.

Inspired by style-profile and voice-analyzer projects, but adapted for Chinese
VN/Galgame writing instead of blog posts or generic prose.

## Core Principle

Style imitation should not become a long checklist. Produce a compact profile
with examples, measurable tendencies, and revision tests.

## Profile Layers

### 1. Surface Metrics

- average sentence length
- dialogue / narration / thought / command ratio
- punctuation distribution
- casual particles and modal words
- repeated sentence endings
- line payload and click-unit density

### 2. Sentence Engine

Capture how lines are built:

- short reply plus object action
- question that pressures the listener
- apology hidden in procedure
- joke that dodges a dangerous noun
- private inference in thought row
- choice cost stated as concrete operation

### 3. VN Display Layer

Capture how prose is displayed:

- dialogue marks
- thought marks
- speaker labels
- stage commands
- branch labels
- when a line should stay open without a period
- when a multi-sentence textbox is justified

### 4. Emotional Delivery

Capture how emotion appears without naming it:

- hand action changes
- object handling changes
- address/name changes
- delayed answer
- misread or dodge
- body distance
- task failure or over-careful task execution

### 5. Anti-Drift Examples

For each profile, include:

- `Do`: 3-5 sample line shapes.
- `Do not`: 3-5 forbidden drifts.
- `Repair`: how to revise a flat line into the target style.

## Output Shape

Write profiles to:

`06_学习输入/_风格画像/style_profile_<name>.md`

Recommended sections:

```text
# Style Profile: <name>

## Corpus
## Metrics
## Sentence Engine
## Display Rules
## Dialogue Voice Lessons
## Interiority Lessons
## Click Rhythm Lessons
## Do / Do Not / Repair
## Prompt Snippet
## QA Checklist
```

## VN Adaptation Rule

Novel prose style cannot be copied directly into VN script. Convert it into:

- textbox rhythm
- line payload
- character-specific dialogue moves
- thought-row function
- scene object pressure
- choice/state consequences

