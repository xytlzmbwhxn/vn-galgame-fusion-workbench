# Workbench Architecture

## 设计目标

把“AI 帮写视觉小说”拆成可审计的状态流：

```text
角色卡 / 世界卡 / 记忆账本
        ↓
场景卡 + 路线卡 + 选择压力
        ↓
Excel/CSV 剧本行
        ↓
机械 QA + 人声 QA
        ↓
状态变更声明
        ↓
WebGAL / Ren'Py 导出
```

## 五个核心层

### 1. Bible layer

来自 Novel-OS 的 Standards / Novel 思路。这里放全书级约束：

- `premise.md`: 题材、玩家身份、核心承诺。
- `style_rules.md`: 文风、文本框节奏、禁用 AI 腔。
- `anti_ai_phrases.md`: 项目级禁句和失败例。

项目内对应目录：`02_projects/<project>/00_project_memory/bible/`。

### 2. Card layer

来自 NovelForge 和 Character Card V2。所有重要设定都要卡片化：

- character cards
- location cards
- item cards
- route cards
- scene cards

卡片优先用 JSON，方便脚本校验；给人看的说明放 Markdown。

项目内对应目录：

- 项目私有卡片：`02_projects/<project>/00_project_memory/cards/`
- 路线和场景设计：`02_projects/<project>/01_narrative_design/`

### 3. Memory layer

来自 MemoryBooks、CharMemory、Lorewalker。

- `global_memory.md`: 全局已经发生的事。
- `character_memory/*.md`: 每个角色自己的经历、旧伤、关系债。
- `promises.json`: 承诺与违背。
- `secrets.json`: 秘密、知情者、揭露方式。
- `item_ledger.json`: 物品持有者、状态、痕迹。

项目内对应目录：`02_projects/<project>/00_project_memory/memory_logs/` 和 `00_project_memory/runtime_state/`。

### 4. Script layer

来自 WebGAL / Ren'Py / novelWriter。

Excel/CSV 是作者可编辑的剧本表。每行对应一个 textbox beat、一个命令或一个选择项。脚本不直接相信文本质量，必须通过 QA。

项目内对应目录：`02_projects/<project>/02_generated_content/scripts/`。

生成内容不进入 `00_project_memory`。只有经过确认会影响后续正史的事实，才写回 memory logs 或 runtime state。

### 5. Gate layer

来自 Tianming 和 NovelForge 的门禁思路。

门禁分三类：

- Form gate: 表头、字段、角色 ID、选择目标。
- Performance gate: 台词长度、身体动作、环境可操作物、AI 腔。
- State gate: 每场戏必须写回关系、记忆、物品、秘密、flag 或截止状态。

## 为什么先做轻量 CLI

大型项目已经有完整前后端，但当前任务的最短有效路径是：

- 下载成熟项目作架构样本。
- 用本地文件和脚本落一个可控骨架。
- 用 Excel 写剧本，导出到 WebGAL。
- 后面再决定是否接入完整 UI 或 RAG。

这样不会被 UI、数据库、向量库和模型配置拖住正文生产。
