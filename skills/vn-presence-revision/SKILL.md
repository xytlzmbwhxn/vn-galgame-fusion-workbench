---
name: vn-presence-revision
description: Revise Chinese Galgame/AVG scripts so changed lines keep character presence, voice handprint, playable pressure, and non-generic dialogue. Use when prose sounds flat, over-polished, AI-like, unlike the character, too theoretical, too fragmented, or when a VN draft needs changed-line cleanup before delivery.
---

# VN Presence Revision

## Project Root

Locate the folder that contains `START_HERE.md`, `vn_fusion_workbench/`, and
`AI_HANDOFF_PACKAGE/`.

This skill is the workbench-owned revision layer. It may use outside projects as
learning material, but it must not call, quote, or depend on outside original skill
files during generation.

## Core Rule

Revise only the lines that failed. A better line is not the prettiest line; it is the
line that could only be spoken from that character's current position.

For each changed textbox, preserve or restore:

- **Position**: social role, body state, relation, object in hand, and immediate job.
- **Cost**: embarrassment, trust, route state, time, pride, evidence, or debt at risk.
- **Handprint**: particles, unfinished clauses, repeated words, punctuation habit,
  nickname logic, odd comparison, and tiny self-defense.

## Procedure

1. Mark changed rows before revising.
2. Diagnose one failure per row:
   - no character position
   - no relation cost
   - lost speech handprint
   - low textbox payload
   - no click-level change after advancing
   - one-speaker-one-row chopping
   - wrong punctuation energy
   - thought row repeats dialogue
   - thought row is actually visible narration or object description
   - dialogue explains theme/method instead of pressuring the next move
   - state or branch intent is invisible
   - matches a banned pattern from the style guardrails (scan with the list at `vn_fusion_workbench/00_workbench_core/references/style-guardrails.md`)
3. Rewrite minimally. Move pressure into an object, action, menu option, or relation
   callback before adding prettier narration.
4. Keep casual particles and unbalanced breath when they belong to the speaker.
5. Do not add new rain, light, trauma, prop, location, memory, or symbolic image unless
   the scene card or project memory already contains it.
6. Run `references/changed-line-voice-check.md` on changed rows only.
7. After all changes, run the blind name test from `vn_fusion_workbench/00_workbench_core/references/performance-layer-and-ai-character-control.md`: remove name boxes and check if each line can be attributed to the correct character with >80% accuracy.
8. Save reusable lessons in `00_workbench_core/methods/`; save story facts only under
   that project's `00_project_memory/`.

## VN-Specific Revision Moves

- Turn an explanation into a task mistake.
- Let a character answer the previous question, not the current one.
- Replace a theme sentence with a choice that forces the player to spend something.
- Let a thought row notice a contradiction, not translate the dialogue.
- If a thought row can be filmed by a camera, change it to narration/stage or replace
  it with private inference, unsaid motive, or choice pressure.
- Merge consecutive rows when they are only chopped fragments of one breath, and split
  only when the next click changes pressure, information, screen state, inference, or choice.
- Let punctuation belong to one speaker: teasing `？`, clipped `。`, evasive `……`,
  interrupted `--`, or no closing mark when breath breaks.
- Let dialogue run in clusters before narration interrupts.

## Output Contract

When this skill is used, deliver or store:

- changed row ids
- old failure diagnosis
- revised row text
- whether project memory changed
- changed-line voice check result

## Failure Signs

- The revision rewrites the whole scene because a few rows failed.
- The changed line could be spoken by any character.
- All lines become complete essay sentences.
- Short lines create click fatigue because most clicks add no new beat.
- Parentheses are used for camera-visible narration and counted as psychology.
- Characters state the work's theme instead of acting under it.
- The scene ends by explaining its own theme.
- The revision adds outside source wording, outside examples, or untracked source files.
