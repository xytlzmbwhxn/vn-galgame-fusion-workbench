---
name: vn-scene-drafting
description: Portable skill for drafting Chinese Galgame/AVG visual novel scenes with playable choices, CSV rows, readable preview rules, character voice, state changes, and QA discipline.
---

# VN Scene Drafting

## Use When

Use this skill for a new visual novel scene, rewrite, short test work, route branch,
choice sequence, Excel/CSV script, Ren'Py/WebGAL/Ink/Yarn export source, or readable
Gal-style preview.

## Project Root

Locate the workbench root first: the folder that contains `START_HERE.md`,
`vn_fusion_workbench/`, and `AI_HANDOFF_PACKAGE/`. Then load local `draft-session`
and method files from that root.

## Required Inputs

Read these before drafting:

1. The active project's `draft-session` files in `99_内部工作/上下文包/当前/`.
2. `00_project_memory/cards/characters/*.json`
3. `00_project_memory/runtime_state/characters/*.json`
4. `00_project_memory/memory_logs/character_memory/*.md`
5. `01_narrative_design/scenes/scene_cards/*.json`
6. `01_narrative_design/routes/route_map.json`
7. `01_narrative_design/interactive_design/*.json` when present
8. Method cards listed in the draft-session invocation trace.
9. For serious Chinese VN drafting after corpus learning, load
   `deep_vn_corpus_application`, `vn_style_handprint_fusion`,
   `dialogue_block_ownership`, and `chinese_vn_generation_hard_gates`.
10. Load the newest `VN文风手印融合资产` before drafting. The draft must show
    style absorption through original sentence moves, emotional turns, character
    breath, punctuation energy, and click-level prose feel, not only by citing
    rules or metrics.
11. For dialogue-heavy scenes, write a dialogue ownership plan before drafting:
    pressure owner, same-speaker run owner, run length target, interruption point,
    narration/thought hinge, and anti-ping-pong move.
9. **Style guardrails** at `vn_fusion_workbench/00_workbench_core/references/style-guardrails.md` (or `AI_HANDOFF_PACKAGE/references/style-guardrails.md`). Must scan every new draft against the banned patterns list.
10. **Performance layer** at `vn_fusion_workbench/00_workbench_core/references/performance-layer-and-ai-character-control.md`. Apply blind-name test, object-interaction density, and environment test before final delivery.

## Drafting Rules

- Treat every row as a restricted-view textbox, not as a novel paragraph.
- Treat the row as a click unit, not a speaker unit. Do not assume one speaker equals
  one row, and do not split only because a sentence can be shorter.
- Each serious row must have an inferable `click_function`: reply pressure, new
  information, screen state, relationship cost, private inference, choice pressure,
  state effect, or breath control.
- If a click does not change what the player knows, sees, risks, hears, chooses, or
  infers, merge it, delete it, or turn it into a production cue.
- Dialogue can run in blocks. Do not alternate one dialogue, one thought, one narration
  by habit.
- Every dialogue line should do at least two jobs: pressure, charm, dodge, reveal,
  mislead, test, confess, alter state, or set up a later callback.
- Give each character a sentence engine:
  - opening habit
  - preferred clause length
  - allowed particles
  - stress punctuation
  - dodge pattern
  - what they say when cornered
- Keep narration and thought distinct:
  - narration: visible action, object, light, sound, production cue
  - thought: playable hesitation, private inference, unsaid emotional cost
- Thought rows fail if a camera could film their content. Visible action, object
  texture, light, sound, and room layout belong to narration/stage unless the row
  also contains private inference or decision pressure.
- Use `【角色】『台词』` for readable dialogue previews and `（内心文本）` for thought rows.
- Use production cues for silence, fades, sprites, SFX, BGM, CG, menu timing, and
  callbacks. Do not spend multiple empty textboxes on pure ellipsis.
- Choices must cost something: information, relationship, time, route access, or
  moral self-image.
- Track visible options and branch states separately. A menu option is what the
  player sees; a branch is a state, route, information, callback, or later text
  difference that survives the click.
- Dialogue should not explain the scene's thesis, writing rule, or moral. Convert
  preachy lines into requests, refusals, bargains, wrong answers, object operations,
  relation costs, or choice pressure.

## Scene Block Shape

A strong scene usually contains:

1. Entry image: where the player is, what object is in hand, what pressure is already moving.
2. Continuous dialogue block: characters test each other before the narration explains them.
3. Interiority pocket: the player character privately notices a contradiction or desire.
4. Work action or inspection: a concrete operation changes knowledge or state.
5. Choice at pressure peak: options are different stances, not right/wrong answers.
6. Consequence callback: a visible line, object, or state change remembers the choice.
7. Exit image: something remains on screen that has changed meaning.

## Output Contract

For CSV scripts, include or preserve:

- `row_id` or the project's click-id column such as `beat_id`; read the CSV header
  before patching rows and do not assume one fixed id field
- `label`
- `speaker`
- `row_type`
- `text`
- `stage`
- `choice_group`
- `choice_text`
- `target`
- `state_effects`
- `memory_refs`
- `qa_notes`

Use `qa_notes` to record `click_function` for important dialogue, thought, narration,
choice, or state rows when the function is not obvious.

For readable previews, render the script like a Gal scene rather than prose.

Store finished human-facing files under `05_交付文件/`. Store Ren'Py, WebGAL,
Ink, Yarn, and Godot Dialogue exports under `05_交付文件/引擎导出/`. Store QA
reports, draft-session bundles, context packs, traces, and internal screenshots
under `99_内部工作/`, not in public deliverables.

## Failure Signs

- Characters sound interchangeable once name boxes are removed.
- Lines are all short, low-payload fragments.
- Rows follow one-speaker-one-line habit without click-level change.
- Punctuation is sprinkled instead of belonging to the speaker.
- Thought rows describe visible action or decorative objects instead of private pressure.
- Dialogue explains a theme or method instead of giving the next speaker an actable problem.
- The theme is explained in narration instead of tested through play.
- The scene could be pasted into a novel without losing anything mechanical.

## 2026-06-23 Literary Depth Addendum

Before serious Chinese VN drafting or revision, also load method card literary_depth_liveliness_control when character voice feels flat, psychology feels mechanical, prose lacks spirit, or the user asks for more cute/casual human timing and philosophy-guided inner pressure. The pre-draft note must include literary pressure, scene reversal, recognition point, character self-story under threat, live hook + half step, thought-pocket chain, cute/casual timing, and branch debt.

