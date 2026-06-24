---
id: codex_chat_creation_protocol
type: method_card
---

# Codex Chat Creation Protocol

## Call This When

Call this whenever the user asks through chat to create, rewrite, expand, or test a
VN/Galgame work.

## Core Rule

Codex chat is the active creative interface. The web UI is quarantined. Chat
responses must become workbench files and validated artifacts, not just visible
assistant prose.

## Required Flow

1. Classify the newest user intent.
2. Decide whether the change is reusable method knowledge or project-only memory.
3. For new work, create project memory before script text.
4. Create character cards with stable voice and liveliness +1.
5. Create route/state/scene design before drafting.
6. Run `draft-session`.
7. Write CSV and readable preview.
8. Validate, deep-audit, and classify quality debt.
9. Only then summarize output to the user.

## Output Contract

The final answer must state:

- project id
- visible title
- character memory files touched
- scene card and state delta files touched
- script/readable paths
- QA/deep-audit/quality-debt results

## Failure Signs

- Only chat text changes.
- Project memory is missing.
- Character voice is not anchored to a card.
- A scene has no state delta.
- The workflow depends on the quarantined web UI.
