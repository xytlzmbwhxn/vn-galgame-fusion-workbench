# Skills Snapshot

公开仓库不需要提交整台机器的技能快照。

别人接手本工作台时，应使用：

```text
skills/
vn_fusion_workbench/00_workbench_core/portable_skills/
AI_HANDOFF_PACKAGE/portable_skills/
```

这三处已经包含本工作台必需的：

- `galgame-workbench-loader`
- `vn-fusion-writer`
- `vn-scene-drafting`
- `vn-presence-revision`
- `vn-character-memory`

校验命令：

```powershell
cd <repo>\vn_fusion_workbench
py .\00_workbench_core\tools\vn_skill_backup_check.py
```
