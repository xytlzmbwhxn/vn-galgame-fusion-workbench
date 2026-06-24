# Style And Memory System

## Why This Exists

The workbench must prevent three common failures:

- Dialogue, thought, and scenery alternate one by one until the scene feels mechanical.
- Characters drift into the same polite assistant voice.
- A scene has plot motion but no pressure on the project's central idea.

## Required Context Before Drafting

For every new scene, load these files:

- `00_project_memory/bible/core_theme.md`
- `00_project_memory/bible/style_rules.md`
- `00_project_memory/bible/style_reference_pack.md`
- `00_project_memory/cards/characters/*.json`
- `00_project_memory/runtime_state/characters/*.json`
- `00_project_memory/memory_logs/theme_motifs.md`
- the current scene card and state delta

## Rhythm Rule

Do not write a repeating chain of:

```text
dialogue -> narration -> dialogue -> narration
```

Use blocks:

- A staging block establishes objects, distance, deadline, or inner pressure.
- A dialogue block lets two or more characters push each other for several clicks.
- An interior block lets one mind turn around a problem without being interrupted by scenery.
- A consequence block records the visible result of a choice.

Short narration inside a dialogue block is allowed only when it changes the next line: a sound interrupts, a hand moves an object, someone sees something, or a deadline advances.

## Voice Lock

Character cards define baseline identity. `runtime_state/characters/*.json` defines runtime voice and psychology:

- current six-axis state
- active wants and fears
- unspoken truths
- sentence shapes allowed right now
- phrases or moves forbidden right now
- promises and debts from previous scenes

Before drafting, ask:

1. What does this character want in the next two clicks?
2. What word are they avoiding?
3. What old promise or debt bends the line?
4. Which axis is highest right now?
5. What physical object is closest to their hand?

## Theme Lock

The project must not merely tell events. Every route and key scene tests the core question in action.

For `rain_gate_demo`, the current core question is:

> When a system only protects what it can record, what does a person owe to someone who cannot safely be named?

Every important choice should make the player pay through one of these:

- loss of proof
- loss of trust
- loss of time
- loss of procedural safety
- accepting a debt that the system cannot write down

## QA Additions

The CLI now reports:

- dialogue block count
- narration block count
- longest dialogue block
- longest narration block
- single narration beats trapped between dialogue lines
- missing character runtime state files

A scene with many single narration bridges must be revised into stronger blocks.
