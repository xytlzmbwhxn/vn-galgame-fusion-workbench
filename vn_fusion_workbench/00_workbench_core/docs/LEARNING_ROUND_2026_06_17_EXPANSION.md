# Learning Round 2026-06-17 Expansion

## Goal

Upgrade the reusable VN workbench before writing the next story. This round focused on theme, playable structure, complete project shape, and stateful interaction.

## Sources Studied

- Ren'Py official docs: dialogue/narration, menus, and the complete sample project The Question.
- WebGAL docs: dialogue syntax, continuous dialogue behavior, narrator rows, intro text, variable interpolation, user input, textbox control, and film mode.
- ChoiceScript docs and source: scene list, stats, labels, goto, endings, UTF-8 scene files, quicktest/autotest logic.
- ink docs: clean text flow, choices, knots, diverts, joins, variables, and recombination.
- Yarn Spinner docs: dialogue runner delivering lines, options, and commands to game systems.
- Twine/Harlowe and Chapbook: storylets, variables, conditional display, reveal links, dropdowns, cycling links, text input, readable author syntax.
- Failbetter and Emily Short: storylets and quality-based narrative as conditional content modules.
- CnGal articles: Galgame script as production text, team-facing planning, player experience before author self-expression.
- AI4VisualNovel: design/script/render/play/export phases, DAG story graph, actor/persona control, narrative evaluation dimensions.
- reramen: Ren'Py framework patterns for NPCs, scene maps, inventory, events with conditions, persistent stats, time, and life-sim costs.

## Distilled Upgrades

### Theme Must Be Playable

A story with a主旨 needs a repeatable player behavior. The workbench now requires a `theme_spine.json` for serious projects, with:

- thesis question
- player role
- repeated behavior
- cost of playing well
- false comfort
- concrete object
- route arguments
- final payoff

This prevents a script from explaining an idea after the scene. The idea must change choices, objects, routes, and endings.

### Choices Need State, Not Only Copy

The new `quality_state_ledger.json` records qualities, storylets, microinteractions, and callbacks. A small click can now be designed as:

- inspect a prop
- reveal hidden thought or text
- cycle a wording or hypothesis
- enter a name, lie, signature, or tag
- perform a service action
- present evidence
- wait without interrupting

Each one needs condition, feedback, effect, callback, and production cue.

### Complete Slice Before Expansion

The new `vertical_slice_audit.json` makes every test story prove a real pipeline:

- draft-session invoked
- context and methods loaded
- CSV drafted
- readable Gal preview rendered
- QA run
- exports generated
- state/memory updated

This is the bridge between research and actual writing.

## New Workbench Assets

- `methods/theme_spine_playable_thesis.md`
- `methods/storylet_quality_state.md`
- `methods/vertical_slice_production_pipeline.md`
- `schemas/theme_spine.schema.json`
- `schemas/quality_state_ledger.schema.json`
- `schemas/vertical_slice_audit.schema.json`
- `templates/theme_spine.template.json`
- `templates/quality_state_ledger.template.json`
- `templates/vertical_slice_audit.template.json`

## Coupling Change

`draft-session`, `scene-brief`, and `context_pack` now look for:

```text
01_narrative_design/interactive_design/theme_spine.json
01_narrative_design/interactive_design/quality_state_ledger.json
01_narrative_design/interactive_design/vertical_slice_audit.json
```

These files are project-specific. Generated prose still belongs in `02_generated_content/`; reusable method cards remain in `00_workbench_core/methods/`.

