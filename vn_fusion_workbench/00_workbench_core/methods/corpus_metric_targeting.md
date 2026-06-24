---
id: corpus_metric_targeting
type: method_card
---

# Corpus Metric Targeting

## Purpose

Use complete VN/open-source script corpora as calibration before drafting.
This method prevents vague "learning from famous works" claims by forcing the
draft to declare measurable pacing targets and then compare the output against
them.

## Borrowed Structure

- First Snow / Twofold: master flow calls small scene files; dense screen,
  sprite, sound, and pause cues keep the script producible.
- LearnToCodeRPG: menus, flags, overlays, and calendar/stat modules make player
  behavior legible over time.
- Ren'Py tutorial and The Question: a short vertical slice can still teach
  labels, scene changes, dialogue, menu choices, and endings.
- Story Skills and write-good style tools: prose is not trusted until it has
  passed deterministic checks.

## Procedure

Before drafting:

1. Refresh `full_script_metrics.json`.
2. Pick:
   - primary corpus for flow and staging density
   - secondary corpus for choice/state behavior
   - one writing-tool reference for consistency control
3. Declare targets:
   - textbox count band
   - average textbox length band
   - dialogue/narration balance
   - minimum choices and branch labels
   - minimum production cue coverage
   - required character-control files
4. Convert every target into an original scene constraint. Never imitate names,
   events, jokes, signature scenes, or prose.

After drafting:

1. Run `validate`.
2. Run `deep-audit`.
3. Compare the draft with its declared targets in a QA note.
4. If the draft misses a target, either revise or write a visible exception.

## Output Fields

- `primary_corpus`
- `secondary_corpus`
- `consistency_reference`
- `target_textbox_count`
- `target_avg_chars_per_textbox`
- `target_dialogue_narration_shape`
- `target_choice_state_shape`
- `target_stage_cue_shape`
- `post_draft_metric_result`

## Failure Signs

- The draft cites famous works but has no measurable target.
- It copies tone or text instead of converting structure.
- It has choices with no state payoff.
- It has character cards that the dialogue visibly ignores.
- Validation passes but the script does not meet the declared reading rhythm.
