# Deep Narrative Audit

Project: `rain_shed_code_demo`
Script: `02_generated_content\scripts\csv\S001_rain_shed_v1.csv`
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
- rows: 64
- row_types: {"command": 7, "narration": 3, "thought": 6, "dialogue": 48}
- speakers: {"CHR_lujin": 21, "CHR_chengyan": 20, "CHR_xuzhi": 7}
- memory_refs: ARC_chengyan, ARC_lujin, ARC_xuzhi, CHR_chengyan, CHR_lujin, CHR_xuzhi, FS_rain_alarm, FS_recorder, FS_ticket_7, OBJ_logbook, OBJ_phone, OBJ_recorder, OBJ_stamp, OBJ_ticket_scanner, OBJ_ticket_slip, OBJ_umbrella_7, THR_rain_shed, THR_recorder, THR_ticket

### CHOICE
- rows: 3
- row_types: {"choice": 3}
- speakers: {}
- memory_refs: FS_rain_alarm, FS_recorder, FS_ticket_7, OBJ_logbook, OBJ_recorder, OBJ_stamp, THR_recorder, THR_ticket
- choice B068: 扫入系统，给七号伞盖章 -> LOG | choice_label_48=rain_log; trust_lujin-=1; record_clean+=1; delay_clock+=0; rule_breach+=0; kept_recording=false
- choice B069: 拧开伞柄，先看录音笔 -> OPEN | choice_label_48=rain_open; trust_lujin+=1; record_clean+=0; delay_clock+=1; rule_breach+=1; kept_recording=true
- choice B070: 改成待核验，拖过失效点 -> HOLD | choice_label_48=rain_hold; trust_lujin+=2; record_clean-=1; delay_clock+=2; rule_breach+=1; kept_recording=true

### LOG
- rows: 6
- row_types: {"narration": 1, "dialogue": 3, "thought": 1, "command": 1}
- speakers: {"CHR_chengyan": 1, "CHR_lujin": 1, "CHR_xuzhi": 1}
- memory_refs: CHR_chengyan, CHR_xuzhi, FS_recorder, OBJ_logbook, OBJ_recorder, OBJ_stamp, OBJ_ticket_slip, THR_rain_shed
- jump B077: -> REJOIN

### OPEN
- rows: 8
- row_types: {"narration": 1, "dialogue": 5, "thought": 1, "command": 1}
- speakers: {"CHR_lujin": 2, "CHR_chengyan": 2, "CHR_xuzhi": 1}
- memory_refs: ARC_chengyan, ARC_lujin, CHR_chengyan, CHR_lujin, CHR_xuzhi, FS_recorder, OBJ_recorder, OBJ_stamp, OBJ_umbrella_7, THR_rain_shed, THR_recorder
- jump B086: -> REJOIN

### HOLD
- rows: 9
- row_types: {"narration": 1, "dialogue": 6, "thought": 1, "command": 1}
- speakers: {"CHR_chengyan": 2, "CHR_lujin": 2, "CHR_xuzhi": 2}
- memory_refs: ARC_chengyan, CHR_lujin, CHR_xuzhi, FS_rain_alarm, OBJ_logbook, OBJ_stamp, OBJ_umbrella_7, THR_rain_shed, THR_recorder, THR_ticket
- jump B096: -> REJOIN

### REJOIN
- rows: 9
- row_types: {"narration": 1, "dialogue": 7, "thought": 1}
- speakers: {"CHR_lujin": 3, "CHR_chengyan": 2, "CHR_xuzhi": 2}
- memory_refs: ARC_chengyan, ARC_lujin, ARC_xuzhi, CHR_chengyan, CHR_xuzhi, FS_rain_alarm, FS_recorder, OBJ_logbook, OBJ_recorder, OBJ_stamp, OBJ_ticket_scanner, OBJ_ticket_slip, OBJ_umbrella_7, THR_recorder, THR_ticket

## Character Control

- `CHR_chengyan` rows=27, state=True, memory=True, retrieval_blocks=3, voice_targets=['流程冷幽默']
- `CHR_lujin` rows=29, state=True, memory=True, retrieval_blocks=3, voice_targets=['lively_plead', '撒娇岔题']
- `CHR_xuzhi` rows=13, state=True, memory=True, retrieval_blocks=3, voice_targets=['轻声自修正']

## State Effects

- effect variables in CSV: choice_label_48, delay_clock, kept_recording, record_clean, rule_breach, trust_lujin
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `04_quality\reports\S001_rain_shed_v1_deep_audit.json`
