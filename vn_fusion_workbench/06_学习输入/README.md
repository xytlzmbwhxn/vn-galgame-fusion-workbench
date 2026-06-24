# 学习输入区

这里是工作台继续吸收教程、剧本文本、写作方法论和风格样本的入口。

公开仓库保留完整流程：

- `教程文本/`：教程类输入和学习输出。
- `视觉小说剧本文本/`：VN / Galgame / AVG 剧本文本输入和学习输出。
- `_风格画像/`：可复用、可调用的抽象风格资产。
- `_处理日志/`：公开处理日志模板和说明。
- `_外部项目评估/`：公开评估模板和说明。

## 推荐流程

从 `vn_fusion_workbench` 目录运行：

```powershell
py .\00_workbench_core\tools\vn_learning_intake.py --kind all
py .\00_workbench_core\tools\vn_style_profile_compiler.py --kind tutorials --name tutorial_batch
py .\00_workbench_core\tools\vn_style_profile_compiler.py --kind scripts --name vn_script_batch
```

学习结果不要只停留在摘要里。能复用的部分应该沉淀为：

- `00_workbench_core/methods/` 方法卡；
- `06_学习输入/_风格画像/` 风格画像；
- 项目自己的 `00_project_memory/`；
- 质量检查或导出工具。

生成前，AI 应读取已经压缩过的风格画像和方法卡，而不是把大段原始语料直接塞进上下文。
