# Current Task State

Updated: 2026-06-24

## Workbench Status

OPERATIONAL.

This repository is prepared as a public, portable VN / Galgame workbench:

- top-level portable skills are under `skills/`;
- core tools are under `vn_fusion_workbench/00_workbench_core/tools/`;
- reusable writing methods are under `vn_fusion_workbench/00_workbench_core/methods/`;
- workbench portable skills are under `vn_fusion_workbench/00_workbench_core/portable_skills/`;
- AI handoff mirror skills are under `AI_HANDOFF_PACKAGE/portable_skills/`;
- projects are under `vn_fusion_workbench/02_projects/`;
- public style assets are under `vn_fusion_workbench/06_学习输入/_风格画像/`.

## Mandatory Startup

Before writing, rewriting, reviewing, or delivering:

```powershell
cd <repo>\vn_fusion_workbench
py .\00_workbench_core\tools\vn_context_bootstrap.py --project <Pxxx> --task <draft|rewrite|review>
```

The bootstrap receipt must show that mandatory portable skills and method cards loaded.

## Delivery Gate

Before claiming a work is complete, run:

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project <Pxxx> --script <script.csv>
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project <Pxxx> --script <script.csv>
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project <Pxxx> --script <script.csv>
py .\00_workbench_core\tools\vn_encoding_guard.py --project <Pxxx>
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project <Pxxx> --strict
py .\00_workbench_core\tools\vn_skill_backup_check.py
py .\00_workbench_core\tools\vn_handoff_guard.py --target <public readable md> --strict
```

Then clean rebuildable intermediates:

```powershell
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
py .\00_workbench_core\tools\vn_workspace_cleanup.py --audit
```
