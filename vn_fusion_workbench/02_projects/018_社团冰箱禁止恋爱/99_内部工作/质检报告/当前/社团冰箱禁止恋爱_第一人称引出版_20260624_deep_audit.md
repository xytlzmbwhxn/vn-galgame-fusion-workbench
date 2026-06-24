# Deep Narrative Audit

Project: `018_社团冰箱禁止恋爱`
Script: `02_generated_content\scripts\csv\社团冰箱禁止恋爱_第一人称引出版_20260624.csv`
Scene: `S001`

## Result

- PASS: graph, refs, state effects, and character-control layers are aligned.

## Branch Graph

### __START__
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### S001_冰箱先生今天也不收情书
- rows: 130
- row_types: {"narration": 49, "thought": 10, "dialogue": 68, "comment": 1, "choice": 2}
- speakers: {"CHR_xia_li": 44, "CHR_gu_huai": 24}
- memory_refs: CHR_gu_huai, CHR_xia_li
- choice S001_delivery_0130: 按流程登记为冷藏凭证 -> S001_A | note_as_receipt=true
- choice S001_delivery_0131: 直接问“这张是给我的吗” -> S001_B | direct_question=true

### S001_A
- rows: 24
- row_types: {"dialogue": 20, "narration": 4}
- speakers: {"CHR_gu_huai": 9, "CHR_xia_li": 11}
- memory_refs: CHR_gu_huai, CHR_xia_li

### S001_REJOIN
- rows: 15
- row_types: {"narration": 5, "dialogue": 7, "thought": 2, "command": 1}
- speakers: {"CHR_xia_li": 5, "CHR_gu_huai": 2}
- memory_refs: CHR_gu_huai, CHR_xia_li

### S001_B
- rows: 36
- row_types: {"dialogue": 27, "narration": 8, "command": 1}
- speakers: {"CHR_gu_huai": 12, "CHR_xia_li": 15}
- memory_refs: CHR_gu_huai, CHR_xia_li
- jump S001_delivery_0209: -> S001_REJOIN

## Character Control

- `CHR_gu_huai` rows=47, state=True, memory=True, retrieval_blocks=5, voice_targets=[]
- `CHR_xia_li` rows=75, state=True, memory=True, retrieval_blocks=5, voice_targets=[]

## State Effects

- effect variables in CSV: direct_question, note_as_receipt
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `99_内部工作\质检报告\当前\社团冰箱禁止恋爱_第一人称引出版_20260624_deep_audit.json`
