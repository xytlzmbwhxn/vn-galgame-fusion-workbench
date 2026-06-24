from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = next(p for p in (ROOT / "02_projects").glob("017_*") if "?" not in p.name)
SRC = PROJECT / "02_generated_content/drafts/readable/便利店把雨收好_最终链路重写_20260624.md"
OUT = PROJECT / "02_generated_content/drafts/readable/便利店把雨收好_正史密度修订_20260624.md"
CSV_OUT = PROJECT / "02_generated_content/scripts/csv/便利店把雨收好_正史密度修订_20260624.csv"


HEADERS = [
    "scene_id",
    "beat_id",
    "row_type",
    "speaker",
    "text",
    "voice_target",
    "expression",
    "body_action",
    "bg",
    "bgm",
    "sfx",
    "choice_group",
    "choice_text",
    "choice_target",
    "condition",
    "effects",
    "memory_refs",
    "qa_notes",
]


ROLE_TO_ID = {"江迟": "CHR_jiangchi", "林檐": "CHR_linyan", "何姨": "CHR_heyi"}


MERGE_MAP: dict[str, list[str]] = {
    "001": ["收银机屏幕待机，绿色光点一闪一闪。"],
    "006": ["【演出】", "自动门响，雨声被门缝推了进来。"],
    "019": ["（她说得太快，像怕慢下来就得解释自己为什么一个人站在雨里。）"],
    "024": ["林檐伸手，又停住。"],
    "031": ["她笑了一下，手指落在伞柄牙印旁边，轻得像怕把旧胶带碰醒。"],
    "044": ["我把登记本推过去，笔滚到姓名栏旁边。"],
    "056": ["（她盯着那个“檐”。我写错，她大概也会笑，然后把这家店从明天的路线上划掉。）"],
    "065": ["她低头写号码。最后四位写到一半，门外末班公交驶过，车尾灯被雨水揉散。"],
    "077": ["【林檐】", "『今天小测结束就下雨，公交还刚好走掉。袜子和伞都没保住。』"],
    "079": ["她说完，看向那把蓝伞；伞柄牙印被水光照得发亮。"],
    "082": ["（她没有说自己也想回去，只把能开口的那件东西摆在柜台上。）"],
    "084": ["收银机旁贴着何姨的便签：失物签收留底，借伞押金，夜班不准离岗。最后一行被红笔圈得很重。"],
    "099": ["我拉开抽屉，黑伞压在一叠押金单下面，伞套上贴着一张旧标签：备用。"],
    "110": ["她把伞柄往自己那边轻轻挪了一点，又挪回去。"],
    "135": ["（逗号安全。逗号后面可以继续写，不用马上把句子交出去。）"],
    "141A": ["【江迟】", "『现在在箱子里，明天在本子里。』"],
    "160": ["她问完，立刻去看雨袋架，像刚才那句话被她塞进雨袋架下面。"],
    "162": ["（我认了，就要替她欠系统一栏；我不认，她今晚只能把玩笑一路撑回雨里。）"],
    "166": ["【江迟】", "『小票，或者失物本备注。』"],
    "169": ["【江迟】", "『小票在你手里，备注在我这里。』"],
    "178C": ["我按下打印，热敏纸吐出来，边缘卷着一点热。"],
    "190C": ["（小票会替我解释二十七分钟，也替她证明今晚有人认真等过。）"],
    "193D": ["（这张凭证没有纸，所以丢了也没人能赔。）"],
    "200": ["【江迟】", "『雨大，你拿两把不方便。』"],
    "206": ["林檐低头看蓝伞。这一次，她没有马上给它起新外号。"],
    "220": ["（她把“我妈”放出来以后，立刻伸手去捞玩笑；我不能替她捞，只能让那把伞在这里有个位置。）"],
    "223": ["我在失物本新开一栏：蓝伞寄存，明日自取；黑伞借出，押金备注。"],
    "242": ["她笑起来，笑声比刚进门时低一点，低到可以不用急着保护自己。"],
    "244": ["何姨的便签被风吹起一角：便利店没开托儿业务。豆浆钱从你工资扣。别摆臭脸。"],
    "277": ["她在便签末尾点了两下，两个黑点一个高一个低。"],
    "291": ["（她把明天说得很小，小到一杯豆浆就能压住；这样走进雨里时，旧伞也不会重得只剩下旧。）"],
    "294": ["【演出】", "自动门打开，雨声涨起来。林檐撑开黑伞。"],
    "304": ["她愣住，很快把伞沿压低。"],
    "308": ["门铃响。黑伞被风顶起，又被她压稳；旧蓝伞留在柜台边，伞柄朝着门口。"],
    "312": ["我把她的便签夹进失物本，两个黑点正对着押金栏。"],
    "315": ["收银机屏幕暗下去。雨还在下，失物箱空出一个位置。"],
    "318": ["（明天她会来。这句话还没写进备注，我已经替它留了格子。）"],
}


SKIP_IDS = {
    "002",
    "007",
    "020",
    "025",
    "032",
    "033",
    "045",
    "057",
    "058",
    "066",
    "067",
    "078",
    "080",
    "083",
    "085",
    "086",
    "087",
    "088",
    "100",
    "111",
    "136",
    "142A",
    "161",
    "163",
    "167",
    "170",
    "179C",
    "191C",
    "194D",
    "201",
    "207",
    "221",
    "222",
    "224",
    "225",
    "243",
    "245",
    "246",
    "247",
    "278",
    "292",
    "293",
    "295",
    "296",
    "305",
    "309",
    "310",
    "311",
    "313",
    "316",
    "317",
    "319",
}


LINE_REPLACEMENTS = {
    "『你们便利店的人都这么相信物理世界吗？』": "『那你们这儿晚上一定很安全。』",
    "『很危险欸，灵魂会被小票机收走的。』": "『连箱子都被要求板着脸。』",
    "『不要写成盐，也不要写成烟。盐会咸，烟会飘，我只是比较容易淋雨。』": "『不要写成盐，也不要写成烟。我今晚已经够湿了，再咸就很过分。』",
    "『评分系统正在被雨淋，加载很慢。』": "『评分系统今晚进水，暂不公布。』",
    "『不过没事，我腿多。』": "『不过没事，我还有两条腿，虽然它们现在都不太服我。』",
    "『而且我这双腿参加过高三二周目，耐久度应该比普通版本高一点。』": "『高三二周目嘛，总得比普通版本多一点耐久。』",
    "『黑伞同志还没出场，已经背债了。』": "『黑伞同志还没出场，账已经挂上了。』",
    "『听起来很可靠，也很社畜。』": "『听起来很可靠，也很累。』",
    "『不，它刚刚那个提示音非常铁算盘。』": "『它刚刚那个提示音很像在翻账本。』",
    "『哇，你们夜班人际关系好复杂。』": "『你们夜班同事还挺多。』",
    "『天气局联合数学组，对本人实施雨夜伏击。』": "『今天小测结束就下雨，公交还刚好走掉。』",
    "『战况惨烈，袜子阵亡，伞被俘虏，公交车叛逃。』": "『袜子和伞都没保住，我本人暂时幸存。』",
    "『它刚才那声，是在讨厌我这种雨夜空手套黑伞的人吧？』": "『它刚才那声，好像在说：空手借伞，胆子很大。』",
    "『谢谢是古代货币，流通范围广，情绪价值高。』": "『那我先欠着。谢谢这两个字，明天一起还。』",
    "『万一我明天迟到，你不能拿铁算盘威胁我，说林檐女士，你的信用分正在便利店门口淋雨。』": "『万一我明天迟到，你不能拿铁算盘威胁我，说林檐女士，黑伞正在替你扣分。』",
    "『很好，记账先生开始懂得节省点击次数了。』": "『很好，记账先生开始懂得省力了。』",
    "『完了。铁算盘变斗鸡眼了。』": "『完了。铁算盘看起来更凶了。』",
    "『合理慰问夜班员工。贿赂两个字自己走远一点。』": "『先声明，豆浆属于合理慰问夜班员工。』",
    "『今晚卖伞。』": "『今晚借伞。』",
    "『借伞。』": "『还记账。』",
    "『记账。』": "『嗯。』",
}


def parse_units(lines: list[str]) -> tuple[list[str], list[tuple[str, list[str]]]]:
    preamble: list[str] = []
    units: list[tuple[str, list[str]]] = []
    current_id: str | None = None
    current: list[str] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if re.fullmatch(r"\d{3}[A-Z]?", stripped):
            if current_id is None:
                preamble.extend(current)
            else:
                units.append((current_id, current))
            current_id = stripped
            current = []
        elif stripped.startswith("## ") and current_id is not None:
            units.append((current_id, current))
            current_id = f"__HEADING_{len(units)}"
            current = [lines[i]]
        else:
            current.append(lines[i])
        i += 1
    if current_id is None:
        preamble.extend(current)
    else:
        units.append((current_id, current))
    return preamble, units


def replace_lines(block: list[str]) -> list[str]:
    out: list[str] = []
    for line in block:
        stripped = line.strip()
        if stripped in LINE_REPLACEMENTS:
            out.append(line.replace(stripped, LINE_REPLACEMENTS[stripped]))
        else:
            out.append(line)
    return out


def render_readable() -> None:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    preamble, units = parse_units(lines)
    out: list[str] = ["# 便利店把雨收好_正史密度修订_20260624", ""]
    # Keep scene heading and opening cue from the previous draft.
    for line in preamble[2:]:
        out.append(line)
    for uid, block in units:
        if uid in SKIP_IDS:
            continue
        if uid.startswith("__HEADING_"):
            out.extend(block)
            continue
        out.append("")
        out.append(f"{uid}  ")
        if uid in MERGE_MAP:
            out.extend(MERGE_MAP[uid])
        else:
            out.extend(replace_lines(block))
    OUT.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def clean_quote(text: str) -> str:
    text = text.strip()
    if text.startswith("『") and text.endswith("』"):
        return text[1:-1]
    return text


def to_csv() -> None:
    lines = OUT.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, str]] = []
    seq = 0
    visible_id = "000"
    current_role: str | None = None
    choice_count = 0

    def add(row_type: str, text: str = "", speaker: str = "", **kwargs: str) -> None:
        nonlocal seq
        seq += 1
        row = {h: "" for h in HEADERS}
        row.update(
            {
                "scene_id": "S001",
                "beat_id": f"S001_density_20260624_{seq:04d}",
                "row_type": row_type,
                "speaker": speaker,
                "text": text,
            }
        )
        row.update(kwargs)
        note = row.get("qa_notes", "")
        row["qa_notes"] = (note + "; " if note else "") + f"source_visible_id={visible_id}"
        rows.append(row)

    def label(name: str) -> None:
        add("command", f"label:{name}", qa_notes="branch_label")

    def jump(name: str) -> None:
        add("command", f"jumpLabel:{name}", qa_notes="branch_jump")

    def state_effect(text: str) -> str:
        if "umbrella_recorded" in text:
            return "umbrella_recorded=true"
        if "early_trust" in text:
            return "early_trust=true"
        if "receipt_kept" in text:
            return "receipt_kept=true"
        if "receipt_hidden" in text:
            return "receipt_hidden=true"
        return "story_state_updated=true"

    label("S001_START")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("#"):
            if line.startswith("## 分支 A"):
                label("CHOICE_01_A")
            elif line.startswith("## 分支 B"):
                jump("CHOICE_01_REJOIN")
                label("CHOICE_01_B")
            elif line.startswith("## 回流") and not any(r["text"] == "label:CHOICE_01_REJOIN" for r in rows):
                label("CHOICE_01_REJOIN")
            elif line.startswith("## 分支 C"):
                label("CHOICE_02_C")
            elif line.startswith("## 分支 D"):
                jump("CHOICE_02_REJOIN")
                label("CHOICE_02_D")
            elif "再回流" in line and not any(r["text"] == "label:CHOICE_02_REJOIN" for r in rows):
                label("CHOICE_02_REJOIN")
            i += 1
            continue
        if re.fullmatch(r"\d{3}[A-Z]?", line):
            visible_id = line
            i += 1
            continue
        if line.startswith("【") and line.endswith("】"):
            current_role = line[1:-1]
            if current_role == "选择":
                choice_count += 1
                group = f"CHOICE_{choice_count:02d}"
                targets = {1: ["CHOICE_01_A", "CHOICE_01_B"], 2: ["CHOICE_02_C", "CHOICE_02_D"]}.get(choice_count, [])
                j = i + 1
                opt_index = 0
                while j < len(lines):
                    opt = lines[j].strip()
                    if not opt:
                        j += 1
                        continue
                    if opt.startswith("#") or re.fullmatch(r"\d{3}[A-Z]?", opt) or opt.startswith("【"):
                        break
                    match = re.match(r"^(\d+)\.\s*(.*)$", opt)
                    if match:
                        opt_index += 1
                        text = clean_quote(match.group(2).rstrip())
                        target = targets[opt_index - 1] if opt_index - 1 < len(targets) else f"{group}_{opt_index}"
                        effects = {
                            "CHOICE_01_A": "umbrella_recorded=true",
                            "CHOICE_01_B": "early_trust=true",
                            "CHOICE_02_C": "receipt_kept=true",
                            "CHOICE_02_D": "receipt_hidden=true",
                        }.get(target, "choice_made=true")
                        add(
                            "choice",
                            text,
                            choice_group=group,
                            choice_text=text,
                            choice_target=target,
                            effects=effects,
                            memory_refs="CHR_jiangchi;CHR_linyan",
                            qa_notes="visible_choice; branch_debt_persistent",
                        )
                    j += 1
                current_role = None
                i = j
                continue
            if current_role == "状态":
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                state_text = lines[j].strip() if j < len(lines) else ""
                add("command", "state:" + state_text, effects=state_effect(state_text), qa_notes="branch_state_and_persistent_debt")
                current_role = None
                i = j + 1
                continue
            i += 1
            continue
        if re.match(r"^\d+\.\s*", line):
            i += 1
            continue
        if current_role in ROLE_TO_ID:
            cid = ROLE_TO_ID[current_role]
            add(
                "dialogue",
                clean_quote(line),
                speaker=cid,
                voice_target=cid,
                expression="dry" if cid == "CHR_jiangchi" else "lively",
                body_action="sprite_expression",
                memory_refs=cid,
                qa_notes="click_function=dialogue_pressure_or_charm",
            )
            current_role = None
        elif current_role == "系统":
            add("command", "system_message:" + clean_quote(line), sfx="ui_prompt", qa_notes="system_prompt")
            current_role = None
        elif current_role == "演出":
            add("narration", line, bg="convenience_store_rain_night", body_action="stage_image", qa_notes="click_function=screen_state")
            current_role = None
        elif line.startswith("（") and line.endswith("）"):
            add(
                "thought",
                line[1:-1],
                speaker="CHR_jiangchi",
                voice_target="inner",
                expression="inner",
                memory_refs="CHR_jiangchi",
                qa_notes="click_function=private_inference_or_cost; thought_job=private_pressure",
            )
        else:
            add("narration", line, bg="convenience_store_rain_night", body_action="object_or_stage_change", qa_notes="click_function=screen_state_or_object_operation")
        i += 1
    if not any(r["text"] == "label:CHOICE_02_REJOIN" for r in rows):
        label("CHOICE_02_REJOIN")
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    render_readable()
    to_csv()
    print(OUT)
    print(CSV_OUT)
