# Portable Skills

这个目录保存工作台自己的可迁移 skills。它们不依赖本机 Codex / CC Switch
技能目录，可以随 `VN_Workbench_Project` 一起交给其他 Codex、通用 AI、写作代理或人工协作者。

## How To Use

1. 先读 `portable_skill_manifest.json`。
2. 根据任务选择一个或多个 `*/SKILL.md`。
3. 再读对应 skill 中列出的工作台文件，例如 `method_index.json`、`CURRENT_TASK_STATE.md`、角色卡、scene card、draft-session。
4. 生成或修改前，确认输出会落在对应边界：
   - 可复用方法：`00_workbench_core/methods/`
   - 可迁移技能：`00_workbench_core/portable_skills/`
   - 项目记忆：`02_projects/<project>/00_project_memory/`
   - 生成剧本源：`02_projects/<project>/02_generated_content/`
   - 人类和引擎交付物：`02_projects/<project>/05_交付文件/`
   - QA、上下文、trace、截图：`02_projects/<project>/99_内部工作/`

## Skill List

- `galgame-workbench-loader`: 接手工作台、定位当前项目、装配上下文。
- `vn-fusion-writer`: 设计、起草、修订、QA 玩法融合型视觉小说。
- `vn-scene-drafting`: 按 Galgame/AVG 剧本标准生成场景、分支和 CSV。
- `vn-presence-revision`: 工作台自有的存在感修订，用于去 AI 腔、保留角色手迹、检查改动行。
- `vn-character-memory`: 固定角色声纹、运行状态、记忆点和可见人设。

## Handoff Rule

如果只能交给其他 AI 一个文件夹，优先交整个 `VN_Workbench_Project`。如果只能交较小包，至少包含：

- `START_HERE.md`
- `项目结构总览.md`
- `AI_HANDOFF_PACKAGE/`
- `vn_fusion_workbench/00_workbench_core/portable_skills/`
- `vn_fusion_workbench/00_workbench_core/methods/`
- 当前项目的 `00_project_memory/`
- 当前项目的 `01_narrative_design/`
- 当前项目的 `02_generated_content/`
- 当前项目的 `05_交付文件/`
- 当前项目的 `99_内部工作/上下文包/当前/`
