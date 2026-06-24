---
id: plain_text_project_granularity
type: method_card
---

# Plain Text Project Granularity

## Call This When

When organizing a long story, creating project folders, preparing handoff files, or expanding a test scene into a complete work.

## Borrowed Structure

- novelWriter: large novels are easier to maintain as many small human-readable documents with metadata and cross-references.
- Manuskript: premise, synopsis, characters, plots, outlines, index cards, status fields, and story-world items are separate planning surfaces.

## Rule

The workbench must stay readable without a special app. Use many small files with stable names. Do not hide all canon in a single giant document.

## Required Granularity

| Scope | File shape |
| --- | --- |
| project premise | one sentence, one paragraph, full pitch |
| theme | thesis question, repeated action, object, cost, ending pressure |
| character | stable card, user brief, runtime state, memory log |
| route | route map with labels, locks, callbacks, endings |
| chapter | summary, status, scene list, turning point |
| scene | scene card, state delta, CSV script, readable preview, QA |
| source learning | source ledger, learning summary, implemented method cards |

## Metadata Fields

For new planning files, prefer these reusable fields:

- `id`
- `title`
- `status`
- `summary_sentence`
- `summary_paragraph`
- `pov`
- `route`
- `tags`
- `depends_on`
- `changes`
- `callbacks`
- `source_refs`

## Handoff Contract

Another AI should be able to start at `START_HERE.md`, read `AI_HANDOFF_PACKAGE/handoff_notes/`, inspect the active project, run validation, and continue without reading the whole Downloads folder.

## Failure Signs

- a project depends on chat history to understand canon
- new methods are stored inside one story project
- a generated draft is treated as the only source of memory
- file names change after every rewrite, breaking references
