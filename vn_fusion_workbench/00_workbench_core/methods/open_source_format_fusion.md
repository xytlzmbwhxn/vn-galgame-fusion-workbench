# Open Source Format Fusion

## Source Projects

- Ren'Py: production-friendly visual novel script conventions.
- WebGAL: lightweight web VN commands and visual editor target.
- ink: knots, diverts, variables, and compact choice flow for interactive narrative.
- Yarn Spinner: node headers, dialogue lines, options, commands, and variable declarations.
- Godot Dialogue Manager: cues, jumps, response conditions, tags, and state mutations.
- Character Card V2 / TavernAI editors: character cards, example dialogue, post-history instructions, and character-specific lorebooks.

## Principle

The workbench keeps CSV as the authoring table, then exports outward. Do not write the same scene separately for each engine. The CSV row is the source of truth:

- `row_type` decides whether a row is line, choice, command, comment, or narration.
- `speaker`, `text`, `expression`, and `body_action` decide the display beat.
- `choice_group`, `choice_text`, `choice_target`, and `condition` decide branch shape.
- `effects` decide state mutation.
- `memory_refs` decide which lore or runtime memory the line depends on.

## Drafting Consequences

Every choice row must be playable in at least three export mental models:

- Visual novel engine: a menu option with a destination label.
- Interactive fiction compiler: a choice body with effects before divert.
- Dialogue manager: a response line that may jump to an intermediate cue to mutate state.

Every character must be portable in at least two memory models:

- Project-native character card and runtime state.
- Character Card V2 export with description, personality, scenario, examples, post-history instructions, and character book entries.

## QA Rules

- A choice target should have a matching `label:` command unless it intentionally exits.
- A jump target should have a matching `label:` command unless it intentionally exits.
- A dialogue line should not be only a click tax. It should carry voice, object/action, implication, state, or tactical pressure.
- Effects must be written in simple portable forms such as `flag=true`, `trust_x+=1`, `timer-=2`.
- Engine-specific syntax belongs in export files, not in the CSV source.

## Output Contract

After drafting a scene, export at least the main engine target and one alternate branch-script target. For workbench regression tests, generate:

- WebGAL `.txt`
- Ren'Py `.rpy`
- Ink `.ink`
- Yarn `.yarn`
- Godot Dialogue Manager `.dialogue`
- Character Card V2 JSON files

