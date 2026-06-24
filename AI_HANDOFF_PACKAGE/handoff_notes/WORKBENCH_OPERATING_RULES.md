# Workbench Operating Rules

## Startup

Read in order:

1. `START_HERE.md`
2. `项目结构总览.md`
3. `skills/portable_skill_manifest.json`
4. `skills/galgame-workbench-loader/SKILL.md`
5. `skills/vn-fusion-writer/SKILL.md`
6. `skills/vn-scene-drafting/SKILL.md`
7. `skills/vn-presence-revision/SKILL.md`
8. `skills/vn-character-memory/SKILL.md`
9. `AI_HANDOFF_PACKAGE/handoff_notes/CURRENT_TASK_STATE.md`
10. `AI_HANDOFF_PACKAGE/handoff_notes/WORKBENCH_OPERATING_RULES.md`
11. `AI_HANDOFF_PACKAGE/handoff_notes/OTHER_AI_FAILURE_PREVENTION.md`
12. `vn_fusion_workbench/00_workbench_core/docs/METHOD_CALLING_WORKFLOW.md`
13. `vn_fusion_workbench/00_workbench_core/docs/FULL_GENERATION_FLOW_PUBLIC.md`
14. `vn_fusion_workbench/00_workbench_core/docs/PATH_ALIAS_PROTOCOL.md`
15. `vn_fusion_workbench/00_workbench_core/methods/method_index.json`

Then run:

```powershell
cd <repo>\vn_fusion_workbench
py .\00_workbench_core\tools\vn_context_bootstrap.py --project <Pxxx> --task <draft|rewrite|review>
```

## Portable Skills

Do not rely on host-level installed skills. Use bundled skills:

```text
skills/
vn_fusion_workbench/00_workbench_core/portable_skills/
AI_HANDOFF_PACKAGE/portable_skills/
```

Mandatory VN/Gal skills:

- `galgame-workbench-loader`
- `vn-fusion-writer`
- `vn-scene-drafting`
- `vn-presence-revision`
- `vn-character-memory`

Mandatory failure-prevention and style markers for handoff guards:

- `OTHER_AI_FAILURE_PREVENTION`
- `spoken_private_thought_texture`
- `interior_breath_relaxation`
- `complete_delivery_package_contract`

## Positive Constraint Model

A-type constraints are floors and must never be removed:

- encoding guard;
- CSV / label / choice / branch format;
- unresolved branch target checks;
- delivery completeness checks;
- no internal tags in user-facing output;
- mandatory skills backup check.

B-type constraints are craft guides:

- private thought must be character-owned, not author explanation;
- relaxed interiority can use fillers, half-jokes, self-corrections and softening particles;
- dialogue blocks can use same-speaker runs and interruptions;
- choices must leave state, object, relationship, route or information debt;
- complete delivery includes readable MD, source CSV, public CSV, Excel, engine exports, character cards, character brief, QA reports, runtime states, memory logs and route map.

Do not loosen A-type gates to make a draft pass. Fix the artifact.

## Writing Rules

- A row is a click unit, not a speaker unit.
- New characters need soft introduction through scene pressure, object, action, relation or question. Do not open by dumping “我叫……我是……” unless the story has a deliberate reason.
- Dialogue can run in blocks. Do not mechanically alternate A/B/A/B across a long exchange.
- Thought rows must contain private inference, hesitation, self-defense, route pressure or unsaid cost. If a camera can film it, it is narration/stage, not thought.
- Casual breath matters: “嗯……当然？它应该没有抗议功能。” is different from a flat declarative sentence. Use particles, relaxation, half-retreats and punctuation when the character position calls for them.
- Do not explain the theme. Convert thesis sentences into requests, refusals, bargains, object operations, relationship cost or playable choice pressure.

## Required Method Cards

For serious Chinese VN/Galgame drafting or revision, load:

```text
00_workbench_core/methods/chinese_vn_generation_hard_gates.md
00_workbench_core/methods/deep_vn_corpus_application.md
00_workbench_core/methods/vn_style_handprint_fusion.md
00_workbench_core/methods/dialogue_block_ownership.md
00_workbench_core/methods/pov_interiority_control.md
00_workbench_core/methods/spoken_private_thought_texture.md
00_workbench_core/methods/interior_breath_relaxation.md
00_workbench_core/methods/complete_delivery_package_contract.md
```

## Delivery Rule

Never claim completion from a readable draft alone. Use:

```powershell
py .\00_workbench_core\tools\vn_delivery_completeness_guard.py --project <Pxxx> --strict
py .\00_workbench_core\tools\vn_handoff_guard.py --target <readable.md> --strict
```

After generation/export:

```powershell
py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation
py .\00_workbench_core\tools\vn_workspace_cleanup.py --audit
```

## User Prompt Routing

Before substantial work, classify the newest user request:

- learning / absorbing projects -> update reusable core and public style assets;
- new writing -> create or read project memory, then draft-session;
- rewrite / critique -> diagnose failure, update method or project memory, then revise;
- continue -> resume the latest unfinished objective;
- character setup -> write and show a character brief with memory points;
- artifact request -> deliver the requested artifact, not a method summary.

If stored state conflicts with the newest user request, the newest user request wins.
