# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = WORKBENCH_ROOT.parent

INTERNAL_TAG_PATTERNS = [
    "</s>",
    "<think",
    "</think",
    "think_never",
    "codex_internal_context",
    "<turn_aborted>",
]

BANNED_STYLE_PATTERNS = [
    "不是", "而是", "与其说", "不如说", "真正", "所谓",
    "突然意识到", "终于明白", "???", "\ufffd",
]

AUTHORIAL_THOUGHT_PATTERNS = [
    "原来", "其实", "说明", "意味着", "本质", "真正", "只是",
    "他/她是在", "他是在", "她是在", "这代表", "这说明",
]

ORAL_THOUGHT_TOKENS = [
    "啊", "嗯", "诶", "……", "的话", "应该", "大概", "或许",
    "吧", "算了", "等一下", "先别", "完蛋", "好像",
]

RELAXED_THOUGHT_TOKENS = [
    "嗯", "啊", "诶", "呃", "唔", "……", "...",
    "好吧", "算了", "先这样", "当我没说", "这句撤回",
    "吧", "嘛", "啦", "大概", "应该", "先别",
]

CONTEXT_RECEIPT = WORKBENCH_ROOT / "00_workbench_core" / "runtime" / "last_context_bootstrap.json"

MANDATORY_PORTABLE_SKILL_IDS = {
    "galgame-workbench-loader",
    "vn-character-memory",
    "vn-fusion-writer",
    "vn-presence-revision",
    "vn-scene-drafting",
}

REQUIRED_FILES = [
    PROJECT_ROOT / "START_HERE.md",
    PROJECT_ROOT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "CURRENT_TASK_STATE.md",
    PROJECT_ROOT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "WORKBENCH_OPERATING_RULES.md",
    PROJECT_ROOT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "OTHER_AI_FAILURE_PREVENTION.md",
    WORKBENCH_ROOT / "00_workbench_core" / "methods" / "chinese_vn_generation_hard_gates.md",
    WORKBENCH_ROOT / "00_workbench_core" / "methods" / "spoken_private_thought_texture.md",
    WORKBENCH_ROOT / "00_workbench_core" / "methods" / "interior_breath_relaxation.md",
    WORKBENCH_ROOT / "00_workbench_core" / "methods" / "complete_delivery_package_contract.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_context_receipt(findings: list[str]) -> None:
    if not CONTEXT_RECEIPT.exists():
        findings.append(
            "ERROR context bootstrap receipt missing. Run: "
            "py vn_fusion_workbench/00_workbench_core/tools/vn_context_bootstrap.py --project <Pxxx> --task <draft|rewrite>"
        )
        return
    try:
        import json
        data = json.loads(CONTEXT_RECEIPT.read_text(encoding="utf-8"))
        missing = data.get("missing", [])
        loaded_count = data.get("loaded_count", 0)
        if missing:
            findings.append("ERROR context bootstrap has missing files: " + "; ".join(missing[:5]))
        if loaded_count < 8:
            findings.append(f"ERROR context bootstrap loaded too few files: {loaded_count}")
        loaded_skill_paths = data.get("mandatory_portable_skills", [])
        loaded_skill_ids = {
            Path(item).parent.name
            for item in loaded_skill_paths
            if str(item).endswith("SKILL.md")
        }
        missing_skill_ids = sorted(MANDATORY_PORTABLE_SKILL_IDS - loaded_skill_ids)
        if missing_skill_ids:
            findings.append(
                "ERROR mandatory VN/Gal portable skills were not bootstrapped: "
                + ", ".join(missing_skill_ids)
            )
    except Exception as exc:
        findings.append(f"ERROR context bootstrap receipt unreadable: {exc}")

def check_required_files(findings: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            findings.append(f"ERROR missing required file: {path}")

    wrong_handoff = WORKBENCH_ROOT / "AI_HANDOFF_PACKAGE"
    if wrong_handoff.exists():
        findings.append(
            f"ERROR wrong handoff path exists under vn_fusion_workbench: {wrong_handoff}. "
            "AI_HANDOFF_PACKAGE must live under VN_Workbench_Project."
        )


def check_rules_loaded(findings: list[str]) -> None:
    rules = PROJECT_ROOT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "WORKBENCH_OPERATING_RULES.md"
    if not rules.exists():
        return
    content = read_text(rules)
    for marker in [
        "OTHER_AI_FAILURE_PREVENTION",
        "spoken_private_thought_texture",
        "interior_breath_relaxation",
        "complete_delivery_package_contract",
        "Positive Constraint Model",
    ]:
        if marker not in content:
            findings.append(f"ERROR operating rules do not reference marker: {marker}")


def check_text_file(path: Path, findings: list[str], strict: bool) -> None:
    if not path.exists():
        findings.append(f"ERROR target text does not exist: {path}")
        return

    content = read_text(path)

    for pat in INTERNAL_TAG_PATTERNS:
        if pat in content:
            findings.append(f"ERROR internal tag leaked into output: {pat}")

    for pat in BANNED_STYLE_PATTERNS:
        count = content.count(pat)
        if count:
            findings.append(f"{'ERROR' if strict else 'WARN'} banned/high-risk pattern {pat}: {count}")

    # Thought rows: a Chinese VN thought row starts with full-width parenthesis.
    thought_rows = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("（") and stripped.endswith("）"):
            thought_rows.append(stripped)

    if thought_rows:
        head = "\n".join(content.splitlines()[:80])
        if "默认视角" not in head and "POV" not in head and "@pov" not in content:
            findings.append("ERROR POV declaration missing: thought rows require 默认视角 or @pov marker.")
        if "@pov" in content:
            bad_pov = []
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith("@pov") and len(stripped.split()) < 2:
                    bad_pov.append(stripped)
            if bad_pov:
                findings.append("ERROR malformed @pov marker: " + " | ".join(bad_pov[:3]))

        oral_count = sum(
            1 for row in thought_rows
            if any(tok in row for tok in ORAL_THOUGHT_TOKENS)
        )
        relaxed_count = sum(
            1 for row in thought_rows
            if any(tok in row for tok in RELAXED_THOUGHT_TOKENS)
        )
        authorial_hits = []
        for row in thought_rows:
            if any(pat in row for pat in AUTHORIAL_THOUGHT_PATTERNS):
                if not any(tok in row for tok in ORAL_THOUGHT_TOKENS):
                    authorial_hits.append(row)

        if len(thought_rows) >= 5:
            ratio = oral_count / len(thought_rows)
            if ratio < 0.5:
                findings.append(
                    f"ERROR thought rows are too authorial: oral/private texture {oral_count}/{len(thought_rows)}"
                )
            relaxed_ratio = relaxed_count / len(thought_rows)
            if relaxed_count == 0:
                findings.append(
                    "ERROR thought rows have no relaxation/particle texture; "
                    "add character-owned fillers, retreats, particles, half-jokes, or practical masks where pressure releases."
                )
            elif relaxed_ratio < 0.25:
                findings.append(
                    f"WARN thought rows may be stiff: relaxation/particle texture {relaxed_count}/{len(thought_rows)}"
                )

        if authorial_hits:
            findings.append(
                "ERROR authorial thought rows without private oral texture: "
                + " | ".join(authorial_hits[:3])
            )


def check_dialogue_pingpong(path: Path, findings: list[str]) -> None:
    if not path.exists():
        return
    content = read_text(path)
    speakers = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("【") and "】" in stripped and "『" in stripped:
            speaker = stripped.split("】", 1)[0].replace("【", "")
            speakers.append(speaker)

    if len(speakers) < 8:
        return

    same_speaker_runs = 0
    current_run = 1
    max_run = 1
    for i in range(1, len(speakers)):
        if speakers[i] == speakers[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            if current_run >= 2:
                same_speaker_runs += 1
            current_run = 1
    if current_run >= 2:
        same_speaker_runs += 1

    pure_alt_windows = 0
    for i in range(0, len(speakers) - 5):
        w = speakers[i:i+6]
        if len(set(w)) == 2 and all(w[j] != w[j-1] for j in range(1, len(w))):
            pure_alt_windows += 1

    # A dialogue-heavy scene with no same-speaker run and several A/B/A/B windows fails.
    if pure_alt_windows >= 3 and max_run < 2:
        findings.append(
            f"ERROR dialogue is pure ping-pong: {pure_alt_windows} alternating windows, max same-speaker run {max_run}. "
            "Plan dialogue ownership and same-speaker runs."
        )
    elif pure_alt_windows >= 5 and same_speaker_runs <= 1:
        findings.append(
            f"WARN dialogue may be over-alternating: {pure_alt_windows} alternating windows, same-speaker runs {same_speaker_runs}."
        )

def check_language_leak(path: Path, findings: list[str]) -> None:
    if not path.exists():
        return
    content = read_text(path)
    # Heuristic: if the final user-facing artifact is mostly English words and also has Chinese dialogue markers absent,
    # flag it. Engine variables and method docs are not checked with this function by default.
    words = re.findall(r"[A-Za-z]{4,}", content)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", content)
    if len(words) > 120 and len(words) > len(chinese_chars):
        findings.append("WARN target seems English-dominant; user-facing creative drafts should be Chinese unless requested.")


def main() -> int:
    parser = argparse.ArgumentParser(description="VN workbench handoff/failure guard.")
    parser.add_argument("--target", help="User-facing draft or final answer artifact to inspect.")
    parser.add_argument("--strict", action="store_true", help="Treat banned style hits as errors.")
    args = parser.parse_args()

    findings: list[str] = []
    check_required_files(findings)
    check_context_receipt(findings)
    check_rules_loaded(findings)

    if args.target:
        target = Path(args.target)
        check_text_file(target, findings, args.strict)
        check_dialogue_pingpong(target, findings)
        check_language_leak(target, findings)

    errors = [f for f in findings if f.startswith("ERROR")]
    warnings = [f for f in findings if f.startswith("WARN")]

    print("# VN Handoff Guard")
    print(f"- errors: {len(errors)}")
    print(f"- warnings: {len(warnings)}")
    for item in findings:
        print("- " + item)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
