---
id: deep_vn_corpus_application
type: method_card
---

# Deep VN Corpus Application

## Call This When

Load this after any complete VN script corpus has been ingested, and before any
serious Chinese Galgame / AVG drafting that claims to have learned from mature
works.

This card uses public method cards plus optional private corpus assets when they
exist locally:

- `06_学习输入/_风格画像/PUBLIC_STYLE_HANDPRINT.md`
- `06_学习输入/_风格画像/VN文风手印融合资产_20260623.md`
- `00_workbench_core/methods/chinese_vn_generation_hard_gates.md`
- `00_workbench_core/methods/tutorial_absorption_to_generation_contract.md`
- `00_workbench_core/methods/click_unit_textbox_rhythm.md`
- `00_workbench_core/methods/interiority_not_narration.md`
- `00_workbench_core/methods/choice_mental_model.md`
- `00_workbench_core/methods/branch_bottleneck_state.md`

## Core Principle

Do not copy the corpus surface. Use it to calibrate playable craft:

- textbox rhythm
- dialogue block length
- sentence endings
- punctuation ownership
- speaker profile separation
- thought placement
- narration/thought distinction
- visible option menus
- hidden branch state
- route locks and bottleneck callbacks
- repeated daily-life pressure

## What To Study Before Drafting

### 1. Textbox / Click Rhythm

Use corpus length statistics only as a guardrail. They do not become a template.

Private corpus calibration shows compact rows can work, but compact does not
mean low payload. Each row must still have a click function:

- reply pressure
- new usable information
- screen state
- relationship cost
- private inference
- choice pressure
- state effect
- breath control

Split when the player needs to feel a new beat. Merge when fragments are one
breath, one tactic, or one camera moment.

### 2. Dialogue Blocks

Dialogue blocks are allowed and expected. The corpus contains many short turns,
but also longer continuous dialogue runs during comedy, conflict, and relation
testing.

Do not obey either false rule:

- false rule A: one speaker equals one row
- false rule B: every important exchange must become a long block

Correct rule: keep dialogue continuous while the speakers are actively testing,
dodging, teasing, or cornering each other. Insert narration or thought only when
the click changes screen state, private inference, or choice pressure.

### 3. Punctuation And Voice

Punctuation must be a speaker fingerprint, not a global decoration pack.

Before drafting, for each major speaker define:

- normal sentence length
- question tendency
- exclamation tendency
- ellipsis tendency
- favorite particles
- preferred final sounds
- interruption shape
- what happens when embarrassed, cornered, proud, or lying

After drafting, hide the names. If two speakers keep the same punctuation profile,
the voice pass fails.

### 4. Thought / Interiority

Thought is not narration in parentheses.

A thought row is valid only if it contains at least one:

- private misread
- hidden cost
- unsaid motive
- self-deception
- unsafe tenderness
- choice pressure
- contradiction between role and desire
- comparison with remembered state

Camera-visible action, object texture, room layout, weather, and lighting are
narration or stage. They can sit near a thought, but they cannot replace the
thought.

Use thought pockets, not thought flooding. A thought doublet is allowed when the
player must infer before choosing. Three consecutive thought rows usually means
the draft has become essay narration.

### 5. Narration

Narration should present what is on screen or what the protagonist experiences
without repeatedly saying "I saw / I noticed / he approached".

Prefer:

- direct screen/object state
- sensory consequence
- concrete social action
- production cue
- a visible object whose meaning has changed

Avoid:

- prose-level camera explanation
- decorative metaphor with no state effect
- summary of theme
- authorial explanation of what the player should feel

### 6. Options Are Not Branches

Visible choice option count and branch count are different things.

Track separately:

- `visible_option_count`: how many options the player sees
- `branch_state_count`: how many distinct state outcomes exist
- `route_flag_count`: route locks/unlocks touched
- `immediate_feedback`: line, expression, object, sound, or menu change
- `rejoin_point`: where branches bottleneck
- `persistent_debt`: what remains different after reconvergence
- `delayed_callback`: where the branch is remembered later

A three-option menu can produce two branch states. A two-option menu can produce
four later route states. A hidden flag can create a branch with no visible menu.

Do not call a menu "branching" unless it changes state or later text.

### 7. Corpus-Control Cross Check

RealLive `.org` control-flow hints include many non-story jumps: window control,
read markers, animation loops, background setup, and internal labels. Treat raw
jump counts as control complexity, not as story branch count.

When writing our own project, make branch structure explicit in route maps and
CSV rows instead of relying on raw engine jumps:

- choice row
- target label
- state_effects
- memory_refs
- route flag
- callback row or scene

### 8. Tutorial Cross Validation

Every corpus-derived lesson must survive the tutorial hard gates:

- row is a click unit
- dialogue can run in blocks
- thought must be private
- punctuation belongs to character
- dialogue creates actable pressure
- local life carries emotion
- branches leave visible debt
- theme is played, not explained

If corpus statistics and tutorial rules seem to conflict, obey the gameplay
function. For example: short rows are acceptable only when a click does work.

## Required Pre-Draft Note

Before generating a serious scene, write or include a compact note:

```text
Corpus rhythm target:
Dialogue block plan:
Narration placement:
Private thought pockets:
Speaker punctuation fingerprints:
Visible option count:
Branch state count:
Rejoin / bottleneck:
Persistent debt:
Tutorial cross-check:
```

## Blocking QA

Reject or revise the draft if any are true:

- It uses corpus metrics as a surface template.
- It has many short clicks with no new pressure, information, or state.
- It alternates dialogue / thought / narration mechanically.
- It uses parentheses for camera-visible action and calls it psychology.
- It makes every character share the same punctuation rhythm.
- It treats option count as branch count.
- It reconverges branches without persistent debt.
- It explains the theme after choices instead of making choices embody it.
- It cannot point to a specific corpus-derived craft decision and a tutorial
  rule that supports it.
