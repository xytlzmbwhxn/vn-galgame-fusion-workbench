---
id: chinese_vn_generation_hard_gates
type: method_card
---

# Chinese VN Generation Hard Gates

## Call This When

Load this before every Chinese Galgame / AVG / visual novel draft or rewrite.
These are blocking gates, not optional taste notes.

Use together with:

- `tutorial_absorption_to_generation_contract`
- `deep_vn_corpus_application`
- `click_unit_textbox_rhythm`
- `interiority_not_narration`
- `private_thought_pocket_texture`
- `choice_mental_model`
- `branch_bottleneck_state`
- `line_energy_punctuation`
- `character_liveliness_bias`

## Gate 1: Row Is Click Unit, Not Speaker Unit

Every row is a player click. A row must change at least one:

- what the player knows
- what the player sees or hears
- what the player risks
- relationship pressure
- private inference
- choice pressure
- state, flag, route, object, or callback
- breath / timing

Do not split only because the speaker changed. Do not write one person, one
sentence, one row by habit.

## Gate 2: Dialogue Blocks Are Allowed

Dialogue may run continuously while characters are testing, teasing, dodging,
pressuring, lying, bargaining, or cornering each other.

Do not alternate mechanically:

dialogue -> thought -> narration -> dialogue -> thought.

Prefer:

dialogue block -> private inference pocket -> concrete action / inspection ->
choice pressure -> consequence.

## Gate 3: Thought Must Be Private

Thought rows must contain something a camera cannot film:

- private inference
- hidden cost
- self-deception
- unsafe desire
- shame, jealousy, fear, tenderness, calculation
- choice pressure
- a contradiction between role and desire
- comparison with a memory or earlier branch state

Visible action, object texture, light, sound, weather, and room layout are
narration or stage unless the same row creates private inference.

Never use parentheses to hide ordinary narration.

Thought texture must pass `private_thought_pocket_texture`: a thought row should
sound like the protagonist is still inside the pressure, not like the author is
diagnosing a scene. Prefer small private questions, unsafe guesses, remembered
branch debt, swallowed names, and practical worries that hide softer feelings.

## Gate 4: Chinese Display Rhythm

Readable previews use:

- dialogue: `『……』`
- thought: `（……）`
- narration: no quotation marks
- production cue: `[cue: ...]`

Punctuation is part of voice and pressure. Use `？` `！` `……` `——`, particles,
soft endings, and unfinished lines only when the speaker and situation earn them.

Do not give every sentence a period. Do not sprinkle question marks, exclamation
marks, or ellipses evenly across every character.

## Gate 5: Spoken Language Over Written Language

Dialogue is heard. It may interrupt itself, dodge, repeat, soften, joke, swallow
a word, or end without a neat conclusion.

Blocked in dialogue and thought unless intentionally used in a stiff in-world
document:

- 不是 X，而是 Y
- 不是 X。是 Y
- 不是 X。她/他/这/那是 Y
- standalone `不是` used as an interpretive shortcut in thought or narration
- `是不是` used as filler when the line can become a concrete accusation,
  tease, request, or misread
- thought rows that define a character action with `她/他是来...`, `这是...`,
  or similar authorial classification instead of showing the object, gaze,
  hesitation, or pressure
- 并非 X，而是 Y
- 与其说 X，不如说 Y
- 真正的 X 是 Y
- 这不只是 X，也是 Y
- 在某种意义上
- 我突然意识到
- 我终于明白
- 那一刻，我……
- 重要的不是……而是……
- 所谓的 X，其实 Y
- X 的背后是 Y

Replace these with action, request, refusal, joke, correction, misread, bargain,
object operation, relation cost, or choice pressure.

Do not evade the rule by splitting a contrast into two rows. If a thought row says
`不是买东西。` and the next row says what the character is really doing, the draft
still fails. Rewrite it as direct observation, object focus, or private pressure.

## Gate 6: Dialogue Must Create Actable Pressure

Important dialogue must give the next speaker a problem:

- answer or dodge
- accept help or reject debt
- reveal knowledge or pretend not to know
- keep face or lower the mask
- choose public rule or private feeling
- protect someone or expose the truth

If a line only states an idea, rewrite it.

## Gate 7: Character Voice Must Survive Name Removal

Every major character needs a sentence engine:

- preferred clause length
- opening habit
- stress punctuation
- favorite dodge
- allowed particles
- how they joke
- what they say when cornered
- what they never name directly

After drafting, hide speaker names. If lines can be swapped without damage, the
voice pass fails.

## Gate 8: Local Life Carries Emotion

For Chinese Galgame texture, emotion should often travel through ordinary social
pressure:

- who pays
- who waits
- who returns a thing
- family calls
- class duty
- dorm or office rules
- canteen queues
- exam pressure
- repair errands
- part-time work
- address changes
- joking names and avoided names

Do not use generic suffering or abstract depth as a substitute for lived context.

## Gate 9: Options Are Not Branches

Track these separately:

- `visible_option_count`: how many options the player sees
- `branch_state_count`: how many distinct outcomes survive
- `route_flag_count`: locks or unlocks touched
- `immediate_feedback`: line, expression, object, sound, or menu change
- `rejoin_point`: where branches bottleneck
- `persistent_debt`: what remains different after reconvergence
- `delayed_callback`: where the branch is remembered later

A three-option menu can create two branch states. A two-option menu can create
four later route states. A hidden flag can create a branch with no visible menu.

Do not call a choice meaningful unless it changes state or later text.

## Gate 10: Branches Must Leave Visible Debt

Branches may reconverge only if state remains visible:

- relationship flag
- object location
- who owes whom
- changed address/name
- missing or added option
- delayed line variant
- route lock / unlock
- bad end or side scene access

Reconvergence must not erase what the player did.

## Gate 11: Theme Must Be Played

The theme cannot be delivered as a paragraph. It must become repeated player
behavior and cost:

- tell the truth now or protect face
- follow procedure or bend it for someone
- keep a debt clean or make it intimate
- leave a mistake recorded or quietly repair it
- save time or stay with a person

If the protagonist can state the theme without the player making a related
choice, the scene is not yet a VN scene.

## Gate 12: First-Person Perception

VN narration should stay attached to the protagonist's sensorium without
constantly saying "I saw / I noticed / he approached".

Prefer direct presentation:

- window, object, sound, sprite, hand, light, UI state
- sensory consequence
- concrete social action
- private thought only when inference or pressure changes

Avoid prose markers that pull the player outside the textbox:

- 他看见……
- 他注意到……
- 他靠近的时候……
- 他心想……

Write what appears or what changes, not the act of noticing.

## Gate 13: Density Control

No text type should dominate accidentally.

Guidance for dialogue-heavy scenes:

- dialogue : narration : thought can roughly lean around 5 : 3 : 2
- continuous dialogue blocks are allowed
- thought doublets are allowed before a choice or after a painful line
- three or more consecutive thought rows usually fail
- one to two thought rows are a pocket; a third needs choice pressure, route lock,
  or an irreversible reply

If a third consecutive thought seems necessary, replace one with dialogue,
narrated action, production cue, or choice.

## Gate 14: Deep Corpus Use, Not Surface Imitation

When a complete VN corpus has been learned, do not copy its style profile or
average row length. Load `deep_vn_corpus_application` and separate:

- textbox length distribution
- click-function split / merge logic
- dialogue block behavior
- narration placement
- private thought pockets
- punctuation and sentence endings by speaker
- visible option count
- branch state count
- route flags and locks
- rejoin / bottleneck points
- persistent branch debt
- delayed callbacks

Raw engine jump counts are not story branch counts. They may include window
control, animation loops, read markers, and internal labels.

## Gate 15: Style Handprint, Not Data Pile

Corpus learning is incomplete if it only produces summaries, metrics, or method
notes. Before serious drafting, load `vn_style_handprint_fusion` and the newest
`VN文风手印融合资产`.

The draft must carry learned style as original craft behavior:

- sentence moves, not copied sentences
- character-specific breath, not generic liveliness
- emotional turns through task, relation, mistake, or choice
- thought pockets that reveal private cost
- punctuation that belongs to the speaker's pressure state
- click rows that change what the player infers or risks

When new tutorials or scripts are added, update the handprint layer with reusable
sentence moves, voice patterns, emotional transition patterns, and textbox rhythm
lessons. Do not pile raw data into the project without changing generation
behavior.

## Gate 16: Dialogue Ownership, Not Ping-Pong

Dialogue-heavy scenes must not default to equal A/B/A/B alternation.

Before drafting, load `dialogue_block_ownership` and plan who owns the current
pressure. A mature VN scene can let one speaker hold several consecutive
textboxes, as long as each click changes tactic, evidence, emotional leakage,
relationship cost, object handling, or interruption setup.

Long continuous dialogue is allowed, and sometimes required, when the player
needs to stay inside a comic rapid-fire exchange, argument, interrogation,
confession, group scene, route-lock negotiation, or exposition spoken under
hidden agenda. Do not cut a necessary long exchange just to satisfy a metric.

Long pure ping-pong fails only when it has no declared function, no pressure
escalation, no interruption logic, and no changed state by the end.

For every important dialogue block, define:

- pressure owner
- same-speaker run owner
- why the run needs multiple clicks
- where the other speaker interrupts
- where narration or thought enters after the block
- how the block avoids long equal alternation
- if the block stays long, what its long dialogue function is

Before serious drafting, include:

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
Style handprint asset:
Reusable sentence moves:
Emotional transition plan:
Dialogue ownership plan:
Same-speaker run owner:
Anti-ping-pong move:
Long dialogue function, if any:
```

## Blocking QA

Reject or repair the draft if any item is true:

- More than three low-payload clicks in a row.
- Thought rows mostly describe camera-visible action.
- Dialogue explains theme, method, or morals instead of creating pressure.
- Characters share the same punctuation and particle profile.
- Branches reconverge without persistent debt.
- Option count is treated as branch count.
- Local setting is only wallpaper.
- Theme is summarized instead of played.
- Corpus learning appears only as surface style imitation.
- Style learning appears only as summaries or metrics.
- Dialogue defaults to long one-line ping-pong without ownership, run, interruption, hinge, or a valid long-dialogue function.
- The scene could be pasted into a novel without losing gameplay meaning.

## POSITIVE ALTERNATIVES

Each Gate is a floor, not a ceiling. Below are concrete replacements.
These are what to do instead of what to avoid.

---

### Gate 3: Private Thought - What Private Thought Actually Looks Like

Banned: camera-visible narration in thought rows.
Use instead:
1. Small private question: character asks what they cannot say aloud
2. Memory debt interrupting: earlier choice surfaces at wrong moment
3. Swallowed name: thought stops before the vulnerable word
4. Unsafe interpretation: reads hidden meaning revealing what they want

Thought rhythm:
- 1 row: establish pressure
- 2 rows: build contradiction or cost
- 3 rows: ONLY if ends in choice, route lock, or irreversible reply
- If 3 rows seem necessary, replace one with dialogue or narrated action

---

### Gate 5: No Contrast Sentences - What to Write Instead

Banned: not the X but Y patterns, standalone not as shortcut.
Use instead:
1. Action reveals intent (no comparison needed)
2. Direct accusation (player infers the contrast)
3. Object comparison with physical detail (the gap does the work)
4. Silence + practical sentence (contrast lives in the gap)
5. Repetition with one word changed (question mark is the contrast)

---

### Gate 6: Dialogue Creates Pressure - What Makes Dialogue Actable

Every important dialogue gives the next speaker a problem:
Question | Request | Revelation | Accusation | Proposal.
If a line can be deleted without changing what the next speaker must answer, it has no pressure.

---

### Gate 7: Voice Survives Name Removal - Voice Test Protocol

After drafting: copy all dialogue without labels, shuffle, read aloud.
Voice ingredients: clause length, opening habit, stress punctuation, dodges, cornered responses.

---

### Gate 8: Local Life Carries Emotion - Social Pressure Inventory

Use social mechanics as emotion carriers: who pays, who waits, who returns,
family call, class duty, part-time work. NOT: generic suffering or abstract feeling.

---

### Gate 11: Theme Must Be Played - Choice Architecture

For P017 theme (temporarily un-returnable things can be stored, not erased):
Each choice must make the theme more specific to player action, not more abstract.
Theme cannot be stated. It must become repeated player cost.

---

### Gate 13: Density Control - Density Reference Table

From a private VN corpus calibration:
- Median row: 11 chars, P90: 22 chars
- Dialogue proportion: 64%
- Longest dialogue block: 15 rows (legitimate argument confrontation)
- Pure A/B/A/B > 3 rows: only 3.08%

Density guide by scene type:
- Opening:    Dialogue 6 : Narration 3 : Thought 1
- Confrontation: Dialogue 7 : Narration 1 : Thought 2
- Quiet moment: Dialogue 4 : Narration 4 : Thought 2
- Before choice: Dialogue 5 : Narration 2 : Thought 3
Never let any type dominate for more than 5 consecutive rows.

---

### Gate 15: Style Handprint - Extraction Protocol

Extract: sentence moves, voice pivot words, emotional transition triggers,
textbox rhythm patterns, punctuated voice signatures.
Do NOT extract: raw metrics (to method_index), copied dialogue (to raw corpus).

The handprint contains only reusable craft, not reference content.

---
Updated: 2026-06-24 | Source: private VN corpus + tutorial cross-validation

## SPOKEN PRIVATE THOUGHT ADDENDUM

Thought rows must not sound like author notes.

A good thought row may be messier than narration:
- 啊
- 嗯
- ……的话
- 应该
- 大概
- 或许
- 吧
- 算了
- 等一下

These particles are not decoration. They mark private hesitation, self-defense, and incomplete courage.

Before accepting a thought row, ask:
1. Could the character actually think this in this moment?
2. Does it use their own vocabulary?
3. Does it make the next click more awkward, risky, or intimate?
4. If the line sounds clever, is the cleverness coming from the character or from the author?
