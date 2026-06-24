---
id: style_asset_prompt_compiler
type: method_card
---

# Style Asset Prompt Compiler

## Call This When

When style rules, anti-AI rules, reference learning, or writing methods need to
become executable generation constraints.

## Core Rule

Do not pass raw JSON, long notes, or scattered method summaries directly to an AI
model. Compile them into layered prompt blocks.

## Layers

1. `context`: project premise, scene task, player role, current pressure.
2. `style`: reusable writing methods and selected style asset rules.
3. `character`: stable cards, runtime state, voice signatures, relationship costs.
4. `anti_ai`: forbidden, risk, and encouraged behavior.
5. `output`: required artifact format, CSV/readable/script target.
6. `self_check`: short final check before output.

## VN-Specific Compile Priorities

- Click unit rules outrank generic sentence beauty.
- Character voice and current runtime state outrank broad style labels.
- Anti-AI bans must be concrete: no thesis summary, no fake thought, no one-speaker-one-row chopping.
- Output format must be explicit: readable Gal draft, CSV rows, revision plan, or QA report.

## Failure Signs

- The prompt contains the whole method index without task-specific selection.
- The model receives project memory but no output contract.
- The AI call writes prose that is not saved under `02_generated_content/`.
- The result is treated as canon before validation.

