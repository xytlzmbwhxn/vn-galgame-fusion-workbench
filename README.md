# VN Fusion Workbench

一个本地优先、可交接的视觉小说 / Galgame 写作工作台。

它不是单纯的“提示词合集”。这个仓库把角色记忆、场景卡、路线图、CSV 剧本、可读稿、引擎导出、Excel 交付表和质量守门工具放在同一套流程里，让另一个 AI 或协作者 clone 后也能从文件重新启动，而不是依赖某台电脑上的聊天记录。

## 这个仓库能做什么

- 维护角色卡、运行状态、关系记忆和可检索 memory log，减少角色越写越漂。
- 用 scene card、route map、状态变更和伏笔账本管理 VN 结构。
- 生成 CSV 剧本、可读稿、Excel 交付表和多引擎草稿。
- 导出 WebGAL、Ren'Py、Ink、Yarn Spinner、Godot Dialogue Manager 等格式。
- 用 validate、deep-audit、quality-debt、handoff guard、encoding guard 和 delivery guard 检查漏项。
- 内置 portable skills，让 AI 接手时能读仓库里的技能备份，而不是依赖本机 Codex / CC Switch 安装。

## 先看哪里

给人看：

```text
START_HERE.md
项目结构总览.md
```

给 Codex / 其他 AI 看：

```text
START_HERE.md
skills/
AI_HANDOFF_PACKAGE/handoff_notes/
vn_fusion_workbench/00_workbench_core/docs/FULL_GENERATION_FLOW_PUBLIC.md
```

`skills/` 是最显眼的 portable skill 备份；同一批 skills 也保留在工作台内部和 handoff 包里，供工具链和自动检查使用。

## 目录结构

```text
VN_Workbench_Project/
├─ README.md
├─ START_HERE.md
├─ GITHUB_UPLOAD_GUIDE.md
├─ 项目结构总览.md
├─ skills/                         portable AI skills
├─ AI_HANDOFF_PACKAGE/             AI 接手说明、状态、镜像
├─ external_refs/                  可公开的外部参考说明
└─ vn_fusion_workbench/
   ├─ 00_workbench_core/           方法、工具、模板、schema
   ├─ 01_reference_log/            参考研究入口
   ├─ 02_projects/                 每篇作品的独立项目
   └─ 06_学习输入/                 学习输入、风格画像和处理区
```

## 快速启动

从仓库根目录进入工作台：

```powershell
cd .\vn_fusion_workbench
```

查看项目：

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths projects
```

让 AI 或工具链证明它已经加载工作台上下文：

```powershell
py .\00_workbench_core\tools\vn_context_bootstrap.py --project P020 --task review
```

生成或重写场景前：

```powershell
py .\00_workbench_core\tools\vn_workbench.py draft-session --project P020 --scene S001_scene_card.json --draft-name S001_draft
```

交付前至少运行：

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project P020 --strict
```

生成 Excel 交付表不需要 Node 依赖：

```powershell
py .\00_workbench_core\tools\build_excel_template_py.py P020 <script.csv>
```

生成后清理可再生中间产物：

```powershell
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
```

## 示例切片

仓库里保留了一个完整流程示例：

```text
vn_fusion_workbench/02_projects/020_旧钟楼只在午休响一次
```

它包含角色记忆、scene card、route map、CSV 剧本、中文可读稿、Excel 工作簿、引擎导出、角色设定和 QA 报告。新 AI 如果不知道完整交付应该长什么样，可以先对照这个项目。

## 准备上传 GitHub

照着这个文件填：

```text
GITHUB_UPLOAD_GUIDE.md
```

新建 GitHub 仓库时，不要让 GitHub 自动生成 README、.gitignore 或 license；这个本地仓库已经准备好了对应文件。
