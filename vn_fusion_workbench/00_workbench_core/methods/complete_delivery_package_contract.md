---
id: complete_delivery_package_contract
type: method_card
---

# Complete Delivery Package Contract

## Call This When

Use before any user-facing delivery of a VN/Gal project, especially when another
AI may open the workbench from zero and continue the work.

## Required Public Delivery Layers

A serious scene delivery is not complete when it only has a readable Markdown
draft. It must include:

- readable Gal-style Markdown under `05_交付文件/可读稿/`
- source CSV under `02_generated_content/scripts/csv/`
- copied public CSV under `05_交付文件/剧本表/CSV/`
- Excel table under `05_交付文件/剧本表/Excel/` when the table builder is available
- engine exports under `05_交付文件/引擎导出/`:
  - WebGAL `.txt`
  - Ren'Py `.rpy`
  - Ink `.ink`
  - Yarn `.yarn`
  - Godot Dialogue `.dialogue`
- character-setting delivery:
  - Character Card V2 JSON
  - user-readable character brief
- QA evidence:
  - validate QA
  - deep audit
  - quality debt or self-check

## Required Continuity Layers

Other AI handoff also needs project memory, not only public files:

- stable character cards
- runtime character state
- retrievable character memory logs
- scene card
- state delta
- route map / branch debt map

## Mandatory Guard

Before saying delivery is complete, run:

```powershell
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project Pxxx --strict
```

If the guard fails, do not describe the project as fully delivered. Say exactly
which layer is missing and either create it or ask the user whether they only
want a quick readable preview.

## Failure Signs

- `05_交付文件` contains only `可读稿`.
- CSV exists only inside a chat answer, not under `02_generated_content`.
- QA files exist only as informal notes, not as generated guard/audit outputs.
- Other AI can see the prose but cannot see state, route debt, character runtime,
  or engine handoff files.
