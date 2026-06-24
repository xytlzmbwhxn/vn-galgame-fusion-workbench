# Deep Narrative Audit

Project: `017_便利店把雨收好`
Script: `02_generated_content\scripts\csv\convenience_rain_punctuation_liveliness_v4.csv`
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
- rows: 134
- row_types: {"command": 4, "narration": 30, "dialogue": 90, "thought": 8, "choice": 2}
- speakers: {"CHR_jiangchi": 34, "CHR_linyan": 56}
- memory_refs: -
- choice S001_v4_0134: 打印小票。明天凭这个来还伞。 -> S001_BRANCH_A | branch_state=receipt_proof
- choice S001_v4_0135: 只写失物本。我记得你。 -> S001_BRANCH_B | branch_state=memory_trust

### S001_BRANCH_A
- rows: 18
- row_types: {"narration": 4, "dialogue": 10, "thought": 2, "command": 2}
- speakers: {"CHR_jiangchi": 4, "CHR_linyan": 6}
- memory_refs: -

### S001_BRANCH_B
- rows: 20
- row_types: {"narration": 3, "dialogue": 14, "thought": 2, "command": 1}
- speakers: {"CHR_jiangchi": 6, "CHR_linyan": 8}
- memory_refs: -

### S001_REJOIN
- rows: 99
- row_types: {"narration": 25, "dialogue": 65, "thought": 6, "command": 3}
- speakers: {"CHR_linyan": 40, "CHR_jiangchi": 25}
- memory_refs: -

## Character Control

- `CHR_heyi` rows=0, state=True, memory=True, retrieval_blocks=1, voice_targets=[]
- `CHR_jiangchi` rows=69, state=True, memory=True, retrieval_blocks=2, voice_targets=['CHR_jiangchi']
- `CHR_linyan` rows=110, state=True, memory=True, retrieval_blocks=2, voice_targets=['CHR_linyan']

## State Effects

- effect variables in CSV: branch_state
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `99_内部工作\质检报告\当前\convenience_rain_punctuation_liveliness_v4_deep_audit.json`
