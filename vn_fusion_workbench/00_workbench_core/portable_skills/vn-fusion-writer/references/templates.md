# VN Design Templates

Use these templates to create concise but complete design artifacts.

## Project Pitch

```markdown
Title:
Genre / Tone:
Player Role:
Core Promise:
Central Pressure:
Primary Mechanic:
Secondary Mechanic:
Reading Mode: ADV / NVL / mixed
Target Length:
Route Structure:
Replay Value:
Visual Motifs:
Audio Motifs:
Ending Philosophy:
```

## Character Voice Card

```markdown
Name:
Role in System:
Public Want:
Private Want:
Fear:
Social Mask:
Taboo Topic:
Default Speech Rhythm:
Under-Pressure Rhythm:
Favorite Dodge:
Lie Style:
Tenderness Style:
Cruelty Style:
Route Question:
Variables Affected:
```

## Scene Card

```markdown
Scene ID:
Route / Chapter:
Location / Time:
Background:
Sprites / CG:
BGM / SFX:
Entering Pressure:
Protagonist Want:
NPC Wants:
Withheld Truth:
New Information:
Choice Point:
Variables Changed:
Immediate Feedback:
Delayed Callback:
Exit Image:
QA Risk:
```

## Choice Ledger

```markdown
Choice ID:
Scene ID:
Menu Text:
Choice Type: identity / strategy / knowledge / relationship / resource / route
Visible Stakes:
Hidden Stakes:
Immediate Result:
Delayed Result:
Variables:
Failure / Bad-End Use:
Player Mental Model Note:
```

## Variable Ledger

```markdown
Variable:
Type: bool / int / enum / set
Visible To Player: yes / no
Purpose:
Changed In:
Checked In:
Payoff:
Tuning Notes:
```

## Route Map Skeleton

```markdown
Common Route
- C01:
- C02:
- Lock / Sorting Rule:

Route A
- Dramatic Question:
- Unique Mechanic:
- Required Flags:
- Key Bad End:
- Ending:

Route B
- Dramatic Question:
- Unique Mechanic:
- Required Flags:
- Key Bad End:
- Ending:

True Route / Final Route
- Unlock Rule:
- Prior Route Knowledge Used:
- Final Choice:
- Resolution:
```

## Script Sample Format

Use this format for readable drafting even if the final engine is undecided:

```renpy
label scene_id:
    scene bg_location_time
    play music "track_name"

    show character neutral at center
    narrator "Short narration that fits the visual state."

    character "A line with pressure."
    show character tense
    other "A reply that changes leverage."

    menu:
        "Action or spoken line with attitude.":
            $ flag_name = True
            "Immediate feedback line."

        "Another viable cost.":
            $ resource -= 1
            "Different feedback line."

    jump next_scene
```

## First Chapter Outline

```markdown
Chapter 1 Goal:
Player Learns:
Player Chooses:
System Teaches:
Bad End Tease:
Route Seeds:

Scenes:
1. Hook scene
2. First social pressure
3. First mechanic use
4. First consequence
5. Chapter choice
6. Aftermath callback
```
