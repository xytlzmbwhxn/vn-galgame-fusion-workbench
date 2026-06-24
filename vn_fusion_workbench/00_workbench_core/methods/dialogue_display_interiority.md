# Dialogue Display And Interiority

## Purpose

Chinese VN drafts need a display layer, not only raw script rows. Dialogue, inner thought, narration, and stage command should look different when reviewed by a human.

## Display Contract

- CSV source keeps dialogue text raw.
- Readable previews render dialogue as `【角色】『台词』`.
- Inner thought uses `row_type=thought` and renders as `（内心文本）`.
- Narration stays unwrapped.
- Stage commands use `@演出` or stay inside command rows.

This prevents two failures:

- Dialogue looks like flat prose because the preview loses the Gal name-box / quote convention.
- Inner monologue is hidden inside narration, so the protagonist has no playable psychological texture.

## Dialogue Tone Contract

Do not polish every line into complete declarative speech. A VN character can sound cute, casual, evasive, tired, petty, or playful while still carrying plot information.

Default liveliness floor: no major character should be written at their flattest possible setting. After the line's plot function is clear, add a character-owned bit of life: a nickname, a soft particle, a weird object comparison, a tiny complaint, a failed joke, a too-practical kindness, or an unfinished word. Seriousness should reduce the play; it should not erase it from the character's baseline.

Allowed pressure marks:

- `？` for testing, teasing, disbelief, or forcing the other side to answer.
- `？！` for sudden social embarrassment or comic pressure.
- `……` for swallowed words, not empty silence.
- `——` for being cut off or cutting oneself off.
- `嘛`, `啦`, `喂`, `哎`, `欸`, `不是吧`, `行吧`, `好嘛`, `你看`, `算我求你` when the character's voice supports them.

Do not spray marks evenly. Each speaker owns a different set:

- A rule-bound character uses fewer marks and lets punctuation appear when control cracks.
- A playful character uses question marks, nickname shifts, and soft particles to dodge shame.
- A shy character may use unfinished endings and correction.
- A sharp character may use short questions and no apology.

## Interiority Contract

Thought rows are not diary paragraphs. A thought textbox should do at least one job:

- Reveal what the protagonist cannot say.
- Explain why a choice is hard without naming the theme.
- Catch a bodily reaction before dialogue resumes.
- Let the player read a clue before the protagonist acts.
- Expose a private contradiction between role and desire.

Thought rows are also not camera-visible narration. If a camera can film the content,
or a microphone can hear it, mark it as narration, stage, dialogue, SFX, or command.
Parentheses are not a permission slip for decorative object prose.

Use thought at conversation breaks, before choices, or after a line lands and the
POV character cannot answer honestly. During active call-and-response, keep the
dialogue connected unless the interruption itself changes the pressure.

Avoid one-line moral summaries. Use thought to create playable hesitation.

## QA Contract

Validation should track:

- `thought` row count.
- Whether a dialogue-heavy scene has too few thought rows.
- Whether thought rows are actually private inference / unsaid cost, not visible action.
- Whether dialogue contains enough pressure punctuation and casual particles when the scene's tone requires warmth or banter.
- Whether each major character has a repeatable charm hook and character-owned punctuation play.
- Whether readable previews preserve `『』` for dialogue and `（ ）` for thought.
