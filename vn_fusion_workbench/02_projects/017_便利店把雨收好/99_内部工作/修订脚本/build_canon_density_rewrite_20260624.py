from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROJECT = Path(__file__).resolve().parents[2]

READABLE = PROJECT / "02_generated_content" / "drafts" / "readable" / "便利店把雨收好_正史密度重写_20260624.md"
CSV_OUT = PROJECT / "02_generated_content" / "scripts" / "csv" / "便利店把雨收好_正史密度重写_20260624.csv"
NOTES = PROJECT / "99_内部工作" / "修订记录" / "便利店把雨收好_正史密度重写_20260624_修订说明.md"

FIELDS = [
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


def row(scene, beat, row_type, text="", speaker="", **kw):
    base = {field: "" for field in FIELDS}
    base.update(
        {
            "scene_id": scene,
            "beat_id": beat,
            "row_type": row_type,
            "speaker": speaker,
            "text": text,
        }
    )
    base.update(kw)
    if row_type == "dialogue" and speaker:
        base["voice_target"] = base["voice_target"] or speaker
        base["body_action"] = base["body_action"] or "立绘随台词表情变化"
    if row_type == "narration":
        base["body_action"] = base["body_action"] or "画面/物件状态变化"
    if row_type == "thought":
        base["body_action"] = base["body_action"] or "内心独白"
    return base


R = []

R += [
    row("S001", "S001_000", "command", "label:S001_雨袋架旁边", bg="便利店_夜_雨", bgm="雨夜低频", sfx="自动门叮咚", qa_notes="scene_entry"),
    row("S001", "S001_001", "narration", "雨贴着自动门底下挤进来，先湿了脚垫，再把“请勿滑倒”的黄贴纸泡得发亮。", qa_notes="click_function=entry_image+screen_state"),
    row("S001", "S001_002", "narration", "我把雨伞套的纸牌扶正。纸牌慢慢歪回去，夜班用品也有自己的脾气。", qa_notes="click_function=object_state+POV_tone"),
    row("S001", "S001_003", "dialogue", "欢迎光——", "CHR_jiangchi", qa_notes="click_function=interrupted_greeting"),
    row("S001", "S001_004", "dialogue", "先别欢迎。", "CHR_linyan", qa_notes="click_function=pressure_owner_linyan"),
    row("S001", "S001_005", "dialogue", "我现在听见“欢迎光临”四个字，脑子里就自动弹出第二件半价。很可怕的，像便利店咒语。", "CHR_linyan", qa_notes="click_function=cover_shame_with_joke"),
    row("S001", "S001_006", "dialogue", "还有，你们这个雨袋架站得好端正喔，跟班主任派来的监察委员一样。", "CHR_linyan", qa_notes="click_function=object_nickname+voice"),
    row("S001", "S001_007", "dialogue", "所以我先问清楚，便利店有没有把雨收起来的服务？有的话我办会员，没有的话我投诉天气。", "CHR_linyan", qa_notes="click_function=request_disguised_as_comedy"),
    row("S001", "S001_008", "narration", "她一口气说完，脚尖停在黄线外，眼睛却已经绕到雨袋架下面。失物箱的盖子没扣严，露出一截旧蓝色。", qa_notes="click_function=screen_state+hidden_goal"),
    row("S001", "S001_009", "thought", "那一截旧蓝色比她嘴里的天气投诉先到柜台。", qa_notes="thought_job=private_inference;click_function=POV_reads_priority"),
    row("S001", "S001_010", "thought", "箱子要是空，她就得亲手把那串玩笑捡回来。", qa_notes="thought_job=private_cost;click_function=stakes_before_reply"),
    row("S001", "S001_011", "dialogue", "雨伞套免费。雨收不了。失物箱可以看，拿错要登记。", "CHR_jiangchi", qa_notes="click_function=procedure_reply+relation_pressure"),
    row("S001", "S001_012", "dialogue", "哇，你从“欢迎光临”直接跳到“拿错登记”，中间的人类缓冲区呢？被热饮柜吃掉了吗？", "CHR_linyan", qa_notes="click_function=tease_clerk_voice"),
    row("S001", "S001_013", "dialogue", "热饮柜不吃人。", "CHR_jiangchi", qa_notes="click_function=dry_counter"),
    row("S001", "S001_014", "dialogue", "那太好了，我今天已经够倒霉了，暂时不想成为关东煮亲属。", "CHR_linyan", qa_notes="click_function=continues_joke+fatigue_leak"),
    row("S001", "S001_015", "dialogue", "我要找一把蓝伞。旧的，伞骨有点往左偏，撑开以后总想替我绕开晚自习。", "CHR_linyan", qa_notes="click_function=usable_information+voice"),
    row("S001", "S001_016", "dialogue", "手柄缠透明胶，胶下面有牙印。小时候的牙印。现在的我已经进化了，最多咬笔盖。", "CHR_linyan", qa_notes="click_function=object_feature+shame_cover"),
    row("S001", "S001_017", "dialogue", "你要笑的话，先排队。我本人还没笑完。", "CHR_linyan", qa_notes="click_function=defensive_charm"),
    row("S001", "S001_018", "command", "@sfx 收银机滴", sfx="收银机滴", qa_notes="click_function=machine_callback"),
    row("S001", "S001_019", "dialogue", "它笑了。", "CHR_jiangchi", qa_notes="click_function=dry_join_play"),
    row("S001", "S001_020", "dialogue", "铁算盘一号？你们店的电子员工素质好差。", "CHR_linyan", qa_notes="click_function=nickname_created"),
    row("S001", "S001_021", "narration", "我拉出失物本。纸页被空调翻开，停在昨天的雨伞记录旁。", qa_notes="click_function=work_action"),
    row("S001", "S001_022", "dialogue", "找伞写四项。姓名，联系方式，物品特征，遗失时间。", "CHR_jiangchi", qa_notes="click_function=procedure_pressure"),
    row("S001", "S001_023", "dialogue", "特征越丢脸，找回来的概率越高。", "CHR_jiangchi", qa_notes="click_function=procedure_as_comfort"),
    row("S001", "S001_024", "dialogue", "你这个安慰方式，刚从冰柜里拿出来的吧？", "CHR_linyan", qa_notes="click_function=voice_response"),
    row("S001", "S001_025", "dialogue", "经验。", "CHR_jiangchi", qa_notes="click_function=clipped_answer"),
    row("S001", "S001_026", "dialogue", "经验先生，你刚才脑内飘过“未知生物标记领地”这几个字了吧？", "CHR_linyan", qa_notes="click_function=tease_guess"),
    row("S001", "S001_027", "dialogue", "没写。", "CHR_jiangchi", qa_notes="click_function=dodge"),
    row("S001", "S001_028", "dialogue", "没写就行。没写的坏话暂时无罪。", "CHR_linyan", qa_notes="click_function=accepts_rule_play"),
    row("S001", "S001_029", "narration", "她把笔拍到柜台上，拍完又往我这边推了半厘米。", qa_notes="click_function=body_leak"),
    row("S001", "S001_030", "dialogue", "名字，林檐。树林的林，屋檐的檐。雨落下来会先撞到的那个檐。", "CHR_linyan", qa_notes="click_function=identity_info+voice"),
    row("S001", "S001_031", "dialogue", "电话我也给。你不要露出“客户终于配合流程”的表情。", "CHR_linyan", qa_notes="click_function=trust_step"),
    row("S001", "S001_032", "thought", "她把名字报得很熟，熟到像先替别人问过自己。", qa_notes="thought_job=private_inference;click_function=name_pressure"),
    row("S001", "S001_033", "thought", "我差点问她为什么是屋檐。笔尖停住的时候，失物本先替我闭嘴。", qa_notes="thought_job=avoided_question;click_function=POV_restraint"),
    row("S001", "S001_034", "command", "@choice CHOICE_01 蓝伞登记", choice_group="CHOICE_01", qa_notes="choice_group"),
    row("S001", "S001_035A", "choice", "", choice_group="CHOICE_01", choice_text="按失物流程登记", choice_target="S001_036A", effects="umbrella_recorded=true", qa_notes="choice_axis=procedure_first"),
    row("S001", "S001_035B", "choice", "", choice_group="CHOICE_01", choice_text="先拿箱里的蓝伞给她确认", choice_target="S001_036B", effects="early_trust=true", qa_notes="choice_axis=emotion_first"),
    row("S001", "S001_035A_LABEL", "command", "label:S001_036A", condition="umbrella_recorded", qa_notes="branch_label"),
    row("S001", "S001_036A", "dialogue", "我写“手柄旧牙印”。", "CHR_jiangchi", condition="umbrella_recorded", qa_notes="click_function=immediate_feedback"),
    row("S001", "S001_037A", "dialogue", "不会写成熟复读生、未知生物、领地意识。", "CHR_jiangchi", condition="umbrella_recorded", qa_notes="click_function=dry_protection"),
    row("S001", "S001_038A", "dialogue", "你明明都想好了？！", "CHR_linyan", condition="umbrella_recorded", qa_notes="click_function=comic_pressure"),
    row("S001", "S001_039A", "dialogue", "没落笔。", "CHR_jiangchi", condition="umbrella_recorded", qa_notes="click_function=rule_dodge"),
    row("S001", "S001_040A", "dialogue", "行吧，旧牙印可以。旧这个字很优秀，听起来它已经退休，不再代表我本人。", "CHR_linyan", condition="umbrella_recorded", qa_notes="click_function=accepts_record"),
    row("S001", "S001_035B_LABEL", "command", "label:S001_036B", condition="early_trust", qa_notes="branch_label"),
    row("S001", "S001_036B", "narration", "我从失物箱里取出一把蓝伞。伞面褪色，手柄干净得过分。", condition="early_trust", qa_notes="click_function=object_test"),
    row("S001", "S001_037B", "dialogue", "啊。", "CHR_linyan", condition="early_trust", qa_notes="click_function=recognition_drop"),
    row("S001", "S001_038B", "dialogue", "太乖了。我的那把一撑开就往左偏，像见到数学老师想绕路。", "CHR_linyan", condition="early_trust", qa_notes="click_function=feature_detail+voice"),
    row("S001", "S001_039B", "dialogue", "这里没有牙印，清白得很可疑。", "CHR_linyan", condition="early_trust", qa_notes="click_function=confirms_wrong_item"),
    row("S001", "S001_040B", "dialogue", "那继续登记。", "CHR_jiangchi", condition="early_trust", qa_notes="click_function=return_to_procedure"),
    row("S001", "S001_041B", "dialogue", "你刚才可以直接走流程的。", "CHR_linyan", condition="early_trust", qa_notes="click_function=trust_notice"),
    row("S001", "S001_042B", "dialogue", "先看过，明天比较不会赔进去。", "CHR_jiangchi", condition="early_trust", qa_notes="click_function=care_as_reason"),
    row("S001", "S001_043B", "dialogue", "谢谢。正经版的，不准用收银机语气接。", "CHR_linyan", condition="early_trust", qa_notes="click_function=relationship_gain"),
    row("S001", "S001_044B", "dialogue", "收到。", "CHR_jiangchi", condition="early_trust", qa_notes="click_function=clerk_accepts"),
    row("S001", "S001_045", "command", "@merge CHOICE_01_REJOIN", qa_notes="rejoin"),
    row("S001", "S001_046", "dialogue", "遗失时间。六点四十到七点，范围太宽。", "CHR_jiangchi", qa_notes="click_function=work_problem"),
    row("S001", "S001_047", "dialogue", "公交站、门口、热饮柜、雨袋架，四个点都可能。监控要店长权限，何姨十点半睡，现在十点四十八。", "CHR_jiangchi", qa_notes="click_function=constraints"),
    row("S001", "S001_048", "dialogue", "电话打过去，她会先骂我，再骂你，最后骂雨。", "CHR_jiangchi", qa_notes="click_function=dry_humor+stakes"),
    row("S001", "S001_049", "dialogue", "所以先看收银台最近十五分钟，确认你有没有把手上这把也弄丢。", "CHR_jiangchi", qa_notes="click_function=action_plan"),
    row("S001", "S001_050", "dialogue", "你怀疑我连替身都保不住？", "CHR_linyan", qa_notes="click_function=defensive_play"),
    row("S001", "S001_051", "dialogue", "我怀疑你刚才差点把笔盖吞了。", "CHR_jiangchi", qa_notes="click_function=observed_pressure"),
    row("S001", "S001_052", "dialogue", "那叫焦虑式文具管理！", "CHR_linyan", qa_notes="click_function=comic_denial"),
    row("S001", "S001_053", "command", "@sfx 键盘轻响", sfx="键盘轻响", qa_notes="screen_shift"),
    row("S001", "S001_054", "narration", "监控画面弹出来。镜头把便利店拍成发白的盒子，林檐退到黄线外，嘴上还在跟黄线打招呼。", qa_notes="click_function=screen_state+character_bit"),
    row("S001", "S001_055", "dialogue", "黄线大人，我遵守了。铁算盘一号，你也看见了。", "CHR_linyan", qa_notes="click_function=object_witness"),
    row("S001", "S001_056", "dialogue", "如果我等会儿激动，请你们一起作证，我没有碰店员的神圣键盘。", "CHR_linyan", qa_notes="click_function=prepares_emotional_risk"),
    row("S001", "S001_057", "dialogue", "键盘暂时安全。", "CHR_jiangchi", qa_notes="click_function=dry_ack"),
    row("S001", "S001_058", "narration", "画面倒到十点三十六。林檐站在热饮柜前，坏伞靠在右侧雨袋架。她没有买东西，只盯着豆浆看了十一秒。", qa_notes="click_function=new_evidence"),
    row("S001", "S001_059", "dialogue", "你来过。没买东西。看了豆浆。走的时候没拿伞。", "CHR_jiangchi", qa_notes="click_function=evidence_sequence"),
    row("S001", "S001_060", "dialogue", "你能不能别像播案情回顾……", "CHR_linyan", qa_notes="click_function=shame_response"),
    row("S001", "S001_061", "dialogue", "那我换说法。你当时很冷，也很饿。", "CHR_jiangchi", qa_notes="click_function=softens_evidence"),
    row("S001", "S001_062", "dialogue", "但你没有进来求助。", "CHR_jiangchi", qa_notes="click_function=unsafe_observation"),
    row("S001", "S001_063", "thought", "监控屏停在她盯着豆浆的那一帧。我把流程表往心里拉了一下，没拉住。", qa_notes="thought_job=self_check;click_function=POV_cost"),
    row("S001", "S001_064", "dialogue", "我那时候考砸了。", "CHR_linyan", qa_notes="click_function=mask_crack"),
    row("S001", "S001_065", "dialogue", "数学卷子，红得特别热闹。老师说我的基础像旧楼漏水，哪里都能滴。", "CHR_linyan", qa_notes="click_function=backstory_as_voice"),
    row("S001", "S001_066", "dialogue", "我就想，旧楼也没自己报名漏水嘛。", "CHR_linyan", qa_notes="click_function=defensive_joke_soft"),
    row("S001", "S001_067", "dialogue", "后来伞找不到，车也走了。我站在站牌下面，忽然很想听我妈骂我。", "CHR_linyan", qa_notes="click_function=mother_reveal"),
    row("S001", "S001_068", "dialogue", "她会说，林檐，你连咬过的伞都看不住，长大以后怎么管自己啊。", "CHR_linyan", qa_notes="click_function=memory_voice"),
    row("S001", "S001_069", "dialogue", "然后她会把伞拿过去，骂我两句，再用透明胶给它缠一圈。", "CHR_linyan", qa_notes="click_function=object_emotion"),
    row("S001", "S001_070", "dialogue", "现在没人缠了。", "CHR_linyan", qa_notes="click_function=emotional_turn"),
    row("S001", "S001_071", "command", "@sfx 微波炉门打开", sfx="微波炉门打开", qa_notes="action_after_reveal"),
    row("S001", "S001_072", "narration", "我拿了两杯豆浆。杯套碰到柜台，热气往上冒。", qa_notes="click_function=care_action"),
    row("S001", "S001_073", "dialogue", "第二件半价。", "CHR_jiangchi", qa_notes="click_function=care_disguised_as_sale"),
    row("S001", "S001_074", "dialogue", "你这个人……我都快讲到伤心段落了，你插入促销？", "CHR_linyan", qa_notes="click_function=relief_through_comedy"),
    row("S001", "S001_075", "dialogue", "你看了十一秒。", "CHR_jiangchi", qa_notes="click_function=evidence_care"),
    row("S001", "S001_076", "dialogue", "监控先生，求你把嘴闭上。", "CHR_linyan", qa_notes="click_function=nickname_shift"),
    row("S001", "S001_077", "dialogue", "烫。", "CHR_jiangchi", qa_notes="click_function=practical_care"),
    row("S001", "S001_078", "dialogue", "这句提醒来得很及时，比昨晚版本进步巨大。", "CHR_linyan", qa_notes="click_function=accepts_care"),
    row("S001", "S001_079", "narration", "她接过豆浆，两只手捧住。肩膀慢慢降下来。", qa_notes="click_function=visible_emotional_shift"),
    row("S001", "S001_080", "narration", "监控快进。小学生买了水果糖，低头穿雨衣，顺手拿走了那把旧蓝伞。", qa_notes="click_function=case_solution"),
    row("S001", "S001_081", "dialogue", "小孩拿的。看起来还挺普通。", "CHR_linyan", qa_notes="click_function=unexpected_suspect"),
    row("S001", "S001_082", "dialogue", "这就麻烦了。坏人我可以骂，小孩我只能希望他明天别被那把伞戳到脸。", "CHR_linyan", qa_notes="click_function=softening"),
    row("S001", "S001_083", "dialogue", "他买了水果糖。小票有会员记录。", "CHR_jiangchi", qa_notes="click_function=evidence_available"),
    row("S001", "S001_084", "dialogue", "我不能给你会员号，也不能私查完整信息。可以写时间、商品、伞特征，明天让何姨查。", "CHR_jiangchi", qa_notes="click_function=rule_boundary"),
    row("S001", "S001_085", "dialogue", "午休四十分钟。", "CHR_linyan", qa_notes="click_function=time_cost"),
    row("S001", "S001_086", "dialogue", "走过来八分钟。", "CHR_jiangchi", qa_notes="click_function=he_already_calculates"),
    row("S001", "S001_087", "dialogue", "你怎么连这个都算？", "CHR_linyan", qa_notes="click_function=notices_care"),
    row("S001", "S001_088", "dialogue", "夜班太闲。", "CHR_jiangchi", qa_notes="click_function=dodge"),
    row("S001", "S001_089", "dialogue", "闲到替复读生规划午休逃亡路线？", "CHR_linyan", qa_notes="click_function=tease_relation"),
    row("S001", "S001_090", "dialogue", "午休。别逃课。", "CHR_jiangchi", qa_notes="click_function=protective_correction"),
    row("S001", "S001_091", "command", "@choice CHOICE_02 雨夜小票", choice_group="CHOICE_02", qa_notes="choice_group"),
    row("S001", "S001_092A", "choice", "", choice_group="CHOICE_02", choice_text="把小票夹进失物本", choice_target="S001_093A", effects="receipt_kept=true", qa_notes="choice_axis=evidence_risk"),
    row("S001", "S001_092B", "choice", "", choice_group="CHOICE_02", choice_text="不留小票，只记线索", choice_target="S001_093B", effects="receipt_hidden=true", qa_notes="choice_axis=memory_risk"),
    row("S001", "S001_092A_LABEL", "command", "label:S001_093A", condition="receipt_kept", qa_notes="branch_label"),
    row("S001", "S001_093A", "narration", "我从回收盒里抽出小票，遮住会员号，只留时间和商品。", condition="receipt_kept", qa_notes="click_function=object_state"),
    row("S001", "S001_094A", "dialogue", "这张不能给你。可以夹在本子里。", "CHR_jiangchi", condition="receipt_kept", qa_notes="click_function=rule_bent"),
    row("S001", "S001_095A", "dialogue", "明天何姨看到，会知道我半夜没编故事。", "CHR_jiangchi", condition="receipt_kept", qa_notes="click_function=cost_self"),
    row("S001", "S001_096A", "dialogue", "那你负责被骂？", "CHR_linyan", condition="receipt_kept", qa_notes="click_function=checks_debt"),
    row("S001", "S001_097A", "dialogue", "熟练业务。", "CHR_jiangchi", condition="receipt_kept", qa_notes="click_function=dry_accept"),
    row("S001", "S001_092B_LABEL", "command", "label:S001_093B", condition="receipt_hidden", qa_notes="branch_label"),
    row("S001", "S001_093B", "narration", "我把小票折起来，丢进废纸袋。", condition="receipt_hidden", qa_notes="click_function=object_removed"),
    row("S001", "S001_094B", "dialogue", "十点三十七。水果糖。黑色书包，小学生，拿错伞。", "CHR_jiangchi", condition="receipt_hidden", qa_notes="click_function=memory_commitment"),
    row("S001", "S001_095B", "dialogue", "我记。", "CHR_jiangchi", condition="receipt_hidden", qa_notes="click_function=relation_debt"),
    row("S001", "S001_096B", "dialogue", "你的脑子保质期多久？", "CHR_linyan", condition="receipt_hidden", qa_notes="click_function=tests_trust"),
    row("S001", "S001_097B", "dialogue", "到明天午休。", "CHR_jiangchi", condition="receipt_hidden", qa_notes="click_function=promise"),
    row("S001", "S001_098B", "dialogue", "过期的话，我先预存两句骂。", "CHR_linyan", condition="receipt_hidden", qa_notes="click_function=debt_joke"),
    row("S001", "S001_099", "command", "@merge CHOICE_02_REJOIN", qa_notes="rejoin"),
    row("S001", "S001_100", "narration", "雨声又重了一层。最后一班公交的灯从门外经过，没有停很久。", qa_notes="click_function=time_pressure"),
    row("S001", "S001_101", "dialogue", "我没车了。", "CHR_linyan", qa_notes="click_function=new_problem"),
    row("S001", "S001_102", "dialogue", "家里那边要转一趟，站牌离小区门口还有一段。我爸会问我怎么又淋成这样。", "CHR_linyan", qa_notes="click_function=family_pressure"),
    row("S001", "S001_103", "dialogue", "他说再买就好。可再买太简单了，简单到让人很烦。", "CHR_linyan", qa_notes="click_function=theme_pressure_spoken_personally"),
    row("S001", "S001_104", "thought", "黑伞就在柜台下面。拿出来以后，这件事就没法只算失物。", qa_notes="thought_job=choice_pressure;click_function=POV_decision"),
    row("S001", "S001_105", "narration", "我从柜台下面拿出自己的黑伞。挂绳断了一半，伞套边缘磨白。", qa_notes="click_function=object_offer"),
    row("S001", "S001_106", "dialogue", "拿这个。我两点下班。雨不停，我跑回去。", "CHR_jiangchi", qa_notes="click_function=offer_with_cost"),
    row("S001", "S001_107", "dialogue", "你明天不来，我把它登记成失物。特征：黑伞，旧，挂绳断，借给一个把收银机叫铁算盘的人。", "CHR_jiangchi", qa_notes="click_function=callback_hook"),
    row("S001", "S001_108", "dialogue", "你这算威胁还是售后？", "CHR_linyan", qa_notes="click_function=acceptance_pressure"),
    row("S001", "S001_109", "dialogue", "流程。", "CHR_jiangchi", qa_notes="click_function=mask"),
    row("S001", "S001_110", "dialogue", "江迟。", "CHR_linyan", qa_notes="click_function=name_shift"),
    row("S001", "S001_111", "dialogue", "嗯。", "CHR_jiangchi", qa_notes="click_function=receives_name"),
    row("S001", "S001_112", "dialogue", "你别把好心讲得这么像罚单。", "CHR_linyan", qa_notes="click_function=names_mask"),
    row("S001", "S001_113", "dialogue", "那你拿不拿。", "CHR_jiangchi", qa_notes="click_function=practical_reply"),
    row("S001", "S001_114", "dialogue", "我拿了就欠你。", "CHR_linyan", qa_notes="click_function=debt_admitted"),
    row("S001", "S001_115", "dialogue", "我现在欠得有点多。欠我妈一把伞，欠数学卷子一个解释，欠家里一次不发脾气。", "CHR_linyan", qa_notes="click_function=emotional_list"),
    row("S001", "S001_116", "dialogue", "再欠你，我明天过来会很没气势。我这个人主要靠气势营业，你不要砸我饭碗。", "CHR_linyan", qa_notes="click_function=charm_with_cost"),
    row("S001", "S001_117", "dialogue", "那记账。欠便利店一把黑伞，欠店员三句骂，欠豆浆一声谢谢。分期还。", "CHR_jiangchi", qa_notes="click_function=procedure_turns_care"),
    row("S001", "S001_118", "dialogue", "铁算盘一号，你家店员很会放贷。", "CHR_linyan", qa_notes="click_function=accepts_debt"),
    row("S001", "S001_119", "command", "@sfx 自动门叮咚", sfx="自动门叮咚", qa_notes="exit_cue"),
    row("S001", "S001_120", "narration", "她撑开黑伞，伞面太大，把她整个人压小了一圈。", qa_notes="click_function=exit_image"),
    row("S001", "S001_121", "dialogue", "江迟！明天别迟到。", "CHR_linyan", qa_notes="click_function=callback_request"),
    row("S001", "S001_122", "dialogue", "我夜班。", "CHR_jiangchi", qa_notes="click_function=dry_fact"),
    row("S001", "S001_123", "dialogue", "那也别。", "CHR_linyan", qa_notes="click_function=soft_close"),
    row("S001", "S001_124", "command", "@fadeout", qa_notes="scene_end"),
]

R += [
    row("S002", "S002_000", "command", "label:S002_午休四十分钟", bg="便利店_中午_阴", bgm="午后空调", sfx="自动门叮咚", qa_notes="scene_entry"),
    row("S002", "S002_001", "narration", "第二天中午，雨停得不干净。蓝伞找到了，旧牙印被透明胶压在下面。", qa_notes="click_function=state_callback"),
    row("S002", "S002_002", "narration", "何姨在失物本旁贴了便签：江迟，便利店没开托儿业务。豆浆钱从工资扣。伞查到了，别摆臭脸。", qa_notes="click_function=heyi_voice+case_resolution"),
    row("S002", "S002_003", "dialogue", "我只待十九分钟。", "CHR_linyan", qa_notes="click_function=entry_pressure"),
    row("S002", "S002_004", "dialogue", "三分钟还伞，两分钟确认蓝伞，一分钟喝豆浆。剩下十三分钟本来打算骂你。", "CHR_linyan", qa_notes="click_function=same_speaker_run_time_plan"),
    row("S002", "S002_005", "dialogue", "路上想了想，骂你太浪费午休，改成赊账。你们店支持赊骂吗？", "CHR_linyan", qa_notes="click_function=charm+relationship_callback"),
    row("S002", "S002_006", "dialogue", "可以登记。", "CHR_jiangchi", qa_notes="click_function=running_joke"),
    row("S002", "S002_007", "dialogue", "你这人真的什么都登记！", "CHR_linyan", qa_notes="click_function=voice_hit"),
    row("S002", "S002_008", "narration", "她把黑伞递回来。伞套上贴着一张小便利贴，歪歪画了个笑脸。", qa_notes="click_function=object_return"),
    row("S002", "S002_009", "dialogue", "还你。没有摔，没有折，没有带它逃课。", "CHR_linyan", qa_notes="click_function=debt_repayment"),
    row("S002", "S002_010", "dialogue", "它昨晚表现很好，就是伞面太大，我爸问我从哪儿领了个移动蘑菇。", "CHR_linyan", qa_notes="click_function=family_callback+joke"),
    row("S002", "S002_011", "dialogue", "我说便利店借的。他沉默三秒，问现在便利店业务这么广？", "CHR_linyan", qa_notes="click_function=world_reaction"),
    row("S002", "S002_012", "dialogue", "我说，是啊，还能收雨，收伞，收复读生的坏脾气。", "CHR_linyan", qa_notes="click_function=theme_as_joke"),
    row("S002", "S002_013", "dialogue", "找到了。小孩妈妈早上送来的。伞骨左偏，手柄旧牙印，透明胶三圈。", "CHR_jiangchi", qa_notes="click_function=object_confirmation"),
    row("S002", "S002_014", "narration", "林檐没有马上接。她摸了摸伞柄，指腹停在牙印的位置。", qa_notes="click_function=visible_hesitation"),
    row("S002", "S002_015", "thought", "她找回了伞，手却没急着拿走。还有什么东西卡在那圈透明胶下面。", qa_notes="thought_job=private_inference;click_function=delays_completion"),
    row("S002", "S002_016A", "narration", "小票夹在失物本那页。林檐看见十点三十七分，嘴角先动了一下，又压住。", condition="receipt_kept", qa_notes="click_function=branch_callback_receipt"),
    row("S002", "S002_017A", "dialogue", "你昨晚把小票留着。", "CHR_linyan", condition="receipt_kept", qa_notes="click_function=recognizes_evidence"),
    row("S002", "S002_018A", "dialogue", "我知道你会办事。可“会办事”和“真的等到明天”，中间还差一点东西。", "CHR_linyan", condition="receipt_kept", qa_notes="click_function=trust_articulation"),
    row("S002", "S002_019A", "dialogue", "这张小票把那一点补上了。", "CHR_linyan", condition="receipt_kept", effects="trust_plus=1", qa_notes="click_function=branch_debt_paid"),
    row("S002", "S002_016B", "narration", "失物本上没有小票。林檐先看我，又看备注栏。", condition="receipt_hidden", qa_notes="click_function=branch_callback_memory"),
    row("S002", "S002_017B", "dialogue", "背一遍。", "CHR_linyan", condition="receipt_hidden", qa_notes="click_function=trust_test"),
    row("S002", "S002_018B", "dialogue", "十点三十七。水果糖。黑色书包，小学生。拿错伞，早上归还。", "CHR_jiangchi", condition="receipt_hidden", qa_notes="click_function=memory_performance"),
    row("S002", "S002_019B", "dialogue", "还在缓存里啊。那我昨晚少信你一点，今天补回来一点。你们店收这种账吗？", "CHR_linyan", condition="receipt_hidden", effects="trust_repaired=1", qa_notes="click_function=trust_repaired"),
    row("S002", "S002_020", "dialogue", "可以登记。", "CHR_jiangchi", qa_notes="click_function=rejoin_running_joke"),
    row("S002", "S002_021", "dialogue", "又来！", "CHR_linyan", qa_notes="click_function=voice_reaction"),
    row("S002", "S002_022", "narration", "我把豆浆放到柜台上。杯套写着“午休限定”，字迹被何姨圈了个问号。", qa_notes="click_function=object_callback"),
    row("S002", "S002_023", "dialogue", "这个字是你写的。“限”字站得特别僵，一看就怕被人发现。", "CHR_linyan", qa_notes="click_function=observes_jiangchi"),
    row("S002", "S002_024", "dialogue", "何姨如果写，应该会写“自费”。所以，江迟同学，便利店豆浆事业今天也需要我吗？", "CHR_linyan", qa_notes="click_function=asks_connection"),
    row("S002", "S002_025", "dialogue", "需要。", "CHR_jiangchi", qa_notes="click_function=direct_acceptance"),
    row("S002", "S002_026", "dialogue", "你答得太快了！", "CHR_linyan", qa_notes="click_function=embarrassed_reaction"),
    row("S002", "S002_027", "dialogue", "午休只有十九分钟。", "CHR_jiangchi", qa_notes="click_function=practical_cover"),
    row("S002", "S002_028", "narration", "她捧起豆浆，先吹了吹。热气挡住她半张脸。", qa_notes="click_function=breath_after_comedy"),
    row("S002", "S002_029", "dialogue", "我今天早上带了新伞。自动开合，防晒，黑得像要去参加物理竞赛。", "CHR_linyan", qa_notes="click_function=new_object"),
    row("S002", "S002_030", "dialogue", "以前我讨厌它。一按按钮就啪地开，特别积极，急着证明旧东西该退休。", "CHR_linyan", qa_notes="click_function=value_conflict"),
    row("S002", "S002_031", "dialogue", "可我撑它走到校门口，发现它也挺努力。我爸也挺努力。他不会修伞，只会买新的。", "CHR_linyan", qa_notes="click_function=recognition"),
    row("S002", "S002_032", "dialogue", "我不能因为他不会透明胶，就判他不合格，对吧？", "CHR_linyan", qa_notes="click_function=asks_without_theme_summary"),
    row("S002", "S002_033", "thought", "她问的是我，眼睛却压在蓝伞胶带上。答案大概不能从我这里领走。", qa_notes="thought_job=private_inference+care;click_function=POV_receives"),
    row("S002", "S002_034", "dialogue", "那这把呢。", "CHR_jiangchi", qa_notes="click_function=practical_next_action"),
    row("S002", "S002_035", "dialogue", "先放你这。别写丢，写寄存。", "CHR_linyan", qa_notes="click_function=turn_to_deposit"),
    row("S002", "S002_036", "dialogue", "我今天拿新伞回去。说不好的话，明天再来取旧伞壮胆。说得好的话，也来取，因为它是我的。", "CHR_linyan", qa_notes="click_function=branchless_future_callback"),
    row("S002", "S002_037", "dialogue", "本店没有寄存服务。", "CHR_jiangchi", qa_notes="click_function=rule_resistance"),
    row("S002", "S002_038", "dialogue", "昨天也没有收雨服务。", "CHR_linyan", qa_notes="click_function=beats_rule"),
    row("S002", "S002_039", "dialogue", "那登记。寄存人，林檐。物品，蓝伞。期限，她想拿走的时候。", "CHR_jiangchi", qa_notes="click_function=new_business_created"),
    row("S002", "S002_040", "dialogue", "备注，欠骂若干，豆浆不固定供应。", "CHR_jiangchi", qa_notes="click_function=relationship_joke"),
    row("S002", "S002_041", "dialogue", "最后一句划掉！", "CHR_linyan", qa_notes="click_function=lively_rebuttal"),
    row("S002", "S002_042", "dialogue", "不划。", "CHR_jiangchi", qa_notes="click_function=playful_firmness"),
    row("S002", "S002_043", "dialogue", "那我明天来检查。后天也可能来。你这个嗯听起来很得意，先登记欠骂一句。", "CHR_linyan", qa_notes="click_function=callback_promise"),
    row("S002", "S002_044", "narration", "她跑回街对面。蓝伞留在柜台边，透明胶在灯下亮了一小圈。", qa_notes="click_function=exit_image"),
    row("S002", "S002_045", "narration", "我翻开失物本，在“失物”旁边空出一栏。", qa_notes="click_function=system_change"),
    row("S002", "S002_046", "narration", "新栏写：寄存。", qa_notes="click_function=theme_played_object"),
    row("S002", "S002_047", "command", "@fadeout", qa_notes="scene_end"),
]

R += [
    row("S003", "S003_000", "command", "label:S003_晚自习前的寄存格", bg="便利店_傍晚_雨后", bgm="傍晚空调", sfx="自动门叮咚", qa_notes="scene_entry"),
    row("S003", "S003_001", "narration", "傍晚六点二十，复读学校的学生成排走过玻璃门外。我把蓝伞从柜台边挪到失物箱上方，寄存栏还空得像刚开业。", qa_notes="click_function=new_scene_state"),
    row("S003", "S003_002", "dialogue", "江迟，你在本子上写的寄存是什么意思？便利店没开车站行李房业务。", "CHR_heyi", qa_notes="click_function=authority_pressure"),
    row("S003", "S003_003", "dialogue", "还有，谁欠你骂？欠骂也要写？你别装哑巴，你一安静我就知道你又拿规章当橡皮筋用。", "CHR_heyi", qa_notes="click_function=heyi_voice"),
    row("S003", "S003_004", "dialogue", "何姨，橡皮筋是消耗品。", "CHR_jiangchi", qa_notes="click_function=dry_reply"),
    row("S003", "S003_005", "dialogue", "少贫。晚班结束前，把新栏目解释写给我。", "CHR_heyi", qa_notes="click_function=task_set"),
    row("S003", "S003_006", "narration", "电话挂断。收银机屏幕暗下去，像也不想承担新业务责任。", qa_notes="click_function=screen_state"),
    row("S003", "S003_007", "thought", "何姨要解释。失物本旁边还空着一栏，我得给那一栏找个不挨骂的名字。", qa_notes="thought_job=practical_worry+theme_pressure"),
    row("S003", "S003_008", "dialogue", "先声明，我赶在晚自习前来办正事。", "CHR_linyan", qa_notes="click_function=entry"),
    row("S003", "S003_009", "dialogue", "这是一项非常严肃的伞类外交。对象包括我爸的新伞、我妈的旧伞、你的黑伞，以及你们店疑似非法开设的寄存柜。", "CHR_linyan", qa_notes="click_function=same_speaker_run_setup"),
    row("S003", "S003_010", "dialogue", "你的黑伞表现稳定，昨晚护送有功，午休后又陪我去了趟办公室。它有点像班里那个不说话但作业全对的同学。讨厌，很可靠。", "CHR_linyan", qa_notes="click_function=object_report+affection"),
    row("S003", "S003_011", "dialogue", "你夸伞比夸人熟练。", "CHR_jiangchi", qa_notes="click_function=tease"),
    row("S003", "S003_012", "dialogue", "人容易得意，伞不会。", "CHR_linyan", qa_notes="click_function=voice"),
    row("S003", "S003_013", "dialogue", "晚自习几点。从这里走回去八分钟。你还有十四分钟，其中买豆浆一分钟，骂人视语速而定。", "CHR_jiangchi", qa_notes="click_function=care_as_schedule"),
    row("S003", "S003_014", "dialogue", "你现在连我的骂人效率都纳入排班了？", "CHR_linyan", qa_notes="click_function=relationship_tease"),
    row("S003", "S003_015", "dialogue", "寄存新业务需要数据。", "CHR_jiangchi", qa_notes="click_function=mask"),
    row("S003", "S003_016", "dialogue", "铁算盘一号，听见没有，你们店员开始创业了。", "CHR_linyan", qa_notes="click_function=machine_callback"),
    row("S003", "S003_017", "command", "@sfx 收银机滴", sfx="收银机滴", qa_notes="callback"),
    row("S003", "S003_018", "dialogue", "它同意了。", "CHR_linyan", qa_notes="click_function=object_witness"),
    row("S003", "S003_019", "dialogue", "扫码枪误触。", "CHR_jiangchi", qa_notes="click_function=dry_denial"),
    row("S003", "S003_020", "dialogue", "你们一家三口都很嘴硬。", "CHR_linyan", qa_notes="click_function=relationship_family_joke"),
    row("S003", "S003_021", "narration", "她把新伞立在柜台边。伞柄光滑，连一道多余划痕都没有。", qa_notes="click_function=object_contrast"),
    row("S003", "S003_022", "dialogue", "我跟我爸说了。说旧伞找回来了，说我昨晚在便利店查监控，说有个夜班店员讲话像商品说明书，但没有赶我走。", "CHR_linyan", qa_notes="click_function=family_report"),
    row("S003", "S003_023", "dialogue", "他第一句问店员多大，第二句问店长知道吗，第三句说下次别给人添麻烦。", "CHR_linyan", qa_notes="click_function=father_voice"),
    row("S003", "S003_024", "dialogue", "我差点炸。然后他把新伞递给我，说旧的找回来就好，新的也不用我喜欢。", "CHR_linyan", qa_notes="click_function=reversal"),
    row("S003", "S003_025", "dialogue", "他说他不会修伞。说这句的时候，一直捏着伞套。那把黑科技新伞差点被他捏成咸菜。", "CHR_linyan", qa_notes="click_function=recognition_detail"),
    row("S003", "S003_026", "dialogue", "我准备好的帅气台词全用不上了。他一说不会，我就没法赢。", "CHR_linyan", qa_notes="click_function=soft_defeat"),
    row("S003", "S003_027", "thought", "她把新伞立得很正。那场准备好的架，被她压在书包最里面。", qa_notes="thought_job=private_inference;click_function=emotion_read"),
    row("S003", "S003_028", "dialogue", "那旧伞呢。", "CHR_jiangchi", qa_notes="click_function=returns_to_object"),
    row("S003", "S003_029", "dialogue", "继续放你这。我今天拿新伞回去。旧伞一起带走的话，会像打赢一场架。", "CHR_linyan", qa_notes="click_function=chooses_state"),
    row("S003", "S003_030", "dialogue", "可我今天没打架。我只是发现我爸不会透明胶。", "CHR_linyan", qa_notes="click_function=theme_as_personal_line"),
    row("S003", "S003_031", "dialogue", "寄存期。", "CHR_jiangchi", qa_notes="click_function=procedure_prompt"),
    row("S003", "S003_032", "dialogue", "到我敢拿回去为止。", "CHR_linyan", qa_notes="click_function=state_duration"),
    row("S003", "S003_033", "dialogue", "可以。", "CHR_jiangchi", qa_notes="click_function=accepts_new_rule"),
    row("S003", "S003_034", "narration", "我在失物本新栏下面写字，笔尖停在“寄存期限”后面。", qa_notes="click_function=work_action"),
    row("S003", "S003_035", "dialogue", "寄存期限：她敢拿回去为止。寄存状态：雨后。保管要求：别让铁算盘一号发表意见。", "CHR_jiangchi", qa_notes="click_function=procedure_poetry_owned"),
    row("S003", "S003_036", "dialogue", "备注：豆浆不固定供应，骂人额度可延期。", "CHR_jiangchi", qa_notes="click_function=running_joke"),
    row("S003", "S003_037", "dialogue", "最后一句又乱写！你这个业务迟早被何姨取缔！", "CHR_linyan", qa_notes="click_function=lively_pressure"),
    row("S003", "S003_038", "dialogue", "已经在解释。", "CHR_jiangchi", qa_notes="click_function=callback_to_heyi"),
    row("S003", "S003_039", "narration", "我把给何姨的解释纸拿出来。上面只写了一行：暂时放不回去的东西，先不要丢。", qa_notes="click_function=theme_object_line"),
    row("S003", "S003_040", "narration", "林檐看了那行字，两秒没有说话。", qa_notes="click_function=breath"),
    row("S003", "S003_041", "dialogue", "这句能给我吗？我想夹到错题本里。", "CHR_linyan", qa_notes="click_function=request"),
    row("S003", "S003_042", "dialogue", "以后我又想把话说绝的时候，先看一眼。提醒一下，雨伞和人都能晚点拿回去。", "CHR_linyan", qa_notes="click_function=theme_played_as_object_use"),
    row("S003", "S003_043", "dialogue", "何姨要看。", "CHR_jiangchi", qa_notes="click_function=rule"),
    row("S003", "S003_044", "dialogue", "那你再写一张。", "CHR_linyan", qa_notes="click_function=practical_solution"),
    row("S003", "S003_045", "dialogue", "纸要钱。", "CHR_jiangchi", qa_notes="click_function=dry_block"),
    row("S003", "S003_046", "dialogue", "我买豆浆。", "CHR_linyan", qa_notes="click_function=bargain"),
    row("S003", "S003_047", "dialogue", "第二件半价。", "CHR_jiangchi", qa_notes="click_function=callback"),
    row("S003", "S003_048", "dialogue", "江迟，你真的很会把感人场面拐进收银台。", "CHR_linyan", qa_notes="click_function=names_habit"),
    row("S003", "S003_049", "dialogue", "这样比较安全。", "CHR_jiangchi", qa_notes="click_function=slip"),
    row("S003", "S003_050", "thought", "安全。收银台挡在我前面，扫码、找零、登记，哪一句都像有地方可放。", qa_notes="thought_job=self_recognition;click_function=POV_crack"),
    row("S003", "S003_051", "thought", "每句话都有用途，就少有人问我为什么还没走出去。", qa_notes="thought_job=private_cost;click_function=sets_up_question"),
    row("S003", "S003_052", "dialogue", "你以前为什么离开对面学校？", "CHR_linyan", qa_notes="click_function=asks_unsafe"),
    row("S003", "S003_053", "dialogue", "社团退了。成绩掉了。家里说先工作一阵也行。", "CHR_jiangchi", qa_notes="click_function=short_history"),
    row("S003", "S003_054", "dialogue", "我说好。后来发现“好”很方便。别人给台阶，你说好；别人不问了，你也说好；排班表贴出来，你还是说好。", "CHR_jiangchi", qa_notes="click_function=voice_run_confession"),
    row("S003", "S003_055", "dialogue", "说多了，自己懒得查到底哪里不好。", "CHR_jiangchi", qa_notes="click_function=confession_end"),
    row("S003", "S003_056", "narration", "林檐把豆浆推到我这边，又推回来，像在试杯子还烫不烫。", qa_notes="click_function=body_response"),
    row("S003", "S003_057", "dialogue", "那你也寄存一下。", "CHR_linyan", qa_notes="click_function=turns_method_back"),
    row("S003", "S003_058", "dialogue", "什么。", "CHR_jiangchi", qa_notes="click_function=prompt"),
    row("S003", "S003_059", "dialogue", "你那些说好。暂时放不回去的东西，先不要丢。你自己写的，别装没看见。", "CHR_linyan", qa_notes="click_function=relation_pressure"),
    row("S003", "S003_060", "dialogue", "可以寄存在本子里，也可以寄存在铁算盘一号那里。它嘴严，最多滴一声。", "CHR_linyan", qa_notes="click_function=cute_pressure_with_cost"),
    row("S003", "S003_061", "command", "@sfx 收银机滴", sfx="收银机滴", qa_notes="callback"),
    row("S003", "S003_062", "dialogue", "你看，它答应了。", "CHR_linyan", qa_notes="click_function=object_witness"),
    row("S003", "S003_063", "dialogue", "扫码枪误触。", "CHR_jiangchi", qa_notes="click_function=mask"),
    row("S003", "S003_064", "dialogue", "今天它是证人。", "CHR_linyan", qa_notes="click_function=relationship_lock"),
    row("S003", "S003_065", "narration", "晚自习铃从街对面响起来。林檐拿起新伞，蓝伞留在柜台上。", qa_notes="click_function=time_exit"),
    row("S003", "S003_066", "dialogue", "我走了。明天不一定来，后天也不一定。", "CHR_linyan", qa_notes="click_function=soft_future"),
    row("S003", "S003_067", "dialogue", "但这把伞在这里，我就不会忘得太干净。你也别忘得太干净。", "CHR_linyan", qa_notes="click_function=theme_callback"),
    row("S003", "S003_068", "dialogue", "忘什么。", "CHR_jiangchi", qa_notes="click_function=invites_final"),
    row("S003", "S003_069", "dialogue", "忘了自己还有东西没拿回去。", "CHR_linyan", qa_notes="click_function=final_pressure"),
    row("S003", "S003_070", "command", "@sfx 自动门叮咚", sfx="自动门叮咚", qa_notes="exit"),
    row("S003", "S003_071", "narration", "她跑进傍晚的人流。新伞没有撑开，被她夹在胳膊下面，像一项暂时讲和的证据。", qa_notes="click_function=exit_image"),
    row("S003", "S003_072", "narration", "我低头看失物本。寄存栏下，林檐的蓝伞占了一行。", qa_notes="click_function=screen_state"),
    row("S003", "S003_073", "narration", "我在下一行写：江迟。", qa_notes="click_function=POV_state_change"),
    row("S003", "S003_074", "narration", "物品：说好的事。期限：想拿回去的时候。", qa_notes="click_function=ending_state"),
    row("S003", "S003_075", "command", "@sfx 收银机滴", sfx="收银机滴", qa_notes="final_callback"),
    row("S003", "S003_076", "narration", "这次没有商品经过。", qa_notes="click_function=ending_image"),
    row("S003", "S003_077", "command", "@ending true_after_rain_end", qa_notes="ending"),
    row("S003", "S003_078", "command", "@fadeout", qa_notes="fadeout"),
]


def render_readable(rows):
    out = [
        "# 便利店把雨收好_正史密度重写_20260624",
        "",
        "## 生成前执行记录",
        "",
        "- 基准：以早期《对白块重写版》的连续对话和角色口吻为骨架，吸收最终链路版的 CSV/分支/状态要求。",
        "- 修订重点：合并低信息碎行，删除作者解释型心理，保留角色口语、外号、问号、打断和运行中的关系债。",
        "- 对白所有权：S001 开场由林檐连续占压，S001 中段由江迟用流程接住；S002 用回调和寄存转关系；S003 用寄存栏反照江迟。",
        "- 分支：2 个可见选择，4 个持久状态；分支回流后通过小票/记忆、信任文本和寄存债回调。",
        "",
        "---",
        "",
    ]
    n = 1
    for item in rows:
        typ = item["row_type"]
        text = item["text"]
        speaker = item["speaker"]
        if typ == "command":
            if text.startswith("label:"):
                out.append("@label " + text.split(":", 1)[1])
            else:
                out.append(text)
            out.append("")
            continue
        if typ == "choice":
            out.append(f"{n:03d}")
            out.append(f"@option {item['choice_text']} -> {item['choice_target']} [{item['effects']}]")
            out.append("")
            n += 1
            continue
        out.append(f"{n:03d}")
        if typ == "dialogue":
            name = {"CHR_jiangchi": "江迟", "CHR_linyan": "林檐", "CHR_heyi": "何姨/电话"}.get(speaker, speaker)
            out.append(f"【{name}】『{text}』")
        elif typ == "thought":
            out.append(f"（{text}）")
        else:
            out.append(text)
        out.append("")
        n += 1
    return "\n".join(out)


def main() -> None:
    READABLE.parent.mkdir(parents=True, exist_ok=True)
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    NOTES.parent.mkdir(parents=True, exist_ok=True)

    READABLE.write_text(render_readable(R), encoding="utf-8")
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(R)

    NOTES.write_text(
        "\n".join(
            [
                "# 正史密度重写修订说明",
                "",
                "## 针对用户指出的问题",
                "",
                "- 早期对白块版本被误放在 `02_generated_content/可读剧本/`，上一轮 draft-session 只读到 `drafts/readable/`，导致好的对白密度没有进入最终链路。",
                "- 新版以早期对白块为骨架，同时补齐 CSV、选择、状态、QA 字段。",
                "- 合并了“动作很轻/轻得像……”这类低信息碎行，正文不再追求小漂亮句。",
                "- 心理行只保留江迟的私密判断、越流程成本、要不要承认等待等压力。",
                "- 林檐保留快语速、外号、问号、夸张防御，但减少连续卖弄式物件玩笑。",
                "",
                "## 生成前对话所有权计划",
                "",
                "- S001：林檐拥有开场压力，连续 4-6 格把找伞、尴尬、求助伪装成玩笑；江迟用流程接住。",
                "- S001 中段：江迟拥有监控/登记压力，短句推进事实；林檐用玩笑漏出家庭和母亲。",
                "- S002：回调分支债，小票或记忆改变信任文本，然后转入寄存。",
                "- S003：何姨给规章压力，林檐把寄存栏反推给江迟，完成双向主题。",
            ]
        ),
        encoding="utf-8",
    )

    print(READABLE)
    print(CSV_OUT)
    print(NOTES)


if __name__ == "__main__":
    main()
