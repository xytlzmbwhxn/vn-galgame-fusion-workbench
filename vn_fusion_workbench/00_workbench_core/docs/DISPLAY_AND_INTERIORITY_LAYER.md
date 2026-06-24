# Display And Interiority Layer

The workbench keeps engine-facing script text and human review text separate.

## Row Types

- `dialogue`: raw spoken textbox text. Readable previews wrap it as `【角色】『台词』`.
- `thought`: inner monologue or POV pressure. Readable previews wrap it as `【角色】（心理文本）`.
- `narration`: visible description or transition text.
- `command`: stage cues, labels, jumps, effects, and engine commands.

## Why Dialogue Is Raw In CSV

Most VN engines already have a name box and dialogue layer. Putting `『』` inside CSV dialogue can pollute engine exports. The Markdown preview adds display marks for human review, while exporters keep the engine text clean.

## QA Signals

`validate` tracks:

- thought row count and thought-to-dialogue ratio.
- casual speech particles and character-specific looseness.
- pressure punctuation: questions, exclamations, pauses, cutoffs.
- line ending variety by speaker.
- low-payload clicks and overlong thought boxes.

This layer exists because structure alone does not make a scene feel like a Galgame. The review surface must show name boxes, spoken lines, inner thought, and stage cues as different reading modes.
