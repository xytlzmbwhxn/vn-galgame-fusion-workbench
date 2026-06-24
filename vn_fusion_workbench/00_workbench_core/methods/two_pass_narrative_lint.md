---
id: two_pass_narrative_lint
type: method_card
---

# Two-Pass Narrative Lint

## Call This When

Before trusting a serious draft, expanding a route, handing a project to another AI, or claiming that character voice/state is fixed.

## Borrowed Structure

- Yarn Spinner: analyze authored dialogue as nodes, blocks, options, and destinations.
- ink: parse author-facing flow first, then resolve references into runtime objects in a later pass.
- Ren'Py: lint labels, menus, jumps, show/say boundaries, and unresolved script references before runtime.
- TwineJS: treat passage id, passage text, tags, story metadata, and story format as separate searchable fields.
- Character-memory projects: keep stable card, runtime state, and retrievable episodic memory separate.

## Rule

Do not judge a visual novel script only by reading prose. Run at least two passes:

1. Authoring pass: inspect textbox rhythm, dialogue energy, Gal display, and scene readability.
2. Structural pass: parse the script as a graph, resolve refs, compare state effects, and check character-control layers.

## Deep Audit Checks

The workbench command is:

```powershell
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
```

It checks:

- labels, choice targets, jumps, and branch graph
- memory refs against known project ids, objects, threads, arcs, and foreshadow ids
- choice effects against state-delta choices
- stable character card, runtime state, memory log, and retrieval-shaped memory block
- sentence kernel, line energy, and social texture profile presence

## Character-Control Minimum

Each speaking character should have:

- stable character card
- runtime state JSON
- character memory log
- at least one retrieval-shaped memory block beginning with `- [tags]`
- `sentence_kernel_profile`
- `line_energy_profile`
- `social_texture_profile`

## State Minimum

Each choice must have:

- visible option text
- target label
- effects in CSV
- matching state-delta entry
- delayed callback or memory ref

## Failure Signs

- QA passes but state delta and CSV effects disagree.
- A character speaks but has no retrievable memory block.
- A branch reconverges without carrying any changed variable, object, or memory ref.
- A line cites a thread/object/arc id that no local file defines.
- Character voice depends on chat context instead of card, state, and memory.
