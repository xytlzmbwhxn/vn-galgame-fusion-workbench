---
id: galgame_textbox_production
type: method_card
---

# Galgame Textbox And Production Script

## Call This When

Load before drafting, rendering, or validating Chinese Galgame / AVG scripts.

## Production Mindset

A Galgame script is a production document for a game, not a finished prose page.
Each row should be useful to writing, direction, UI, audio, art, or branching.

## Display Rules

- dialogue preview: `『……』`
- thought preview: `（……）`
- narration: no quotation marks
- production cue: `[cue: ...]`
- choices: explicit `choice_group`, `choice_text`, `target`, `state_effects`

## Textbox Rules

- Treat each row as restricted-view reading.
- Do not overload one textbox with novel paragraphs.
- Do not spend multiple empty rows on pure ellipsis when a cue can carry silence.
- Keep staging in cues or narration, not in fake thoughts.
- Keep actor name, expression, BGM, SFX, CG, and UI changes explicit when they
  matter to production.

## Failure Signs

- readable preview looks like a novel chopped into lines
- no production cues where visual/audio timing matters
- dialogue punctuation is uniform across characters
- choices have no target or state effect
- branch state is invisible after reconvergence
