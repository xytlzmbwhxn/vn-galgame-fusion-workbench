# Style Reference Pack

This pack records borrowed methods, not copied prose.

## Target Read

- ADV text boxes with strong dialogue blocks.
- Sparse narration that changes the next line or the player's available reading.
- Concrete objects: ticket, register, umbrella, door glass, camera dead zone.
- Urban Chinese realism with a light mystery edge.
- Emotional pressure carried by errands, records, favors, and delayed alarms.

## Reference Axes

### Dialogue Density

Borrow from VN dialogue advice: spoken lines should feel realistic without copying real-life filler. Dialogue needs selection, compression, and subtext.

Implementation:

- Let two characters speak for 5-10 clicks before a narration beat interrupts.
- A narration beat inside dialogue must alter leverage.
- Avoid using narration as a translation layer for every line.

### Route And Theme

Borrow from route-heavy Galgame structure: common route should introduce crisis, cast, background, and伏笔 without chewing exposition for the player.

Implementation:

- Common-route choices express what the player protects first.
- Route unlock is based on repeated behavior, not a final "pick a route" menu.
- Every bad end teaches one system rule or one moral cost.

### AI Character Control

Borrow from character-card, desktop-pet, and memory-bank systems:

- fixed persona
- example dialogue
- current state
- long-term memory
- promises and debts
- voice drift checks

Implementation:

- Character cards define identity.
- Character state JSON defines current psychology and allowed drift.
- Scene state delta writes back relationship, object, secret, promise, and deadline changes.

### Prose Linting

Borrow from Vale, textlint, write-good, and human-voice:

- rules should be explicit
- checks should be repeatable
- style violations should name the pattern
- a warning points to revision, not shame

Implementation:

- `vn_workbench.py validate` catches repeated dialogue/narration alternation.
- The project keeps a banned-pattern list.
- Voice and state files are required before a scene can pass cleanly.

## Project Do

- Use continuous dialogue when characters are testing each other.
- Use continuous interior narration only when the player's interpretation is changing.
- Let objects become relationship tools.
- Let choices carry mixed costs.
- Let the same object return with changed meaning.

## Project Avoid

- One line of dialogue followed by one explanatory narration line.
- Scene endings that state the lesson.
- Characters explaining their whole motive once pressured.
- Pretty weather that can be deleted without changing the scene.
- Dialogue that only exists to inform the player.
