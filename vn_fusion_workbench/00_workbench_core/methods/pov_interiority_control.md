---
id: pov_interiority_control
type: method_card
---

# POV Interiority Control

## Purpose

心理描写和人称绑定。VN 不是随便在括号里写任何人的想法。
默认心理属于当前 POV。配角心理可以写，但必须有演出许可。

## Default Rule

- 没有标记时，括号心理属于当前默认视角角色。
- 当前默认视角必须在稿件开头写清楚：默认视角：角色名。
- 如果出现配角心理，必须先用 @pov 角色名 标记。
- 视角切回时也要标记：@pov 顾淮 / @pov 主角。

## When To Use Protagonist Thought

适合写主角心理的情况：

- 对白块之后，需要玩家理解误读、犹豫、选择成本。
- 选择前，主角知道自己选哪边都会付代价。
- 主角手里有物件、规则、债务，正在拿它遮掩感情。
- 玩家需要知道主角为什么没有立刻回话。

不适合写主角心理的情况：

- 只是重复刚才台词。
- 只是描述镜头能拍到的动作。
- 只是总结主题。
- 每句对白后都插一句想法。

## When To Use Side Character Thought

配角心理只在以下情况使用：

1. 明确 POV 切换段落，比如 @pov 夏梨。
2. 路线分支或隐藏好感度需要玩家短暂看到配角的真实压力。
3. 反差喜剧：玩家知道配角在硬撑，主角不知道。
4. 结尾小回扣：用极短配角心理留下糖点或悬念。
5. 多视角作品，场景卡允许切换。

配角心理不应该用于替作者解释角色。它必须增加玩家的戏剧性信息差。

## Marking Convention

Readable draft:

- 默认视角：顾淮
- @pov 顾淮
- @pov 夏梨
- （心理文本）

CSV:

- row_type=command, text=@pov CHR_linyan
- row_type=thought, speaker=CHR_linyan, text=...

## Side POV Density

- 一场短废萌最多 1 个配角 POV 口袋。
- 每个配角 POV 口袋 1-3 行。
- 配角 POV 结束后必须切回默认 POV 或结束场景。
- 配角 POV 应该制造玩家知道、主角不知道的甜点或压力。

## Examples

Bad:
（她其实很高兴。）

Better with side POV:
@pov 夏梨
（完蛋。顾会计刚才那句“批准”，听起来有点太像偏心了吧。）
（小十二，你没有听见。你只是一盒布丁。）

@pov 顾淮

## QA

Fail if:
- thought rows exist and no default POV is declared.
- side character thought appears without @pov.
- @pov switches are not closed or are used to explain theme.
- side POV repeats information the player already knows.
