# Visual Novel Methodology

Use this file as the working method for visual novels, galgame/AVG scripts, and choice-based interactive fiction.

## Core Principles

1. Treat the text box as the real page. A prose paragraph that works in a novel may feel slow when every sentence requires a click.
2. Make every screen state intentional: background, sprite expression, name box, text length, silence, BGM, SFX, and menu timing all count as writing.
3. Start from pressure, then decide structure. Romance, mystery, horror, comedy, political intrigue, and survival all need different branch logic.
4. Keep player agency legible. The player should know the kind of thing a choice is deciding, even when they cannot know every consequence.
5. Budget branches by importance. Line variation is cheap, scene variation is moderate, route variation is expensive, ending variation is very expensive.
6. Reuse locations and scenes with changed meaning. Repetition becomes powerful when a later route reveals new context.
7. Track consequences with variables, but pay them off in prose. A hidden flag only matters when it changes a line, silence, route, clue, or cost.
8. Make failure authored. Bad ends, failed checks, and missed routes should reveal theme, character, or useful information.
9. Prototype playable rhythm early. VN pacing is discovered by clicking through scenes, not by reading a document.

## VN Text Units

- Beat: one click, one image/text state, one emotional pulse.
- Line: one character utterance or narration unit.
- Exchange: a short back-and-forth that shifts leverage.
- Scene: a location/time unit with a pressure, turn, and exit.
- Sequence: multiple scenes that resolve a short-term objective.
- Route: a sustained interpretation of the premise through one character, faction, mystery path, or worldview.

ADV mode favors immediacy, face-to-face pressure, sprite work, and dialogue rhythm. NVL mode favors memory, documents, inner narration, dense atmosphere, and long-form revelation. Switch modes only when the reading posture should change.

## Branch Structures

### Kinetic

Linear VN with no meaningful choices. Use for tightly controlled tragedy, horror, mystery, or literary drama. The design work shifts to pacing, staging, and scene order.

### Common Route With Character Routes

A shared opening introduces cast, world, premise, and route seeds. Choices accumulate affection, trust, suspicion, knowledge, or worldview points until the story locks into a route. Each route should reinterpret the common route, not merely add private episodes.

Common route duties:

- Establish why the cast repeatedly meets.
- Give each route a visible unresolved tension.
- Seed route-specific mysteries that feel innocuous at first.
- Avoid a long neutral social hangout unless the banter itself is the core reward.
- Place early choices that express the player character, then later choices that commit them.

### Branch-And-Bottleneck

The player diverges locally, then returns to shared major scenes. Use this when production scope is limited and the story still needs agency. Make the bottleneck feel altered by remembered state: changed dialogue, altered relationship, different clue, missing person, cost, or emotional framing.

### Gauntlet

A mostly linear path with failure branches, short detours, and bad ends. Use for horror, survival, trials, curses, locked-room scenarios, or stories about constrained systems. The pleasure comes from pressure and authored failure.

### Time Cave

Broad branches with little reconvergence. Use for short, replayable works where discovery and surprise matter more than a long main plot. Dangerous for large VNs because content cost grows fast.

### Storylet / Quality-Based

Content units unlock through prerequisites: location, time, relationship, inventory, knowledge, previous choices, mood, or danger level. Use for open exploration, town life, mystery boards, travel, repeated days, and relationship webs. Always maintain a spine so the player does not feel lost.

### Time Loop / Hub Loop

Each run yields knowledge, flags, voices, items, or route keys. Use for mysteries, horror, roguelite VN structures, unreliable worlds, or repeated interrogations. The loop must change what the player can notice and attempt.

### Parallel POV

Multiple protagonists or perspectives affect each other. Use for ensemble mysteries, citywide crises, courtroom/investigation stories, and puzzle-like route solving. Provide a readable map or timeline when complexity becomes part of the game.

## Route Design

Each route needs a distinct dramatic question:

- Romance route: "What kind of person must the protagonist become to love this person honestly?"
- Mystery route: "Which truth becomes visible only from this angle?"
- Faction route: "Which cost does this alliance normalize?"
- Horror route: "Which fear does this path make intimate?"
- True route: "What can the player now understand because previous routes taught them how to read the world?"

Route lock methods:

- Point threshold: affection/trust/suspicion reaches a value.
- Flag bundle: key choices collected.
- Explicit commitment: the player chooses a character/faction/path.
- Knowledge lock: the player has seen prior endings or found clues.
- Failure lock: a bad end teaches the route condition.

Avoid route logic that requires blind walkthrough behavior unless the project intentionally embraces puzzle-VN route solving. If route access is hidden, provide repeated pattern language so players can infer the system.

## Scene Design

Scene card minimum:

- Location and time.
- Visual state and sound state.
- Entering pressure.
- The protagonist's immediate want.
- Each major NPC's immediate want.
- Private agenda or withheld truth.
- New fact, cost, or relationship shift.
- Choice or irreversible turn.
- Exit image.
- Variables changed.

Strong VN scenes often use a "quiet pressure, social maneuver, visual interruption, choice, aftermath line" rhythm. The interruption can be a phone buzz, a sprite expression drop, an SFX, a CG reveal, a background change, a name box change, or a line that refuses the current topic.

## Dialogue Method

Build a voice card for every major character:

- Vocabulary: formal, blunt, slangy, ornate, technical, childish, ritualistic.
- Sentence shape: short jabs, long spirals, clipped fragments, questions, commands, jokes.
- Social mask: helpful, bored, seductive, professional, helpless, theatrical.
- Pressure response: attack, deflect, flatter, freeze, joke, confess, bargain, vanish.
- Taboo: the topic they never name cleanly.
- Tell: a repeated gesture, punctuation habit, pet phrase, or kind of omission.

Each exchange should shift leverage. A line can answer, dodge, raise the price, expose a wound, misread the other person, or force a new choice. Dialogue that only conveys lore should be broken into interactable objects, conflict, investigation, or a character trying to hide the lore.

VN-specific dialogue checks:

- Can this line fit in a text box without visual fatigue?
- Does the click boundary create a rhythm or merely chop a paragraph?
- Does the speaker sound like themselves without the name box?
- Does the line give the next speaker something to react to?
- Can the same information be delivered through a sprite change, silence, or object?

## Choice Design

Good choice menus carry at least one of these tensions:

- Values: safety against honesty, loyalty against truth, mercy against responsibility.
- Strategy: gather information, spend resource, protect relationship, change location.
- Identity: cold, reckless, tender, ambitious, obedient, suspicious.
- Knowledge: accuse, inspect, ask, lie, reveal, conceal.
- Timing: act now, delay, prepare, interrupt, follow.
- Cost: lose time, reveal weakness, take injury, owe a favor, burn a route.

Feedback types:

- Immediate: line response, expression, point change, clue, menu change.
- Delayed: callback, altered rumor, missing option, changed relationship scene.
- Structural: route lock, bad end, unlocked perspective, new map node.
- Interpretive: same event reads differently because the player knows more.

Avoid false drama. If a menu looks consequential, pay it off. If it is only roleplay flavor, make it feel like flavor through copy, placement, and scale.

## Consequence And Mental Model

Players form a mental model of what the game simulates. Keep that model stable:

- Do not imply the player can solve a problem through a route the system cannot support.
- If a choice is remembered, show how it is remembered.
- If a choice is ignored, keep it small, local, or clearly expressive.
- If a system uses hidden stats, let prose reveal the pattern over time.
- If a system uses visible stats, tune checks so players are not forced into perfect builds.

Useful consequence categories:

- Cosmetic: name, outfit, small line, UI label.
- Local: this scene changes.
- Relational: an NPC's later behavior changes.
- Informational: new clue or interpretation.
- Mechanical: resource, stat, clock, unlock.
- Structural: route, ending, scene order, POV.

## Writing Workflow

1. Write the linear golden path in scene cards.
2. Mark decision points by emotional pressure, not by arbitrary chapter spacing.
3. Decide branch scale at each point: line, exchange, scene, route, ending.
4. Create a variable ledger before drafting.
5. Draft a small vertical slice: one intro, one choice, one consequence, one callback.
6. Click-test the slice and cut text until the rhythm works.
7. Expand one route at a time, keeping shared bottlenecks reactive.
8. Build route maps and player-facing maps when route solving is part of the fun.
9. Add bad ends that teach rules, reveal character, or sharpen dread.
10. Run style QA, branch QA, and state QA.

## Branch Budget

Prefer these before creating full new routes:

- Conditional line variants.
- Conditional menu options.
- Re-enterable investigation nodes.
- Route-specific reinterpretation of a shared scene.
- Character-specific interruption in a shared scene.
- One shared outcome reached through different emotional costs.
- A later callback that validates the earlier choice.

Spend full-route budget only when the branch changes the central dramatic question.

## QA Checklist

- The first 10 minutes show the promise of both story and gameplay.
- The player can explain what kinds of choices matter.
- Major choices carry mixed costs.
- Every route has unique emotional, informational, and mechanical value.
- No route feels like the "wrong" route unless that is intentional and rewarding.
- Replayed shared scenes gain new meaning or become skippable.
- Bad ends are short, sharp, and useful.
- The true route requires understanding, not only flag collection.
- The ending resolves the player role, not just the plot.
