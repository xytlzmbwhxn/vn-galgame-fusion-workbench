---
id: source_adaptation_protocol
type: method_card
---

# Source Adaptation Protocol

## Purpose

Allow the workbench to learn from outside projects without making outside original
files part of the active generation layer.

## Rule

Outside sources may be read, studied, measured, or kept in a clearly marked reference
area. Active skills, method cards, prompts, templates, generated scripts, and handoff
instructions must be workbench-owned adaptations.

Strict user boundary: do not use another person's original file as the final callable
asset. If a source is useful, translate its mechanism into this workbench's vocabulary,
rewrite the procedure for Chinese Gal/VN production, and store only that adapted
version in the active layer.

## Adaptation Steps

1. Identify the transferable mechanism, not the source wording.
2. Rename it in workbench vocabulary.
3. Rewrite instructions from scratch for Chinese Gal/VN production.
4. Store the result under `00_workbench_core/methods/` or `00_workbench_core/portable_skills/`.
5. Record provenance in source logs without copying long source text.
6. Ensure `draft-session` loads only internal method cards.
7. Keep raw sources out of installed Codex skills and out of human-facing作品集.
8. If a copied source file is needed for evidence, keep it only under
   `external_refs/_raw_reference_archive/` and mark it non-active in the ledger.

## Output Contract

Every adaptation must include:

- source category
- adapted workbench file
- what changed to fit this project
- active/not-active status
- validation result

## Failure Signs

- A skill in `.codex/skills` is just an outside original package.
- A method card points to an outside local original file as required context.
- A draft-session depends on raw source folders.
- A human-facing test work quotes or imitates source text instead of using original prose.
- A portable skill folder is only a renamed outside package instead of a rewritten
  workbench-owned skill.
