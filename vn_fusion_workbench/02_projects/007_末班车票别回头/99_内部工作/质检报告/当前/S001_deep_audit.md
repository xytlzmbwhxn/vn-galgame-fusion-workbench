# Deep Narrative Audit

Project: `last_bus_ticket_demo`
Script: `02_generated_content\scripts\csv\S001_last_bus_ticket_v1.csv`
Scene: `S001`

## Result

- PASS: graph, refs, state effects, and character-control layers are aligned.

## Branch Graph

### __START__
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

### START
- rows: 45
- row_types: {"narration": 2, "command": 4, "thought": 7, "dialogue": 29, "choice": 3}
- speakers: {"CHR_linyu": 15, "CHR_qiaomeng": 14}
- memory_refs: ARC_linyu_procedure_to_witness, ARC_qiaomeng_joke_to_bell, CHR_duanbo, CHR_linyu, CHR_qiaomeng, FS_duanbo_key, FS_orange_charm, FS_wet_ticket, OBJ_bell, OBJ_green_stamp, OBJ_ticket_stub, OBJ_wet_ticket, QS_old_station_mark, THR_linyu_father, THR_qiaomeng_grandma, THR_station_exists
- choice BP042: 按旧线路盖章 -> STAMP_OLD | old_station_mark=stamp;trust_qiaomeng+=2;duanbo_warning+=2
- choice BP043: 留下票根证据 -> KEEP_STUB | old_station_mark=stub;trust_qiaomeng+=1;duanbo_warning+=1
- choice BP044: 让她亲自按铃 -> RING_BELL | old_station_mark=bell;trust_qiaomeng+=2;duanbo_warning+=3

### STAMP_OLD
- rows: 4
- row_types: {"dialogue": 3, "command": 1}
- speakers: {"CHR_linyu": 2, "CHR_qiaomeng": 1}
- memory_refs: CHR_linyu, CHR_qiaomeng, FS_wet_ticket, OBJ_green_stamp, OBJ_wet_ticket
- jump BP049: -> MERGE

### KEEP_STUB
- rows: 4
- row_types: {"dialogue": 3, "command": 1}
- speakers: {"CHR_linyu": 2, "CHR_qiaomeng": 1}
- memory_refs: CHR_linyu, CHR_qiaomeng, FS_wet_ticket, OBJ_ticket_stub
- jump BP054: -> MERGE

### RING_BELL
- rows: 6
- row_types: {"dialogue": 4, "command": 2}
- speakers: {"CHR_linyu": 2, "CHR_qiaomeng": 2}
- memory_refs: ARC_qiaomeng_joke_to_bell, CHR_linyu, CHR_qiaomeng, OBJ_bell, QS_old_station_mark
- jump BP061: -> MERGE

### MERGE
- rows: 24
- row_types: {"command": 1, "dialogue": 18, "thought": 4, "narration": 1}
- speakers: {"CHR_duanbo": 7, "CHR_qiaomeng": 6, "CHR_linyu": 5}
- memory_refs: ARC_duanbo_silence_to_key, ARC_linyu_procedure_to_witness, ARC_qiaomeng_joke_to_bell, CHR_duanbo, CHR_linyu, CHR_qiaomeng, FS_duanbo_key, FS_old_manual, FS_orange_charm, OBJ_bell, OBJ_old_manual, OBJ_wet_ticket, QS_duanbo_warning, QS_old_station_mark, THR_linyu_father, THR_qiaomeng_grandma, THR_station_exists

### END
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

## Character Control

- `CHR_duanbo` rows=7, state=True, memory=True, retrieval_blocks=4, voice_targets=['block', 'gruff', 'gruff_close', 'hard_entry', 'pressure', 'rough_care', 'warning']
- `CHR_linyu` rows=26, state=True, memory=True, retrieval_blocks=4, voice_targets=['accept_cost', 'ask', 'care_operation', 'care_order', 'choice_detail', 'choice_frame', 'deadpan', 'decision_bell', 'decision_stamp', 'decision_stub', 'dry_reply', 'honest', 'invitation', 'limited_help', 'machine_mutter', 'operation', 'plain_tender', 'procedure', 'quiet_promise', 'rule_first', 'rule_soft', 'soft_boundary', 'stand', 'understated']
- `CHR_qiaomeng` rows=24, state=True, memory=True, retrieval_blocks=4, voice_targets=['accept_cute', 'banter_fear', 'brave_joke', 'bright_probe', 'cute_push', 'defend_small', 'hope_joke', 'joke_drop', 'memory_leak', 'nervous_joke', 'panic_cute', 'playful_defense', 'protest_cute', 'relief_bright', 'relief_play', 'relief_tease', 'request', 'request_true', 'resist_soft', 'self_ready', 'small_question', 'tease', 'tease_nervous', 'truth_small']

## State Effects

- effect variables in CSV: duanbo_warning, old_station_mark, trust_qiaomeng
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `04_quality\reports\S001_deep_audit.json`
