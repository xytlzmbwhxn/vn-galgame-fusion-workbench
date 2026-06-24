# Deep Narrative Audit

Project: `summer_echo_demo`
Script: `02_generated_content/scripts/csv/S001_summer_echo_v1.csv`
Scene: `S001`

## Result

- [ISSUE] Unresolved branch targets: S001_branch_borrowed_voice, S001_branch_leave_unsaid, S001_branch_own_voice
- [ISSUE] Unknown memory_refs: [CHR_linzhishi], [CHR_linzhishi][OBJ_empty_binder][OBJ_pencil][branch_borrowed_voice], [CHR_linzhishi][OBJ_empty_binder][subtext], [CHR_linzhishi][OBJ_pencil][OBJ_score_page_10][forbidden_line], [CHR_linzhishi][OBJ_pencil][branch_borrowed_voice], [CHR_linzhishi][OBJ_pencil][branch_own_voice], [CHR_linzhishi][OBJ_pencil][character_lie], [CHR_linzhishi][OBJ_pencil][dodge], [CHR_linzhishi][OBJ_pencil][professional_ritual], [CHR_linzhishi][OBJ_piano][branch_leave_unsaid], [CHR_linzhishi][OBJ_piano][branch_own_voice], [CHR_linzhishi][OBJ_piano][character_lie], [CHR_linzhishi][OBJ_score_page_10], [CHR_linzhishi][OBJ_score_page_10][branch_borrowed_voice], [CHR_linzhishi][OBJ_score_page_10][character_lie], [CHR_linzhishi][OBJ_score_shelf], [CHR_linzhishi][dodge], [CHR_linzhishi][embodied_action], [CHR_linzhishi][forbidden_line][branch_own_voice], [CHR_linzhishi][voice_state_memory], [CHR_tangxu], [CHR_tangxu][OBJ_empty_binder], [CHR_tangxu][OBJ_empty_binder][OBJ_pencil][sequel_decision], [CHR_tangxu][OBJ_empty_binder][character_lie], [CHR_tangxu][OBJ_pencil][OBJ_empty_binder][branch_borrowed_voice], [CHR_tangxu][OBJ_pencil][branch_borrowed_voice], [CHR_tangxu][OBJ_pencil][sequel_decision], [CHR_tangxu][OBJ_piano_cover], [CHR_tangxu][OBJ_piano_cover][subtext], [CHR_tangxu][OBJ_piano_cover][voice_state_memory], [CHR_tangxu][OBJ_score_page_10], [CHR_tangxu][OBJ_score_page_10][subtext], [CHR_tangxu][THR_echo][branch_borrowed_voice], [CHR_tangxu][branch_leave_unsaid], [CHR_tangxu][branch_own_voice], [CHR_tangxu][forbidden_line][voice_state_memory], [CHR_tangxu][scene_question], [THR_echo], [choice_mental_model], [choice_mental_model][memory_refs], click_function=attack+relationship_cost, click_function=choice_pressure, click_function=private_inference, click_function=private_inference+choice_pressure, click_function=private_inference+new_info, click_function=relationship_cost+breath_control, click_function=reply_pressure, click_function=reply_pressure+new_info, click_function=screen_state, click_function=screen_state+breath_control, click_function=screen_state+new_info, click_function=screen_state+reply_pressure, click_function=screen_state+state_effect, click_function=test

## Branch Graph

### __START__
- rows: 95
- row_types: {"narration": 31, "thought": 9, "dialogue": 49, "choice": 3, "command": 3}
- speakers: {"CHR_tangxu": 27, "CHR_linzhishi": 22}
- memory_refs: [CHR_linzhishi], [CHR_linzhishi][OBJ_empty_binder][OBJ_pencil][branch_borrowed_voice], [CHR_linzhishi][OBJ_empty_binder][subtext], [CHR_linzhishi][OBJ_pencil][OBJ_score_page_10][forbidden_line], [CHR_linzhishi][OBJ_pencil][branch_borrowed_voice], [CHR_linzhishi][OBJ_pencil][branch_own_voice], [CHR_linzhishi][OBJ_pencil][character_lie], [CHR_linzhishi][OBJ_pencil][dodge], [CHR_linzhishi][OBJ_pencil][professional_ritual], [CHR_linzhishi][OBJ_piano][branch_leave_unsaid], [CHR_linzhishi][OBJ_piano][branch_own_voice], [CHR_linzhishi][OBJ_piano][character_lie], [CHR_linzhishi][OBJ_score_page_10], [CHR_linzhishi][OBJ_score_page_10][branch_borrowed_voice], [CHR_linzhishi][OBJ_score_page_10][character_lie], [CHR_linzhishi][OBJ_score_shelf], [CHR_linzhishi][dodge], [CHR_linzhishi][embodied_action], [CHR_linzhishi][forbidden_line][branch_own_voice], [CHR_linzhishi][voice_state_memory], [CHR_tangxu], [CHR_tangxu][OBJ_empty_binder], [CHR_tangxu][OBJ_empty_binder][OBJ_pencil][sequel_decision], [CHR_tangxu][OBJ_empty_binder][character_lie], [CHR_tangxu][OBJ_pencil][OBJ_empty_binder][branch_borrowed_voice], [CHR_tangxu][OBJ_pencil][branch_borrowed_voice], [CHR_tangxu][OBJ_pencil][sequel_decision], [CHR_tangxu][OBJ_piano_cover], [CHR_tangxu][OBJ_piano_cover][subtext], [CHR_tangxu][OBJ_piano_cover][voice_state_memory], [CHR_tangxu][OBJ_score_page_10], [CHR_tangxu][OBJ_score_page_10][subtext], [CHR_tangxu][THR_echo][branch_borrowed_voice], [CHR_tangxu][branch_leave_unsaid], [CHR_tangxu][branch_own_voice], [CHR_tangxu][forbidden_line][voice_state_memory], [CHR_tangxu][scene_question], [THR_echo], [choice_mental_model], [choice_mental_model][memory_refs], click_function=attack+relationship_cost, click_function=choice_pressure, click_function=private_inference, click_function=private_inference+choice_pressure, click_function=private_inference+new_info, click_function=relationship_cost+breath_control, click_function=reply_pressure, click_function=reply_pressure+new_info, click_function=screen_state, click_function=screen_state+breath_control, click_function=screen_state+new_info, click_function=screen_state+reply_pressure, click_function=screen_state+state_effect, click_function=test
- choice S001_055: 替我自己。替一首烂掉的歌。 -> S001_branch_own_voice | truth_admitted=self;trust_tangxu=3;shame_tangxu=4
- choice S001_056: 沉默——弹了三个小节。不回答。 -> S001_branch_leave_unsaid | truth_admitted=music;trust_tangxu=2;curiosity_tangxu=4
- choice S001_057: 替许声远。这个教室应该有人替他把最后一张谱弹完。 -> S001_branch_borrowed_voice | truth_admitted=xushengyuan;trust_tangxu=3;shame_linzhishi=2

## Character Control

- `CHR_linzhishi` rows=22, state=True, memory=True, retrieval_blocks=4, voice_targets=['CHR_linzhishi']
- `CHR_tangxu` rows=27, state=True, memory=True, retrieval_blocks=5, voice_targets=['CHR_tangxu']

## State Effects

- effect variables in CSV: curiosity, curiosity_tangxu, fatigue, fear, shame, shame_linzhishi, shame_tangxu, trust, trust_tangxu, truth_admitted
- state delta mismatches: 0

## Source Lessons Applied

- Yarn Spinner: node/block/destination analysis.
- ink: authored flow is not trusted until references resolve.
- Ren'Py: lint labels, jumps, choices, and expression boundaries.
- TwineJS: use ids/tags as searchable story metadata.
- Character memory systems: stable card + runtime state + retrievable memory blocks.

Machine-readable payload: `04_quality/reports/S001_summer_echo_v1_deep_audit.json`
