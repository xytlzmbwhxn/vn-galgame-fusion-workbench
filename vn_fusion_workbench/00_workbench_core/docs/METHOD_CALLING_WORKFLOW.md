# Method Calling Workflow

## Purpose

This workbench now treats writing methods as callable local assets.

The method cards live in:

```text
00_workbench_core/methods/
```

The registry is:

```text
00_workbench_core/methods/method_index.json
```

Portable skills for other AI systems live in:

```text
00_workbench_core/portable_skills/
```

Those skills explain how to use the workbench without relying on host-specific Codex
skill installation. Method cards are loaded by `draft-session`; portable skills are
the human/AI operating layer.

## How Methods Are Called

Use `draft-session` before drafting a scene. It is the preferred Codex-to-workbench coupling point because it generates the method brief, context pack, machine-readable manifest, output paths, and post-draft commands in one call:

```powershell
python .\00_workbench_core\tools\vn_workbench.py draft-session --project .\02_projects\<project_id> --scene .\02_projects\<project_id>\01_narrative_design\scenes\scene_cards\S001_scene_card.json --draft-name S001_draft
```

Before serious drafting, another AI or the local web UI should first read the control-plane projection:

```powershell
python .\00_workbench_core\tools\vn_control_room.py status --project <project_id>
python .\00_workbench_core\tools\vn_control_room.py context-trace --project <project_id> --draft-name S001_draft
python .\00_workbench_core\tools\vn_control_room.py style-contract --project <project_id> --draft-name S001_draft
```

`vn_control_room.py` is the workbench control surface. It records controlled commands,
compiles method/style contracts, projects current status, and writes VN-specific
quality-debt reports. It delegates actual CSV validation, readable rendering, and
engine exports to `vn_workbench.py`.

Use `scene-brief` only when you need a standalone method brief:

```powershell
python .\00_workbench_core\tools\vn_workbench.py scene-brief --project .\02_projects\rain_gate_demo --scene .\02_projects\rain_gate_demo\01_narrative_design\scenes\scene_cards\S002_scene_card.json --out .\02_projects\rain_gate_demo\99_内部工作\上下文包\当前\S002_scene_brief.md
```

By default it loads all method cards marked `default_enabled`.

To load only selected methods:

```powershell
python .\00_workbench_core\tools\vn_workbench.py scene-brief --project .\02_projects\rain_gate_demo --scene .\02_projects\rain_gate_demo\01_narrative_design\scenes\scene_cards\S002_scene_card.json --methods scene_question_answer,subtext_want_need,voice_state_memory --out .\02_projects\rain_gate_demo\99_内部工作\上下文包\当前\S002_scene_brief.md
```

## What The Draft Session Contains

- `Sxxx_draft_session.md`: human-readable invocation contract.
- `Sxxx_draft_session.json`: machine-readable manifest for Codex or other tools.
- `Sxxx_scene_brief.md`: full method invocation brief.
- `Sxxx_context_pack.md`: project bible, scene card, character cards, runtime state, and memory.
- Exact required output locations for script CSV, readable draft, revision notes, QA report, WebGAL, Ren'Py, Ink, Yarn Spinner, Godot Dialogue Manager, Character Card V2, and Excel.
- Public-clone Excel fallback: `00_workbench_core/tools/build_excel_template_py.py`, which uses only Python standard library and does not depend on ignored `node_modules`.
- Post-draft commands to run validation and exports.
- A `deep-audit` command for graph/ref/state/character-control verification.

## Portable Skills

Before substantial writing, another AI should read:

```text
00_workbench_core/portable_skills/portable_skill_manifest.json
00_workbench_core/portable_skills/galgame-workbench-loader/SKILL.md
00_workbench_core/portable_skills/vn-scene-drafting/SKILL.md
```

For revisions that sound too polished, generic, or unlike the character, also read:

```text
00_workbench_core/portable_skills/vn-presence-revision/SKILL.md
00_workbench_core/portable_skills/vn-presence-revision/references/changed-line-voice-check.md
```

For click rhythm, thought rows, or preachy dialogue problems, the draft session must
load and obey these method cards:

```text
00_workbench_core/methods/click_unit_textbox_rhythm.md
00_workbench_core/methods/interiority_not_narration.md
00_workbench_core/methods/non_preachy_dialogue_pressure.md
```

The practical check is: a row is not "one speaker said one thing." A row is one click
beat. If the next click does not change pressure, screen state, information, inference,
choice, or relationship cost, merge/delete/reclassify that row.

For serious Chinese VN/Galgame drafting after tutorial or full-script intake, also
load the style handprint layer before writing:

```text
00_workbench_core/methods/deep_vn_corpus_application.md
00_workbench_core/methods/vn_style_handprint_fusion.md
00_workbench_core/methods/dialogue_block_ownership.md
06_学习输入/_风格画像/VN文风手印融合资产_20260623.md
06_学习输入/_风格画像/style_profile_cn_gal_tutorial_lessons_20260623.md
```

This layer is not a metric report. It must change the generated prose through
original sentence movement, emotional transitions, character-specific breath,
punctuation energy, private thought pockets, and click-level prose feel.

For dialogue-heavy scenes, the draft must also include a dialogue ownership plan:
which speaker owns the pressure, where a same-speaker run is needed, where the
interruption lands, and how the block avoids long pure A/B/A/B ping-pong.

For character setup or voice stabilization, also read:

```text
00_workbench_core/portable_skills/vn-character-memory/SKILL.md
```

## What The Brief Contains

- Invocation Trace: method id, source refs, why it was loaded, output contract.
- Scene contract: question, answer, ritual, turn, decision, theme pressure.
- Project theme and style rules.
- Playable theme spine, quality/state ledger, and vertical slice audit when present.
- Character cards and runtime character states.
- Drafting checklist generated from the method cards.
- Full method card text.

## Full Script Corpus Study

When the user asks to reference actual complete VN scripts, or when a serious new script must prove corpus-grounded pacing, use only legal corpora and the public manifest template.

Read:

```text
01_reference_log/full_script_corpus/README.md
01_reference_log/full_script_corpus/corpus_manifest.example.json
00_workbench_core/methods/full_script_corpus_study.md
```

If no legal corpus is available, do not invent corpus-specific claims. Fall back to
the public method cards and public style handprint.

The draft session should name:

- primary corpus for scene-flow shape
- secondary corpus for mechanic/state shape
- target textbox length band
- target dialogue/narration balance
- target staging cue density
- what original premise replaces the reference premise
- a note that no source prose/dialogue is copied

## Deep Narrative Audit

For serious drafts, run both ordinary QA and deep audit:

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
```

`validate` reads the script like a Gal textbox artifact. `deep-audit` reads it like an engine graph plus character-memory package.

Then run the VN quality debt pass:

```powershell
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project <project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
```

This pass separates click rhythm, thought, voice, punctuation, performance cue,
playable-theme, and state-memory debt so repair work targets the actual failure.

## Post-Generation Cleanup

After a generation/export run, clean rebuildable intermediate files:

```powershell
py .\\00_workbench_core\\tools\\vn_workspace_cleanup.py --post-generation
```

The cleanup tool protects canon and deliverables: 00_project_memory/,
01_narrative_design/, 02_generated_content/, 05_交付文件/, reusable method
cards, portable skills, templates, schemas, and learned/style assets. It removes
project-internal dependency snapshots, cache folders, and one-off internal build
workspaces.

## Why This Matters

The assistant should no longer vaguely claim it has "learned" from references.

Before writing, it must produce or read a draft session that shows:

- which methods were loaded
- which local memory files were loaded
- which fields the scene must satisfy
- which theme, quality, storylet, microinteraction, and vertical-slice files are currently present
- which later state files must be updated
- where generated prose is allowed to go
- which validation and export commands must run after drafting

That session bundle is the visible bridge between research, workbench, and script.

## User Prompt Routing

Before doing substantial work, classify the newest user request:

- learning / absorbing projects -> update source log and reusable core
- new writing -> create or read project memory, then draft-session
- rewrite / critique -> diagnose failure, update method or project memory, then generate a new draft
- continue -> resume the latest unfinished objective
- expand / long work -> update theme spine, route map, character arcs, quality state, and vertical-slice audit
- character setup -> write and show a character brief with memory points before or alongside generated script
- artifact request -> deliver the requested artifact, not a method summary

This routing is now formalized in:

```text
00_workbench_core/methods/user_prompt_response_protocol.md
```

## Active Project Resolution Gate

Before running `status`, `draft-session`, `style-contract`, or any rewrite, resolve
the current target in this order:

1. newest user message, including attached or pasted prior assistant output
2. explicitly named local file or project path
3. current unfinished objective from this conversation
4. `AI_HANDOFF_PACKAGE/manifests/portable_manifest.json`
5. `AI_HANDOFF_PACKAGE/handoff_notes/CURRENT_TASK_STATE.md`

If step 1-3 conflicts with step 4-5, update the manifest or handoff note before
drafting. Do not let an old active project resurrect an already-finished work.

## Character Briefs

When characters are new, unstable, or user-facing, render a visible character brief:

```powershell
python .\00_workbench_core\tools\vn_workbench.py character-brief --project .\02_projects\<project_id> --out .\02_projects\<project_id>\05_交付文件\角色设定\characters.md
```

The brief pulls from:

- `00_project_memory/cards/characters/*.json`
- `00_project_memory/runtime_state/characters/*.json`
- `00_project_memory/memory_logs/character_memory/*.md`

The goal is to give the user memorable anchors: first-screen impression, public/private want, taboo, social mask, memory points, voice signature, body signature, relationship hooks, arc promise, and example lines.
