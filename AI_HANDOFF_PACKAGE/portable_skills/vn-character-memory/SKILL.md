---
name: vn-character-memory
description: Portable skill for keeping VN characters stable across scenes through stable cards, runtime state, episodic memory blocks, visible briefs, and voice signatures.
---

# VN Character Memory

## Use When

Use this skill when creating characters, revising voice, showing character settings
to the user, updating relationship state, or diagnosing flat dialogue.

## Project Root

Locate the workbench root first: the folder that contains `START_HERE.md`,
`vn_fusion_workbench/`, and `AI_HANDOFF_PACKAGE/`. Character cards and runtime
state live under `vn_fusion_workbench/02_projects/<project>/00_project_memory/`.

## Memory Layers

Keep these layers separate:

- **Stable card**: identity, desire, fear, taboo, social mask, voice fingerprint,
  body habit, charm hook.
- **Runtime state**: current emotion, relationship pressure, known facts, route flags,
  recent embarrassment, current lie, physical condition.
- **Episodic memory**: scene-specific memories with tags, triggers, quote-like
  anchors, and update dates.
- **Visible brief**: a user-readable summary that proves the character has memory
  points and can be recognized.

## Required Character Fields

Every major character needs:

- first-screen impression
- public want
- private want
- fear
- taboo topic
- what they do when cornered
- charm hook
- ordinary quirk
- sentence kernel
- punctuation habit
- body signature
- relationship hooks
- example lines
- arc promise

Apply `liveliness +1`: whatever the archetype is, make the character slightly more
interesting, cute, playful, or socially textured than the plain version.

## Before Drafting Dialogue

For each speaking character, check:

1. What do they want in this exact exchange?
2. What are they refusing to say?
3. What word or topic feels unsafe?
4. What object, job, or social rule can they hide behind?
5. Which memory block can leak into the line without exposition?
6. What punctuation belongs to them under pressure?

## After Draft Validation

Update memory only for accepted, canon-changing facts:

- relationship change
- new promise or debt
- object state
- revealed lie
- emotional threshold crossed
- route flag or quality change

Do not write failed draft material into memory.

## Output Contract

When asked to show character settings, produce a visible brief with memory points and
example lines. When writing scripts, cite memory refs in the CSV so another AI can
trace why a line sounds that way.
