---
id: vn_quality_debt_attribution
type: method_card
---

# VN Quality Debt Attribution

## Call This When

Call this after a serious CSV draft, rewrite, or QA pass, especially when the
draft "passes" mechanically but still feels flat, fragmented, preachy, or unlike
a playable Galgame scene.

## Core Rule

Do not collapse all writing problems into "文笔不好". Classify the debt by the
part of the VN production chain that failed.

## Debt Types

- `click_unit_low_payload`: a click advances almost nothing.
- `click_unit_overfragmented`: one speaker is split into low-value micro rows.
- `thought_missing`: the scene lacks private inference, hidden cost, or player-side pressure.
- `thought_misclassified_narration`: camera-visible action is written as inner thought.
- `flat_voice`: a character lacks sentence shape, social mask, body habit, or pressure punctuation.
- `punctuation_energy_loss`: lines close too neatly and do not feel actable.
- `preachy_dialogue`: characters explain theme, advice, or writing theory instead of pursuing an agenda.
- `performance_cue_gap`: dialogue needs expression, body action, SFX, BGM, or screen-state support.
- `theme_not_playable`: the theme exists as an idea but not as player behavior and cost.
- `state_unremembered`: choices, information, or relationship changes are not written into effects or memory refs.

## Repair Routing

- Click debt -> merge, delete, or re-split rows by click function.
- Thought debt -> rewrite as private inference, self-deception, risk, or unsaid motive.
- Voice debt -> read character card/runtime state, then revise changed rows only.
- Punctuation debt -> add character-owned interruption, hesitation, tease, refusal, or unfinished pressure.
- Preachy debt -> convert explanation into request, refusal, bargain, mistake, object operation, or relation cost.
- Performance debt -> add production cue, sprite expression, body action, sound, or camera state.
- Theme debt -> add a choice, resource spend, route lock, evidence flag, or repeated playable behavior.
- State debt -> add effects, memory refs, route flags, or delayed callback hooks.

## Local Tool

```powershell
py .\00_workbench_core\tools\vn_control_room.py quality-debt --project <project_id>
```

The report is written to:

```text
02_projects/<project_id>/99_内部工作/质检报告/当前/
```

## Output Contract

Every serious delivery should be able to say whether the quality debt pass was
run, where the report is, and which debt categories remain.
