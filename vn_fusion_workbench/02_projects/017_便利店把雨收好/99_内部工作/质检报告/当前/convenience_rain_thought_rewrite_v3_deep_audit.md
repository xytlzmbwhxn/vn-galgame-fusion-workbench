# Deep Narrative Audit

Project: `017_便利店把雨收好`
Script: `02_generated_content\scripts\csv\convenience_rain_thought_rewrite_v3.csv`
Scene: `S001`

## Result

- PASS: graph, refs, state effects, and character-control layers are aligned.

## Branch Graph

### __START__
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### S001_雨袋架旁边
- rows: 50
- row_types: {"command": 5, "narration": 12, "dialogue": 28, "thought": 4, "choice": 1}
- speakers: {"CHR_jiangchi": 10, "CHR_linyan": 18}
- memory_refs: CHR_jiangchi, CHR_linyan, THR_blue_umbrella, THR_receipt_debt
- choice S001_0051: 按失物流程登记 -> CHOICE_01_A | umbrella_recorded=true; trust_style=procedure

### CHOICE_01_A
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### LINE_043_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_044_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_045_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_046_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_047_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_048_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_049_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_050_A
- rows: 2
- row_types: {"command": 1, "choice": 1}
- speakers: {}
- memory_refs: THR_blue_umbrella, THR_receipt_debt
- choice S001_0069: 先把箱里的蓝伞拿给她确认 -> CHOICE_01_B | early_trust=true; registration_delayed=true

### CHOICE_01_B
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### LINE_052_B
- rows: 2
- row_types: {"narration": 2}
- speakers: {}
- memory_refs: -

### LINE_053_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_054_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_055_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_056_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_057_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_058_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_059_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_060_B
- rows: 1
- row_types: {"narration": 1}
- speakers: {}
- memory_refs: -

### LINE_061_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_062_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_063_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_064_B
- rows: 2
- row_types: {"command": 2}
- speakers: {}
- memory_refs: -

### CHOICE_01_REJOIN
- rows: 78
- row_types: {"dialogue": 54, "command": 4, "narration": 17, "thought": 2, "choice": 1}
- speakers: {"CHR_jiangchi": 26, "CHR_linyan": 28}
- memory_refs: CHR_jiangchi, CHR_linyan, THR_blue_umbrella, THR_receipt_debt
- choice S001_0177: 把小票夹进失物本 -> CHOICE_02_A | receipt_kept=true; heyi_risk=true

### CHOICE_02_A
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### LINE_136_A
- rows: 1
- row_types: {"narration": 1}
- speakers: {}
- memory_refs: -

### LINE_137_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_138_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_139_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_140_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_141_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_142_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_143_A
- rows: 2
- row_types: {"command": 1, "choice": 1}
- speakers: {}
- memory_refs: THR_blue_umbrella, THR_receipt_debt
- choice S001_0195: 不留小票，只记下线索 -> CHOICE_02_B | receipt_hidden=true; memory_debt=true

### CHOICE_02_B
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### LINE_145_B
- rows: 1
- row_types: {"narration": 1}
- speakers: {}
- memory_refs: -

### LINE_146_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_147_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_148_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_149_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_150_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_151_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_152_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_153_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_154_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_155_B
- rows: 2
- row_types: {"command": 2}
- speakers: {}
- memory_refs: -

### CHOICE_02_REJOIN
- rows: 48
- row_types: {"narration": 12, "dialogue": 32, "thought": 2, "command": 2}
- speakers: {"CHR_linyan": 17, "CHR_jiangchi": 15}
- memory_refs: CHR_jiangchi, CHR_linyan

### S002_午休四十分钟
- rows: 36
- row_types: {"command": 4, "narration": 13, "dialogue": 17, "thought": 2}
- speakers: {"CHR_heyi": 1, "CHR_linyan": 11, "CHR_jiangchi": 5}
- memory_refs: CHR_heyi, CHR_jiangchi, CHR_linyan

### LINE_226_A
- rows: 2
- row_types: {"narration": 2}
- speakers: {}
- memory_refs: -

### LINE_227_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_228_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_229_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_230_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_231_A
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_232_A
- rows: 2
- row_types: {"command": 2}
- speakers: {}
- memory_refs: -

### LINE_234_B
- rows: 2
- row_types: {"narration": 2}
- speakers: {}
- memory_refs: -

### LINE_235_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_236_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_237_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_238_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_239_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_240_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_241_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_242_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_243_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_jiangchi": 1}
- memory_refs: CHR_jiangchi

### LINE_244_B
- rows: 1
- row_types: {"dialogue": 1}
- speakers: {"CHR_linyan": 1}
- memory_refs: CHR_linyan

### LINE_245_B
- rows: 57
- row_types: {"command": 6, "narration": 14, "dialogue": 35, "thought": 2}
- speakers: {"CHR_linyan": 22, "CHR_jiangchi": 13}
- memory_refs: CHR_jiangchi, CHR_linyan

### S003_晚自习前的寄存格
- rows: 150
- row_types: {"command": 9, "narration": 39, "dialogue": 95, "thought": 7}
- speakers: {"CHR_heyi": 5, "CHR_jiangchi": 32, "CHR_linyan": 58}
- memory_refs: CHR_heyi, CHR_jiangchi, CHR_linyan

## Character Control

- `CHR_heyi` rows=6, state=True, memory=True, retrieval_blocks=1, voice_targets=['CHR_heyi']
- `CHR_jiangchi` rows=124, state=True, memory=True, retrieval_blocks=2, voice_targets=['CHR_jiangchi']
- `CHR_linyan` rows=178, state=True, memory=True, retrieval_blocks=2, voice_targets=['CHR_linyan']

## State Effects

- effect variables in CSV: early_trust, heyi_risk, memory_debt, receipt_hidden, receipt_kept, registration_delayed, trust_plus, trust_repaired, trust_style, umbrella_recorded
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `99_内部工作\质检报告\当前\convenience_rain_thought_rewrite_v3_deep_audit.json`
