# Novel Architecture Layer

This layer turns novel-writing project structure into reusable VN drafting context.

## Required Files

Project-level files live in:

```text
02_projects/<project_id>/01_narrative_design/novel_architecture/
  chapter_plan.json
  narrative_threads.json
  character_arcs.json
  foreshadow_ledger.json
```

## How It Is Called

`draft-session` lists these files in `loaded_files`, adds them to the scene brief, and writes the storage contract. `context` includes their full JSON bodies. `validate` checks that a script references at least one `THR_`, `ARC_`, and `FS_` id in `memory_refs` when those ledgers exist.

## Why It Exists

VN dialogue can become lively but weightless if it only follows local banter. This layer forces every scene to answer four questions before prose starts:

- Which chapter goal is being served?
- Which narrative strand is touched?
- Which character arc changes or resists change?
- Which foreshadow seed, echo, reveal, or payoff is being handled?

The text still appears as ADV rows, choices, and stage commands. The long-form structure stays in metadata and memory refs, so characters do not explain the design aloud.
