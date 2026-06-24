# Style Corpus Intake Protocol

Use this when the user drops tutorials, novels, VN scripts, dialogue exports, or
style references into `06_学习输入`.

## Purpose

Turn raw source files into stable, searchable workbench assets before any model
uses them for generation.

## Folder Contract

Raw pending input goes only to:

- `06_学习输入/教程文本/待学习/`
- `06_学习输入/视觉小说剧本文本/待学习/`

Normalized learned text goes to:

- `06_学习输入/教程文本/已学习/`
- `06_学习输入/视觉小说剧本文本/已学习/`

Derived assets go to:

- `06_学习输入/_风格画像/`
- `00_workbench_core/methods/`
- project-specific `00_project_memory/` only when the source belongs to one story.

## Processing Steps

1. Run `vn_learning_intake.py` to convert supported files into Markdown.
2. Read the normalized Markdown, not the raw files, for learning.
3. Extract reusable craft into method cards or style profiles.
4. Keep copyrighted or external source text out of generation prompts unless the
   user explicitly supplies it for private reference and requests direct use.
5. If source text was fully learned and the user wants cleanup, remove it from
   `待学习`; keep the normalized Markdown in `已学习`.

## Output Contract

Every learning round must produce at least one of:

- a style profile in `06_学习输入/_风格画像/`
- a lesson card in `06_学习输入/_风格画像/`
- a reusable method in `00_workbench_core/methods/`
- a project-only memory update under `02_projects/<project>/00_project_memory/`

## Failure Signs

- The model reads raw files from `Downloads` and writes no learned artifact.
- A style source changes generation only through chat memory.
- A huge rule list is loaded without examples or source metrics.
- Tutorial advice and script examples are mixed into the same undifferentiated notes.

