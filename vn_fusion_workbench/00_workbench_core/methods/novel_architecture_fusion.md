# Novel Architecture Fusion

## Purpose

Use novel-writing project structure to stop a VN scene from becoming a loose dialogue test. Before drafting, the scene must belong to a chapter goal, a narrative strand, a character arc, and a foreshadow ledger.

## Borrowed Structures

- Manuskript: expand from one-line premise to paragraph summary to full summary. A scene should be checked against a larger promise instead of only against its local exchange.
- bibisco: keep premise, fabula, narrative strands, locations, objects, and character knowledge visible. Character believability comes from pressure, contradictions, and social context.
- Quoll Writer: treat chapters, scenes, outline items, notes, goals, and problem checks as attached objects. A note is not a mood board; it must be reachable from the scene.
- Skribisto: use project tree, synopsis, notes, tags, snapshots, and word goals. A scene needs a synopsis before prose starts, and a snapshot after revision.
- Story Architect / NovelStar: maintain outline, cards, timeline, character/location documents, scene wall, and statistics. A VN scene is still a designed unit inside a larger book/game structure.

## VN Adaptation

Each project may add:

- `01_narrative_design/novel_architecture/chapter_plan.json`
- `01_narrative_design/novel_architecture/narrative_threads.json`
- `01_narrative_design/novel_architecture/character_arcs.json`
- `01_narrative_design/novel_architecture/foreshadow_ledger.json`

Each scene card should include:

- `chapter_goal`: what this chapter is trying to break, prove, or withhold.
- `scene_synopsis`: one compact paragraph of what changes on screen.
- `pov_character`: whose restricted-view pressure controls the textbox order.
- `narrative_threads`: strand ids touched by this scene.
- `foreshadow_role`: seed, echo, mislead, reveal, or payoff.
- `prose_texture_target`: concrete texture to prevent generic tone.

Each draft row should use `memory_refs` to point to thread, arc, and foreshadow ids when the line touches them. This keeps the prose tied to long-form structure without stuffing explanation into dialogue.

## Drafting Rules

- Start from the chapter goal, then the scene question, then the character's current private pressure.
- Do not let every textbox carry the same amount of information. Let a block build: setup, pressure, deflection, leak, decision.
- A line can be quiet only if it changes leverage, reveals habit, hides a fact, or primes a later payoff.
- Use concrete objects to carry abstract meaning. Tickets, receipts, doors, signatures, photos, call logs, tools, stains, and sounds are better than named emotions.
- After drafting, update only the project memory that changed inside this scene. Reusable methods stay in `00_workbench_core/methods/`.

## QA Contract

Validation should warn when a scene has no novel architecture directory, no chapter goal, no narrative strand, no character arc reference, or no foreshadow reference. The warning is not a style opinion; it means the scene is not yet anchored inside a complete work.
