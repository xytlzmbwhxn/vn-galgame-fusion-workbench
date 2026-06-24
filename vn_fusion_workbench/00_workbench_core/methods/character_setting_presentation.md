---
id: character_setting_presentation
type: method_card
---

# Character Setting Presentation And Memory Points

## Purpose

Use this when creating, revising, or presenting characters. A character cannot be only an internal JSON card. The user sometimes needs to see the design: what to remember, what voice to expect, how the role changes, and which details should stay stable.

## Borrowed Structures

- Story Skills character files: user-readable character profile, motivations, voice, arc, timeline, relationship references.
- Character Card V2 and AI roleplay systems: description, personality, scenario, first message, example dialogue, character book.
- Dialogic character resources: display name, nicknames, portraits, custom info, color, and visual identity as production-facing metadata.
- Agnai memory books: trigger keywords, priority, insertion order, and context budget prevent all memory from being dumped at once.
- Desktop-pet / AI companion patterns: idle actions, touch reactions, time-of-day behavior, affection/fear/fatigue state, visible gestures.

## Required Character Layers

### 1. User-Visible Brief

Show this when the user asks for characters, when a new cast is created, or when a character's voice has been criticized.

Minimum fields:

- First-screen impression: what the player sees in the first 5 seconds.
- Role in the story system: why this person exists mechanically and dramatically.
- Public want / private want.
- Fear / shame / taboo.
- Social mask.
- Memory points: 3 to 7 concrete hooks the user can remember.
- Charm hook / liveliness floor: the small repeatable thing that makes this character more fun, cute, or alive than their plain role.
- Voice signature: rhythm, vocabulary, filler words, punctuation habits.
- Body signature: hands, gaze, posture, idle action, pressure action.
- Relationship hooks: what this character wants from each important other character.
- Arc promise: starting state, breaking point, projected ending.
- Example lines: relaxed, pressured, lying, intimate or soft.

### 2. Machine Character Card

Store full data in:

```text
00_project_memory/cards/characters/CHR_xxx.json
```

Must include stable identity, desire, fear, taboo topics, speech fingerprint, embodiment, emotion axes, relationships, and example dialogue.

### 3. Runtime State

Store scene-current state in:

```text
00_project_memory/runtime_state/characters/CHR_xxx.json
```

Must include current axes, active wants, active fears, unspoken truths, voice lock, relationship pressure, promises/debts, and state history.

### 4. Memory Log

Store evolving canon in:

```text
00_project_memory/memory_logs/character_memory/CHR_xxx.md
```

Only confirmed scene results go here. Do not add speculative future changes as canon.

## Memory Point Rules

Memory points should be concrete and repeatable:

- object: ticket corner, broken compass, chipped cup
- gesture: thumb on stamp box key, counting coins twice
- phrase: "先把票放平", "我就问问嘛"
- contradiction: jokes when asking for dangerous help
- relationship handle: calls someone by role until trust changes
- visual mark: red thread, wet sleeve, old school badge
- liveliness hook: gives machines nicknames, folds receipts into tiny squares, says harsh things with snack metaphors, counts coins wrong on purpose

Avoid vague labels such as "kind", "mysterious", "complex", "gentle", "traumatized" unless tied to visible behavior.

Default bias: every character gets `liveliness +1`. A grim person may be grim with a dry little joke; a quiet person may have a tiny ritual; a professional may have a fussy object preference; a villain may be charmingly polite. Do not let a role become only its social function.

## Prompt Integration

Before drafting a scene with major characters:

1. Read character card.
2. Read runtime state.
3. Read character memory log.
4. Select 2 to 4 active memory points relevant to the scene.
5. Ensure at least one line or body action in the scene uses a selected memory point.

## Output Contract

When characters are newly created or materially changed, the assistant must provide a concise user-visible character brief and store machine-readable cards. Future draft sessions should be able to render the same brief with `character-brief`.

## Failure Signs

- Character design exists only in JSON and the user cannot remember the cast.
- The same character has no stable object, gesture, phrase, or contradiction.
- The character is correct but not fun to click through; no cute, odd, lively, petty, or memorable hook exists.
- Example dialogue is missing for pressure states.
- Runtime state does not say what the character wants right now.
- The script uses a character before their taboo, mask, and voice lock are defined.
