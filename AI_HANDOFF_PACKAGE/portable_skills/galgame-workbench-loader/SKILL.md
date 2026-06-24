---
name: galgame-workbench-loader
description: Portable startup skill for another AI receiving VN_Workbench_Project. Use to locate the active project, load methods, load portable skills, and avoid relying on this machine's Codex installation.
---

# Galgame Workbench Loader

## Use When

Use this skill first when you receive this project folder, continue a previous task,
repair a draft, generate a new VN scene, or hand the folder to another AI.

## Project Root

Search for the folder that contains `START_HERE.md`,
`vn_fusion_workbench/`, and `AI_HANDOFF_PACKAGE/`. Do not rely on host-level Codex
skills being installed.

## Required Reading Order

1. `START_HERE.md`
2. `AI_HANDOFF_PACKAGE/handoff_notes/CURRENT_TASK_STATE.md`
3. `AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md`
4. `skills/portable_skill_manifest.json`
5. `skills/vn-fusion-writer/SKILL.md`
6. `skills/vn-scene-drafting/SKILL.md`
7. `skills/vn-presence-revision/SKILL.md`
8. `skills/vn-character-memory/SKILL.md`
9. `vn_fusion_workbench/00_workbench_core/docs/METHOD_CALLING_WORKFLOW.md`
10. `vn_fusion_workbench/00_workbench_core/docs/PATH_ALIAS_PROTOCOL.md`
11. `vn_fusion_workbench/00_workbench_core/methods/method_index.json`

Do not assume host-level skills exist. Treat top-level `skills/`, workbench
`portable_skills/`, and `methods/` as the source of truth.

## Startup Procedure

1. Resolve the newest active objective before trusting stored state:
   - newest user message or attachment
   - explicit file/project path
   - unfinished objective in the current conversation
   - then `AI_HANDOFF_PACKAGE/manifests/portable_manifest.json` as fallback
2. If the newest objective conflicts with stored `active_project`, update the
   handoff state before drafting.
3. Identify `portable_root` and `active_workbench` from
   `AI_HANDOFF_PACKAGE/manifests/portable_manifest.json`.
4. Classify the newest user request:
   - learn / ingest source
   - create reusable skill or method
   - write a new scene
   - rewrite an existing scene
   - update character memory
   - export or QA artifact
5. If writing or rewriting, run or read a `draft-session` bundle before prose.
6. If learning or skill creation, write reusable output under `00_workbench_core/`.
7. If the new information is only true for one story, write it under that story's
   `00_project_memory/`.
8. Keep downloaded references under root `external_refs/` or
   `vn_fusion_workbench/01_reference_log/`.

## Minimal Commands

Run from `vn_fusion_workbench`:

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths projects
py .\00_workbench_core\tools\vn_workbench.py paths list
py .\00_workbench_core\tools\vn_workbench.py read PATH_ALIAS_PROTOCOL.md
py .\00_workbench_core\tools\vn_workbench.py read STYLE_HANDPRINT_CURRENT
py .\00_workbench_core\tools\vn_workbench.py draft-session --project P017 --scene S001_scene_card.json --draft-name S001_draft
py .\00_workbench_core\tools\vn_workbench.py validate --project P017 --script S001_draft.csv
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project P017 --script S001_draft.csv
```

Do not hand-write Chinese subpaths in inline PowerShell or Python snippets.
Prefer project keys such as `P017`, path aliases such as `LEARN_VN_DONE`, and
`vn_workbench.py read` for UTF-8 file loading.

## Output Contract

Before final delivery, state:

- which portable skills were read
- which method cards were loaded
- which project memory files were touched
- where generated content was written
- what QA or JSON validation passed

## Failure Signs

- Writing directly from chat history without loading local files.
- Saving reusable writing rules inside a one-off project.
- Updating character memory before a draft is accepted.
- Depending on a host-level Codex / CC Switch skills directory instead of bundled portable skills.
