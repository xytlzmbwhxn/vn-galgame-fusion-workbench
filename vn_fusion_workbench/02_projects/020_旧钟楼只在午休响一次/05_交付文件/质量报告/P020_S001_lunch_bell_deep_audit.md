# Deep Narrative Audit

Project: `020_旧钟楼只在午休响一次`
Script: `02_generated_content\scripts\csv\P020_S001_lunch_bell.csv`
Scene: `S001`

## Result

- PASS: graph, refs, state effects, and character-control layers are aligned.

## Branch Graph

### __START__
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### start
- rows: 23
- row_types: {"narration": 4, "thought": 3, "dialogue": 13, "choice": 3}
- speakers: {"CHR_shenlu": 4, "CHR_fuyao": 6, "CHR_wenmian": 3}
- memory_refs: ARC_fuyao_request, ARC_shenlu_visible, ARC_wenmian_soft_threat, CHR_fuyao, CHR_shenlu, CHR_wenmian, FS_bell_1217, MEM_fuyao_broadcast_cover, MEM_fuyao_volume_knob, MEM_shenlu_key_ring, MEM_shenlu_lunch_delay, MEM_wenmian_empty_cup, MEM_wenmian_pudding_debt, MEM_wenmian_soft_pressure, THR_lunch_bell
- choice S001_0022: 先让钟楼冷静下来 -> branch_calm | choice_label_48=branch_calm; trust_fuyao += 1; bell_clue += 1
- choice S001_0023: 先处理布丁赔偿问题 -> branch_snack | choice_label_48=branch_snack; trust_wenmian += 1; bell_clue += 1
- choice S001_0024: 声明自己只是路过 -> branch_escape | choice_label_48=branch_escape; shenlu_escape_debt += 1; bell_clue += 1

### branch_calm
- rows: 4
- row_types: {"dialogue": 3, "command": 1}
- speakers: {"CHR_shenlu": 1, "CHR_fuyao": 1, "CHR_wenmian": 1}
- memory_refs: ARC_fuyao_request, ARC_wenmian_soft_threat, CHR_fuyao, CHR_shenlu, CHR_wenmian, MEM_fuyao_broadcast_cover, THR_lunch_bell
- jump S001_0029: -> merge_after_choice

### branch_snack
- rows: 4
- row_types: {"dialogue": 3, "command": 1}
- speakers: {"CHR_shenlu": 1, "CHR_wenmian": 1, "CHR_fuyao": 1}
- memory_refs: ARC_fuyao_request, ARC_wenmian_soft_threat, CHR_fuyao, CHR_shenlu, CHR_wenmian, MEM_wenmian_pudding_debt, THR_lunch_bell
- jump S001_0034: -> merge_after_choice

### branch_escape
- rows: 5
- row_types: {"dialogue": 3, "thought": 1, "command": 1}
- speakers: {"CHR_shenlu": 1, "CHR_fuyao": 1, "CHR_wenmian": 1}
- memory_refs: CHR_fuyao, CHR_shenlu, CHR_wenmian, MEM_fuyao_needs_shenlu, MEM_shenlu_key_ring, MEM_wenmian_soft_pressure, THR_lunch_bell
- jump S001_0040: -> merge_after_choice

### merge_after_choice
- rows: 15
- row_types: {"narration": 3, "dialogue": 10, "thought": 1, "command": 1}
- speakers: {"CHR_fuyao": 4, "CHR_shenlu": 3, "CHR_wenmian": 3}
- memory_refs: ARC_fuyao_request, ARC_shenlu_visible, ARC_wenmian_soft_threat, CHR_fuyao, CHR_shenlu, CHR_wenmian, FS_bell_1217, MEM_fuyao_needs_shenlu, MEM_wenmian_empty_cup, MEM_wenmian_pudding_debt, THR_lunch_bell
- jump S001_0056: -> END

## Character Control

- `CHR_fuyao` rows=13, state=True, memory=True, retrieval_blocks=3, voice_targets=['CHR_fuyao']
- `CHR_shenlu` rows=10, state=True, memory=True, retrieval_blocks=3, voice_targets=['CHR_shenlu']
- `CHR_wenmian` rows=9, state=True, memory=True, retrieval_blocks=3, voice_targets=['CHR_wenmian']

## State Effects

- effect variables in CSV: bell_clue, choice_label_48, shenlu_escape_debt, trust_fuyao, trust_wenmian
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `99_内部工作\质检报告\当前\P020_S001_lunch_bell_deep_audit.json`
