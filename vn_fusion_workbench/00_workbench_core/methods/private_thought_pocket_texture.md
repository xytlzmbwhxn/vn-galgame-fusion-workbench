---
id: private_thought_pocket_texture
type: method_card
---

# Private Thought Pocket Texture

## Call This When

Load before writing or revising Chinese VN thought rows, especially after a full
script corpus or tutorial batch has been learned.

Use together with:

- `interiority_not_narration`
- `click_unit_textbox_rhythm`
- `dialogue_block_ownership`
- `vn_style_handprint_fusion`
- `chinese_vn_generation_hard_gates`

## Corpus And Tutorial Lesson

The learned VN corpus and tutorial notes point to the same rule: thought should
enter after pressure has accumulated, then leave before it becomes author
commentary.

Current private-corpus inner-row calibration:

- thought-like parenthetical rows: 1274
- average length: about 14 characters
- median length: about 13 characters
- p90 length: about 22 characters
- thought runs are usually single rows; two-row pockets are common enough to use;
  three or more consecutive thought rows require a strong reason.

Do not turn these numbers into a template. Use them to avoid empty fragments and
essay-length inner monologue.

## Valid Thought Pocket Jobs

A thought pocket should do at least one of these:

- misread a person in a way only this POV would make
- catch a contradiction between public role and private desire
- admit an unsafe wish, shame, jealousy, tenderness, or calculation
- compare two actions before a choice
- remember a branch debt, old promise, nickname, object, or previous failure
- turn spoken dialogue into private risk
- make the next menu option harder to choose

## Human Texture Rules

Good VN thought often sounds slightly unfinished because the character is still
inside the moment.

Use:

- small private questions
- self-interruption
- relaxation after pressure: filler, particle, retreat, half joke, or practical mask
- a swallowed name or noun
- a wrong guess corrected by a specific detail
- a bodily reaction only when it changes the next move
- a remembered sentence that stings because the current scene has touched it
- a practical worry that hides a softer feeling

Avoid:

- replacing every stiff line with a rhetorical question
- adding `嗯` / `……` / `吧` after a sentence that still reads like an author's verdict
- diagnosing another character from above
- repeating what the dialogue already showed
- classifying a visible action as psychology
- lyrical comparison with no decision pressure
- balanced contrast formulas split across rows
- summarizing the scene's theme

## Placement Pattern

Preferred rhythm:

```text
dialogue block
screen/action hinge
1-2 thought rows
choice, reply, or object operation
```

Allowed longer pocket:

```text
thought row 1: first unsafe inference
thought row 2: why that inference costs the POV something
thought row 3: only if it triggers a choice, route lock, or irreversible reply
```

If a fourth thought row appears, stop and convert one beat into dialogue,
narration, production cue, or a menu option.

## Rewrite Moves

Mechanical:

`（她把名字讲得很熟。）`

Repair direction:

- tie the name to a previous debt or route state
- let the POV wonder why the practiced answer bothers them
- make the next reply harder

Mechanical:

`（她在等失物箱给一个回音。）`

Repair direction:

- make the box a visible narration beat first
- use thought for the POV's private fear: what answer would be worse than no
  answer

Mechanical:

`（她是来确认什么东西还愿不愿意等她。）`

Repair direction:

- remove author classification
- write the object, hesitation, or avoided name
- let the POV guess too much, then pay for guessing

Mechanical:

`（当然，它应该没有抗议功能。）`

Repair direction:

- give the POV a half-beat to hear how ridiculous the thought is
- loosen with a character-owned filler or particle
- keep the object joke tied to the next action

Example:

`（嗯……当然？它应该没有抗议功能。）`

## Output Contract

Before delivery, changed thought rows must expose:

- `thought_job`
- `private_cost`
- `trigger_line_or_object`
- `next_click_effect`

Reject the thought row if it can be filmed by a camera and does not change a
private inference, choice, relationship cost, or route state.
