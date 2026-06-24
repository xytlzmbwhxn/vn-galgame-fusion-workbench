# VN Control Room

The VN Control Room is the workbench control plane. It does not replace
`vn_workbench.py`; it wraps the existing production chain with project status,
command ledger, style-contract compilation, context tracing, and VN-specific
quality debt reports.

## Why It Exists

The workbench should not depend on a chat transcript to remember how to write.
Every serious action should be visible as files:

- project facts
- recommended next step
- command ledger entry
- context trace
- method/style contract
- generated artifact
- QA and quality debt report

This is the VN adaptation of AI-native workflow architecture. Public files should
keep rewritten concepts, reusable methods, tool code and delivery-facing reports.

## Main Commands

Run from:

```powershell
cd <repo>\vn_fusion_workbench
```

Project status:

```powershell
py .\00_workbench_core\tools\vn_control_room.py status --project blue_photo_booth_demo
```

Create and run a controlled command:

```powershell
py .\00_workbench_core\tools\vn_control_room.py command-create --project blue_photo_booth_demo --action draft_session --draft-name S001_next
py .\00_workbench_core\tools\vn_control_room.py command-list --project blue_photo_booth_demo
py .\00_workbench_core\tools\vn_control_room.py command-run --id <command_id>
```

Compile style/method contract:

```powershell
py .\00_workbench_core\tools\vn_control_room.py style-contract --project blue_photo_booth_demo --draft-name S001_next
```

Write a context trace:

```powershell
py .\00_workbench_core\tools\vn_control_room.py context-trace --project blue_photo_booth_demo --draft-name S001_next
```

Classify VN-specific quality debt:

```powershell
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project blue_photo_booth_demo
```

## Command Ledger

Commands are stored in:

```text
00_workbench_core/runtime/commands/command_ledger.jsonl
```

Each command records:

- id
- project id
- action
- scene/script/draft name
- status
- result
- timestamps

The command ledger is runtime state, not reusable method knowledge.

## VN Quality Debt Types

The deterministic debt pass does not replace human or AI review. It identifies
repeatable VN failure shapes:

- `click_unit_low_payload`
- `click_unit_overfragmented`
- `thought_missing`
- `thought_misclassified_narration`
- `flat_voice`
- `punctuation_energy_loss`
- `preachy_dialogue`
- `performance_cue_gap`
- `theme_not_playable`
- `state_unremembered`

Reports are written under:

```text
02_projects/<project>/99_内部工作/质检报告/当前/
```

## Relationship To Existing Tools

`vn_control_room.py` dispatches to `vn_workbench.py` for:

- `draft-session`
- `validate`
- `deep-audit`
- `render-readable`
- engine exports
- character brief

All writing and QA should still use the same CSV-centered production chain.
Do not add a second writer path for Codex chat, local web UI, or future AI agents.

## Handoff Rule

Another AI should start with:

1. `START_HERE.md`
2. `AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md`
3. `00_workbench_core/docs/METHOD_CALLING_WORKFLOW.md`
4. this file
5. `vn_control_room.py status --project <project>`

Only after the status projection and context trace are visible should it draft or
revise a scene.
