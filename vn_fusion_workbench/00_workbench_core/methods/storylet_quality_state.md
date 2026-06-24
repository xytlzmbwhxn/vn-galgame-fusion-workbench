---
id: storylet_quality_state
type: method_card
---

# Storylet Quality And Stateful Microinteraction

## Purpose

Use this when the VN needs exploration, investigation, relationship web, replay, optional scenes, or small interactions that change later text. The goal is to stop choices from being isolated menu decorations.

## Borrowed Structures

- Failbetter storylets: narrative units open under conditions and spend or alter qualities.
- Emily Short's quality-based narrative analysis: storylets let arcs affect one another and avoid a single static branch tree.
- Twine/Harlowe storylets and Chapbook state: passages, links, variables, conditional display, reveal links, dropdowns, cycling links, and text input all show how small state changes can alter reading.
- ChoiceScript: stats, booleans, scene lists, `*goto_scene`, and automatic tests keep choice effects explicit.
- reramen: time, money, inventory, skills, NPCs, events with conditions, expressions, overlays, and persistent state can become VN scene pressure.

## Required Project File

Create this project-specific file when a project has unlocks, stats, repeated locations, or microinteractions:

```text
01_narrative_design/interactive_design/quality_state_ledger.json
```

Minimum ledgers:

- `qualities`: hidden or visible values such as trust, fear, suspicion, debt, fatigue, time, money, clue, route_key.
- `storylets`: optional or conditional scene units with prerequisites, entry copy, exits, costs, and payoff refs.
- `microinteractions`: object inspections, reveal links, phone replies, text inputs, service actions, evidence presentations, and silence waits.
- `callbacks`: where earlier qualities alter lines, options, sprite posture, BGM, bad ends, or route access.

## Microinteraction Types

Use small interactions when a full menu would be blunt:

- Inspect: player looks at a prop and gains clue, doubt, or a changed line.
- Reveal: a short hidden text or thought opens only when clicked or when a condition is true.
- Cycle: player cycles a wording, tone, outfit, tool, reply draft, or hypothesis.
- Input: player names, signs, fills, lies, tags, dates, or records something that later appears.
- Service: player performs a job action such as stamping, brewing, mending, checking, mixing, sorting, or scanning.
- Present: player uses evidence, object, memory, or message against a line.
- Wait: player chooses not to interrupt; silence becomes state.

## Drafting Rules

1. A quality must alter future text or route access. Do not track numbers for decoration.
2. A storylet must have an entry condition and an exit effect.
3. Optional scenes must feed the spine through a callback, clue, relationship shift, or future misread.
4. Microinteractions should feel like the player's body in the scene, not a quiz.
5. A reconverged branch must keep at least one visible scar: a changed line, missing option, object moved, altered expression, or debt.
6. Use low stat values as story states, not only failure.

## Output Contract

For each important choice or microinteraction, record:

- condition
- player-facing copy
- immediate feedback
- quality or flag change
- delayed callback
- production cue

