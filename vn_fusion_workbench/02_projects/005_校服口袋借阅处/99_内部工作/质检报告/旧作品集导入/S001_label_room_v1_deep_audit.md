# Deep Narrative Audit

Project: `label_room_demo`
Script: `02_generated_content\scripts\csv\S001_label_room_v1.csv`
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
- row_types: {"narration": 3, "thought": 5, "dialogue": 32, "command": 2, "choice": 3}
- speakers: {"CHR_taosheng": 9, "CHR_linqiu": 11, "CHR_tangmi": 12}
- memory_refs: ARC_linqiu, ARC_tangmi, ARC_taosheng, FS_blue_card, FS_paper_star, OBJ_blue_card, OBJ_jacket_48, OBJ_paper_star, OBJ_phone, OBJ_yellow_label, STL_label_choice, THR_borrowed_time, THR_label, THR_teacher_box
- choice SC044: 贴上黄标签 -> SC_RECYCLE | choice_label_48=recycle;trust_tangmi-=1;kept_pocket_note=false;teacher_patience+=1;rule_breach=0
- choice SC045: 拆内袋留档 -> SC_ARCHIVE | choice_label_48=archive;trust_tangmi+=1;kept_pocket_note=true;teacher_patience-=1;rule_breach+=1
- choice SC046: 改借出牌 -> SC_BORROW | choice_label_48=borrow;trust_tangmi+=2;kept_pocket_note=true;teacher_patience-=2;rule_breach+=2

### SC_RECYCLE
- rows: 6
- row_types: {"dialogue": 3, "thought": 1, "command": 2}
- speakers: {"CHR_linqiu": 1, "CHR_tangmi": 1, "CHR_taosheng": 1}
- memory_refs: ARC_linqiu, ARC_tangmi, ARC_taosheng, FS_paper_star, FS_tape_sound, OBJ_yellow_label, THR_borrowed_time, THR_label
- jump SC053: -> SC_REJOIN

### SC_ARCHIVE
- rows: 8
- row_types: {"dialogue": 5, "thought": 1, "command": 2}
- speakers: {"CHR_linqiu": 2, "CHR_tangmi": 2, "CHR_taosheng": 1}
- memory_refs: ARC_linqiu, ARC_tangmi, ARC_taosheng, FS_paper_star, OBJ_paper_star, OBJ_yellow_label, THR_teacher_box
- jump SC062: -> SC_REJOIN

### SC_BORROW
- rows: 8
- row_types: {"dialogue": 5, "thought": 1, "command": 2}
- speakers: {"CHR_linqiu": 2, "CHR_tangmi": 2, "CHR_taosheng": 1}
- memory_refs: ARC_linqiu, ARC_tangmi, ARC_taosheng, FS_blue_card, OBJ_blue_card, OBJ_jacket_48, THR_label, THR_teacher_box
- jump SC071: -> SC_REJOIN

### SC_REJOIN
- rows: 14
- row_types: {"narration": 1, "dialogue": 11, "thought": 1, "command": 1}
- speakers: {"CHR_taosheng": 4, "CHR_tangmi": 5, "CHR_linqiu": 2}
- memory_refs: ARC_linqiu, ARC_tangmi, ARC_taosheng, FS_blue_card, FS_paper_star, FS_tape_sound, OBJ_blue_card, OBJ_yellow_label, THR_borrowed_time, THR_label, THR_teacher_box

### DONE
- rows: 0
- row_types: {}
- speakers: {}
- memory_refs: -

## Character Control

- `CHR_linqiu` rows=18, state=True, memory=True, retrieval_blocks=1, voice_targets=['block', 'choice_setup', 'counter', 'decision', 'dry', 'dry_block', 'dry_order', 'dry_soft', 'explain_action', 'inventory', 'probe', 'report', 'rule', 'rule_patch', 'tender_dry']
- `CHR_tangmi` rows=22, state=True, memory=True, retrieval_blocks=1, voice_targets=['ask_sideways', 'bargain', 'brace_joke', 'burst', 'claim', 'confess', 'confess_soft', 'cover', 'cover_soft', 'deflect_cute', 'fond_complain', 'hurt', 'hurt_joke', 'lie_play', 'obey_play', 'panic_joke', 'plain_turn', 'plead_plain', 'soft_tease', 'surprised_play', 'tease', 'test']
- `CHR_taosheng` rows=16, state=True, memory=True, retrieval_blocks=1, voice_targets=['phone', 'phone_alarm', 'phone_cover', 'phone_cut', 'phone_leak', 'phone_order', 'phone_practical', 'phone_press', 'phone_protect', 'phone_release', 'phone_rule', 'phone_soft_rule', 'phone_stop', 'phone_warn']

## State Effects

- effect variables in CSV: choice_label_48, kept_pocket_note, rule_breach, teacher_patience, trust_tangmi
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `04_quality\reports\S001_label_room_v1_deep_audit.json`
