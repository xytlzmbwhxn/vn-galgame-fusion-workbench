# Writing Workflow

## 0. 开项目

1. 写 `02_projects/<project>/00_project_memory/bible/premise.md`。
2. 写 `02_projects/<project>/00_project_memory/bible/style_rules.md`。
3. 建角色卡、地点卡、物件卡，放入 `02_projects/<project>/00_project_memory/cards/`。
4. 写路线图和变量表，放入 `02_projects/<project>/01_narrative_design/routes/`。

## 1. 写场景前

必须完成：

- `01_narrative_design/scenes/scene_cards/*.json`
- 参与角色的 current state
- 关系矩阵
- 场景内 5 个可操作物
- 本场会用到的记忆
- 本场要写回的 state delta

然后生成 draft session：

```powershell
python .\00_workbench_core\tools\vn_workbench.py draft-session --project .\02_projects\<project_id> --scene .\02_projects\<project_id>\01_narrative_design\scenes\scene_cards\S001_scene_card.json --draft-name S001_draft
```

写作前先看 `S001_draft_session.md`、`S001_scene_brief.md` 和 `S001_context_pack.md`。如果没有方法卡来源、输出契约、角色运行态和后续验证命令，不能开始写正文。

## 2. 写 Excel / CSV

每行只承担一个 click beat。

- 不在单行塞长段解释。
- `body_action` 要持续出现。
- 选择项用 `choice_group` 归并。
- 本行用到旧记忆，就写进 `memory_refs`。

## 3. 跑门禁

```powershell
python .\00_workbench_core\tools\vn_workbench.py validate --project .\02_projects\rain_gate_demo --script .\02_projects\rain_gate_demo\02_generated_content\scripts\csv\S001_script.csv
```

失败项先改剧本，再改卡片。不要用解释盖过去。

## 4. 打上下文包

```powershell
python .\00_workbench_core\tools\vn_workbench.py context --project .\02_projects\rain_gate_demo --scene .\02_projects\rain_gate_demo\01_narrative_design\scenes\scene_cards\S001_scene_card.json --out .\02_projects\rain_gate_demo\99_内部工作\上下文包\当前\S001_context_pack.md
```

上下文包给下一轮起草或精修用。它只收本场必要内容，避免全项目乱塞。

## 5. 导出 WebGAL

```powershell
python .\00_workbench_core\tools\vn_workbench.py export-webgal --project .\02_projects\rain_gate_demo --script .\02_projects\rain_gate_demo\02_generated_content\scripts\csv\S001_script.csv --out .\02_projects\rain_gate_demo\05_交付文件\引擎导出\webgal\S001.txt
```

导出后用 WebGAL Terre 或 WebGAL 项目预览节奏。
