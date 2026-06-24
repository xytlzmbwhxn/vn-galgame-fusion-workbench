---
id: external_project_ingestion_protocol
type: method_card
---

# External Project Ingestion Protocol

## Purpose

Use this whenever the user asks to keep learning from other projects, open-source tools, mature games, writing workbenches, AI character systems, or engine files. The workbench must absorb structure in a traceable way instead of vaguely claiming experience.

## Borrowed Structures

- Dialogic: separates characters, portraits, timelines, event resources, visual editor surfaces, and unit tests.
- Agnai: prompt order, scenario/personality/memory/example dialogue sections, memory books with keywords, depth, priority, weight, and context budgets.
- Story Skills: story bible, character files, worldbuilding, plot arcs, scenes, continuity questions, promises/payoffs, durable state, deterministic maintenance checks.
- Existing local references: Ren'Py, WebGAL, ink, Yarn, Godot Dialogue Manager, Character Card V2, SillyTavern, RisuAI, Manuskript, bibisco, Quoll Writer, Skribisto, Story Architect, NovelStar, AI4VisualNovel, reramen.

## Ingestion Steps

1. Identify the project and why it is relevant to VN writing, character control, prompt workflow, engine export, continuity, or QA.
2. Check license and record whether code may be copied. If license is restrictive or unclear, only borrow structure.
3. Read README, license, docs, sample project files, schemas, tests, and at least one domain-specific resource file.
4. Extract structures, not text:
   - folders and file boundaries
   - data schemas and required fields
   - runtime state flow
   - prompt/context assembly order
   - validation or test strategy
   - editor-facing or user-facing presentation surfaces
5. Map each useful idea to a local artifact:
   - method card
   - schema/template
   - tool command
   - QA validator
   - project memory convention
   - export format
6. Update `01_reference_log/BORROWED_PROJECTS.md` with path, commit, license note, and absorbed structure.
7. Implement locally with new code or docs; do not paste external source.
8. Verify the local workbench still parses method index, schemas, templates, and at least one draft-session.

## Output Contract

Every learning round must leave:

- a source-log entry
- at least one local method/template/tool/doc improvement when a reusable pattern is found
- a clear note of what was not copied due to license or scope
- a verification command/result

## Failure Signs

- The assistant says it learned from a project but cannot name the local file changed.
- A project is added to the source log without license or commit.
- External code is copied into the workbench without license review.
- The absorbed pattern lives only in the assistant's reply, not in `00_workbench_core`.
- A mature project has an editor/runtime/test concept, but the workbench only records writing advice.
