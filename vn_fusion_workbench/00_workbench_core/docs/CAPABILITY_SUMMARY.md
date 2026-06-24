# VN Fusion Workbench Capability Summary

## Core Capability

The workbench now supports a reusable Chinese visual novel writing pipeline:

- Project memory: premise, theme, style rules, display rules, anti-AI phrase guardrails.
- Character control: character cards, speech fingerprints, example dialogue, runtime state, character memory.
- Novel architecture: chapter plans, narrative threads, character arcs, foreshadow ledgers.
- Interactive design: playable theme spine, quality/state ledger, storylets, microinteractions, vertical slice audit.
- Scene design: scene cards, operable objects, route maps, state deltas.
- Script format: spreadsheet-style CSV with `dialogue`, `thought`, `narration`, `choice`, `command`, and `comment` rows.
- Display layer: readable Markdown renders dialogue as `【角色】『台词』` and thought rows as `【角色】（心理文本）`.
- QA: branch integrity, dialogue payload, punctuation energy, casual particles, inner monologue, textbox production, scene contract, character state, and novel architecture references.
- Export: WebGAL, Ren'Py, Ink, Yarn Spinner, Godot Dialogue Manager, Character Card V2, and Excel.
- Handoff: a portable root folder with `START_HERE.md`, AI handoff notes, skills snapshots, source ledgers, and method index.
- Open-source fusion: runtime dialogue pipeline, retrievable character memory blocks, plain-text project granularity, and passage tag route mapping.
- Deep audit: graph/ref/state/character-control lint inspired by Yarn Spinner, ink, Ren'Py, TwineJS, and character-memory systems.

## Required New-Scene Workflow

1. Create or update project memory and character cards.
2. Create scene card, route map, state delta, and novel architecture files.
3. Create interactive design files when the project has a theme, qualities, storylets, or a required vertical slice.
4. Run `draft-session` to assemble the local context and method invocation trace.
5. Draft CSV rows with concrete `memory_refs`: `THR_`, `ARC_`, `FS_`, object ids, quality ids, and callback ids.
6. Use `thought` rows for playable hesitation, clue reading, and unsaid pressure.
7. Retrieve only relevant character memory blocks instead of dumping the whole memory folder into the draft.
8. Run `validate` until the report has zero errors and zero warnings.
9. Run `deep-audit` to check labels, choices, memory refs, state effects, and character-control layers.
10. Run `render-readable` to inspect Gal display rhythm.
11. Export to target engines and rebuild Excel.

## Style Guardrails

- Do not depend on balanced explanation, thesis sentences, or abstract emotion labels.
- Dialogue must survive hidden-name testing through vocabulary, sentence shape, punctuation, and dodge style.
- Environment must be operable: a tool, stain, sound, deadline, door, screen, paper, or physical position should change the scene.
- Inner monologue is not filler. It must carry clue reading, hesitation, contradiction, bodily reaction, or choice pressure.
- Choices must change information, relationship, resource, state, or route access.
- A theme must become a repeated player behavior, a cost, a concrete object, and a later payoff.
- Storylets and microinteractions must have conditions, feedback, effects, and callbacks.
- New story tests should prove a vertical slice instead of only a prose sample.

## Current Test Baseline

The last verified baseline is `last_bus_demo` draft `S001_last_bus_novel_v3`:

- 67 rows.
- 42 dialogue rows.
- 10 thought rows.
- 2 choices.
- 0 QA errors and 0 QA warnings.
- Readable preview contains Gal dialogue marks and thought brackets.

New tests should use a different premise, location, professional ritual, object system, character voices, and theme pressure so quality is not inherited from one repeatedly revised scene.

## Latest Expansion

The 2026-06-17 expansion adds:

- `theme_spine_playable_thesis`
- `storylet_quality_state`
- `vertical_slice_production_pipeline`
- `01_narrative_design/interactive_design/`
- templates and schemas for theme spine, quality ledger, and vertical slice audit

`draft-session`, `scene-brief`, and `context_pack` now surface these project files before drafting.
