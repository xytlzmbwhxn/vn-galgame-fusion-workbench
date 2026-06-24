---
id: sentence_kernel_display_voice
type: method_card
---

# Sentence Kernel And Display Voice

## Call This When

Before drafting Chinese VN dialogue, narration, inner monologue, document text, or readable script previews.

## Goal

Separate sentence logic from surface decoration. A character's line should be generated from their inner motor, social pressure, and available escape route. Display marks then present the line clearly in VN form.

## Layer Rules

- Narration: no speaker brackets; concrete camera, object, process, and timing. Keep it dry unless the POV is explicitly lyrical.
- Dialogue: name box or readable label carries speaker identity; the line itself can use no final punctuation if it is a command, fragment, or interrupted move. Do not assume one speaker equals one textbox; the click beat decides.
- Inner thought: use a different display mark from spoken dialogue in readable drafts, such as `（...）`, and keep it more private than narration. It should contain inference, hesitation, or unsaid cost, not camera-visible action.
- Quoted document or system text: use `『...』` or a command/comment row; make it sound institutional, not emotional.
- Choice text: concise action or spoken intent. It must reveal what kind of cost the player is choosing.

## Character Sentence Kernel

For each major speaker, define these before drafting:

- sentence engine: what pressure makes their sentence move
- default line shapes: command, question, fragment, bargaining chain, joke, formal sentence, copied institutional phrase
- forbidden line shapes: the forms that would make them sound like another character
- unclosed lines: when they are allowed to end without punctuation
- particles and fillers: words they naturally use under stress
- cut point: what noun or admission they refuse to finish
- recovery move: what they do after saying too much

## Punctuation Rules

- Full stop: use when a line is deliberately closed, controlled, or procedural.
- No final punctuation: use for clipped commands, half answers, or a line that expects immediate action.
- Question mark: use when the speaker is pushing, testing, or refusing the other person's frame.
- Exclamation mark: use only when the mask breaks or a command becomes urgent.
- Ellipsis: use only when a specific noun is swallowed.
- Dash: use for self-correction, interruption, or a line cut by another action.

## Output Fields

- display_layer
- sentence_engine
- allowed_line_shapes
- unclosed_line_rule
- particles_and_fillers
- cut_point
- recovery_move

## Failure Signs

- every line has a neat final punctuation mark
- all dialogue uses the same literary sentence shape
- brackets are used as decoration without changing display layer
- narration explains emotion already shown by voice
- a character says a sentence that their social position would not produce
