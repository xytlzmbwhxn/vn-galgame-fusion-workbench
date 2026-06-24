# VN Fusion Workbench

本地视觉小说 / Galgame 写作工作台。目标是把项目记忆、角色声纹、小说工程、场景卡、CSV/Excel 剧本、分支状态、QA 门禁和多引擎导出绑成一套可重复调用的流程。

## 核心结构

```text
vn_fusion_workbench/
  00_workbench_core/
    docs/        工作流和架构说明
    methods/     可调用写作方法卡
    schemas/     角色、场景、状态变更、小说工程、导出包 schema
    templates/   CSV/JSON 模板
    tools/       vn_workbench.py、QA 门禁、清理工具与 Excel 生成器
  01_reference_log/
    BORROWED_PROJECTS.md
  02_projects/
    <project_id>/
      00_project_memory/       只属于该项目的 bible、角色卡、运行状态、记忆账本
      01_narrative_design/
        routes/                路线和状态变量
        scenes/                场景卡、状态变更
        novel_architecture/    章计划、叙事线、角色弧、伏笔账本
        interactive_design/    主旨脊柱、质量状态、垂直切片审计
      02_generated_content/    生成的剧本、可读稿、修订稿、Excel
      03_exports/              WebGAL、Ren'Py、Ink、Yarn、Godot Dialogue、角色卡导出
      04_quality/              QA 报告和预览
```

## 新增小说工程层

本轮融合 Manuskript、bibisco、Quoll Writer、Skribisto、Story Architect、NovelStar 的写作工程结构，新增：

- `00_workbench_core/methods/novel_architecture_fusion.md`
- `00_workbench_core/schemas/chapter_plan.schema.json`
- `00_workbench_core/schemas/narrative_thread.schema.json`
- `00_workbench_core/schemas/character_arc.schema.json`
- `00_workbench_core/schemas/foreshadow_ledger.schema.json`

项目可放置：

```text
01_narrative_design/novel_architecture/
  chapter_plan.json
  narrative_threads.json
  character_arcs.json
  foreshadow_ledger.json
```

`draft-session` 会把这些文件列入起草上下文，`validate` 会检查剧本行是否在 `memory_refs` 中引用 `THR_`、`ARC_`、`FS_` 结构。

## 新增互动主旨层

本轮继续融合 Ren'Py 官方样例、WebGAL、ChoiceScript、ink、Yarn、Twine/Chapbook、Failbetter storylets、Emily Short 的质量叙事、AI4VisualNovel、reramen 等项目，新增：

- `00_workbench_core/methods/theme_spine_playable_thesis.md`
- `00_workbench_core/methods/storylet_quality_state.md`
- `00_workbench_core/methods/vertical_slice_production_pipeline.md`
- `00_workbench_core/schemas/theme_spine.schema.json`
- `00_workbench_core/schemas/quality_state_ledger.schema.json`
- `00_workbench_core/schemas/vertical_slice_audit.schema.json`

项目可放置：

```text
01_narrative_design/interactive_design/
  theme_spine.json
  quality_state_ledger.json
  vertical_slice_audit.json
```

`draft-session` 和 `scene-brief` 会自动列入这些文件。它们负责回答：

- 主旨如何变成玩家反复执行的行为。
- 选择、微互动、storylet、质量数值如何被状态和回调记住。
- 一个测试故事是否已经证明 CSV、可读稿、QA、导出和项目记忆更新的完整链路。

## 显示层与心理描写

本轮新增 `thought` 行类型和可读稿渲染：

- CSV 中 `dialogue` 保持裸台词，方便导出到 WebGAL、Ren'Py、Ink、Yarn、Godot Dialogue。
- `render-readable` 会把对话渲染成 `【角色】『台词』`。
- `thought` 行会渲染成 `【角色】（心理文本）` 或 `（心理文本）`。
- QA 会统计心理行数量、心理/对话比例、语气词、问号/叹号/拖尾、句尾变化和低信息点击。

渲染可读稿：

```powershell
python .\00_workbench_core\tools\vn_workbench.py render-readable --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv --out .\02_projects\<project_id>\02_generated_content\drafts\readable\S001_draft.md
```

## 使用流程

写新场景前生成 draft session：

```powershell
python .\00_workbench_core\tools\vn_workbench.py draft-session --project .\02_projects\<project_id> --scene .\02_projects\<project_id>\01_narrative_design\scenes\scene_cards\S001_scene_card.json --draft-name S001_draft
```

校验剧本：

```powershell
python .\00_workbench_core\tools\vn_workbench.py validate --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv
```

导出：

```powershell
python .\00_workbench_core\tools\vn_workbench.py export-webgal --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv --out .\02_projects\<project_id>\03_exports\webgal\S001_draft.txt
python .\00_workbench_core\tools\vn_workbench.py export-renpy --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv --out .\02_projects\<project_id>\03_exports\renpy\S001_draft.rpy
python .\00_workbench_core\tools\vn_workbench.py export-ink --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv --out .\02_projects\<project_id>\03_exports\ink\S001_draft.ink
python .\00_workbench_core\tools\vn_workbench.py export-yarn --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv --out .\02_projects\<project_id>\03_exports\yarn\S001_draft.yarn
python .\00_workbench_core\tools\vn_workbench.py export-godot-dialogue --project .\02_projects\<project_id> --script .\02_projects\<project_id>\02_generated_content\scripts\csv\S001_draft.csv --out .\02_projects\<project_id>\03_exports\godot_dialogue\S001_draft.dialogue
```

生成 Excel。公开仓库默认使用 Python 标准库版，不依赖被 `.gitignore` 屏蔽的 `node_modules`：

```powershell
python .\00_workbench_core\tools\build_excel_template_py.py <project_id> S001_draft.csv
```

如果本机已经安装了工作台 Node 依赖，也可以使用增强版：

```powershell
node .\00_workbench_core\tools\build_excel_template.mjs <project_id> S001_draft.csv
```

## CSV 剧本字段

```text
scene_id, beat_id, row_type, speaker, text, voice_target, expression, body_action, bg, bgm, sfx, choice_group, choice_text, choice_target, condition, effects, memory_refs, qa_notes
```

要点：

- 每行是一个 textbox beat、选择项、演出命令或注释。
- `row_type` 支持 `dialogue`、`narration`、`thought`、`choice`、`command`、`comment`。
- `speaker` 放角色 ID，正文不要套双引号。
- `choice_target` 应对上 `command` 行的 `label:<target>;`。
- `effects` 使用可移植写法：`flag=true;trust_x+=1;timer-=2`。
- 长期结构引用放进 `memory_refs`：`THR_` 叙事线、`ARC_` 角色弧、`FS_` 伏笔。
- 主旨、质量状态、垂直切片审计放进 `01_narrative_design/interactive_design/`。
- 项目专属记忆放进 `00_project_memory/`；生成正文放进 `02_generated_content/`；可复用方法放进 `00_workbench_core/methods/`。

## QA 门禁

`validate` 会检查：

- CSV 列、行类型、空文本、未知角色。
- 选择项、跳转项、label 是否能对上。
- 对话/旁白是否机械交替。
- 台词是否过长、过短、低信息量。
- 句尾是否单一，标点是否缺乏角色压力。
- 对话是否缺少角色化语气词、随性口吻或可爱的回弹。
- 对话重的场景是否缺心理行，心理行是否有具体压力。
- 十行内是否缺少身体、物件、环境动作。
- 是否缺角色运行状态文件。
- 场景卡是否缺核心字段。
- 小说工程文件是否存在，剧本行是否引用叙事线、角色弧、伏笔。
- 是否出现常见 AI 腔、抽象情绪词、双引号式小说写法。
- 是否有状态变更和可见分支成本。

完整来源和许可证备注见 [BORROWED_PROJECTS.md](01_reference_log/BORROWED_PROJECTS.md)。
