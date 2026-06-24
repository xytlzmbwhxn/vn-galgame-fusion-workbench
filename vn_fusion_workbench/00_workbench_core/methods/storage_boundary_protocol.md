---
id: storage_boundary_protocol
type: method_card
---

# Storage Boundary Protocol

## Call This When

Before adding any new writing method, project memory, generated script, export, or QA artifact.

## Rule

Reusable writing knowledge belongs to the workbench core. Project-specific story data belongs to the project. Generated source scripts belong to generated content. Human-facing deliverables and engine exports belong to the project's delivery folder. QA, draft-session bundles, context packs, traces, and screenshots belong to internal work.

## Directories

| Content type | Destination |
| --- | --- |
| reusable writing method | `00_workbench_core/methods/` |
| reusable schema/template/tool | `00_workbench_core/schemas/`, `templates/`, `tools/` |
| source/research log | `01_reference_log/` |
| project bible/theme/style | `02_projects/<project>/00_project_memory/bible/` |
| character/location/item cards | `02_projects/<project>/00_project_memory/cards/` |
| runtime character state | `02_projects/<project>/00_project_memory/runtime_state/characters/` |
| project memory logs | `02_projects/<project>/00_project_memory/memory_logs/` |
| route maps and scene cards | `02_projects/<project>/01_narrative_design/` |
| generated scripts and drafts | `02_projects/<project>/02_generated_content/` |
| human-facing works, readable copies, Excel, CSV, character briefs | `02_projects/<project>/05_交付文件/` |
| engine exports: WebGAL, Ren'Py, Ink, Yarn, Godot Dialogue | `02_projects/<project>/05_交付文件/引擎导出/` |
| character card exports for other tools/AIs | `02_projects/<project>/05_交付文件/角色设定/角色卡导出/` |
| draft-session, scene brief, context pack, traces | `02_projects/<project>/99_内部工作/上下文包/` |
| QA reports, deep audits, quality debt, internal screenshots | `02_projects/<project>/99_内部工作/质检报告/` |

## Procedure

1. Decide whether the new file is reusable method, project memory, generated source, delivery export, or internal QA/context.
2. Place it in the matching directory before drafting.
3. If a generated scene reveals new canon, update project memory separately.
4. Never store reusable method notes inside a project folder.
5. Never store character cards or project secrets inside `00_workbench_core`.

## Failure Signs

- a method card mentions only one project's character names
- a project character card lives beside reusable tools
- generated drafts sit next to curated memory
- engine exports are hidden inside internal context folders
- QA reports, traces, or screenshots appear as public deliverables
