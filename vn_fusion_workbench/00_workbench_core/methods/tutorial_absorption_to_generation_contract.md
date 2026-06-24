---
id: tutorial_absorption_to_generation_contract
type: method_card
---

# Tutorial Absorption To Generation Contract

## Purpose

Use this card before drafting Chinese Galgame / AVG prose after a tutorial intake
round. Its job is to prove that learned tutorials are changing generation, not
only being summarized.

This card is grounded in the learned tutorial batch under:

- `06_学习输入/教程文本/已学习/`
- `06_学习输入/_风格画像/style_profile_cn_gal_tutorial_lessons_20260623.md`
- `00_workbench_core/methods/chinese_vn_generation_hard_gates.md`

## Required Evidence In The Draft

A draft that claims to use the tutorial learning must show all of these:

1. **Textbox is a click unit**
   - Rows are split or merged by change in pressure, information, inference,
     screen state, choice pressure, or state effect.
   - The script must not use one-speaker-one-row as the default rhythm.

2. **Dialogue arrives in playable blocks**
   - At least one important social exchange should run as continuous dialogue
     before the protagonist explains it internally.
   - Narration and thought may interrupt only when the click changes what the
     player can infer, risk, or choose.

3. **Thought rows are private**
   - A thought row must contain private inference, hidden cost, self-deception,
     choice pressure, or an unsafe desire.
   - Camera-visible action, object texture, room layout, and light belong to
     narration or stage unless the row also changes private inference.

4. **Chinese display layer is explicit**
   - Readable previews render dialogue with `『』`.
   - Thought rows render with `（）`.
   - Production cues use command rows or cue notation.

5. **Language is spoken, not essay-polished**
   - Dialogue and thought avoid banned balanced formulas such as `不是X，而是Y`,
     `与其说X，不如说Y`, `真正的X是Y`, and assistant-like theme summaries.
   - Lines may be unfinished, self-corrected, teasing, practical, petty, or
     socially awkward when the character voice allows it.

6. **Character punctuation is owned**
   - `？`, `？！`, `……`, `——`, particles, clipped endings, and no-final-punctuation
     must belong to a speaker's sentence engine.
   - If two characters share the same particle and punctuation profile, the
     scene fails the voice pass.

7. **Emotion travels through local life**
   - Use small obligations, procedures, tools, social face, debts, delays,
     work routines, family/work/school pressure, or returned objects.
   - Do not use generic pain, abstract depth, or literary haze as a substitute.

8. **Choices leave visible debt**
   - Every important choice must record one immediate response and one delayed
     callback: object state, relationship debt, line variant, route flag, missing
     option, or changed address.
   - Recombined branches must keep the debt visible.

9. **Theme is played**
   - The theme must become a repeated player behavior and cost.
   - No scene may end by telling the player what the story means.

10. **Interesting scene requirement**
    - Each major scene needs a playable surprise, a misunderstanding that shifts,
      a quote-worthy line, and a moment where the player has to decide what kind
      of person they are being.

## Pre-Draft Mini Contract

Before writing a scene, fill this in the draft-session notes or project audit:

```text
Tutorial-derived rhythm target:
Dialogue block target:
Private thought target:
Character-owned punctuation:
Local-life pressure:
Choice debt:
Theme action:
Banned-pattern scan target:
```

## Post-Draft Check

Reject the draft if any of these are true:

- A scene can be read as a novel paragraph merely chopped into rows.
- Most thoughts are visible action in parentheses.
- Dialogue explains the author's point instead of pressuring the next move.
- Characters lose voice when name boxes are hidden.
- Choices do not alter state, memory, option availability, or callback text.
- The learned tutorial files cannot be traced to concrete row-level decisions.
