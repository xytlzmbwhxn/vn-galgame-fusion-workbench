# Portable Skills

这个目录是工作台最显眼的 skills 入口。另一个 AI 拿到仓库后，不需要依赖本机 Codex / CC Switch 安装，直接读这里即可。

## 使用顺序

1. 读 `portable_skill_manifest.json`。
2. 读 `galgame-workbench-loader/SKILL.md`。
3. 根据任务继续读：
   - `vn-fusion-writer/SKILL.md`
   - `vn-scene-drafting/SKILL.md`
   - `vn-presence-revision/SKILL.md`
   - `vn-character-memory/SKILL.md`
4. 再回到 `START_HERE.md` 和 `AI_HANDOFF_PACKAGE/handoff_notes/`，按项目上下文启动。

## 技能说明

- `galgame-workbench-loader`：定位工作台、读取启动文件、避免依赖本机安装。
- `vn-fusion-writer`：设计、起草、修订和 QA 玩法融合型视觉小说。
- `vn-scene-drafting`：生成 Galgame/AVG 场景、CSV 行、分支和可读预览。
- `vn-presence-revision`：修掉 AI 腔、平滑过度、角色不像自己、心理死板等问题。
- `vn-character-memory`：固定角色卡、运行状态、关系记忆和声音手印。

## 备份位置

同一批 skills 还镜像在：

```text
vn_fusion_workbench/00_workbench_core/portable_skills/
AI_HANDOFF_PACKAGE/portable_skills/
```

运行下面的命令可以确认三处都可读：

```powershell
cd <repo>\vn_fusion_workbench
py .\00_workbench_core\tools\vn_skill_backup_check.py
```
