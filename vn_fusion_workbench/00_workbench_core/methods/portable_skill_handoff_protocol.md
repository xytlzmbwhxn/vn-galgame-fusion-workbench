---
id: portable_skill_handoff_protocol
type: method_card
---

# Portable Skill Handoff Protocol

## Purpose

Make the workbench usable by another AI even when local Codex skills are not installed.

## Required Portable Skill Surfaces

- `00_workbench_core/portable_skills/portable_skill_manifest.json`
- `00_workbench_core/portable_skills/*/SKILL.md`
- `AI_HANDOFF_PACKAGE/portable_skills/`
- `AI_HANDOFF_PACKAGE/handoff_notes/CURRENT_TASK_STATE.md`
- `AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md`

## Procedure

1. Whenever a new reusable capability is added, decide whether it is:
   - method card: invoked by `draft-session`
   - portable skill: read by another AI as an operating skill
   - project memory: true only for one story
2. Add method cards to `method_index.json` if they must be loaded by `draft-session`.
3. Add portable skills to `portable_skill_manifest.json`.
4. Mirror portable skills into `AI_HANDOFF_PACKAGE/portable_skills/`.
5. Update `START_HERE.md`, `CURRENT_TASK_STATE.md`, and the source ledger.
6. Validate JSON files.

## Output Contract

A handoff-ready update must state:

- new skill ids
- new method ids
- canonical skill path
- handoff copy path
- validation result

## Failure Signs

- A useful workflow exists only in chat.
- A skill exists only under the host user's Codex directory.
- New methods are not in `method_index.json`.
- Handoff docs mention an old active project or old latest method list.

