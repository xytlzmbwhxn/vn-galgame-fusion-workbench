# VN Fusion Workbench

面向中文视觉小说 / Galgame 写作的本地工作台。

它把角色记忆、场景卡、路线图、CSV 剧本、可读稿、引擎导出、Excel 交付表和质量检查工具放在一套流程里。AI 或协作者拿到仓库后，可以沿着文件结构理解项目、继续写作、检查交付。

默认工作语言优先中文。用户明确指定其他语言时，再切换到对应语言。

## 可以用来做什么

- 写中文视觉小说、Galgame、AVG、互动短篇。
- 维护角色卡、运行状态、关系记忆和长期 memory log。
- 用 scene card、route map、状态变更和伏笔账本管理故事结构。
- 输出 CSV 剧本、中文可读稿、Excel 交付表和多引擎草稿。
- 导出 WebGAL、Ren'Py、Ink、Yarn Spinner、Godot Dialogue Manager 等格式。
- 检查剧本格式、分支目标、角色记忆、交付完整性、编码问题、AI 腔和上下文加载情况。

## 短篇项目说明

`vn_fusion_workbench/02_projects/` 下面的编号项目，主要是工作台优化过程中的测试文本和流程切片。

项目序号基本对应迭代顺序：编号越靠后，越接近当前工作台的写作规范、交付结构和 QA 流程。早期项目保留了旧流程痕迹，适合用来观察工作台的演进。

当前最适合作为完整流程参考的是：

```text
vn_fusion_workbench/02_projects/020_旧钟楼只在午休响一次
```

它包含角色记忆、scene card、route map、CSV 剧本、可读稿、Excel、引擎导出、角色设定和质量报告，可以作为完整交付样例。

## 快速上手方法

最简单的用法就是把这个仓库交给 AI，然后用自然语言说明目标。

可以这样说：

```text
请先阅读 START_HERE.md 和 skills/，再按工作台流程帮我写一个新的中文 Galgame 短篇。
```

```text
请参考 020_旧钟楼只在午休响一次 的完整交付结构，新建一个随机题材项目，并跑完整检查。
```

```text
请打开 vn_fusion_workbench/02_projects/<项目名>，检查它的角色记忆、剧本、交付文件和 QA 报告有没有漏项。
```

如果你只是想体验流程，可以先让 AI 看这个示例项目：

```text
vn_fusion_workbench/02_projects/020_旧钟楼只在午休响一次
```

它是当前最完整的样例。

## 维护者检查命令

这些命令用于确认工作台真的加载了上下文、skills 和检查工具。普通使用者可以让 AI 代跑。

进入工作台目录：

```powershell
cd .\vn_fusion_workbench
```

查看已有项目：

```powershell
py .\00_workbench_core\tools\vn_workbench.py paths projects
```

加载项目上下文：

```powershell
py .\00_workbench_core\tools\vn_context_bootstrap.py --project P020 --task review
```

写作或重写前，生成 draft session：

```powershell
py .\00_workbench_core\tools\vn_workbench.py draft-session --project P020 --scene S001_scene_card.json --draft-name S001_draft
```

交付前检查：

```powershell
py .\00_workbench_core\tools\vn_workbench.py validate --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_workbench.py deep-audit --project P020 --script <script.csv>
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project P020 --strict
py .\00_workbench_core\tools\vn_handoff_guard.py --target <可读稿.md> --strict
```

生成后清理可再生中间产物：

```powershell
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
```

## 目录结构

```text
VN_Workbench_Project/
├─ README.md
├─ START_HERE.md
├─ 项目结构总览.md
├─ skills/
├─ AI_HANDOFF_PACKAGE/
├─ external_refs/
└─ vn_fusion_workbench/
   ├─ 00_workbench_core/
   ├─ 01_reference_log/
   ├─ 02_projects/
   └─ 06_学习输入/
```

常用入口：

- `START_HERE.md`：人和 AI 接手时的启动入口。
- `skills/`：随仓库携带的 portable skills。
- `AI_HANDOFF_PACKAGE/`：给 AI 接手用的状态、规则和镜像。
- `vn_fusion_workbench/00_workbench_core/`：工具、方法卡、模板、schema 和工作流文档。
- `vn_fusion_workbench/02_projects/`：短篇项目和流程测试切片。
- `vn_fusion_workbench/06_学习输入/_风格画像/`：抽象后的公开风格资产。

## AI 接手流程

先读：

```text
START_HERE.md
skills/portable_skill_manifest.json
skills/galgame-workbench-loader/SKILL.md
AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md
vn_fusion_workbench/00_workbench_core/docs/FULL_GENERATION_FLOW_PUBLIC.md
```

再运行：

```powershell
cd .\vn_fusion_workbench
py .\00_workbench_core\tools\vn_context_bootstrap.py --project <Pxxx> --task review
py .\00_workbench_core\tools\vn_skill_backup_check.py
```

工作台原则：先读本地文件，再生成内容；先跑检查，再交付。

默认用中文回应和交付。工具名、文件名、引擎格式可以保留英文。


## License

暂未指定许可证。公开使用、改造或再发布前，请先确认仓库维护者后续补充的授权说明。
