---
id: click_unit_textbox_rhythm
type: method_card
---

# Click Unit Textbox Rhythm

## Call This When

Load before drafting or revising any click-to-advance VN / Galgame / ADV script.

## Core Rule

A row is a click unit, not a speaker unit and not a sentence unit.

After a click, something must be newly true:

- reply pressure
- new usable information
- screen state
- relationship cost
- private inference
- choice pressure
- state / flag / route effect
- breath or timing control

## Split When

- the screen state changes
- the speaker changes tactic
- the player needs a beat to infer
- a choice or state mutation occurs
- text would overflow the textbox
- interruption, self-correction, or swallowed speech is being performed

## Merge When

- several fragments are one breath
- several fragments are one tactic
- consecutive rows do not change pressure or information
- the split exists only for decorative suspense
- a thought repeats what dialogue already implies
- a visible action and object detail are one camera moment
- a second row only rephrases, beautifies, or metaphorically extends the previous row
- a narration pair can be read as one camera shot, such as `动作很轻` + `轻得像...`
- a line break merely imitates literary rhythm without giving the player a new click payoff

## Length Guidance

Compact rows are common, but short does not mean low payload. A very short row
must have a strong click function. A longer row must remain one readable breath.

## Required QA Note

For CSV rows, write a `click_function` in `qa_notes` when the function is not
obvious:

- `click_function=reply_pressure+relationship_cost`
- `click_function=private_inference before choice`
- `click_function=screen_state`
- `click_function=breath_control`

## Failure Signs

- one speaker, one row by habit
- one dialogue, one thought, one narration loop
- rows are short but empty
- the player can merge five rows without losing timing, emotion, or state
- psychological beats are split only to look dramatic
- narration becomes two or three tiny rows whose only effect is prettiness
- a cute or lyrical line asks the player to admire the sentence instead of advancing play
