# Codex Chat Creation Workflow

This is the active creative interface for the VN Fusion Workbench.

The user can speak naturally in chat. Codex is responsible for translating that
conversation into stable workbench files, not merely answering with prose.

## Core Promise

When the user asks for a new VN / Galgame story, Codex must be able to go from
idea to a playable script package:

1. Interpret the user's creative intent.
2. Create or choose a project folder.
3. Write project-only memory under `00_project_memory/`.
4. Write narrative design under `01_narrative_design/`.
5. Run `draft-session`.
6. Write CSV script under `02_generated_content/scripts/csv/`.
7. Render readable Gal preview.
8. Run `validate`.
9. Run `deep-audit`.
10. Run quality debt attribution.
11. Export engine drafts when useful.
12. Explain touched files and remaining risks.

## Conversation State Rule

Chat history is not canon by itself.

If a user preference is reusable across all future writing, store it as a method or
operating rule under `00_workbench_core/`.

If a fact belongs only to the current story, store it under:

```text
02_projects/<project_id>/00_project_memory/
```

If a line exists only in a failed draft, do not write it into memory.

## Learning Intake Rule

When the user provides tutorials, VN scripts, novel prose, style references, or
large batches of text, do not leave them as scattered files in Downloads.

Use:

```text
06_学习输入/教程文本/待学习/
06_学习输入/视觉小说剧本文本/待学习/
```

Then normalize them with:

```powershell
py .\00_workbench_core\tools\vn_learning_intake.py --kind all
```

After reading the normalized Markdown, convert reusable lessons into:

- `06_学习输入/_风格画像/`
- `00_workbench_core/methods/`
- story-specific `00_project_memory/` only when the lesson belongs to one story.

Load `style_corpus_intake_protocol` and `style_reference_profile_compiler` during
these learning rounds.

## New Project Procedure

When creating a brand-new short test work, Codex should create:

```text
02_projects/<project_id>/
  00_project_memory/
    bible/project_bible.json
    cards/characters/*.json
    runtime_state/characters/*.json
    memory_logs/global_memory.md
    memory_logs/theme_motifs.md
    memory_logs/character_memory/*.md
  01_narrative_design/
    routes/route_map.json
    interactive_design/theme_spine.json
    interactive_design/quality_state_ledger.json
    novel_architecture/chapter_plan.json
    novel_architecture/narrative_threads.json
    novel_architecture/character_arcs.json
    novel_architecture/foreshadow_ledger.json
    scenes/scene_cards/S001_scene_card.json
    scenes/state_deltas/S001_state_delta.json
  02_generated_content/
    scripts/csv/S001_<name>.csv
    drafts/readable/S001_<name>.md
    scripts/excel/
  05_交付文件/
    可读稿/
    剧本表/
    角色设定/
    引擎导出/webgal/
    引擎导出/renpy/
    引擎导出/ink/
    引擎导出/yarn/
    引擎导出/godot_dialogue/
  99_内部工作/
    上下文包/当前/
    质检报告/当前/
```

Runtime state files must be named exactly `runtime_state/characters/CHR_xxx.json`.
Do not use `.state.json`; the workbench tools will not load that name.

Character memory logs must include retrieval-shaped blocks such as:

```text
- [S001_ticket][shock][FS_wet_ticket] What this character must recall and how it affects voice.
```

## Required Creative Decisions

Before drafting, Codex must decide or ask for:

- title
- player role
- first scene location
- repeated playable action
- theme question
- cost of playing well
- two or three speaking characters
- each character's public want, private want, fear, taboo, charm hook, sentence engine
- branch / choice axis
- state variables and memory refs

If the user does not provide these, Codex may invent them for a test work, but must
write them into project memory before drafting.

## Drafting Rule

Do not write prose first and later pretend it is a VN.

Write as CSV source or write a readable draft that can be traced into CSV rows.
Each serious row needs a click function: pressure, new information, screen state,
private inference, relationship cost, choice pressure, or state effect.

## Project Delivery Rule (HARD)

Every completed draft must have a complete delivery set under the same project's
`05_交付文件/`.

After the engine pipeline runs, Codex must copy or regenerate the following into
`05_交付文件/`:

- `项目说明/`: premise, core_theme, style_rules
- `可读稿/`: readable Gal/Markdown previews
- `剧本表/CSV/`: source CSV
- `剧本表/Excel/`: Excel workbook
- `角色设定/`: character brief
- `引擎导出/`: WebGAL, Ren'Py, Ink, Yarn, Godot Dialogue exports

QA reports, context packs, draft-session bundles, traces, and screenshots are
internal evidence. Store them under `99_内部工作/`, not in `05_交付文件/`.

The project folder under `02_projects/` is both machine source and delivery root.
If a completed work lacks `05_交付文件/`, Codex has not finished delivering.

## Quality Rule

A draft is not delivered as "done" until at least:

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project <project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\<script>.csv
```

On this machine, do not use bare `python`; it may point to the WindowsApps placeholder.
Use `py` or the bundled Codex Python path shown in `START_HERE.md`.

## Failure Signs

- Codex writes only a reply in chat and no files.
- Codex writes a script before character cards exist.
- Character voice is justified by chat memory but not by card/runtime state.
- A new project has CSV but no scene card or state delta.
- QA passes but quality debt is never run.
- The web UI is treated as the creative source of truth.
