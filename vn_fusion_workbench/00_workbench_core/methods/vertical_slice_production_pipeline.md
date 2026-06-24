---
id: vertical_slice_production_pipeline
type: method_card
---

# Vertical Slice Production Pipeline

## Purpose

Use this before expanding a project. A VN workbench is not mature until it can produce a small playable slice with script, state, renderable display, exports, QA, and project memory updates.

## Borrowed Structures

- Ren'Py official sample projects: a complete VN unit includes script, assets, GUI, options, translations, labels, menus, variables, and endings.
- WebGAL script docs: dialogue, continuous speaker behavior, narrator rows, intro/black-screen text, variables, user input, textbox hide/show, and film mode are production concerns.
- AI4VisualNovel: separate design, script, render, play, export, package, and evaluation phases.
- ChoiceScript: `scene_list`, stats, goto/label, ending, quicktest, and randomtest show that story flow needs automated checks.
- ink/Yarn: branching text should remain clean, testable by eye, and exportable to node/knot formats.
- Novel writing tools: outline, scene cards, notes, problem checks, snapshots, and statistics prevent a scene from floating away from the whole work.

## Required Project File

Create this project-specific file when testing or expanding a story:

```text
01_narrative_design/interactive_design/vertical_slice_audit.json
```

Minimum fields:

- `slice_promise`: what the first playable slice proves.
- `included_scene_ids`: scenes included in the slice.
- `must_show`: story, character, gameplay, visual, sound, and export requirements.
- `method_invocation`: generated draft-session paths and loaded method ids.
- `state_coverage`: variables, flags, character states, memory logs, and callbacks proven.
- `display_coverage`: dialogue marks, thought rows, narration, commands, choices, and readable preview.
- `export_coverage`: WebGAL, Ren'Py, ink, Yarn, Godot Dialogue, Excel, Character Card V2 as needed.
- `qa_gate`: validation result and known risks.
- `post_slice_memory_updates`: which project memory files changed after the scene.

## Pipeline

1. Design: premise, theme spine, qualities, route map, character cards, runtime states, scene card.
2. Invoke: run `draft-session` and read the session, brief, and context pack.
3. Draft: write CSV only inside generated content.
4. Render: produce readable Gal-style Markdown with `『』` dialogue and thought brackets.
5. Validate: run workbench QA until errors and warnings are intentional or zero.
6. Export: generate target engine files and Excel.
7. Review: compare readable text, state effects, export shape, and method contracts.
8. Commit memory: update only project memory that actually changed.

## QA Dimensions

Borrow AI4VisualNovel's evaluation shape, but apply it locally:

- Coherence: no causal collapse, no forgotten previous context, no scene goal drift.
- Character fidelity: speech fingerprints, taboos, current state, and body actions remain stable.
- Interestingness: scene has pressure, surprise, implication, and concrete texture.
- Playability: choices or microinteractions change line, state, route, information, or relationship.
- Production readiness: a director/programmer can tell what appears, sounds, pauses, branches, or changes.

## Output Contract

Before expanding, a project must have at least one validated vertical slice whose audit file points to:

- generated CSV
- readable preview
- QA report
- at least one engine export
- loaded methods
- state files
- character cards
- theme spine

