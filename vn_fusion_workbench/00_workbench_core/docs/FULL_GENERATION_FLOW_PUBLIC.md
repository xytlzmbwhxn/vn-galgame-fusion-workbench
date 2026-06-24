# Full Generation Flow

This is the public, repository-contained flow for generating or revising a VN / Galgame project. It assumes another AI only has this repository and no host-level skills.

## 1. Start from the repository

Read:

```text
START_HERE.md
项目结构总览.md
skills/portable_skill_manifest.json
skills/galgame-workbench-loader/SKILL.md
skills/vn-fusion-writer/SKILL.md
skills/vn-scene-drafting/SKILL.md
skills/vn-presence-revision/SKILL.md
skills/vn-character-memory/SKILL.md
AI_HANDOFF_PACKAGE/handoff_notes/CURRENT_TASK_STATE.md
AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md
AI_HANDOFF_PACKAGE/handoff_notes/OTHER_AI_FAILURE_PREVENTION.md
```

Then enter:

```powershell
cd <repo>\vn_fusion_workbench
```

## 2. Resolve the active project

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths projects
py .\00_workbench_core\tools\vn_workbench.py paths list
```

Use the newest user request first. Stored state is only a fallback.

## 3. Bootstrap context

```powershell
py .\00_workbench_core\tools\vn_context_bootstrap.py --project <Pxxx> --task <draft|rewrite|review>
```

The receipt must prove that mandatory portable skills and method cards loaded. Do not draft from memory alone.

## 4. Create or read a draft session

```powershell
py .\00_workbench_core\tools\vn_workbench.py draft-session --project <Pxxx> --scene S001_scene_card.json --draft-name S001_draft
```

The draft session tells the AI:

- where character cards live;
- where runtime state lives;
- where memory logs live;
- which scene card and route map apply;
- which method cards are loaded;
- where CSV, readable draft, engine exports and QA reports must be written.

## 5. Draft or revise

Use the VN row model:

- one row is one click beat;
- speaker alternation is not a structure by itself;
- narration, dialogue and thought are distinct;
- thought rows require POV discipline;
- dialogue should pressure the next move, not explain the theme;
- choices must leave state, relationship, route, object or information debt.

For Chinese VN/Galgame prose, load these method cards:

```text
00_workbench_core/methods/chinese_vn_generation_hard_gates.md
00_workbench_core/methods/vn_style_handprint_fusion.md
00_workbench_core/methods/dialogue_block_ownership.md
00_workbench_core/methods/pov_interiority_control.md
00_workbench_core/methods/spoken_private_thought_texture.md
00_workbench_core/methods/interior_breath_relaxation.md
```

## 6. Export the delivery package

At minimum, a complete project should contain:

```text
02_projects/<project>/
├─ 00_project_memory/
├─ 01_narrative_design/
├─ 02_generated_content/
├─ 05_交付文件/
│  ├─ 可读稿/
│  ├─ 剧本表_CSV/
│  ├─ 剧本表_Excel/
│  ├─ 引擎导出/
│  └─ 角色设定/
└─ 99_内部工作/质检报告/
```

Excel can be generated without Node:

```powershell
py .\00_workbench_core\tools\build_excel_template_py.py <Pxxx> <script.csv>
```

## 7. Run QA gates

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project <Pxxx> --script <script.csv>
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project <Pxxx> --script <script.csv>
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project <Pxxx> --script <script.csv>
py .\00_workbench_core\tools\vn_encoding_guard.py --project <Pxxx>
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project <Pxxx> --strict
py .\00_workbench_core\tools\vn_handoff_guard.py --target <readable.md> --strict
py .\00_workbench_core\tools\vn_skill_backup_check.py
```

Warnings are not decorative. Decide whether they affect delivery, then fix the artifact or document the reason.

## 8. Clean rebuildable intermediates

```powershell
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
py .\00_workbench_core\tools\vn_workspace_cleanup.py --audit
```

The cleanup tool protects canon and deliverables: project memory, narrative design, generated content, delivery files, method cards, portable skills, schemas, templates and public style assets.

## 9. Git visibility check

Important files must not be ignored:

```powershell
git check-ignore -v README.md
git check-ignore -v START_HERE.md
git check-ignore -v skills\galgame-workbench-loader\SKILL.md
git check-ignore -v vn_fusion_workbench\00_workbench_core\tools\vn_context_bootstrap.py
git check-ignore -v vn_fusion_workbench\00_workbench_core\tools\build_excel_template_py.py
```

These commands should have no output.
