# START HERE

这是 `VN_Workbench_Project` 的正式入口。无论是人、Codex，还是别的 AI，从这个文件开始。

## 冷启动顺序

任何 AI 接手这个仓库时，先按顺序读取：

1. `START_HERE.md`
2. `项目结构总览.md`
3. `skills/portable_skill_manifest.json`
4. `skills/galgame-workbench-loader/SKILL.md`
5. `skills/vn-fusion-writer/SKILL.md`
6. `skills/vn-scene-drafting/SKILL.md`
7. `skills/vn-presence-revision/SKILL.md`
8. `skills/vn-character-memory/SKILL.md`
9. `AI_HANDOFF_PACKAGE/handoff_notes/CURRENT_TASK_STATE.md`
10. `AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md`
11. `vn_fusion_workbench/00_workbench_core/docs/METHOD_CALLING_WORKFLOW.md`
12. `vn_fusion_workbench/00_workbench_core/docs/FULL_GENERATION_FLOW_PUBLIC.md`
13. `vn_fusion_workbench/00_workbench_core/docs/PATH_ALIAS_PROTOCOL.md`
14. `vn_fusion_workbench/00_workbench_core/methods/method_index.json`

不要假设本机已经安装过任何 Codex / CC Switch skill。仓库里的 `skills/` 是优先入口。

## 常用命令

进入工作台：

```powershell
cd <repo>\vn_fusion_workbench
```

查看项目列表：

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths projects
```

查看路径别名：

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths list
```

读取中文文件时，优先用工作台命令或路径别名，避免在临时脚本里手写中文路径：

```powershell
py .\00_workbench_core\tools\vn_workbench.py read ROOT_START_HERE
py .\00_workbench_core\tools\vn_workbench.py read STYLE_HANDPRINT_CURRENT
```

## 写作前必须启动上下文

新写、重写、审稿或交付前，先运行：

```powershell
py .\00_workbench_core\tools\vn_context_bootstrap.py --project P020 --task review
```

把 `P020` 换成当前项目键。这个命令会写出加载收据，证明 AI 已经读取 portable skills、方法卡、项目记忆、角色卡、runtime state、memory log、scene card 和 route map。

创建正式 draft-session：

```powershell
py .\00_workbench_core\tools\vn_workbench.py draft-session --project P020 --scene S001_scene_card.json --draft-name S001_draft
```

如果需要控制台状态、上下文追踪或风格合同：

```powershell
py .\00_workbench_core\tools\vn_control_room.py status --project P020
py .\00_workbench_core\tools\vn_control_room.py context-trace --project P020 --draft-name S001_draft
py .\00_workbench_core\tools\vn_control_room.py style-contract --project P020 --draft-name S001_draft
```

## 完整交付最少包含

每篇正式作品至少要有：

- `00_project_memory/`：角色卡、runtime state、memory log。
- `01_narrative_design/`：scene card、route map、互动设计。
- `02_generated_content/`：CSV 源剧本和生成稿。
- `05_交付文件/可读稿/`：给人看的中文稿。
- `05_交付文件/剧本表_CSV/`
- `05_交付文件/剧本表_Excel/`
- `05_交付文件/引擎导出/`
- `05_交付文件/角色设定/`
- `99_内部工作/质检报告/`：QA、deep audit、quality debt 等报告。

只交一个 Markdown 可读稿不算完整交付。

## 交付前检查

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_encoding_guard.py --project P020
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project P020 --strict
py .\00_workbench_core\tools\vn_skill_backup_check.py
```

面向用户的可读稿还要跑：

```powershell
py .\00_workbench_core\tools\vn_handoff_guard.py --target <可读稿.md> --strict
```

生成或导出后清理：

```powershell
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
py .\00_workbench_core\tools\vn_workspace_cleanup.py --audit
```

## 写作硬规则

- 每一行是点击单位，不是“说话人单位”。
- 对话可以成块连续，不能机械一人一句。
- 叙述、对白和心理要区分：镜头能拍到的是叙述或舞台；心理必须是私人的推理、退缩、借口、选择压力或未说出口的代价。
- 角色语气词、停顿、反问、放松和自我修正要在适当时机出现；不能把心理写成死板说明书。
- 人物登场要有软引出：环境、问题、物件、压力和动作先行，不要默认读者已经认识所有角色。
- 禁止用“不是……而是……”等公式句把主题讲出来。主题要通过选择、状态、物件、关系代价和回调被玩家感觉到。

## GitHub

上传前看：

```text
GITHUB_UPLOAD_GUIDE.md
```

如果只是想确认仓库能不能被另一个 AI 接手，运行：

```powershell
cd <repo>\vn_fusion_workbench
py .\00_workbench_core\tools\vn_context_bootstrap.py --project P020 --task review
py .\00_workbench_core\tools\vn_skill_backup_check.py
```
