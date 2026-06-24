---
id: rewrite_pipeline
type: method_card
---

# Rewrite Pipeline

## Call This When

Before creating a new draft from an existing scene, sample, or failed writing attempt.

## Goal

Separate method, memory, and generated draft:

- method improvements go to `00_workbench_core/methods/`
- project-only canon and memory go to `00_project_memory/`
- generated rewrite outputs go to `02_generated_content/`

## Procedure

1. Generate or read the scene brief.
2. Identify the old draft's failure mode in one sentence.
3. Write a function pass: what each beat must do.
4. Write a voice pass: make each speaker identifiable without name boxes.
5. Write a playable pass: convert to CSV rows with choices and state effects.
6. Store the new draft as a new file; do not overwrite the old draft.
7. Validate the new file.
8. Only after validation, write confirmed story changes back into project memory.

## Output Fields

- source draft
- rewrite version
- failure diagnosis
- method cards loaded
- generated script path
- memory updates needed

## Failure Signs

- rewriting overwrites the only copy
- project memory changes before draft is accepted
- a new writing technique is buried in a project file
- generated content is treated as canon before QA
