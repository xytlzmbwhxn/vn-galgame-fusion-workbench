# SillyTavern + AnythingLLM Fusion

Use this when the workbench must learn from many tutorials and VN scripts while
also keeping characters stable and expressive.

## Why These Two

### SillyTavern

SillyTavern is a mature, high-star LLM frontend with character cards, WorldInfo
/ lorebooks, Visual Novel Mode, prompt controls, extensions, TTS and image-tool
integration. Its useful lesson for this workbench is not the UI itself, but the
separation between:

- stable character identity
- scenario
- example dialogue
- lorebook/world info
- prompt order
- extension-based memory
- visual-novel display surface

### AnythingLLM

AnythingLLM is a mature, high-star local-first AI/RAG application with workspaces,
document ingestion, vector databases, agents and document pipelines. Its useful
lesson for this workbench is:

- large document libraries must be chunked, indexed, and queried by workspace
- different corpora should not be dumped raw into a prompt
- document retrieval needs source paths and metadata
- agents/tools can operate over the indexed workspace

## Combined Workbench Pattern

Use AnythingLLM-style corpus handling first:

1. Raw tutorial or script enters `06_学习输入/*/待学习`.
2. `vn_learning_intake.py` normalizes it into learned Markdown.
3. `vn_style_profile_compiler.py` creates batch metrics and example candidates.
4. Human/AI distills the batch into compact style profiles and method cards.

Then use SillyTavern-style character/context injection:

1. Stable character card lives in `00_project_memory/cards/characters`.
2. Runtime state lives in `00_project_memory/runtime_state/characters/CHR_xxx.json`.
3. Retrieval-shaped memories live in `00_project_memory/memory_logs/character_memory`.
4. Character brief and draft-session assemble only relevant memory blocks.
5. Scene CSV cites memory refs so dialogue can be traced.

## Required Separation

Do not mix these layers:

- corpus text: raw learned source
- style profile: reusable craft and examples
- character card: stable fictional person
- runtime state: current scene psychology
- episodic memory: scene-specific recalled facts
- generated script: project output

## Prompt Assembly Order

1. Workbench rules and anti-AI rules.
2. Style profile snippets from learned corpus.
3. Project bible and theme spine.
4. Scene card and state delta.
5. Character cards.
6. Runtime state.
7. Retrieval-shaped memory blocks.
8. Output format contract.
9. QA checklist.

## VN-Specific Adaptation

AnythingLLM-like retrieval can provide tutorial lessons and script examples, but
SillyTavern-like character control decides how a line is spoken in the current
scene. If the two conflict, current character state wins over generic style.

## Failure Signs

- Dumping entire learned corpus into the prompt.
- Treating a style profile as a character voice.
- Writing character memory into global methods.
- Letting retrieved examples override the current scene's playable pressure.
- Generating prose without CSV rows, state effects, and QA.

## Output Contract

Before a serious draft using learned corpora, create or cite:

- relevant style profile
- loaded character cards
- runtime state files
- retrieval memory blocks
- scene card
- generated CSV
- validate / deep-audit / quality-debt results

