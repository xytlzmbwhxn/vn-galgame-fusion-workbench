---
id: runtime_dialogue_pipeline
type: method_card
---

# Runtime Dialogue Pipeline

## Call This When

Before drafting, validating, or exporting any scene that contains dialogue, commands, choices, labels, jumps, variables, or engine output.

## Borrowed Structure

- Yarn Spinner: author-facing dialogue source is separate from runtime line delivery, options, and commands.
- ink: prose, choices, knots/stitches, variables, and divert flow are authored as a compact playable graph.
- Ren'Py: script statements, labels, menus, say lines, scene commands, and lint/export are distinct production layers.
- TwineJS: passages are nodes with names, tags, links, and story-format export boundaries.

## Rule

The CSV script is the source of truth. Every row must behave like one runtime unit:

| Row type | Runtime meaning |
| --- | --- |
| `dialogue` | one textbox line from a named speaker |
| `thought` | one interior textbox, tied to current POV |
| `narration` | one camera/environment beat |
| `command` | stage, sprite, BGM, SFX, label, jump, variable, or wait |
| `choice` | one selectable option with target and state effect |
| `comment` | production-only note, never player text |

## Drafting Procedure

1. Give each scene a stable scene id and each branch a stable label.
2. Write the visible player flow first: label -> lines -> pressure point -> choices -> branch labels -> rejoin or ending.
3. Place production commands in their own rows. Do not hide stage direction inside dialogue.
4. Every choice row must have option text, target label, cost/gain, and later callback.
5. Every branch that reconverges must leave visible state: changed object, changed relationship, changed line, changed option, or changed route flag.
6. Export files are build artifacts. If an export disagrees with CSV, fix CSV and regenerate export.

## Output Contract

A scene using this method must provide:

- stable labels and choice targets
- no unresolved jumps
- state notes on each branch
- command rows for display/BGM/sprite changes
- exported Ren'Py, Ink, Yarn, WebGAL, and Godot Dialogue files when requested

## Failure Signs

- a choice has no remembered cost
- a command is written as poetic narration
- an export is edited as canon
- a branch returns to the main path with no later visible trace
