# Learning Round 2026-06-18 - Open-Source Fusion

## Implemented Upgrades

- Runtime dialogue pipeline: every CSV row now has a stricter runtime meaning and export boundary.
- Retrievable character memory blocks: stable cards, runtime state, and episodic memories are treated as separate layers.
- Plain-text project granularity: projects should remain readable through small, stable, portable files.
- Passage tag route map: branches and scenes should carry route, character, object, state, lock, and callback tags.

## Why This Matters

The user repeatedly identified two failure modes:

- quality depended on the current chat instead of a reusable workbench
- character voice and state were not obviously fixed across scenes

This learning round addresses both by making the draft session load local method cards, local character cards, runtime state, and memory blocks before writing.

## Added Method Cards

- `runtime_dialogue_pipeline`
- `retrievable_character_memory_blocks`
- `plain_text_project_granularity`
- `passage_tag_route_map`

## Verification Targets

After adding these methods, run:

```powershell
py -m py_compile .\00_workbench_core\tools\vn_workbench.py
py .\00_workbench_core\tools\vn_workbench.py draft-session --project .\02_projects\label_room_demo --scene .\02_projects\label_room_demo\01_narrative_design\scenes\scene_cards\S001_scene_card.json --draft-name S001_label_room_v1
py .\00_workbench_core\tools\vn_workbench.py validate --project .\02_projects\label_room_demo --script .\02_projects\label_room_demo\02_generated_content\scripts\csv\S001_label_room_v1.csv
```
