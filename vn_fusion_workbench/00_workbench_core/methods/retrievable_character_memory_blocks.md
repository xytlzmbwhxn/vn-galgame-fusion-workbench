---
id: retrievable_character_memory_blocks
type: method_card
---

# Retrievable Character Memory Blocks

## Call This When

Before writing character dialogue, updating relationship state, creating character cards, or handing a project to another AI.

## Borrowed Structure

- Character Card V2: stable identity, creator notes, system prompt, post-history instructions, alternate greetings, character book, tags, and extensions are portable character metadata.
- SillyTavern Character Memory: a character card describes who someone is; memory blocks describe what happened and what should be recalled later.

## Rule

Separate character control into three layers:

| Layer | Storage | Purpose |
| --- | --- | --- |
| stable card | `00_project_memory/cards/characters/` | identity, voice rules, fear, desire, quirks, taboos |
| runtime state | `00_project_memory/runtime_state/characters/` | current mood, pressure, relationship deltas, recent scene effects |
| memory block | `00_project_memory/memory_logs/character_memory/` | scene events worth retrieving later |

## Memory Block Shape

Use short, searchable blocks. Put tags first, then 3-5 concrete bullets.

```text
- [林秋, 唐米 - 48号外套 / 借出牌 / 欠名]
  - 林秋 allowed a rule-bending option only after naming its return time.
  - 唐米 asked to leave the signature blank because the debt belonged to her.
  - The 48号外套 became a shared object for ownership, return, and unfinished apology.
```

## Extraction Rules

- Store what changed, not a play-by-play of every line.
- Name people, objects, promises, and wounds directly.
- Do not re-store baseline traits already in the character card.
- Keep one memory block per scene per important relationship/object.
- Mark whether the memory is public, private, suspected, or hidden from the POV character.

## Pre-Draft Retrieval

Before drafting a scene, load:

1. stable character card
2. current runtime state
3. scene card
4. last 1-3 relevant memory blocks
5. object or promise memory if the scene centers on a recurring item

Do not load the entire memory folder into the draft voice. Too much memory flattens the present scene.

## Post-Scene Update

After validation, update runtime state and add new memory blocks only for canon changes:

- promise made or broken
- relationship axis moved
- object changed hands
- private fact revealed
- line/choice that must be echoed later

## Failure Signs

- every scene starts from a clean slate
- character voice depends on the chat history instead of local files
- memory notes repeat the whole script
- a card trait is extracted again as if it newly happened
