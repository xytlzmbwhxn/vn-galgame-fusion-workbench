---
id: user_prompt_response_protocol
type: method_card
---

# User Prompt Response Protocol

## Purpose

Use this before acting on user instructions in the VN workbench. The user often gives critique, asks to continue, asks for learning, asks for a rewrite, or asks for a new story. Each prompt type should trigger a different production path.

## Prompt Types And Required Response

| User prompt type | Meaning | Required workbench action |
| --- | --- | --- |
| "学习/吸收/搜索/参考项目" | Improve reusable capability | Run external ingestion, update `01_reference_log`, add or revise method/template/tool files, verify. |
| "写一份/开始创作/测试作品" | Produce generated content | Create or read project memory, generate draft-session, draft CSV, render readable, validate, export. |
| "重写/不行/文笔差/不像人说话" | Diagnose and repair a failure mode | Name the failure, update reusable methods if systemic, update project memory if canon, create a new generated draft. |
| "继续" | Resume newest unfinished objective | Check current plan/context, continue the latest active work, do not resurrect older tasks. |
| "扩大/长篇/有主旨" | Move from slice to project | Build or update theme spine, route map, arcs, quality state, vertical-slice audit, then draft. |
| "角色不稳定/口吻太平" | Voice/state issue | Update character cards, runtime state, example dialogue, memory logs, then run voice pass. |
| "人物设定给我看" | User needs visible cast anchors | Produce character brief with memory points before or alongside script; store cards and runtime state. |
| "只要 Excel/剧本标准写法" | Artifact request | Put creative text in spreadsheet/source CSV, not method notes; export Excel and readable preview. |

## Response Algorithm

0. Resolve the active objective from the newest user-visible context.
   - If the newest prompt names a project, file, pasted prior result, or says
     "that piece / 刚才那篇 / 重写", use that newest reference first.
   - Treat `CURRENT_TASK_STATE.md` and `portable_manifest.json` as fallback state,
     not as stronger evidence than the user's latest message.
   - If fallback state conflicts with the newest user prompt, update the handoff
     state before drafting.
   - A bare "继续" resumes the newest unfinished objective in the conversation,
     not the last project mentioned in an old manifest.
1. Classify the user's newest prompt.
2. Decide the storage boundary:
   - reusable method goes to `00_workbench_core`
   - project canon goes to `00_project_memory`
   - generated prose goes to `02_generated_content`
   - human-facing proof and engine exports go to `05_交付文件`
   - QA/context proof goes to `99_内部工作`
3. If the prompt asks for learning, do not write only a summary. Convert useful findings into method/tool/template changes.
4. If the prompt asks for writing, do not start from blank prose. Read or generate a draft-session first.
5. If the prompt critiques quality, treat it as a new QA dimension. Add the rule to the workbench if it generalizes.
6. If characters are new or unclear, present a user-visible character brief before deep drafting.
7. After generation, validate and update only confirmed project memory.

## User-Facing Behavior

- When the user gives a craft insight, explicitly decide whether it belongs in reusable method, project memory, or the current generated draft.
- When the user says "not this, do X", obey the newest instruction and avoid defending the previous artifact.
- When the user asks for learning first, separate learning from generated story output.
- When the user asks for story output, include enough visible character setup that the user can remember the cast.
- When continuing after interruption, sanity-check the latest user request before finalizing.

## Output Contract

Every response to a non-trivial prompt must leave one of:

- updated reusable method/tool/template
- updated project memory/character state
- generated draft/export/QA artifact
- clear blocked note with missing required context

## Failure Signs

- The assistant replies with advice but no workbench file changes after a learning request.
- The assistant rewrites text without updating the rules that caused the failure.
- Character cards exist but the user never sees a readable character setup.
- Generated text embeds project memory in reusable core.
- A "continue" request resumes an old task instead of the newest objective.
- The assistant loads an older active project from manifest after the user has
  attached or quoted a newer target file.
