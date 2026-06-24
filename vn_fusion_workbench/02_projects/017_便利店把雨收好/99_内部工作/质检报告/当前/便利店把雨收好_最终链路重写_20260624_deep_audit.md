# Deep Narrative Audit

Project: `017_便利店把雨收好`
Script: `02_generated_content\scripts\csv\便利店把雨收好_最终链路重写_20260624.csv`
Scene: `S001`

## Result

- PASS: graph, refs, state effects, and character-control layers are aligned.

## Branch Graph

### __START__
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### S001_START
- rows: 139
- row_types: {"narration": 33, "dialogue": 94, "thought": 9, "command": 1, "choice": 2}
- speakers: {"CHR_jiangchi": 37, "CHR_linyan": 57}
- memory_refs: CHR_jiangchi, CHR_linyan
- choice S001_final_20260624_0139: 先按失物流程登记。 -> CHOICE_01_A | umbrella_recorded=true
- choice S001_final_20260624_0140: 先把蓝伞递给她确认。 -> CHOICE_01_B | early_trust=true

### CHOICE_01_A
- rows: 12
- row_types: {"narration": 2, "dialogue": 8, "command": 2}
- speakers: {"CHR_jiangchi": 4, "CHR_linyan": 4}
- memory_refs: CHR_jiangchi, CHR_linyan
- jump S001_final_20260624_0153: -> CHOICE_01_REJOIN

### CHOICE_01_B
- rows: 12
- row_types: {"narration": 3, "dialogue": 6, "thought": 2, "command": 1}
- speakers: {"CHR_jiangchi": 2, "CHR_linyan": 4}
- memory_refs: CHR_jiangchi, CHR_linyan

### CHOICE_01_REJOIN
- rows: 29
- row_types: {"narration": 4, "command": 1, "dialogue": 20, "thought": 2, "choice": 2}
- speakers: {"CHR_linyan": 10, "CHR_jiangchi": 10}
- memory_refs: CHR_jiangchi, CHR_linyan
- choice S001_final_20260624_0195: 打印小票。明天凭这个还伞。 -> CHOICE_02_C | receipt_kept=true
- choice S001_final_20260624_0196: 写进失物本。我记一笔。 -> CHOICE_02_D | receipt_hidden=true

### CHOICE_02_C
- rows: 16
- row_types: {"narration": 3, "dialogue": 9, "thought": 2, "command": 2}
- speakers: {"CHR_jiangchi": 3, "CHR_linyan": 6}
- memory_refs: CHR_jiangchi, CHR_linyan
- jump S001_final_20260624_0213: -> CHOICE_02_REJOIN

### CHOICE_02_D
- rows: 18
- row_types: {"narration": 3, "dialogue": 12, "thought": 2, "command": 1}
- speakers: {"CHR_jiangchi": 5, "CHR_linyan": 7}
- memory_refs: CHR_jiangchi, CHR_linyan

### CHOICE_02_REJOIN
- rows: 124
- row_types: {"narration": 35, "dialogue": 80, "thought": 8, "command": 1}
- speakers: {"CHR_jiangchi": 31, "CHR_linyan": 49}
- memory_refs: CHR_jiangchi, CHR_linyan

## Character Control

- `CHR_heyi` rows=0, state=True, memory=True, retrieval_blocks=2, voice_targets=[]
- `CHR_jiangchi` rows=92, state=True, memory=True, retrieval_blocks=4, voice_targets=['CHR_jiangchi']
- `CHR_linyan` rows=137, state=True, memory=True, retrieval_blocks=4, voice_targets=['CHR_linyan']

## State Effects

- effect variables in CSV: early_trust, receipt_hidden, receipt_kept, umbrella_recorded
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `99_内部工作\质检报告\当前\便利店把雨收好_最终链路重写_20260624_deep_audit.json`
