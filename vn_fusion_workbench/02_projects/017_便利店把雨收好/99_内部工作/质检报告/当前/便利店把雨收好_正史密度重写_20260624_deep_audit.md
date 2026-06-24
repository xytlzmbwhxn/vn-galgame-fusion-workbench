# Deep Narrative Audit

Project: `017_便利店把雨收好`
Script: `02_generated_content\scripts\csv\便利店把雨收好_正史密度重写_20260624.csv`
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
- rows: 36
- row_types: {"narration": 5, "dialogue": 23, "thought": 4, "command": 2, "choice": 2}
- speakers: {"CHR_jiangchi": 8, "CHR_linyan": 15}
- memory_refs: -
- choice S001_035A: 按失物流程登记 -> S001_036A | umbrella_recorded=true
- choice S001_035B: 先拿箱里的蓝伞给她确认 -> S001_036B | early_trust=true

### S001_036A
- rows: 5
- row_types: {"dialogue": 5}
- speakers: {"CHR_jiangchi": 3, "CHR_linyan": 2}
- memory_refs: -

### S001_036B
- rows: 58
- row_types: {"narration": 6, "dialogue": 45, "command": 4, "thought": 1, "choice": 2}
- speakers: {"CHR_linyan": 25, "CHR_jiangchi": 20}
- memory_refs: -
- choice S001_092A: 把小票夹进失物本 -> S001_093A | receipt_kept=true
- choice S001_092B: 不留小票，只记线索 -> S001_093B | receipt_hidden=true

### S001_093A
- rows: 5
- row_types: {"narration": 1, "dialogue": 4}
- speakers: {"CHR_jiangchi": 3, "CHR_linyan": 1}
- memory_refs: -

### S001_093B
- rows: 32
- row_types: {"narration": 4, "dialogue": 24, "command": 3, "thought": 1}
- speakers: {"CHR_jiangchi": 10, "CHR_linyan": 14}
- memory_refs: -

### S002_午休四十分钟
- rows: 51
- row_types: {"narration": 11, "dialogue": 37, "thought": 2, "command": 1}
- speakers: {"CHR_linyan": 26, "CHR_jiangchi": 11}
- memory_refs: -

### S003_晚自习前的寄存格
- rows: 78
- row_types: {"narration": 13, "dialogue": 55, "thought": 4, "command": 6}
- speakers: {"CHR_heyi": 3, "CHR_jiangchi": 21, "CHR_linyan": 31}
- memory_refs: -

## Character Control

- `CHR_heyi` rows=3, state=True, memory=True, retrieval_blocks=2, voice_targets=['CHR_heyi']
- `CHR_jiangchi` rows=76, state=True, memory=True, retrieval_blocks=4, voice_targets=['CHR_jiangchi']
- `CHR_linyan` rows=114, state=True, memory=True, retrieval_blocks=4, voice_targets=['CHR_linyan']

## State Effects

- effect variables in CSV: early_trust, receipt_hidden, receipt_kept, trust_plus, trust_repaired, umbrella_recorded
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `99_内部工作\质检报告\当前\便利店把雨收好_正史密度重写_20260624_deep_audit.json`
