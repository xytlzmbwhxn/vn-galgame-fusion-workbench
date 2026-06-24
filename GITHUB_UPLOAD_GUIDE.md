# GitHub 上传指南

这份指南只负责把 `VN_Workbench_Project` 上传成一个干净、可读、可 clone 后直接使用的 GitHub 仓库。

## 1. GitHub 新建仓库页面怎么填

在你截图里的页面，建议这样填：

```text
Repository name:
vn-fusion-workbench

Description:
Local-first visual novel / Galgame workbench with portable AI skills, character memory, script exports, and QA guards.

Visibility:
Public

Add README:
Off

Add .gitignore:
No .gitignore

Add license:
No license

Copilot prompt:
留空
```

然后点 `Create repository`。

为什么 README / .gitignore / license 都不要让 GitHub 生成：本地仓库已经有 README 和 .gitignore；license 需要你以后按真实授权意图单独决定，不要随手选 CC0。

## 2. 本地先检查

打开 PowerShell：

```powershell
cd D:\Users\Admin\Downloads\VN_Workbench_Master_Package\VN_Workbench_Project
git status --short
git status --ignored
```

确认你要上传的是 `VN_Workbench_Project`，不是外层 `VN_Workbench_Master_Package`。

再确认几个关键文件没有被忽略：

```powershell
git check-ignore -v README.md
git check-ignore -v START_HERE.md
git check-ignore -v skills\galgame-workbench-loader\SKILL.md
git check-ignore -v vn_fusion_workbench\00_workbench_core\tools\vn_context_bootstrap.py
git check-ignore -v vn_fusion_workbench\00_workbench_core\tools\build_excel_template_py.py
```

这些命令如果没有输出，表示它们会被正常提交。

## 3. 第一次提交

```powershell
git add .
git status --short
git commit -m "Initial public VN workbench"
```

如果 `git commit` 提示没有配置用户名邮箱，按提示设置即可，例如：

```powershell
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的邮箱"
git commit -m "Initial public VN workbench"
```

## 4. 连接 GitHub 仓库

创建仓库后，GitHub 会给你一个地址。HTTPS 大概长这样：

```text
https://github.com/<你的用户名>/vn-fusion-workbench.git
```

运行：

```powershell
git branch -M main
git remote add origin https://github.com/<你的用户名>/vn-fusion-workbench.git
git push -u origin main
```

如果你用 SSH，则是：

```powershell
git branch -M main
git remote add origin git@github.com:<你的用户名>/vn-fusion-workbench.git
git push -u origin main
```

如果提示 `remote origin already exists`：

```powershell
git remote -v
git remote set-url origin https://github.com/<你的用户名>/vn-fusion-workbench.git
git push -u origin main
```

## 5. 上传后让别人怎么用

对方 clone 后，从仓库根目录读：

```text
README.md
START_HERE.md
skills/
```

AI 接手时运行：

```powershell
cd <repo>\vn_fusion_workbench
py .\00_workbench_core\tools\vn_workbench.py paths projects
py .\00_workbench_core\tools\vn_context_bootstrap.py --project P020 --task review
py .\00_workbench_core\tools\vn_skill_backup_check.py
```

`P020` 是完整流程示例。实际写新作品时，换成当前项目键。

## 6. 后续更新

每次生成、导出或整理后：

```powershell
cd D:\Users\Admin\Downloads\VN_Workbench_Master_Package\VN_Workbench_Project\vn_fusion_workbench
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
py .\00_workbench_core\tools\vn_workspace_cleanup.py --audit
cd ..
git status --short
```

确认没有意外文件后：

```powershell
git add .
git commit -m "Update workbench"
git push
```
