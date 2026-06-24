#!/usr/bin/env python3
"""VN Fusion Workbench CLI.

Stdlib-only tools for validating spreadsheet-style VN scripts, assembling
context packs, and exporting simple WebGAL / Ren'Py script drafts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PATH_ALIAS_FILE = WORKBENCH_ROOT / "00_workbench_core" / "runtime" / "path_aliases.json"
PROJECT_KEY_RE = re.compile(r"^(?:P)?(\d{1,3})$")
ALIAS_SPEC_RE = re.compile(r"^@([A-Z0-9_]+)(?:[\\/](.*))?$")


SCRIPT_HEADERS = [
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

KNOWN_ROW_TYPES = {"dialogue", "narration", "thought", "choice", "command", "comment"}

AI_PHRASE_PATTERNS = [
    re.compile(r"不是.{0,20}而是"),
    re.compile(r"不只是.{0,20}也是"),
    re.compile(r"真正的.{0,20}是"),
    re.compile(r"某种意义上"),
    re.compile(r"[他她我]意识到"),
    re.compile(r"空气凝固"),
    re.compile(r"命运的齿轮"),
    re.compile(r"无声地诉说"),
    re.compile(r"眼神复杂"),
    re.compile(r"一切都变得不同"),
]

ABSTRACT_EMOTION_WORDS = [
    "悲伤",
    "愤怒",
    "恐惧",
    "绝望",
    "温柔",
    "复杂",
    "震惊",
]

REQUIRED_SCENE_CONTRACT_FIELDS = [
    "scene_question",
    "scene_answer",
    "professional_ritual",
    "dramatic_turn",
    "sequel_decision",
    "theme_pressure",
]

ENERGY_PUNCTUATION_RE = re.compile(r"[?!\uFF1F\uFF01\u2026\u2014]")
CASUAL_PARTICLE_RE = re.compile(r"(嘛|啦|喂|欸|诶|哎|呀|吧|哟|呗|哈|好嘛|行吧|不是吧|拜托|算我求你)")
QUESTION_RE = re.compile(r"[?\uFF1F]")
EXCLAIM_RE = re.compile(r"[!\uFF01]")
PAUSE_OR_CUT_RE = re.compile(r"(\u2026|\.{3}|\u2014|--)")
FULL_STOP_END_RE = re.compile(r"[\u3002.]$")
SENTENCE_CLOSED_RE = re.compile(r"[\u3002.!?\uFF01\uFF1F\u2026\u2014.]$")
WRAPPED_DIALOGUE_QUOTE_RE = re.compile(r'^\s*["“「『].*["”」』]\s*$')
DOUBLE_QUOTE_RE = re.compile(r'["“”]')
ONLY_PAUSE_RE = re.compile(r"^\s*(\u2026|\.{3,}|-{2,}|\u2014+)+\s*$")
TEXTBOX_SENTENCE_END_RE = re.compile(r"[。.!?\uFF01\uFF1F]")
FIRST_PERSON_RE = re.compile(r"(^|[，。！？；、\s])我")
COMMA_RE = re.compile(r"[，,]")


@dataclass
class Issue:
    level: str
    beat_id: str
    message: str


def load_path_aliases() -> dict[str, str]:
    if not PATH_ALIAS_FILE.exists():
        return {}
    data = load_json_value(PATH_ALIAS_FILE)
    if isinstance(data, dict) and isinstance(data.get("aliases"), dict):
        return {str(k): str(v) for k, v in data["aliases"].items()}
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items()}
    return {}


def project_registry(workbench_root: Path = WORKBENCH_ROOT) -> dict[str, Path]:
    projects_root = workbench_root / "02_projects"
    registry: dict[str, Path] = {}
    if not projects_root.exists():
        return registry
    for path in sorted(projects_root.iterdir()):
        if not path.is_dir():
            continue
        match = re.match(r"^(\d{1,3})_", path.name)
        if not match:
            continue
        key = f"P{int(match.group(1)):03d}"
        registry[key] = path.resolve()
    return registry


def resolve_project_key(spec: str | None, workbench_root: Path = WORKBENCH_ROOT) -> Path | None:
    if not spec:
        return None
    match = PROJECT_KEY_RE.fullmatch(spec.strip())
    if not match:
        return None
    key = f"P{int(match.group(1)):03d}"
    return project_registry(workbench_root).get(key)


def resolve_alias_target(spec: str | None, workbench_root: Path = WORKBENCH_ROOT) -> Path | None:
    if not spec:
        return None
    stripped = spec.strip()
    alias_name: str | None = None
    alias_tail: str | None = None
    match = ALIAS_SPEC_RE.fullmatch(stripped)
    if match:
        alias_name = match.group(1)
        alias_tail = match.group(2)
    else:
        parts = re.split(r"[\\/]", stripped, maxsplit=1)
        head = parts[0]
        tail = parts[1] if len(parts) > 1 else None
        aliases = load_path_aliases()
        if head in aliases or resolve_project_key(head, workbench_root) is not None:
            alias_name = head
            alias_tail = tail
    if alias_name is None:
        return None
    project_path = resolve_project_key(alias_name, workbench_root)
    if project_path is not None:
        return project_path / alias_tail if alias_tail else project_path
    aliases = load_path_aliases()
    target = aliases.get(alias_name)
    if not target:
        return None
    base = (workbench_root / Path(target)).resolve()
    return (base / alias_tail).resolve() if alias_tail else base


def resolve_direct_path(spec: str | None, base_root: Path = WORKBENCH_ROOT) -> Path | None:
    if not spec:
        return None
    candidate = Path(spec).expanduser()
    if candidate.exists():
        return candidate.resolve()
    rooted = (base_root / candidate).resolve()
    if rooted.exists():
        return rooted
    return None


def resolve_named_file(search_root: Path, spec: str, *, suffix: str | None = None) -> Path:
    direct = (search_root / spec).resolve()
    if direct.exists():
        return direct
    patterns: list[str] = [spec]
    if suffix and not spec.endswith(suffix):
        patterns.append(f"{spec}{suffix}")
        patterns.append(f"{spec}*{suffix}")
        patterns.append(f"*{spec}*{suffix}")
    else:
        patterns.append(f"{spec}*")
        patterns.append(f"*{spec}*")
    matches: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in search_root.rglob(pattern):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            matches.append(resolved)
    if not matches:
        raise SystemExit(f"Could not resolve '{spec}' under {search_root}")
    if len(matches) > 1:
        match_list = "\n".join(f"- {path}" for path in matches[:12])
        raise SystemExit(f"Ambiguous spec '{spec}' under {search_root}:\n{match_list}")
    return matches[0]


def resolve_project_arg(spec: str) -> Path:
    project = resolve_project_key(spec)
    if project is not None:
        return project
    alias_target = resolve_alias_target(spec)
    if alias_target is not None:
        return alias_target.resolve()
    direct = resolve_direct_path(spec)
    if direct is not None:
        return direct
    raise SystemExit(f"Could not resolve project: {spec}")


def resolve_scene_arg(spec: str, project: Path) -> Path:
    alias_target = resolve_alias_target(spec)
    if alias_target is not None:
        return alias_target.resolve()
    direct = resolve_direct_path(spec)
    if direct is not None:
        return direct
    return resolve_named_file(scene_cards_dir(project), spec, suffix=".json")


def resolve_script_arg(spec: str, project: Path) -> Path:
    alias_target = resolve_alias_target(spec)
    if alias_target is not None:
        return alias_target.resolve()
    direct = resolve_direct_path(spec)
    if direct is not None:
        return direct
    return resolve_named_file(generated_csv_dir(project), spec, suffix=".csv")


def resolve_output_arg(spec: str | None, base_root: Path = WORKBENCH_ROOT) -> Path | None:
    if not spec:
        return None
    alias_target = resolve_alias_target(spec, base_root)
    if alias_target is not None:
        return alias_target.resolve()
    path = Path(spec).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (Path.cwd() / path).resolve()


def resolve_generic_readable(spec: str) -> Path | None:
    """Resolve common workbench files without requiring Chinese subpaths."""
    alias_target = resolve_alias_target(spec)
    if alias_target is not None:
        return alias_target.resolve()
    direct = resolve_direct_path(spec)
    if direct is not None:
        return direct
    search_roots = [
        WORKBENCH_ROOT,
        WORKBENCH_ROOT / "00_workbench_core" / "docs",
        WORKBENCH_ROOT / "00_workbench_core" / "methods",
        WORKBENCH_ROOT / "00_workbench_core" / "references",
        WORKBENCH_ROOT / "00_workbench_core" / "portable_skills",
        WORKBENCH_ROOT / "06_学习输入" / "_风格画像",
        WORKBENCH_ROOT / "02_projects",
    ]
    matches: list[Path] = []
    seen: set[Path] = set()
    for root in search_roots:
        if not root.exists():
            continue
        try:
            candidate = resolve_named_file(root, spec)
        except SystemExit:
            continue
        if candidate.is_file() and candidate not in seen:
            seen.add(candidate)
            matches.append(candidate)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        match_list = "\n".join(f"- {path}" for path in matches[:12])
        raise SystemExit(f"Ambiguous readable target '{spec}':\n{match_list}")
    return None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_json_value(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_script_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [h for h in SCRIPT_HEADERS if h not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"Missing required columns: {', '.join(missing)}")
        rows: list[dict[str, str]] = []
        for raw in reader:
            if not any((v or "") for k, v in raw.items() if k is not None):
                continue
            extra = raw.pop(None, None)
            row = {k: (str(v) if v is not None else "").strip() for k, v in raw.items()}
            if extra:
                row["_extra_columns"] = " | ".join(str(x) for x in extra)
            rows.append(row)
        return rows


def first_existing(project: Path, *relative_paths: str) -> Path:
    for rel in relative_paths:
        path = project / rel
        if path.exists():
            return path
    return project / relative_paths[0]


def bible_dir(project: Path) -> Path:
    return first_existing(project, "00_project_memory/bible", "00_bible")


def character_cards_dir(project: Path) -> Path:
    return first_existing(project, "00_project_memory/cards/characters", "01_cards/characters")


def character_state_dir(project: Path) -> Path:
    return first_existing(project, "00_project_memory/runtime_state/characters", "02_memory/character_state")


def character_memory_dir(project: Path) -> Path:
    return first_existing(project, "00_project_memory/memory_logs/character_memory", "02_memory/character_memory")


def scene_summaries_dir(project: Path) -> Path:
    return first_existing(project, "00_project_memory/memory_logs/scene_summaries", "02_memory/scene_summaries")


def global_memory_path(project: Path) -> Path:
    return first_existing(project, "00_project_memory/memory_logs/global_memory.md", "02_memory/global_memory.md")


def theme_motifs_path(project: Path) -> Path:
    return first_existing(project, "00_project_memory/memory_logs/theme_motifs.md", "02_memory/theme_motifs.md")


def routes_dir(project: Path) -> Path:
    return first_existing(project, "01_narrative_design/routes", "03_routes")


def novel_architecture_dir(project: Path) -> Path:
    return first_existing(project, "01_narrative_design/novel_architecture", "03_routes/novel_architecture")


def interactive_design_dir(project: Path) -> Path:
    return first_existing(project, "01_narrative_design/interactive_design", "03_routes/interactive_design")


def scene_cards_dir(project: Path) -> Path:
    return first_existing(project, "01_narrative_design/scenes/scene_cards", "04_scenes/scene_cards")


def state_deltas_dir(project: Path) -> Path:
    return first_existing(project, "01_narrative_design/scenes/state_deltas", "04_scenes/state_deltas")


def generated_csv_dir(project: Path) -> Path:
    return first_existing(project, "02_generated_content/scripts/csv", "05_scripts/csv")


def generated_excel_dir(project: Path) -> Path:
    return first_existing(project, "02_generated_content/scripts/excel", "05_scripts/excel")


def exports_dir(project: Path) -> Path:
    return first_existing(project, "05_交付文件/引擎导出", "03_exports", "06_exports")


def character_export_dir(project: Path) -> Path:
    return first_existing(project, "05_交付文件/角色设定/角色卡导出", "03_exports/character_card_v2")


def quality_reports_dir(project: Path) -> Path:
    return first_existing(project, "99_内部工作/质检报告/当前", "04_quality/reports", "07_qa/reports")


def internal_context_dir(project: Path) -> Path:
    return first_existing(project, "99_内部工作/上下文包/当前", "03_exports/context")


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_characters(project: Path) -> dict[str, dict]:
    characters: dict[str, dict] = {}
    char_dir = character_cards_dir(project)
    for path in sorted(char_dir.glob("*.json")):
        data = load_json(path)
        characters[data.get("char_id") or data.get("id")] = data
    return characters


def visible_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def has_action(row: dict[str, str]) -> bool:
    return bool(row.get("body_action") or row.get("sfx") or row.get("bg"))


def prose_mark(row: dict[str, str]) -> str:
    if row.get("row_type") == "dialogue":
        return "D"
    if row.get("row_type") == "thought":
        return "T"
    if row.get("row_type") == "narration":
        return "N"
    return ""


def rhythm_blocks(rows: list[dict[str, str]]) -> list[tuple[str, str, int]]:
    blocks: list[tuple[str, str, int]] = []
    current_mark = ""
    current_start = ""
    current_len = 0
    for row in rows:
        mark = prose_mark(row)
        if not mark:
            continue
        if mark != current_mark:
            if current_mark:
                blocks.append((current_mark, current_start, current_len))
            current_mark = mark
            current_start = row.get("beat_id", "")
            current_len = 1
        else:
            current_len += 1
    if current_mark:
        blocks.append((current_mark, current_start, current_len))
    return blocks


def validate_rhythm(rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    marks = [(row.get("beat_id", ""), prose_mark(row)) for row in rows if prose_mark(row)]
    blocks = rhythm_blocks(rows)
    dialogue_blocks = [length for mark, _, length in blocks if mark == "D"]
    narration_blocks = [length for mark, _, length in blocks if mark == "N"]
    thought_blocks = [length for mark, _, length in blocks if mark == "T"]
    lonely_narration = 0

    for i in range(1, len(marks) - 1):
        if marks[i][1] == "N" and marks[i - 1][1] == "D" and marks[i + 1][1] == "D":
            lonely_narration += 1

    stats["dialogue_blocks"] = len(dialogue_blocks)
    stats["narration_blocks"] = len(narration_blocks)
    stats["thought_blocks"] = len(thought_blocks)
    stats["max_dialogue_block"] = max(dialogue_blocks) if dialogue_blocks else 0
    stats["max_narration_block"] = max(narration_blocks) if narration_blocks else 0
    stats["max_thought_block"] = max(thought_blocks) if thought_blocks else 0
    stats["lonely_narration_bridges"] = lonely_narration

    for i in range(0, max(0, len(marks) - 5)):
        window = marks[i : i + 6]
        pattern = "".join(mark for _, mark in window)
        if pattern in {"DNDNDN", "NDNDND"}:
            issues.append(
                Issue(
                    "warning",
                    window[-1][0],
                    "dialogue and narration alternate mechanically; group dialogue, interior, or staging into stronger blocks",
                )
            )
            break

    if lonely_narration >= 3:
        issues.append(
            Issue(
                "warning",
                "scene",
                "many single narration beats sit between dialogue lines; consider continuous dialogue blocks for immersion",
            )
        )


def ending_category(text: str) -> str:
    clean = text.strip()
    if not clean:
        return "blank"
    if re.search(r"[?\uFF1F][\u3002.!?\uFF01\uFF1F\u2026]*$", clean):
        return "question"
    if re.search(r"[!\uFF01][\u3002.!?\uFF01\uFF1F\u2026]*$", clean):
        return "exclaim"
    if re.search(r"(\u2026|\.{3}|\u2014|--)[\u3002.!?\uFF01\uFF1F\u2026]*$", clean):
        return "pause_or_cut"
    if re.search(r"[\u3002.]$", clean):
        return "full_stop"
    if re.search(r"[\uFF0C,]$", clean):
        return "comma_open"
    return "unmarked"


def validate_dialogue_energy(rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    dialogue = [row for row in rows if row.get("row_type") == "dialogue"]
    if not dialogue:
        return

    energy_count = 0
    question_count = 0
    exclaim_count = 0
    pause_or_cut_count = 0
    full_stop_count = 0
    unmarked_end_count = 0
    short_fragment_count = 0
    low_payload_count = 0
    casual_particle_count = 0
    payload_score_total = 0
    speaker_endings: dict[str, list[str]] = {}

    for row in dialogue:
        text = row.get("text", "")
        speaker = row.get("speaker", "")
        payload_score = 0
        if ENERGY_PUNCTUATION_RE.search(text):
            energy_count += 1
            payload_score += 1
        if QUESTION_RE.search(text):
            question_count += 1
        if EXCLAIM_RE.search(text):
            exclaim_count += 1
        if PAUSE_OR_CUT_RE.search(text):
            pause_or_cut_count += 1
        if CASUAL_PARTICLE_RE.search(text):
            casual_particle_count += 1
        if FULL_STOP_END_RE.search(text):
            full_stop_count += 1
        if text.strip() and not SENTENCE_CLOSED_RE.search(text.strip()):
            unmarked_end_count += 1
        if visible_len(text) <= 10:
            short_fragment_count += 1
        if visible_len(text) >= 12:
            payload_score += 1
        if row.get("body_action") or row.get("expression") or row.get("sfx"):
            payload_score += 1
        if row.get("effects") or row.get("memory_refs"):
            payload_score += 1
        if row.get("voice_target"):
            payload_score += 1
        payload_score_total += payload_score
        if payload_score <= 1:
            low_payload_count += 1
        speaker_endings.setdefault(speaker, []).append(ending_category(text))

    total = len(dialogue)
    stats["dialogue_energy_marks"] = energy_count
    stats["dialogue_energy_pct"] = round(energy_count * 100 / total)
    stats["dialogue_question_lines"] = question_count
    stats["dialogue_exclaim_lines"] = exclaim_count
    stats["dialogue_pause_or_cut_lines"] = pause_or_cut_count
    stats["dialogue_casual_particle_lines"] = casual_particle_count
    stats["dialogue_casual_particle_pct"] = round(casual_particle_count * 100 / total)
    stats["dialogue_full_stop_pct"] = round(full_stop_count * 100 / total)
    stats["dialogue_unmarked_endings"] = unmarked_end_count
    stats["dialogue_short_fragments"] = short_fragment_count
    stats["dialogue_short_fragment_pct"] = round(short_fragment_count * 100 / total)
    stats["dialogue_low_payload_lines"] = low_payload_count
    stats["dialogue_low_payload_pct"] = round(low_payload_count * 100 / total)
    stats["dialogue_payload_avg_x10"] = round(payload_score_total * 10 / total)

    if total >= 12 and energy_count / total < 0.15:
        issues.append(
            Issue(
                "warning",
                "dialogue",
                "dialogue has low line energy; add character-specific questions, cutoffs, pauses, or mask-breaking punctuation",
            )
        )

    if total >= 20 and casual_particle_count / total < 0.08:
        issues.append(
            Issue(
                "warning",
                "dialogue",
                "dialogue has little casual speech texture; add character-specific particles, nicknames, corrections, or playful pressure where appropriate",
            )
        )

    if total >= 12 and full_stop_count / total > 0.90:
        issues.append(
            Issue(
                "warning",
                "dialogue",
                "too many dialogue lines end the same way; vary punctuation by pressure and speaker voice",
            )
        )

    if total >= 12 and pause_or_cut_count / total > 0.35:
        issues.append(
            Issue(
                "warning",
                "dialogue",
                "pause or cutoff punctuation may be overused; make each hesitation carry a specific hidden word",
            )
        )

    if total >= 12 and short_fragment_count / total > 0.35:
        issues.append(
            Issue(
                "warning",
                "dialogue",
                "too many low-information short textboxes; combine action, response, or implication into fuller playable beats",
            )
        )

    if total >= 12 and low_payload_count / total > 0.25:
        issues.append(
            Issue(
                "warning",
                "dialogue",
                "too many low-payload clicks; each textbox should carry voice, object/action, implication, state, or tactical pressure",
            )
        )

    for speaker, endings in speaker_endings.items():
        if len(endings) >= 8 and len(set(endings)) <= 2:
            issues.append(
                Issue(
                    "warning",
                    speaker or "speaker",
                    "speaker has one-note line endings; update voice card or rewrite the block for actable variation",
                )
            )


def parse_command_payload(text: str, prefix: str) -> str:
    clean = text.strip()
    if not clean.startswith(prefix):
        return ""
    return clean[len(prefix) :].strip().rstrip(";").strip()


def validate_branch_integrity(rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    labels = {
        parse_command_payload(row.get("text", ""), "label:")
        for row in rows
        if row.get("row_type") == "command" and row.get("text", "").startswith("label:")
    }
    labels = {label for label in labels if label}
    choice_targets = [
        (row.get("beat_id", ""), row.get("choice_target", "").strip())
        for row in rows
        if row.get("row_type") == "choice" and row.get("choice_target", "").strip()
    ]
    jump_targets = [
        (row.get("beat_id", ""), parse_command_payload(row.get("text", ""), "jumpLabel:"))
        for row in rows
        if row.get("row_type") == "command" and row.get("text", "").startswith("jumpLabel:")
    ]
    stats["branch_labels"] = len(labels)
    stats["choice_targets"] = len(choice_targets)
    stats["jump_targets"] = len([target for _, target in jump_targets if target])

    unresolved = 0
    for beat, target in choice_targets + jump_targets:
        if target and target not in labels and target.upper() not in {"END", "DONE"}:
            unresolved += 1
            issues.append(Issue("warning", beat, f"branch target '{target}' has no matching label command"))
    stats["unresolved_branch_targets"] = unresolved


def validate_textbox_production(rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    prose_rows = [row for row in rows if row.get("row_type") in {"dialogue", "narration", "thought"}]
    if not prose_rows:
        return

    stage_cue_count = 0
    quote_wrapped_count = 0
    double_quote_count = 0
    ellipsis_only_count = 0
    first_person_narration_count = 0
    comma_fragment_count = 0
    multi_sentence_box_count = 0
    overflow_risk_count = 0

    for row in prose_rows:
        beat = row.get("beat_id", "")
        row_type = row.get("row_type", "")
        text = row.get("text", "")

        if row.get("bg") or row.get("bgm") or row.get("sfx") or row.get("expression") or row.get("body_action"):
            stage_cue_count += 1

        if ONLY_PAUSE_RE.match(text):
            ellipsis_only_count += 1
            issues.append(
                Issue(
                    "warning",
                    beat,
                    "ellipsis-only textbox; use stage direction, fade, SFX, or sprite timing for silence",
                )
            )

        sentence_count = len(TEXTBOX_SENTENCE_END_RE.findall(text))
        if row_type == "dialogue" and sentence_count > 2:
            multi_sentence_box_count += 1
            issues.append(
                Issue(
                    "warning",
                    beat,
                    "dialogue textbox contains too many sentence beats; split only where the click changes leverage",
                )
            )
        if row_type == "narration" and sentence_count > 3:
            multi_sentence_box_count += 1
            issues.append(
                Issue(
                    "warning",
                    beat,
                    "narration textbox may exceed the three-line law; move part into stage cue or next screen state",
                )
            )
        if row_type == "thought" and sentence_count > 2:
            multi_sentence_box_count += 1
            issues.append(
                Issue(
                    "warning",
                    beat,
                    "thought textbox contains too many sentence beats; split only where hesitation, clue reading, or choice pressure changes",
                )
            )

        if row_type == "dialogue":
            if DOUBLE_QUOTE_RE.search(text):
                double_quote_count += 1
                issues.append(
                    Issue(
                        "warning",
                        beat,
                        "dialogue contains double quotes; use speaker/name box or display layer instead",
                    )
                )
            if WRAPPED_DIALOGUE_QUOTE_RE.match(text):
                quote_wrapped_count += 1
                issues.append(
                    Issue(
                        "warning",
                        beat,
                        "dialogue text is wrapped as quoted prose; keep raw textbox text in CSV",
                    )
                )
            if len(COMMA_RE.findall(text)) >= 4:
                comma_fragment_count += 1
                issues.append(
                    Issue(
                        "warning",
                        beat,
                        "dialogue is comma-fragmented; preserve textbox flow instead of chopping the line",
                    )
                )

        if row_type == "narration" and FIRST_PERSON_RE.search(text):
            first_person_narration_count += 1

        if (
            (row_type == "dialogue" and visible_len(text) > 42)
            or (row_type == "narration" and visible_len(text) > 64)
            or (row_type == "thought" and visible_len(text) > 56)
        ):
            overflow_risk_count += 1

    stats["stage_cue_rows"] = stage_cue_count
    stats["stage_cue_pct"] = round(stage_cue_count * 100 / len(prose_rows))
    stats["dialogue_wrapped_quotes"] = quote_wrapped_count
    stats["dialogue_double_quotes"] = double_quote_count
    stats["ellipsis_only_boxes"] = ellipsis_only_count
    stats["first_person_narration_lines"] = first_person_narration_count
    stats["comma_fragment_lines"] = comma_fragment_count
    stats["multi_sentence_boxes"] = multi_sentence_box_count
    stats["textbox_overflow_risk"] = overflow_risk_count

    if stage_cue_count / len(prose_rows) < 0.35:
        issues.append(
            Issue(
                "warning",
                "scene",
                "low production annotation density; add body_action, expression, bg, bgm, sfx, or commands so the script serves game production",
            )
        )
    if first_person_narration_count >= 2:
        issues.append(
            Issue(
                "warning",
                "narration",
                "first-person narration is frequent; Galgame scripts should often soften the protagonist 'I' through name box, action, and screen state",
            )
        )
    if overflow_risk_count >= 4:
        issues.append(
            Issue(
                "warning",
                "textbox",
                "several textboxes risk exceeding ADV display comfort; apply the three-line law",
            )
        )


def validate_state_files(project: Path, characters: dict[str, dict], issues: list[Issue], stats: dict[str, int]) -> None:
    state_dir = character_state_dir(project)
    loaded = 0
    for cid in characters:
        state_path = state_dir / f"{cid}.json"
        if not state_path.exists():
            issues.append(Issue("warning", cid, "missing character_state file for long-term voice and psychology tracking"))
            continue
        data = load_json(state_path)
        loaded += 1
        for key in ["current_axes", "active_wants", "voice_lock", "state_history"]:
            if key not in data:
                issues.append(Issue("warning", cid, f"character_state lacks '{key}'"))
    stats["character_state_files"] = loaded


def validate_interiority(rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    dialogue_count = sum(1 for row in rows if row.get("row_type") == "dialogue")
    thought_rows = [row for row in rows if row.get("row_type") == "thought"]
    thought_count = len(thought_rows)
    stats["thought"] = thought_count
    stats["thought_rows"] = thought_count
    stats["thought_to_dialogue_pct"] = round(thought_count * 100 / dialogue_count) if dialogue_count else 0

    if dialogue_count >= 20 and thought_count < 3:
        issues.append(
            Issue(
                "warning",
                "thought",
                "dialogue-heavy scene has too little inner monologue; add thought rows for playable hesitation, clue reading, or unsaid pressure",
            )
        )

    useful_markers = re.compile(r"(票|章|手|窗|雨|车|字|孔|签|怕|不能|算了|等等|不对|糟|麻烦|要是|万一|为什么)")
    for row in thought_rows:
        text = row.get("text", "")
        beat = row.get("beat_id", "")
        if visible_len(text) < 8:
            issues.append(Issue("warning", beat, "thought row is too thin; inner monologue needs a clue, hesitation, contradiction, or choice pressure"))
        if not useful_markers.search(text):
            issues.append(Issue("warning", beat, "thought row lacks concrete pressure; tie it to object, body, clue, risk, or unsaid word"))


def validate_interiority_v2(rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    dialogue_count = sum(1 for row in rows if row.get("row_type") == "dialogue")
    thought_rows = [row for row in rows if row.get("row_type") == "thought"]
    thought_count = len(thought_rows)
    stats["thought"] = thought_count
    stats["thought_rows"] = thought_count
    stats["thought_to_dialogue_pct"] = round(thought_count * 100 / dialogue_count) if dialogue_count else 0

    if dialogue_count >= 20 and thought_count < 3:
        issues.append(
            Issue(
                "warning",
                "thought",
                "dialogue-heavy scene has too little inner monologue; add thought rows for playable hesitation, clue reading, or unsaid pressure",
            )
        )

    useful_markers = re.compile(
        "|".join(
            [
                "\u7968",
                "\u7ae0",
                "\u624b",
                "\u7a97",
                "\u96e8",
                "\u8f66",
                "\u5b57",
                "\u5b54",
                "\u7b7e",
                "\u6015",
                "\u4e0d\u80fd",
                "\u7b97\u4e86",
                "\u7b49\u7b49",
                "\u4e0d\u5bf9",
                "\u7cdf",
                "\u9ebb\u70e6",
                "\u8981\u662f",
                "\u4e07\u4e00",
                "\u4e3a\u4ec0\u4e48",
                "\u9875",
                "\u7eb8",
                "\u6587\u4ef6",
                "\u5408\u540c",
                "\u6837\u5f20",
                "\u53d6\u4ef6",
                "\u5361\u7eb8",
                "\u9489",
            ]
        )
    )
    for row in thought_rows:
        text = row.get("text", "")
        beat = row.get("beat_id", "")
        if visible_len(text) < 8:
            issues.append(Issue("warning", beat, "thought row is too thin; inner monologue needs a clue, hesitation, contradiction, or choice pressure"))
        if not useful_markers.search(text):
            issues.append(Issue("warning", beat, "thought row lacks concrete pressure; tie it to object, body, clue, risk, or unsaid word"))


def validate_scene_contract(project: Path, rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    scene_ids = [row.get("scene_id", "") for row in rows if row.get("scene_id")]
    scene_id = scene_ids[0] if scene_ids else ""
    if not scene_id:
        issues.append(Issue("error", "scene", "script lacks scene_id"))
        return

    card_path = scene_cards_dir(project) / f"{scene_id}_scene_card.json"
    if not card_path.exists():
        issues.append(Issue("warning", scene_id, f"missing scene card: {card_path.name}"))
        return

    scene = load_json(card_path)
    missing = [field for field in REQUIRED_SCENE_CONTRACT_FIELDS if not scene.get(field)]
    stats["scene_contract_fields"] = len(REQUIRED_SCENE_CONTRACT_FIELDS) - len(missing)
    if missing:
        issues.append(Issue("warning", scene_id, f"scene card lacks complete-work fields: {', '.join(missing)}"))


def as_list_from_json(value: object, *keys: str) -> list[dict]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in keys:
            nested = value.get(key)
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]
    return []


def split_refs(value: str) -> set[str]:
    refs: set[str] = set()
    for part in re.split(r"[;,\s\uFF1B\uFF0C]+", value or ""):
        clean = part.strip()
        if clean:
            refs.add(clean)
    return refs


def validate_novel_architecture(project: Path, rows: list[dict[str, str]], issues: list[Issue], stats: dict[str, int]) -> None:
    scene_ids = [row.get("scene_id", "") for row in rows if row.get("scene_id")]
    scene_id = scene_ids[0] if scene_ids else ""
    arch_dir = novel_architecture_dir(project)
    files = {
        "chapter_plan": arch_dir / "chapter_plan.json",
        "narrative_threads": arch_dir / "narrative_threads.json",
        "character_arcs": arch_dir / "character_arcs.json",
        "foreshadow_ledger": arch_dir / "foreshadow_ledger.json",
    }
    existing = {name: path for name, path in files.items() if path.exists()}
    stats["novel_architecture_files"] = len(existing)
    if not existing:
        issues.append(Issue("warning", scene_id or "scene", "missing novel architecture files; add chapter plan, narrative threads, character arcs, and foreshadow ledger"))
        return

    missing_files = [name for name, path in files.items() if not path.exists()]
    if missing_files:
        issues.append(Issue("warning", scene_id or "scene", f"novel architecture is incomplete: {', '.join(missing_files)}"))

    thread_items = as_list_from_json(load_json_value(files["narrative_threads"]), "threads") if files["narrative_threads"].exists() else []
    arc_items = as_list_from_json(load_json_value(files["character_arcs"]), "arcs") if files["character_arcs"].exists() else []
    fs_items = as_list_from_json(load_json_value(files["foreshadow_ledger"]), "items", "foreshadows") if files["foreshadow_ledger"].exists() else []
    chapter_items = as_list_from_json(load_json_value(files["chapter_plan"]), "chapters") if files["chapter_plan"].exists() else []

    thread_ids = {str(item.get("id")) for item in thread_items if item.get("id")}
    arc_ids = {str(item.get("id")) for item in arc_items if item.get("id")}
    fs_ids = {str(item.get("id")) for item in fs_items if item.get("id")}
    stats["narrative_threads"] = len(thread_ids)
    stats["character_arcs"] = len(arc_ids)
    stats["foreshadow_items"] = len(fs_ids)
    stats["chapter_plan_items"] = len(chapter_items)

    row_refs: set[str] = set()
    for row in rows:
        row_refs |= split_refs(row.get("memory_refs", ""))

    if thread_ids and not (row_refs & thread_ids):
        issues.append(Issue("warning", scene_id or "scene", "script rows do not reference any narrative thread id in memory_refs"))
    if arc_ids and not (row_refs & arc_ids):
        issues.append(Issue("warning", scene_id or "scene", "script rows do not reference any character arc id in memory_refs"))
    if fs_ids and not (row_refs & fs_ids):
        issues.append(Issue("warning", scene_id or "scene", "script rows do not reference any foreshadow id in memory_refs"))

    if not scene_id:
        return
    card_path = scene_cards_dir(project) / f"{scene_id}_scene_card.json"
    if not card_path.exists():
        return
    scene = load_json(card_path)
    novel_fields = [
        "chapter_goal",
        "scene_synopsis",
        "pov_character",
        "narrative_threads",
        "foreshadow_role",
        "prose_texture_target",
    ]
    missing_scene_fields = [field for field in novel_fields if not scene.get(field)]
    stats["novel_scene_layer_fields"] = len(novel_fields) - len(missing_scene_fields)
    if missing_scene_fields:
        issues.append(Issue("warning", scene_id, f"scene card lacks novel-architecture fields: {', '.join(missing_scene_fields)}"))


def validate_script(project: Path, script: Path) -> tuple[list[Issue], dict[str, int]]:
    rows = read_script_csv(script)
    characters = load_characters(project)
    issues: list[Issue] = []
    stats = {
        "rows": len(rows),
        "dialogue": 0,
        "narration": 0,
        "thought": 0,
        "choice": 0,
        "command": 0,
        "comment": 0,
        "errors": 0,
        "warnings": 0,
    }

    action_window: list[bool] = []
    seen_state_effect = False

    for idx, row in enumerate(rows, start=2):
        beat = row.get("beat_id") or f"row{idx}"
        row_type = row.get("row_type")
        text = row.get("text", "")

        if row.get("_extra_columns"):
            issues.append(Issue("error", beat, f"row has extra columns: {row['_extra_columns']}"))

        if row_type not in KNOWN_ROW_TYPES:
            issues.append(Issue("error", beat, f"unknown row_type '{row_type}'"))
        else:
            stats[row_type] += 1

        if row_type in {"dialogue", "narration", "thought"} and not text:
            issues.append(Issue("error", beat, "dialogue/narration/thought row has empty text"))

        if row_type == "dialogue":
            speaker = row.get("speaker")
            if speaker not in characters:
                issues.append(Issue("error", beat, f"unknown speaker '{speaker}'"))
            if visible_len(text) > 48:
                issues.append(Issue("warning", beat, f"textbox line may be long: {visible_len(text)} chars"))
            if not row.get("voice_target"):
                issues.append(Issue("warning", beat, "dialogue row lacks voice_target"))
            action_window.append(has_action(row))

        if row_type == "narration":
            if visible_len(text) > 72:
                issues.append(Issue("warning", beat, f"narration beat may be long: {visible_len(text)} chars"))
            action_window.append(has_action(row))

        if row_type == "thought":
            if visible_len(text) > 60:
                issues.append(Issue("warning", beat, f"thought beat may be long: {visible_len(text)} chars"))
            action_window.append(has_action(row))

        if len(action_window) >= 10:
            window = action_window[-10:]
            if not any(window):
                issues.append(Issue("warning", beat, "last 10 prose/dialogue rows lack body/object/environment action"))

        if row_type == "choice":
            if not row.get("choice_group"):
                issues.append(Issue("error", beat, "choice row lacks choice_group"))
            if not row.get("choice_text"):
                issues.append(Issue("error", beat, "choice row lacks choice_text"))
            if not row.get("choice_target"):
                issues.append(Issue("error", beat, "choice row lacks choice_target"))

        if row.get("effects"):
            seen_state_effect = True

        for pat in AI_PHRASE_PATTERNS:
            if pat.search(text):
                issues.append(Issue("warning", beat, f"possible assistant-like phrase: {pat.pattern}"))

        if row_type in {"dialogue", "narration", "thought"}:
            for word in ABSTRACT_EMOTION_WORDS:
                if word in text and not row.get("body_action"):
                    issues.append(Issue("warning", beat, f"abstract emotion word without body_action: {word}"))

    if not seen_state_effect:
        issues.append(Issue("error", "scene", "script has no effects/state changes"))

    validate_rhythm(rows, issues, stats)
    validate_dialogue_energy(rows, issues, stats)
    validate_branch_integrity(rows, issues, stats)
    validate_textbox_production(rows, issues, stats)
    validate_state_files(project, characters, issues, stats)
    validate_interiority_v2(rows, issues, stats)
    validate_scene_contract(project, rows, issues, stats)
    validate_novel_architecture(project, rows, issues, stats)

    stats["errors"] = 0
    stats["warnings"] = 0
    for issue in issues:
        stats["errors" if issue.level == "error" else "warnings"] += 1
    return issues, stats


def format_report(issues: list[Issue], stats: dict[str, int]) -> str:
    lines = ["# VN Workbench QA Report", ""]
    lines.append("## Stats")
    for key, value in stats.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Issues")
    if not issues:
        lines.append("- PASS: no issues found.")
    else:
        for issue in issues:
            lines.append(f"- [{issue.level.upper()}] {issue.beat_id}: {issue.message}")
    lines.append("")
    return "\n".join(lines)


def render_readable(project: Path, script: Path, out: Path) -> None:
    rows = read_script_csv(script)
    characters = load_characters(project)
    names = {cid: data.get("name", cid) for cid, data in characters.items()}
    scene_id = rows[0].get("scene_id", script.stem) if rows else script.stem
    lines: list[str] = [f"# {scene_id} Readable Draft", ""]

    i = 0
    while i < len(rows):
        row = rows[i]
        row_type = row.get("row_type")
        text = row.get("text", "")

        if row_type == "choice":
            group = row.get("choice_group", "")
            lines.extend(["【选择】", ""])
            while i < len(rows) and rows[i].get("row_type") == "choice" and rows[i].get("choice_group") == group:
                choice = rows[i]
                choice_text = choice.get("choice_text", "")
                description = choice.get("text", "")
                if description and description != choice_text:
                    lines.append(f"- {choice_text}：{description}")
                else:
                    lines.append(f"- {choice_text}")
                i += 1
            lines.append("")
            continue

        if row_type == "dialogue":
            speaker = names.get(row.get("speaker"), row.get("speaker", ""))
            lines.append(f"【{speaker}】『{text}』")
            lines.append("")
        elif row_type == "thought":
            speaker = names.get(row.get("speaker"), row.get("speaker", ""))
            if speaker:
                lines.append(f"【{speaker}】{thought_text(text)}")
            else:
                lines.append(thought_text(text))
            lines.append("")
        elif row_type == "narration":
            lines.append(text)
            lines.append("")
        elif row_type == "command":
            payload = text.strip()
            if payload.startswith("label:"):
                label = parse_command_payload(payload, "label:")
                lines.append(f"## 分支：{label}")
                lines.append("")
            elif payload.startswith("stage:"):
                cue = parse_command_payload(payload, "stage:")
                action = row.get("body_action", "")
                lines.append(f"@演出：{action or cue}")
                lines.append("")
            elif payload.startswith("jumpLabel:"):
                pass
            elif payload == "end":
                lines.append("@END")
                lines.append("")
            else:
                lines.append(f"@命令：{payload}")
                lines.append("")
        elif row_type == "comment":
            lines.append(f"<!-- {text} -->")
            lines.append("")
        i += 1

    write_text(out, "\n".join(lines).rstrip() + "\n")


def sanitize_webgal_text(text: str) -> str:
    return text.replace(";", "；").replace("\n", " ")


def thought_text(text: str) -> str:
    clean = text.strip()
    if clean.startswith("（") and clean.endswith("）"):
        return clean
    return f"（{clean}）"


def effect_to_webgal(effect: str) -> list[str]:
    commands: list[str] = []
    for part in [p.strip() for p in effect.split(";") if p.strip()]:
        if part.startswith("setVar:"):
            commands.append(part + ";")
        elif re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*(=|\+=|-=)", part):
            if "+=" in part:
                key, value = [x.strip() for x in part.split("+=", 1)]
                commands.append(f"setVar:{key}={key}+{value};")
            elif "-=" in part:
                key, value = [x.strip() for x in part.split("-=", 1)]
                commands.append(f"setVar:{key}={key}-{value};")
            else:
                commands.append(f"setVar:{part};")
        else:
            commands.append(f"; effect: {part}")
    return commands


def effect_parts(effect: str) -> list[str]:
    return [part.strip() for part in effect.split(";") if part.strip()]


def safe_identifier(value: str, fallback: str = "node") -> str:
    clean = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip())
    clean = clean.strip("_")
    if not clean:
        clean = fallback
    if re.match(r"^[0-9]", clean):
        clean = f"{fallback}_{clean}"
    return clean


def normalize_effect_for_engine(part: str) -> tuple[str, str, str] | None:
    clean = part.strip()
    if clean.startswith("setVar:"):
        clean = clean[len("setVar:") :].strip()
    for op in ["+=", "-=", "="]:
        if op in clean:
            key, value = [item.strip() for item in clean.split(op, 1)]
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
                return key, op, value
    return None


def collect_effect_variables(rows: list[dict[str, str]]) -> dict[str, str]:
    variables: dict[str, str] = {}
    for row in rows:
        for part in effect_parts(row.get("effects", "")):
            parsed = normalize_effect_for_engine(part)
            if not parsed:
                continue
            key, op, value = parsed
            if op == "=" and value.lower() in {"true", "false"}:
                variables.setdefault(key, "false")
            else:
                variables.setdefault(key, "0")
    return variables


def effect_to_ink(effect: str, indent: str = "") -> list[str]:
    lines: list[str] = []
    for part in effect_parts(effect):
        parsed = normalize_effect_for_engine(part)
        if not parsed:
            lines.append(f"{indent}// effect: {part}")
            continue
        key, op, value = parsed
        if op == "+=":
            lines.append(f"{indent}~ {key} = {key} + {value}")
        elif op == "-=":
            lines.append(f"{indent}~ {key} = {key} - {value}")
        else:
            lines.append(f"{indent}~ {key} = {value}")
    return lines


def effect_to_yarn(effect: str, indent: str = "") -> list[str]:
    lines: list[str] = []
    for part in effect_parts(effect):
        parsed = normalize_effect_for_engine(part)
        if not parsed:
            lines.append(f"{indent}// effect: {part}")
            continue
        key, op, value = parsed
        if op == "+=":
            lines.append(f"{indent}<<set ${key} to ${key} + {value}>>")
        elif op == "-=":
            lines.append(f"{indent}<<set ${key} to ${key} - {value}>>")
        else:
            lines.append(f"{indent}<<set ${key} to {value}>>")
    return lines


def effect_to_godot_dialogue(effect: str) -> list[str]:
    lines: list[str] = []
    for part in effect_parts(effect):
        parsed = normalize_effect_for_engine(part)
        if not parsed:
            lines.append(f"# effect: {part}")
            continue
        key, op, value = parsed
        if op == "+=":
            lines.append(f"do set_state(\"{key}\", {key} + {value})")
        elif op == "-=":
            lines.append(f"do set_state(\"{key}\", {key} - {value})")
        else:
            lines.append(f"do set_state(\"{key}\", {value})")
    return lines


def label_from_command(text: str) -> str:
    return safe_identifier(parse_command_payload(text, "label:"), "label")


def export_webgal(project: Path, script: Path, out: Path) -> None:
    rows = read_script_csv(script)
    characters = load_characters(project)
    names = {cid: data.get("name", cid) for cid, data in characters.items()}
    lines: list[str] = ["; Generated by VN Fusion Workbench"]

    i = 0
    while i < len(rows):
        row = rows[i]
        row_type = row.get("row_type")
        beat = row.get("beat_id", "")

        if row_type == "choice":
            group = row.get("choice_group")
            choices: list[str] = []
            while i < len(rows) and rows[i].get("row_type") == "choice" and rows[i].get("choice_group") == group:
                r = rows[i]
                text = sanitize_webgal_text(r.get("choice_text", ""))
                target = r.get("choice_target", "")
                condition = r.get("condition", "")
                if condition:
                    choices.append(f"({condition})->{text}:{target}")
                else:
                    choices.append(f"{text}:{target}")
                for cmd in effect_to_webgal(r.get("effects", "")):
                    lines.append(f"; choice effect {r.get('beat_id')}: {cmd}")
                i += 1
            lines.append(f"choose:{'|'.join(choices)};")
            continue

        if row_type == "command":
            text = row.get("text", "")
            if text.startswith("label:") or text.startswith("jumpLabel:") or text.startswith("changeScene:") or text.startswith("callScene:") or text.startswith("changeBg:") or text.startswith("bgm:") or text.startswith("setVar:"):
                lines.append(text if text.endswith(";") else text + ";")
            else:
                lines.append(f"; command {beat}: {sanitize_webgal_text(text)}")

        elif row_type == "dialogue":
            speaker = names.get(row.get("speaker"), row.get("speaker"))
            if row.get("body_action") or row.get("expression"):
                lines.append(f"; {beat} expression={row.get('expression')} action={sanitize_webgal_text(row.get('body_action', ''))}")
            lines.append(f"{speaker}:{sanitize_webgal_text(row.get('text', ''))};")
            for cmd in effect_to_webgal(row.get("effects", "")):
                lines.append(cmd)

        elif row_type == "narration":
            if row.get("body_action"):
                lines.append(f"; {beat} action={sanitize_webgal_text(row.get('body_action', ''))}")
            lines.append(f":{sanitize_webgal_text(row.get('text', ''))};")
            for cmd in effect_to_webgal(row.get("effects", "")):
                lines.append(cmd)

        elif row_type == "thought":
            if row.get("body_action"):
                lines.append(f"; {beat} thought_action={sanitize_webgal_text(row.get('body_action', ''))}")
            lines.append(f":{sanitize_webgal_text(thought_text(row.get('text', '')))};")
            for cmd in effect_to_webgal(row.get("effects", "")):
                lines.append(cmd)

        elif row_type == "comment":
            lines.append(f"; {beat}: {sanitize_webgal_text(row.get('text', ''))}")

        i += 1

    write_text(out, "\n".join(lines) + "\n")


def export_renpy(project: Path, script: Path, out: Path) -> None:
    rows = read_script_csv(script)
    characters = load_characters(project)
    names = {cid: data.get("name", cid) for cid, data in characters.items()}
    label = rows[0].get("scene_id", "scene") if rows else "scene"
    lines = ["# Generated by VN Fusion Workbench", f"label {label.lower()}:"]
    declared: set[str] = set()
    for cid, name in names.items():
        var = re.sub(r"[^a-zA-Z0-9_]", "_", cid.replace("CHR_", "c_"))
        if var not in declared:
            lines.insert(1, f'define {var} = Character("{name}")')
            declared.add(var)
    for row in rows:
        row_type = row.get("row_type")
        text = row.get("text", "").replace('"', '\\"')
        if row_type == "dialogue":
            var = re.sub(r"[^a-zA-Z0-9_]", "_", row.get("speaker", "").replace("CHR_", "c_"))
            lines.append(f'    {var} "{text}"')
        elif row_type == "narration":
            lines.append(f'    "{text}"')
        elif row_type == "thought":
            lines.append(f'    "{thought_text(text)}"')
        elif row_type == "command" and row.get("text", "").startswith("label:"):
            lines.append(f"    # {row.get('text')}")
        elif row_type == "choice":
            lines.append(f"    # choice {row.get('choice_group')}: {row.get('choice_text')} -> {row.get('choice_target')}")
    lines.append("    return")
    write_text(out, "\n".join(lines) + "\n")


def export_ink(project: Path, script: Path, out: Path) -> None:
    rows = read_script_csv(script)
    characters = load_characters(project)
    names = {cid: data.get("name", cid) for cid, data in characters.items()}
    scene_id = rows[0].get("scene_id", script.stem) if rows else script.stem
    start = safe_identifier(scene_id, "start")
    variables = collect_effect_variables(rows)
    lines: list[str] = ["// Generated by VN Fusion Workbench", ""]
    for key, default in sorted(variables.items()):
        lines.append(f"VAR {key} = {default}")
    if variables:
        lines.append("")
    lines.extend([f"-> {start}", "", f"=== {start} ==="])

    i = 0
    while i < len(rows):
        row = rows[i]
        row_type = row.get("row_type")
        beat = row.get("beat_id", "")
        if row_type == "choice":
            group = row.get("choice_group")
            while i < len(rows) and rows[i].get("row_type") == "choice" and rows[i].get("choice_group") == group:
                choice = rows[i]
                condition = choice.get("condition", "").strip()
                prefix = f"* {{{condition}}} " if condition else "* "
                lines.append(f"{prefix}[{choice.get('choice_text', '')}]")
                lines.extend(effect_to_ink(choice.get("effects", ""), indent="    "))
                target = safe_identifier(choice.get("choice_target", ""), "target")
                lines.append(f"    -> {target}")
                i += 1
            continue
        if row_type == "command":
            text = row.get("text", "")
            if text.startswith("label:"):
                lines.extend(["", f"=== {label_from_command(text)} ==="])
            elif text.startswith("jumpLabel:"):
                lines.append(f"-> {safe_identifier(parse_command_payload(text, 'jumpLabel:'), 'target')}")
            elif text.startswith("setVar:"):
                lines.extend(effect_to_ink(text, indent=""))
            else:
                lines.append(f"// command {beat}: {text}")
        elif row_type == "dialogue":
            speaker = names.get(row.get("speaker"), row.get("speaker"))
            if row.get("body_action") or row.get("expression"):
                lines.append(f"// {beat} expression={row.get('expression')} action={row.get('body_action')}")
            lines.append(f"{speaker}: {row.get('text', '')}")
            lines.extend(effect_to_ink(row.get("effects", ""), indent=""))
        elif row_type == "narration":
            if row.get("body_action"):
                lines.append(f"// {beat} action={row.get('body_action')}")
            lines.append(row.get("text", ""))
            lines.extend(effect_to_ink(row.get("effects", ""), indent=""))
        elif row_type == "thought":
            if row.get("body_action"):
                lines.append(f"// {beat} thought_action={row.get('body_action')}")
            lines.append(thought_text(row.get("text", "")))
            lines.extend(effect_to_ink(row.get("effects", ""), indent=""))
        elif row_type == "comment":
            lines.append(f"// {beat}: {row.get('text', '')}")
        i += 1

    lines.append("-> END")
    write_text(out, "\n".join(lines) + "\n")


def export_yarn(project: Path, script: Path, out: Path) -> None:
    rows = read_script_csv(script)
    characters = load_characters(project)
    names = {cid: data.get("name", cid) for cid, data in characters.items()}
    scene_id = rows[0].get("scene_id", script.stem) if rows else script.stem
    current_node = safe_identifier(scene_id, "Start")
    variables = collect_effect_variables(rows)
    lines: list[str] = [
        "// Generated by VN Fusion Workbench",
        f"title: {current_node}",
        "---",
    ]
    for key, default in sorted(variables.items()):
        lines.append(f"<<declare ${key} = {default}>>")

    i = 0
    while i < len(rows):
        row = rows[i]
        row_type = row.get("row_type")
        beat = row.get("beat_id", "")
        if row_type == "choice":
            group = row.get("choice_group")
            while i < len(rows) and rows[i].get("row_type") == "choice" and rows[i].get("choice_group") == group:
                choice = rows[i]
                if choice.get("condition"):
                    lines.append(f"// condition for next option: {choice.get('condition')}")
                lines.append(f"-> {choice.get('choice_text', '')}")
                lines.extend(effect_to_yarn(choice.get("effects", ""), indent="    "))
                lines.append(f"    <<jump {safe_identifier(choice.get('choice_target', ''), 'target')}>>")
                i += 1
            continue
        if row_type == "command":
            text = row.get("text", "")
            if text.startswith("label:"):
                current_node = label_from_command(text)
                lines.extend(["===", "", f"title: {current_node}", "---"])
            elif text.startswith("jumpLabel:"):
                lines.append(f"<<jump {safe_identifier(parse_command_payload(text, 'jumpLabel:'), 'target')}>>")
            elif text.startswith("setVar:"):
                lines.extend(effect_to_yarn(text, indent=""))
            else:
                lines.append(f"// command {beat}: {text}")
        elif row_type == "dialogue":
            speaker = names.get(row.get("speaker"), row.get("speaker"))
            if row.get("body_action") or row.get("expression"):
                lines.append(f"// {beat} expression={row.get('expression')} action={row.get('body_action')}")
            lines.append(f"{speaker}: {row.get('text', '')}")
            lines.extend(effect_to_yarn(row.get("effects", ""), indent=""))
        elif row_type == "narration":
            if row.get("body_action"):
                lines.append(f"// {beat} action={row.get('body_action')}")
            lines.append(row.get("text", ""))
            lines.extend(effect_to_yarn(row.get("effects", ""), indent=""))
        elif row_type == "thought":
            if row.get("body_action"):
                lines.append(f"// {beat} thought_action={row.get('body_action')}")
            lines.append(thought_text(row.get("text", "")))
            lines.extend(effect_to_yarn(row.get("effects", ""), indent=""))
        elif row_type == "comment":
            lines.append(f"// {beat}: {row.get('text', '')}")
        i += 1

    lines.extend(["<<stop>>", "==="])
    write_text(out, "\n".join(lines) + "\n")


def export_godot_dialogue(project: Path, script: Path, out: Path) -> None:
    rows = read_script_csv(script)
    characters = load_characters(project)
    names = {cid: data.get("name", cid) for cid, data in characters.items()}
    scene_id = rows[0].get("scene_id", script.stem) if rows else script.stem
    lines: list[str] = [
        "# Generated by VN Fusion Workbench",
        f"~ {safe_identifier(scene_id, 'start')}",
    ]

    i = 0
    auto_choice_index = 0
    while i < len(rows):
        row = rows[i]
        row_type = row.get("row_type")
        beat = row.get("beat_id", "")
        if row_type == "choice":
            group = row.get("choice_group")
            pending_choice_cues: list[tuple[str, dict[str, str]]] = []
            while i < len(rows) and rows[i].get("row_type") == "choice" and rows[i].get("choice_group") == group:
                choice = rows[i]
                target = safe_identifier(choice.get("choice_target", ""), "target")
                if choice.get("effects"):
                    cue = safe_identifier(f"{group}_{auto_choice_index}", "choice")
                    auto_choice_index += 1
                    pending_choice_cues.append((cue, choice))
                    target = cue
                condition = f" [if {choice.get('condition')} /]" if choice.get("condition") else ""
                lines.append(f"- {choice.get('choice_text', '')}{condition} => {target}")
                i += 1
            for cue, choice in pending_choice_cues:
                lines.extend(["", f"~ {cue}"])
                lines.extend(effect_to_godot_dialogue(choice.get("effects", "")))
                lines.append(f"=> {safe_identifier(choice.get('choice_target', ''), 'target')}")
            continue
        if row_type == "command":
            text = row.get("text", "")
            if text.startswith("label:"):
                lines.extend(["", f"~ {label_from_command(text)}"])
            elif text.startswith("jumpLabel:"):
                lines.append(f"=> {safe_identifier(parse_command_payload(text, 'jumpLabel:'), 'target')}")
            elif text.startswith("setVar:"):
                lines.extend(effect_to_godot_dialogue(text))
            else:
                lines.append(f"# command {beat}: {text}")
        elif row_type == "dialogue":
            speaker = names.get(row.get("speaker"), row.get("speaker"))
            tags = []
            if row.get("expression"):
                tags.append(f"#{row.get('expression')}")
            if row.get("voice_target"):
                tags.append(f"#voice={row.get('voice_target')}")
            tag_text = f" [{', '.join(tags)}]" if tags else ""
            if row.get("body_action"):
                lines.append(f"# {beat} action={row.get('body_action')}")
            lines.append(f"{speaker}:{tag_text} {row.get('text', '')}".rstrip())
            lines.extend(effect_to_godot_dialogue(row.get("effects", "")))
        elif row_type == "narration":
            if row.get("body_action"):
                lines.append(f"# {beat} action={row.get('body_action')}")
            lines.append(row.get("text", ""))
            lines.extend(effect_to_godot_dialogue(row.get("effects", "")))
        elif row_type == "thought":
            if row.get("body_action"):
                lines.append(f"# {beat} thought_action={row.get('body_action')}")
            lines.append(thought_text(row.get("text", "")))
            lines.extend(effect_to_godot_dialogue(row.get("effects", "")))
        elif row_type == "comment":
            lines.append(f"# {beat}: {row.get('text', '')}")
        i += 1

    lines.append("=> END")
    write_text(out, "\n".join(lines) + "\n")


def export_character_cards_v2(project: Path, out_dir: Path) -> None:
    characters = load_characters(project)
    out_dir.mkdir(parents=True, exist_ok=True)
    for cid, data in characters.items():
        state_path = character_state_dir(project) / f"{cid}.json"
        state = load_json(state_path) if state_path.exists() else {}
        memory_text = read_optional_text(character_memory_dir(project) / f"{cid}.md")
        fp = data.get("speech_fingerprint", {})
        examples = data.get("example_dialogue", {})
        voice_lock = state.get("voice_lock", {})
        if isinstance(voice_lock, dict):
            forbidden_voice = voice_lock.get("forbidden", [])
        elif isinstance(voice_lock, list):
            forbidden_voice = voice_lock
        elif isinstance(voice_lock, str) and voice_lock.strip():
            forbidden_voice = [voice_lock.strip()]
        else:
            forbidden_voice = []
        example_lines: list[str] = []
        for mode, lines_for_mode in examples.items():
            example_lines.append(f"<START>")
            example_lines.append(f"{{{{char}}}} ({mode}):")
            for line in lines_for_mode:
                example_lines.append(f"{{{{char}}}}: {line}")
        lore_entries = [
            {
                "keys": [data.get("name", cid), data.get("role", "")],
                "content": f"身份：{data.get('role', '')}\n欲望：{data.get('desire', '')}\n恐惧：{data.get('fear', '')}",
                "enabled": True,
                "insertion_order": 0,
            },
            {
                "keys": list(data.get("taboo_topics", [])),
                "content": f"禁区：{', '.join(data.get('taboo_topics', []))}\n禁用表达：{', '.join(forbidden_voice)}",
                "enabled": True,
                "insertion_order": 1,
            },
            {
                "keys": state.get("memory_retrieval_priorities", []),
                "content": memory_text[:1800] if memory_text else "暂无场景记忆。",
                "enabled": True,
                "insertion_order": 2,
            },
        ]
        card = {
            "spec": "chara_card_v2",
            "spec_version": "2.0",
            "data": {
                "name": data.get("name", cid),
                "description": "\n".join(
                    [
                        f"角色：{data.get('role', '')}",
                        f"外壳：{data.get('social_mask', '')}",
                        f"伤口：{data.get('private_wound', '')}",
                        f"当前目标：{'; '.join(state.get('active_wants', []))}",
                    ]
                ),
                "personality": json.dumps(fp, ensure_ascii=False, indent=2),
                "scenario": json.dumps(
                    {
                        "current_axes": state.get("current_axes", {}),
                        "withheld_truths": state.get("withheld_truths", []),
                        "retrieval": state.get("memory_retrieval_priorities", []),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                "first_mes": "",
                "mes_example": "\n".join(example_lines),
                "creator_notes": "Exported from VN Fusion Workbench. This is a compatibility package for voice and lorebook review, not a runtime dependency.",
                "system_prompt": "保持角色声纹、禁区、当前心理轴和关系成本。不要替角色解释主题，用动作、物件、称呼变化和回避来表现。",
                "post_history_instructions": json.dumps(
                    {
                        "voice_lock": state.get("voice_lock", {}),
                        "active_wants": state.get("active_wants", []),
                        "withheld_truths": state.get("withheld_truths", []),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                "alternate_greetings": [],
                "tags": ["vn-fusion-workbench", "galgame", project.name],
                "creator": "VN Fusion Workbench",
                "character_version": "1.0",
                "extensions": {
                    "vn_fusion_workbench": {
                        "character_id": cid,
                        "project": project.name,
                        "source_files": [
                            display_path(character_cards_dir(project) / f"{cid}.json", project),
                            display_path(state_path, project),
                            display_path(character_memory_dir(project) / f"{cid}.md", project),
                        ],
                    }
                },
                "character_book": {
                    "name": f"{data.get('name', cid)} lorebook",
                    "entries": lore_entries,
                },
            },
        }
        write_text(out_dir / f"{cid}.card_v2.json", json.dumps(card, ensure_ascii=False, indent=2) + "\n")


def text_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def inline_list(value: object) -> str:
    return " / ".join(text_list(value))


def derive_memory_points(data: dict, state: dict) -> list[str]:
    presentation = data.get("presentation", {}) if isinstance(data.get("presentation"), dict) else {}
    points: list[str] = []
    for key in (
        "memory_points",
        "signature_objects",
        "signature_gestures",
        "charm_hook",
        "liveliness_floor",
        "punctuation_play",
    ):
        points.extend(text_list(presentation.get(key)))

    embodiment = data.get("embodiment", {}) if isinstance(data.get("embodiment"), dict) else {}
    for key in ("hands", "gaze", "posture"):
        points.extend(text_list(embodiment.get(key))[:2])
    if embodiment.get("idle_action"):
        points.append(f"闲置动作：{embodiment.get('idle_action')}")
    if embodiment.get("pressure_action"):
        points.append(f"受压动作：{embodiment.get('pressure_action')}")

    fp = data.get("speech_fingerprint", {}) if isinstance(data.get("speech_fingerprint"), dict) else {}
    for word in text_list(fp.get("fillers"))[:2]:
        points.append(f"口头钩子：{word}")
    for word in text_list(fp.get("vocabulary"))[:3]:
        points.append(f"词汇钩子：{word}")

    if data.get("social_mask"):
        points.append(f"社交面具：{data.get('social_mask')}")
    if state.get("active_wants"):
        points.append(f"当前想要：{inline_list(state.get('active_wants'))}")

    seen: set[str] = set()
    unique: list[str] = []
    for point in points:
        clean = point.strip()
        if clean and clean not in seen:
            unique.append(clean)
            seen.add(clean)
    return unique[:7]


def render_character_brief(project: Path, out: Path) -> None:
    characters = load_characters(project)
    lines: list[str] = [
        "# Character Brief",
        "",
        f"Project: `{project.name}`",
        "Generated from character cards, runtime state, and character memory logs.",
        "",
    ]

    for cid, data in characters.items():
        state_path = character_state_dir(project) / f"{cid}.json"
        state = load_json(state_path) if state_path.exists() else {}
        memory_text = read_optional_text(character_memory_dir(project) / f"{cid}.md").strip()
        presentation = data.get("presentation", {}) if isinstance(data.get("presentation"), dict) else {}
        fp = data.get("speech_fingerprint", {}) if isinstance(data.get("speech_fingerprint"), dict) else {}
        embodiment = data.get("embodiment", {}) if isinstance(data.get("embodiment"), dict) else {}
        examples = data.get("example_dialogue", {}) if isinstance(data.get("example_dialogue"), dict) else {}
        body_signature = f"hands={inline_list(embodiment.get('hands'))}; gaze={inline_list(embodiment.get('gaze'))}; pressure={embodiment.get('pressure_action', '')}"
        if not any([inline_list(embodiment.get("hands")), inline_list(embodiment.get("gaze")), embodiment.get("pressure_action")]):
            body_signature = inline_list(presentation.get("signature_gestures"))
        relationship_hooks = text_list(presentation.get("relationship_hooks"))
        if not relationship_hooks and isinstance(data.get("relationships"), dict):
            relationship_hooks = [f"{key}: {value}" for key, value in data.get("relationships", {}).items()]
        if not relationship_hooks and isinstance(state.get("relationship_state"), dict):
            relationship_hooks = [f"{key}: {value}" for key, value in state.get("relationship_state", {}).items()]

        lines.extend(
            [
                f"## {data.get('name', cid)} ({cid})",
                "",
                f"- First-screen impression: {presentation.get('first_screen_impression') or data.get('role', '')}",
                f"- Role in system: {data.get('role', '')}",
                f"- Public want: {data.get('public_want') or data.get('desire', '')}",
                f"- Private want: {data.get('private_want') or inline_list(state.get('active_wants'))}",
                f"- Fear / shame / taboo: {data.get('fear', '')}; {data.get('shame_source', '')}; {inline_list(data.get('taboo_topics'))}",
                f"- Social mask: {data.get('social_mask', '')}",
                f"- Charm hook: {presentation.get('charm_hook', '')}",
                f"- Liveliness floor: {presentation.get('liveliness_floor', '')}",
                f"- Punctuation play: {presentation.get('punctuation_play', '')}",
                f"- Voice signature: {fp.get('default_rhythm', '')}; pressure: {fp.get('pressure_rhythm', '')}; fillers: {inline_list(fp.get('fillers'))}; punctuation: {fp.get('punctuation', '')}",
                f"- Body signature: {body_signature}",
                f"- Arc promise: {presentation.get('arc_promise') or data.get('route_question') or ''}",
                "",
                "### Memory Points",
            ]
        )
        memory_points = derive_memory_points(data, state)
        if memory_points:
            for point in memory_points:
                lines.append(f"- {point}")
        else:
            lines.append("- MISSING: add presentation.memory_points or stronger embodiment / voice hooks.")

        lines.extend(["", "### Relationship Hooks"])
        if relationship_hooks:
            for hook in relationship_hooks[:8]:
                lines.append(f"- {hook}")
        else:
            lines.append("- MISSING: add relationship hooks or runtime relationship pressure.")

        lines.extend(["", "### Example Lines"])
        if examples:
            for mode, values in examples.items():
                sample = text_list(values)[:3]
                if sample:
                    lines.append(f"- {mode}: {' | '.join(sample)}")
        else:
            lines.append("- MISSING: add example_dialogue by pressure state.")

        if memory_text:
            preview = "\n".join(memory_text.splitlines()[:8])
            lines.extend(["", "### Memory Log Preview", preview])
        lines.append("")

    write_text(out, "\n".join(lines).rstrip() + "\n")


def read_optional_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def context_pack(project: Path, scene_path: Path, out: Path) -> None:
    scene = load_json(scene_path)
    characters = load_characters(project)
    bible = bible_dir(project)
    arch = novel_architecture_dir(project)
    interactive = interactive_design_dir(project)
    lines: list[str] = [
        "# Context Pack",
        "",
        f"Project: {project.name}",
        f"Scene: {scene.get('scene_id')} {scene.get('title')}",
        "",
        "## Bible",
        read_optional_text(bible / "premise.md"),
        read_optional_text(bible / "core_theme.md"),
        read_optional_text(bible / "style_rules.md"),
        read_optional_text(bible / "style_reference_pack.md"),
        read_optional_text(bible / "anti_ai_phrases.md"),
        read_optional_text(bible / "display_voice_rules.md"),
        "",
        "## Scene Card",
        json.dumps(scene, ensure_ascii=False, indent=2),
        "",
        "## Novel Architecture",
        "### Chapter Plan",
        read_optional_text(arch / "chapter_plan.json"),
        "### Narrative Threads",
        read_optional_text(arch / "narrative_threads.json"),
        "### Character Arcs",
        read_optional_text(arch / "character_arcs.json"),
        "### Foreshadow Ledger",
        read_optional_text(arch / "foreshadow_ledger.json"),
        "",
        "## Playable Thesis And State",
        "### Theme Spine",
        read_optional_text(interactive / "theme_spine.json"),
        "### Quality State Ledger",
        read_optional_text(interactive / "quality_state_ledger.json"),
        "### Vertical Slice Audit",
        read_optional_text(interactive / "vertical_slice_audit.json"),
        "",
        "## Characters",
    ]
    for cid, data in characters.items():
        lines.append(f"### {data.get('name')} ({cid})")
        lines.append(f"- desire: {data.get('desire')}")
        lines.append(f"- fear: {data.get('fear')}")
        presentation = data.get("presentation", {}) if isinstance(data.get("presentation"), dict) else {}
        if presentation:
            lines.append(f"- first_screen_impression: {presentation.get('first_screen_impression')}")
            lines.append(f"- memory_points: {', '.join(text_list(presentation.get('memory_points')))}")
            lines.append(f"- charm_hook: {presentation.get('charm_hook')}")
            lines.append(f"- liveliness_floor: {presentation.get('liveliness_floor')}")
            lines.append(f"- punctuation_play: {presentation.get('punctuation_play')}")
            lines.append(f"- arc_promise: {presentation.get('arc_promise')}")
        fp = data.get("speech_fingerprint", {})
        lines.append(f"- default_rhythm: {fp.get('default_rhythm')}")
        lines.append(f"- pressure_rhythm: {fp.get('pressure_rhythm')}")
        lines.append(f"- vocabulary: {', '.join(fp.get('vocabulary', []))}")
        lines.append(f"- dodge: {fp.get('dodge')}")
        lines.append(f"- lie_style: {fp.get('lie_style')}")
        lines.append(f"- punctuation: {fp.get('punctuation')}")
        if fp.get("line_energy_profile"):
            lines.append(f"- line_energy_profile: {json.dumps(fp.get('line_energy_profile'), ensure_ascii=False)}")
        if fp.get("social_texture_profile"):
            lines.append(f"- social_texture_profile: {json.dumps(fp.get('social_texture_profile'), ensure_ascii=False)}")
        if fp.get("sentence_kernel_profile"):
            lines.append(f"- sentence_kernel_profile: {json.dumps(fp.get('sentence_kernel_profile'), ensure_ascii=False)}")
        lines.append("")
        memory = read_optional_text(character_memory_dir(project) / f"{cid}.md")
        if memory:
            lines.append(memory)
            lines.append("")
        state = character_state_dir(project) / f"{cid}.json"
        if state.exists():
            lines.append("#### Current State")
            lines.append(state.read_text(encoding="utf-8"))
            lines.append("")
    lines.append("## Global Memory")
    lines.append(read_optional_text(global_memory_path(project)))
    motifs = theme_motifs_path(project)
    if motifs.exists():
        lines.append("")
        lines.append("## Theme And Motifs")
        lines.append(motifs.read_text(encoding="utf-8"))
    lines.append("")
    lines.append("## Writing Instructions")
    lines.append("- Draft each line from current want, hidden truth, relationship leverage, emotion axis, and object in hand.")
    lines.append("- Do not let characters state their full inner meaning directly.")
    lines.append("- Every important line should change leverage, reveal a wound, hide a fact, or alter state.")
    write_text(out, "\n".join(lines))


def method_root() -> Path:
    return Path(__file__).resolve().parent.parent / "methods"


def load_method_index() -> dict:
    return load_json(method_root() / "method_index.json")


def load_selected_methods(methods_arg: str | None) -> list[dict]:
    index = load_method_index()
    methods = index.get("methods", [])
    if methods_arg:
        requested = {item.strip() for item in methods_arg.split(",") if item.strip()}
        selected = [method for method in methods if method.get("id") in requested]
        missing = sorted(requested - {method.get("id") for method in selected})
        if missing:
            raise SystemExit(f"Unknown method id(s): {', '.join(missing)}")
    else:
        selected = [method for method in methods if method.get("default_enabled")]

    for method in selected:
        path = method_root() / method["file"]
        method["body"] = path.read_text(encoding="utf-8")
    return selected


def render_invocation_trace(methods: list[dict]) -> list[str]:
    lines = [
        "## Invocation Trace",
        "",
        "| Method | Source refs | Why loaded | Output contract |",
        "| --- | --- | --- | --- |",
    ]
    for method in methods:
        refs = "<br>".join(method.get("source_refs", []))
        lines.append(
            f"| `{method.get('id')}` | {refs} | {method.get('invocation', '')} | {method.get('output_contract', '')} |"
        )
    lines.append("")
    return lines


def pre_draft_files(project: Path, scene_path: Path, characters: dict[str, dict]) -> list[dict[str, object]]:
    bible = bible_dir(project)
    arch = novel_architecture_dir(project)
    interactive = interactive_design_dir(project)
    scene = load_json(scene_path)
    scene_id = scene.get("scene_id") or scene_path.stem.replace("_scene_card", "")
    files: list[tuple[str, Path, bool]] = [
        ("bible", bible / "premise.md", True),
        ("bible", bible / "core_theme.md", True),
        ("bible", bible / "style_rules.md", True),
        ("bible", bible / "style_reference_pack.md", False),
        ("bible", bible / "anti_ai_phrases.md", True),
        ("bible", bible / "display_voice_rules.md", True),
        ("scene", scene_path, True),
        ("scene", state_deltas_dir(project) / f"{scene_id}_state_delta.json", False),
        ("route", routes_dir(project) / "route_map.json", True),
        ("novel_architecture", arch / "chapter_plan.json", False),
        ("novel_architecture", arch / "narrative_threads.json", False),
        ("novel_architecture", arch / "character_arcs.json", False),
        ("novel_architecture", arch / "foreshadow_ledger.json", False),
        ("interactive_design", interactive / "theme_spine.json", False),
        ("interactive_design", interactive / "quality_state_ledger.json", False),
        ("interactive_design", interactive / "vertical_slice_audit.json", False),
        ("memory", global_memory_path(project), False),
        ("memory", theme_motifs_path(project), False),
    ]
    for cid in characters:
        files.append(("character_card", character_cards_dir(project) / f"{cid}.json", True))
        files.append(("character_state", character_state_dir(project) / f"{cid}.json", True))
        files.append(("character_memory", character_memory_dir(project) / f"{cid}.md", False))
    return [
        {
            "category": category,
            "path": display_path(path, project),
            "exists": path.exists(),
            "required": required,
        }
        for category, path, required in files
    ]


def scene_brief(project: Path, scene_path: Path, out: Path, methods_arg: str | None = None) -> None:
    scene = load_json(scene_path)
    characters = load_characters(project)
    methods = load_selected_methods(methods_arg)
    bible = bible_dir(project)
    arch = novel_architecture_dir(project)
    interactive = interactive_design_dir(project)
    loaded_files = [
        bible / "premise.md",
        bible / "core_theme.md",
        bible / "style_rules.md",
        bible / "style_reference_pack.md",
        bible / "anti_ai_phrases.md",
        bible / "display_voice_rules.md",
        scene_path,
        routes_dir(project) / "route_map.json",
        theme_motifs_path(project),
        arch / "chapter_plan.json",
        arch / "narrative_threads.json",
        arch / "character_arcs.json",
        arch / "foreshadow_ledger.json",
        interactive / "theme_spine.json",
        interactive / "quality_state_ledger.json",
        interactive / "vertical_slice_audit.json",
    ]
    for cid in characters:
        loaded_files.append(character_cards_dir(project) / f"{cid}.json")
        loaded_files.append(character_state_dir(project) / f"{cid}.json")

    lines: list[str] = [
        "# Scene Draft Brief",
        "",
        f"Project: `{project.name}`",
        f"Scene: `{scene.get('scene_id')}` {scene.get('title', '')}",
        "",
    ]
    lines.extend(render_invocation_trace(methods))
    lines.extend(
        [
            "## Loaded Local Files",
            "",
        ]
    )
    for path in loaded_files:
        marker = "OK" if path.exists() else "MISSING"
        lines.append(f"- [{marker}] `{display_path(path, project)}`")
    lines.append("")

    lines.extend(
        [
            "## Scene Contract",
            "",
            f"- Question: {scene.get('scene_question', '')}",
            f"- Answer: {scene.get('scene_answer', '')}",
            f"- Professional ritual: {scene.get('professional_ritual', '')}",
            f"- Character lie pressure: {scene.get('character_lie_pressure', '')}",
            f"- Dramatic turn: {scene.get('dramatic_turn', '')}",
            f"- Sequel decision: {scene.get('sequel_decision', '')}",
            f"- Theme pressure: {scene.get('theme_pressure', '')}",
            f"- Choice pressure: {scene.get('choice_pressure', '')}",
            "",
            "## Novel Architecture",
            "",
            "### Scene Layer",
            "",
            f"- Chapter goal: {scene.get('chapter_goal', '')}",
            f"- Scene synopsis: {scene.get('scene_synopsis', '')}",
            f"- POV character: {scene.get('pov_character', '')}",
            f"- Narrative threads: {json.dumps(scene.get('narrative_threads', []), ensure_ascii=False)}",
            f"- Foreshadow role: {json.dumps(scene.get('foreshadow_role', {}), ensure_ascii=False)}",
            f"- Prose texture target: {scene.get('prose_texture_target', '')}",
            "",
            "### Chapter Plan",
            "",
            read_optional_text(arch / "chapter_plan.json"),
            "",
            "### Narrative Threads",
            "",
            read_optional_text(arch / "narrative_threads.json"),
            "",
            "### Character Arcs",
            "",
            read_optional_text(arch / "character_arcs.json"),
            "",
            "### Foreshadow Ledger",
            "",
            read_optional_text(arch / "foreshadow_ledger.json"),
            "",
            "## Playable Thesis And State",
            "",
            "### Theme Spine",
            "",
            read_optional_text(interactive / "theme_spine.json"),
            "",
            "### Quality State Ledger",
            "",
            read_optional_text(interactive / "quality_state_ledger.json"),
            "",
            "### Vertical Slice Audit",
            "",
            read_optional_text(interactive / "vertical_slice_audit.json"),
            "",
            "## Project Theme",
            "",
            read_optional_text(bible / "core_theme.md"),
            "",
            "## Style Rules",
            "",
            read_optional_text(bible / "style_rules.md"),
            "",
            "## Display And Voice Rules",
            "",
            read_optional_text(bible / "display_voice_rules.md"),
            "",
            "## Character Runtime States",
            "",
        ]
    )
    for cid, data in characters.items():
        lines.append(f"### {data.get('name')} ({cid})")
        lines.append("")
        lines.append("#### Character Card Summary")
        lines.append(f"- desire: {data.get('desire')}")
        lines.append(f"- fear: {data.get('fear')}")
        lines.append(f"- taboo_topics: {', '.join(data.get('taboo_topics', []))}")
        fp = data.get("speech_fingerprint", {})
        lines.append(f"- default_rhythm: {fp.get('default_rhythm')}")
        lines.append(f"- pressure_rhythm: {fp.get('pressure_rhythm')}")
        lines.append(f"- dodge: {fp.get('dodge')}")
        lines.append(f"- punctuation: {fp.get('punctuation')}")
        if fp.get("line_energy_profile"):
            lines.append(f"- line_energy_profile: {json.dumps(fp.get('line_energy_profile'), ensure_ascii=False)}")
        if fp.get("social_texture_profile"):
            lines.append(f"- social_texture_profile: {json.dumps(fp.get('social_texture_profile'), ensure_ascii=False)}")
        if fp.get("sentence_kernel_profile"):
            lines.append(f"- sentence_kernel_profile: {json.dumps(fp.get('sentence_kernel_profile'), ensure_ascii=False)}")
        lines.append("")
        state_path = character_state_dir(project) / f"{cid}.json"
        if state_path.exists():
            lines.append("#### Runtime State")
            lines.append("```json")
            lines.append(state_path.read_text(encoding="utf-8"))
            lines.append("```")
        else:
            lines.append("MISSING runtime state.")
        lines.append("")

    lines.extend(
        [
            "## Drafting Checklist Generated From Methods",
            "",
            "- Answer the scene question with cost, not exposition.",
            "- Make the professional ritual move an object, signature, record, door, camera, or deadline.",
            "- For each major exchange, track surface topic, hidden want, unsafe word, and object cover.",
            "- Each choice must show immediate feedback and record delayed state.",
            "- If branches reconverge, preserve visible state in later lines or options.",
            "- Point to one gameplay action, one character action, one plot change, and one theme pressure.",
            "- Read character runtime state before writing dialogue; update it after the scene.",
            "- Assign line energy before each dialogue line; punctuation must express pressure, not decoration.",
            "- Generate each character's sentence from their sentence kernel, then apply display-layer rules.",
            "- Treat each row as a restricted-view textbox with a production cue; avoid prose-only paragraphs.",
            "- Use stage annotations for silence, fades, CG/sprite changes, SFX, and menu timing instead of ellipsis-only boxes.",
            "- Keep dialogue raw in CSV; speaker identity belongs in the speaker/name-box field, not double quotes.",
            "- Anchor the scene in chapter_goal, narrative_threads, character_arcs, and foreshadow_ledger before writing the first row.",
            "- Use memory_refs to point important lines to THR_, ARC_, and FS_ ids instead of explaining the structure inside dialogue.",
            "- Let textbox payload vary: some lines press, some dodge, some leak evidence, but empty filler should be cut.",
            "- Add thought rows where the player needs hesitation, private clue reading, or unsaid pressure.",
            "- Render review drafts with dialogue as 『』 and inner thought as （）; do not judge Gal rhythm from plain prose alone.",
            "- Tie the scene to a playable thesis: repeated player behavior, cost, concrete object, route argument, and final payoff.",
            "- Treat qualities, storylets, and microinteractions as stateful callbacks, not isolated flavor.",
            "- Before expanding a project, prove a vertical slice with CSV, readable preview, QA, exports, and memory updates.",
            "",
            "## Method Cards",
            "",
        ]
    )
    for method in methods:
        lines.append(f"### {method.get('id')}: {method.get('title')}")
        lines.append("")
        lines.append(method.get("body", ""))
        lines.append("")
    write_text(out, "\n".join(lines))


def draft_session(project: Path, scene_path: Path, out_dir: Path, methods_arg: str | None, draft_name: str | None) -> dict[str, Path]:
    scene = load_json(scene_path)
    scene_id = scene.get("scene_id") or scene_path.stem.replace("_scene_card", "")
    draft_base = draft_name or f"{scene_id}_draft"
    characters = load_characters(project)
    methods = load_selected_methods(methods_arg)
    out_dir.mkdir(parents=True, exist_ok=True)

    brief_path = out_dir / f"{scene_id}_scene_brief.md"
    context_path = out_dir / f"{scene_id}_context_pack.md"
    session_json_path = out_dir / f"{scene_id}_draft_session.json"
    session_md_path = out_dir / f"{scene_id}_draft_session.md"

    scene_brief(project, scene_path, brief_path, methods_arg)
    context_pack(project, scene_path, context_path)

    script_path = generated_csv_dir(project) / f"{draft_base}.csv"
    readable_path = project / "02_generated_content" / "drafts" / "readable" / f"{draft_base}.md"
    revision_path = project / "02_generated_content" / "revisions" / f"{draft_base}_notes.md"
    qa_path = quality_reports_dir(project) / f"{draft_base}_qa.md"
    deep_audit_path = quality_reports_dir(project) / f"{draft_base}_deep_audit.md"
    webgal_path = exports_dir(project) / "webgal" / f"{draft_base}.txt"
    renpy_path = exports_dir(project) / "renpy" / f"{draft_base}.rpy"
    ink_path = exports_dir(project) / "ink" / f"{draft_base}.ink"
    yarn_path = exports_dir(project) / "yarn" / f"{draft_base}.yarn"
    godot_dialogue_path = exports_dir(project) / "godot_dialogue" / f"{draft_base}.dialogue"
    character_card_v2_dir = character_export_dir(project)
    character_brief_path = internal_context_dir(project) / f"{draft_base}_character_brief.md"

    method_summaries = [
        {
            "id": method.get("id"),
            "title": method.get("title"),
            "file": str(method_root() / method.get("file", "")),
            "source_refs": method.get("source_refs", []),
            "invocation": method.get("invocation", ""),
            "output_contract": method.get("output_contract", ""),
        }
        for method in methods
    ]
    loaded_files = pre_draft_files(project, scene_path, characters)
    storage_contract = {
        "reusable_methods": "00_workbench_core/methods/",
        "project_memory": "02_projects/<project>/00_project_memory/",
        "narrative_design": "02_projects/<project>/01_narrative_design/",
        "novel_architecture": "02_projects/<project>/01_narrative_design/novel_architecture/",
        "interactive_design": "02_projects/<project>/01_narrative_design/interactive_design/",
        "generated_content": "02_projects/<project>/02_generated_content/",
        "engine_exports": "02_projects/<project>/05_交付文件/引擎导出/",
        "character_exports": "02_projects/<project>/05_交付文件/角色设定/角色卡导出/",
        "internal_context": "02_projects/<project>/99_内部工作/上下文包/",
        "quality_reports": "02_projects/<project>/99_内部工作/质检报告/",
    }
    outputs = {
        "script_csv": display_path(script_path, project),
        "readable_draft": display_path(readable_path, project),
        "revision_notes": display_path(revision_path, project),
        "qa_report": display_path(qa_path, project),
        "deep_audit": display_path(deep_audit_path, project),
        "webgal_export": display_path(webgal_path, project),
        "renpy_export": display_path(renpy_path, project),
        "ink_export": display_path(ink_path, project),
        "yarn_export": display_path(yarn_path, project),
        "godot_dialogue_export": display_path(godot_dialogue_path, project),
        "character_card_v2_dir": display_path(character_card_v2_dir, project),
        "character_brief": display_path(character_brief_path, project),
        "scene_brief": display_path(brief_path, project),
        "context_pack": display_path(context_path, project),
    }
    project_arg = f".\\02_projects\\{project.name}"
    script_arg = f"{project_arg}\\02_generated_content\\scripts\\csv\\{draft_base}.csv"
    commands = [
        f"python .\\00_workbench_core\\tools\\vn_workbench.py validate --project {project_arg} --script {script_arg}",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py deep-audit --project {project_arg} --script {script_arg}",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py export-webgal --project {project_arg} --script {script_arg} --out {project_arg}\\05_交付文件\\引擎导出\\webgal\\{draft_base}.txt",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py export-renpy --project {project_arg} --script {script_arg} --out {project_arg}\\05_交付文件\\引擎导出\\renpy\\{draft_base}.rpy",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py export-ink --project {project_arg} --script {script_arg} --out {project_arg}\\05_交付文件\\引擎导出\\ink\\{draft_base}.ink",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py export-yarn --project {project_arg} --script {script_arg} --out {project_arg}\\05_交付文件\\引擎导出\\yarn\\{draft_base}.yarn",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py export-godot-dialogue --project {project_arg} --script {script_arg} --out {project_arg}\\05_交付文件\\引擎导出\\godot_dialogue\\{draft_base}.dialogue",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py export-character-card-v2 --project {project_arg} --out-dir {project_arg}\\05_交付文件\\角色设定\\角色卡导出",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py character-brief --project {project_arg} --out {project_arg}\\99_内部工作\\上下文包\\当前\\{draft_base}_character_brief.md",
        f"python .\\00_workbench_core\\tools\\vn_workbench.py render-readable --project {project_arg} --script {script_arg} --out {project_arg}\\02_generated_content\\drafts\\readable\\{draft_base}.md",
        f"node .\\00_workbench_core\\tools\\build_excel_template.mjs {project.name} {draft_base}.csv",
    ]
    payload = {
        "project": project.name,
        "scene_id": scene_id,
        "scene_title": scene.get("title", ""),
        "draft_name": draft_base,
        "created_by": "vn_workbench draft-session",
        "must_read_before_drafting": [
            display_path(session_md_path, project),
            display_path(brief_path, project),
            display_path(context_path, project),
        ],
        "methods": method_summaries,
        "loaded_files": loaded_files,
        "storage_contract": storage_contract,
        "required_outputs": outputs,
        "post_draft_commands": commands,
        "draft_rules": [
            "Classify the newest user prompt before acting: learning, writing, rewrite, continuation, expansion, character setup, or artifact delivery.",
            "If new or unstable characters are involved, produce or refresh a user-visible character brief before deep drafting.",
            "Write dialogue in blocks when characters are pressing each other; do not alternate dialogue/narration mechanically.",
            "Before each major line, check current want, unsafe word, relationship leverage, emotion axis, and object in hand.",
            "Before each block, check chapter goal, scene synopsis, narrative thread, character arc, and foreshadow role.",
            "Use thought rows for playable hesitation and unsaid pressure; do not hide all psychology inside narration.",
            "Readable previews must preserve Gal display: dialogue as 『』 and thought as （）.",
            "Use memory_refs for THR_, ARC_, and FS_ ids when a line touches long-form structure.",
            "Every choice must change information, relationship, resource, state, or route access.",
            "After validation, update character memory only for facts this scene actually changes.",
        ],
    }
    write_text(session_json_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    lines: list[str] = [
        "# Draft Session",
        "",
        f"Project: `{project.name}`",
        f"Scene: `{scene_id}` {scene.get('title', '')}",
        f"Draft name: `{draft_base}`",
        "",
        "## Read Before Drafting",
        "",
        f"1. `{display_path(brief_path, project)}`",
        f"2. `{display_path(context_path, project)}`",
        f"3. `{display_path(session_json_path, project)}`",
        "",
        "## Method Invocation",
        "",
        "| Method | Why loaded | Output contract |",
        "| --- | --- | --- |",
    ]
    for method in method_summaries:
        lines.append(f"| `{method['id']}` | {method['invocation']} | {method['output_contract']} |")
    lines.extend(["", "## Loaded Files", ""])
    for item in loaded_files:
        marker = "OK" if item["exists"] else "MISSING"
        req = "required" if item["required"] else "optional"
        lines.append(f"- [{marker}] `{item['path']}` ({item['category']}, {req})")
    lines.extend(["", "## Output Contract", ""])
    for label, rel in outputs.items():
        lines.append(f"- `{label}` -> `{rel}`")
    lines.extend(["", "## Post-Draft Commands", "", "```powershell"])
    lines.extend(commands)
    lines.extend(
        [
            "```",
            "",
            "## Non-Negotiable Draft Rules",
            "",
            "- Continuous dialogue is allowed and expected when leverage is changing fast.",
            "- Narration should touch a usable object, a deadline, a sound, a document, or a body movement.",
            "- Do not use balanced assistant-style explanation in creative text.",
            "- Character voice must survive a hidden-name test.",
            "- If new characters are created or materially revised, generate a user-visible character brief with memory points before or alongside the script.",
            "- Interpret user critique as a workbench signal: update reusable methods for general failures and project memory for canon changes.",
            "- Every dialogue block must carry enough payload for a click: fact, pressure, wound, tactic, or delayed payoff.",
            "- Major evidence, emotional reversals, and route hooks must cite THR_, ARC_, or FS_ ids in `memory_refs`.",
            "- Project-only memory goes under `00_project_memory/`; generated prose goes under `02_generated_content/`.",
            "",
        ]
    )
    write_text(session_md_path, "\n".join(lines))

    return {
        "session_json": session_json_path,
        "session_md": session_md_path,
        "scene_brief": brief_path,
        "context_pack": context_path,
    }


def collect_string_ids(value: object) -> set[str]:
    ids: set[str] = set()
    id_keys = {
        "id",
        "scene_id",
        "choice_id",
        "object_id",
        "thread_id",
        "arc_id",
        "foreshadow_id",
        "variable",
        "variable_id",
        "label",
        "target",
    }
    list_keys = {
        "ids",
        "tags",
        "narrative_threads",
        "seeds",
        "echoes",
        "payoffs",
        "memory_refs",
        "callbacks",
        "depends_on",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if key in id_keys and isinstance(item, str) and item.strip():
                ids.add(item.strip())
            if key in list_keys and isinstance(item, list):
                ids |= {str(entry).strip() for entry in item if str(entry).strip()}
            ids |= collect_string_ids(item)
    elif isinstance(value, list):
        for item in value:
            ids |= collect_string_ids(item)
    return ids


def collect_memory_log_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"\[([A-Za-z][A-Za-z0-9_:-]+)\]", text))


def known_project_refs(project: Path, scene_id: str) -> set[str]:
    refs: set[str] = set()
    for cid in load_characters(project):
        refs.add(cid)
    for memory_path in character_memory_dir(project).glob("*.md"):
        refs |= collect_memory_log_ids(memory_path)
    paths = [
        scene_cards_dir(project) / f"{scene_id}_scene_card.json",
        state_deltas_dir(project) / f"{scene_id}_state_delta.json",
        routes_dir(project) / "route_map.json",
        novel_architecture_dir(project) / "chapter_plan.json",
        novel_architecture_dir(project) / "narrative_threads.json",
        novel_architecture_dir(project) / "character_arcs.json",
        novel_architecture_dir(project) / "foreshadow_ledger.json",
        interactive_design_dir(project) / "theme_spine.json",
        interactive_design_dir(project) / "quality_state_ledger.json",
        interactive_design_dir(project) / "vertical_slice_audit.json",
    ]
    for path in paths:
        if path.exists():
            refs |= collect_string_ids(load_json_value(path))
    return refs


def branch_graph(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    graph: dict[str, dict[str, object]] = {}
    current = "__START__"
    graph[current] = {
        "rows": 0,
        "row_types": {},
        "speakers": {},
        "memory_refs": [],
        "effects": [],
        "choices": [],
        "jumps": [],
    }
    for row in rows:
        row_type = row.get("row_type", "")
        text = row.get("text", "")
        if row_type == "command" and text.startswith("label:"):
            current = parse_command_payload(text, "label:")
            graph.setdefault(
                current,
                {
                    "rows": 0,
                    "row_types": {},
                    "speakers": {},
                    "memory_refs": [],
                    "effects": [],
                    "choices": [],
                    "jumps": [],
                },
            )
            continue

        node = graph.setdefault(
            current,
            {
                "rows": 0,
                "row_types": {},
                "speakers": {},
                "memory_refs": [],
                "effects": [],
                "choices": [],
                "jumps": [],
            },
        )
        node["rows"] = int(node["rows"]) + 1
        row_types = node["row_types"]
        if isinstance(row_types, dict):
            row_types[row_type] = int(row_types.get(row_type, 0)) + 1
        if row_type == "dialogue":
            speakers = node["speakers"]
            if isinstance(speakers, dict):
                speaker = row.get("speaker", "")
                speakers[speaker] = int(speakers.get(speaker, 0)) + 1
        refs = sorted(split_refs(row.get("memory_refs", "")))
        if refs and isinstance(node["memory_refs"], list):
            node["memory_refs"].extend(refs)
        if row.get("effects") and isinstance(node["effects"], list):
            node["effects"].append({"beat_id": row.get("beat_id", ""), "effects": row.get("effects", "")})
        if row_type == "choice" and isinstance(node["choices"], list):
            node["choices"].append(
                {
                    "beat_id": row.get("beat_id", ""),
                    "group": row.get("choice_group", ""),
                    "text": row.get("choice_text", ""),
                    "target": row.get("choice_target", ""),
                    "effects": row.get("effects", ""),
                }
            )
        if row_type == "command" and text.startswith("jumpLabel:") and isinstance(node["jumps"], list):
            node["jumps"].append({"beat_id": row.get("beat_id", ""), "target": parse_command_payload(text, "jumpLabel:")})

    for node in graph.values():
        if isinstance(node.get("memory_refs"), list):
            node["memory_refs"] = sorted(set(str(ref) for ref in node["memory_refs"]))
    return graph


def state_delta_choices(project: Path, scene_id: str) -> dict[str, dict[str, object]]:
    path = state_deltas_dir(project) / f"{scene_id}_state_delta.json"
    if not path.exists():
        return {}
    data = load_json(path)
    choices = data.get("choices", [])
    if not isinstance(choices, list):
        return {}
    result: dict[str, dict[str, object]] = {}
    for item in choices:
        if not isinstance(item, dict):
            continue
        choice_id = str(item.get("choice_id", "")).strip()
        if choice_id:
            result[choice_id] = item
    return result


def effect_variables(effect: str) -> set[str]:
    variables: set[str] = set()
    for part in effect_parts(effect):
        parsed = normalize_effect_for_engine(part)
        if parsed:
            variables.add(parsed[0])
    return variables


def all_effect_variables(rows: list[dict[str, str]]) -> set[str]:
    variables: set[str] = set()
    for row in rows:
        variables |= effect_variables(row.get("effects", ""))
    return variables


def branch_effect_map(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for row in rows:
        if row.get("row_type") != "choice":
            continue
        effects = row.get("effects", "")
        for part in effect_parts(effects):
            parsed = normalize_effect_for_engine(part)
            if not parsed:
                continue
            key, _, value = parsed
            if key == "choice_label_48":
                result.setdefault(str(value), set())
        label_value = ""
        for part in effect_parts(effects):
            parsed = normalize_effect_for_engine(part)
            if parsed and parsed[0] == "choice_label_48":
                label_value = parsed[2]
        if label_value:
            result.setdefault(label_value, set()).update(effect_variables(effects))
    return result


def expected_state_effect_vars(delta_choice: dict[str, object]) -> set[str]:
    effects = delta_choice.get("effects", {})
    if not isinstance(effects, dict):
        return set()
    return {str(key) for key in effects.keys()}


def character_control_audit(project: Path, rows: list[dict[str, str]]) -> list[dict[str, object]]:
    characters = load_characters(project)
    result: list[dict[str, object]] = []
    for cid, data in characters.items():
        state_path = character_state_dir(project) / f"{cid}.json"
        memory_path = character_memory_dir(project) / f"{cid}.md"
        dialogue_rows = [row for row in rows if row.get("speaker") == cid and row.get("row_type") == "dialogue"]
        voice_targets = sorted({row.get("voice_target", "") for row in dialogue_rows if row.get("voice_target", "")})
        memory_text = read_optional_text(memory_path)
        retrieval_blocks = len(re.findall(r"(?m)^-\s*\[[^\]]+\]", memory_text))
        fp = data.get("speech_fingerprint", {}) if isinstance(data.get("speech_fingerprint"), dict) else {}
        result.append(
            {
                "character_id": cid,
                "name": data.get("name", cid),
                "card": True,
                "state": state_path.exists(),
                "memory_log": memory_path.exists(),
                "retrieval_blocks": retrieval_blocks,
                "dialogue_rows": len(dialogue_rows),
                "voice_targets": voice_targets,
                "has_sentence_kernel": bool(fp.get("sentence_kernel_profile")),
                "has_line_energy": bool(fp.get("line_energy_profile")),
                "has_social_texture": bool(fp.get("social_texture_profile")),
            }
        )
    return result


def deep_audit(project: Path, script: Path, out: Path) -> dict[str, object]:
    rows = read_script_csv(script)
    scene_id = rows[0].get("scene_id", script.stem) if rows else script.stem
    graph = branch_graph(rows)
    labels = {label for label in graph.keys() if label != "__START__"}
    choice_targets = {row.get("choice_target", "").strip() for row in rows if row.get("row_type") == "choice" and row.get("choice_target", "").strip()}
    jump_targets = {
        parse_command_payload(row.get("text", ""), "jumpLabel:")
        for row in rows
        if row.get("row_type") == "command" and row.get("text", "").startswith("jumpLabel:")
    }
    jump_targets = {target for target in jump_targets if target}
    unresolved_targets = sorted(target for target in choice_targets | jump_targets if target not in labels and target.upper() not in {"END", "DONE"})
    used_refs: set[str] = set()
    for row in rows:
        used_refs |= split_refs(row.get("memory_refs", ""))
    known_refs = known_project_refs(project, scene_id)
    unknown_refs = sorted(ref for ref in used_refs if ref not in known_refs)
    delta_choices = state_delta_choices(project, scene_id)
    branch_effects = branch_effect_map(rows)
    state_mismatches: list[dict[str, object]] = []
    label_alias = {
        "label_recycle": "recycle",
        "label_archive": "archive",
        "label_borrow": "borrow",
    }
    for choice_id, delta_choice in delta_choices.items():
        branch_key = label_alias.get(choice_id, choice_id)
        expected = expected_state_effect_vars(delta_choice)
        actual = branch_effects.get(branch_key, set())
        missing = sorted(expected - actual)
        extra = sorted(actual - expected - {"choice_label_48"})
        if missing or extra:
            state_mismatches.append(
                {
                    "choice_id": choice_id,
                    "branch_key": branch_key,
                    "missing_in_csv": missing,
                    "extra_in_csv": extra,
                }
            )

    character_audit = character_control_audit(project, rows)
    issues: list[str] = []
    if unresolved_targets:
        issues.append(f"Unresolved branch targets: {', '.join(unresolved_targets)}")
    if unknown_refs:
        issues.append(f"Unknown memory_refs: {', '.join(unknown_refs)}")
    for mismatch in state_mismatches:
        issues.append(
            "State delta mismatch for {choice_id}: missing={missing} extra={extra}".format(
                choice_id=mismatch["choice_id"],
                missing=",".join(mismatch["missing_in_csv"]) or "-",
                extra=",".join(mismatch["extra_in_csv"]) or "-",
            )
        )
    for item in character_audit:
        if item["dialogue_rows"] and not item["retrieval_blocks"]:
            issues.append(f"{item['character_id']} has dialogue but no retrieval-shaped memory block")
        if item["dialogue_rows"] and not item["state"]:
            issues.append(f"{item['character_id']} has dialogue but no runtime state file")

    payload = {
        "project": project.name,
        "script": display_path(script, project),
        "scene_id": scene_id,
        "graph": graph,
        "known_refs_count": len(known_refs),
        "used_memory_refs": sorted(used_refs),
        "unknown_memory_refs": unknown_refs,
        "effect_variables": sorted(all_effect_variables(rows)),
        "state_delta_mismatches": state_mismatches,
        "character_control": character_audit,
        "issues": issues,
        "source_lessons": [
            "Yarn Spinner: analyse dialogue as nodes, blocks, destinations, and options.",
            "ink: parse authored flow, then resolve references into runtime containers.",
            "Ren'Py: lint jump/menu/label and expression boundaries before trusting script output.",
            "TwineJS: keep passage ids, tags, and story metadata searchable.",
            "Character memory systems: separate stable cards, runtime state, and retrievable episodic blocks.",
        ],
    }
    json_path = out.with_suffix(".json")
    write_text(json_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Deep Narrative Audit",
        "",
        f"Project: `{project.name}`",
        f"Script: `{display_path(script, project)}`",
        f"Scene: `{scene_id}`",
        "",
        "## Result",
        "",
    ]
    if issues:
        for issue in issues:
            lines.append(f"- [ISSUE] {issue}")
    else:
        lines.append("- PASS: graph, refs, state effects, and character-control layers are aligned.")
    lines.extend(["", "## Branch Graph", ""])
    for label, node in graph.items():
        choices = node.get("choices", [])
        jumps = node.get("jumps", [])
        lines.append(f"### {label}")
        lines.append(f"- rows: {node.get('rows')}")
        lines.append(f"- row_types: {json.dumps(node.get('row_types', {}), ensure_ascii=False)}")
        lines.append(f"- speakers: {json.dumps(node.get('speakers', {}), ensure_ascii=False)}")
        lines.append(f"- memory_refs: {', '.join(node.get('memory_refs', [])) if node.get('memory_refs') else '-'}")
        if choices:
            for choice in choices:
                lines.append(f"- choice {choice.get('beat_id')}: {choice.get('text')} -> {choice.get('target')} | {choice.get('effects')}")
        if jumps:
            for jump in jumps:
                lines.append(f"- jump {jump.get('beat_id')}: -> {jump.get('target')}")
        lines.append("")
    lines.extend(["## Character Control", ""])
    for item in character_audit:
        lines.append(
            "- `{character_id}` rows={dialogue_rows}, state={state}, memory={memory_log}, retrieval_blocks={retrieval_blocks}, voice_targets={voice_targets}".format(
                **item
            )
        )
    lines.extend(
        [
            "",
            "## State Effects",
            "",
            f"- effect variables in CSV: {', '.join(sorted(all_effect_variables(rows))) or '-'}",
            f"- state delta mismatches: {len(state_mismatches)}",
            "",
            "## Source Lessons Applied",
            "",
            "- Yarn Spinner: node/block/destination analysis.",
            "- ink: authored flow is not trusted until references resolve.",
            "- Ren'Py: lint labels, jumps, choices, and expression boundaries.",
            "- TwineJS: use ids/tags as searchable story metadata.",
            "- Character memory systems: stable card + runtime state + retrievable memory blocks.",
            "",
            f"Machine-readable payload: `{display_path(json_path, project)}`",
            "",
        ]
    )
    write_text(out, "\n".join(lines))
    return payload


def command_deep_audit(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out) if args.out else quality_reports_dir(project) / f"{script.stem}_deep_audit.md"
    payload = deep_audit(project, script, out)
    print(f"Wrote deep audit: {out}")
    print(f"Wrote deep audit json: {out.with_suffix('.json')}")
    return 1 if payload.get("issues") else 0


def command_validate(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    issues, stats = validate_script(project, script)
    report = format_report(issues, stats)
    print(report)
    report_path = quality_reports_dir(project) / f"{script.stem}_qa.md"
    write_text(report_path, report)
    return 1 if stats["errors"] else 0


def command_export_webgal(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out)
    export_webgal(project, script, out)
    print(f"Wrote WebGAL script: {out}")
    return 0


def command_export_renpy(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out)
    export_renpy(project, script, out)
    print(f"Wrote Ren'Py draft: {out}")
    return 0


def command_export_ink(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out)
    export_ink(project, script, out)
    print(f"Wrote Ink draft: {out}")
    return 0


def command_export_yarn(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out)
    export_yarn(project, script, out)
    print(f"Wrote Yarn draft: {out}")
    return 0


def command_export_godot_dialogue(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out)
    export_godot_dialogue(project, script, out)
    print(f"Wrote Godot Dialogue Manager draft: {out}")
    return 0


def command_export_character_card_v2(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    out_dir = resolve_output_arg(args.out_dir)
    export_character_cards_v2(project, out_dir)
    print(f"Wrote Character Card V2 files: {out_dir}")
    return 0


def command_character_brief(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    out = resolve_output_arg(args.out)
    render_character_brief(project, out)
    print(f"Wrote character brief: {out}")
    return 0


def command_render_readable(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    script = resolve_script_arg(args.script, project)
    out = resolve_output_arg(args.out)
    render_readable(project, script, out)
    print(f"Wrote readable draft: {out}")
    return 0


def command_context(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    scene = resolve_scene_arg(args.scene, project)
    out = resolve_output_arg(args.out)
    context_pack(project, scene, out)
    print(f"Wrote context pack: {out}")
    return 0


def command_scene_brief(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    scene = resolve_scene_arg(args.scene, project)
    out = resolve_output_arg(args.out)
    scene_brief(
        project,
        scene,
        out,
        args.methods,
    )
    print(f"Wrote scene brief: {out}")
    return 0


def command_draft_session(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    scene_path = resolve_scene_arg(args.scene, project)
    out_dir = resolve_output_arg(args.out_dir) if args.out_dir else internal_context_dir(project)
    paths = draft_session(project, scene_path, out_dir, args.methods, args.draft_name)
    for label, path in paths.items():
        print(f"Wrote {label}: {path.resolve()}")
    return 0


def command_paths_list(args: argparse.Namespace) -> int:
    aliases = load_path_aliases()
    for key in sorted(aliases):
        print(f"{key}\t{(WORKBENCH_ROOT / aliases[key]).resolve()}")
    return 0


def command_paths_projects(args: argparse.Namespace) -> int:
    for key, path in project_registry().items():
        print(f"{key}\t{path}")
    return 0


def command_paths_scenes(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    for path in sorted(scene_cards_dir(project).glob("*.json")):
        print(path.name)
    return 0


def command_paths_scripts(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project)
    for path in sorted(generated_csv_dir(project).rglob("*.csv")):
        print(path.name)
    return 0


def command_paths_resolve(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project) if getattr(args, "project", None) else None
    if args.kind == "project":
        path = resolve_project_arg(args.spec)
    elif args.kind == "scene":
        if project is None:
            raise SystemExit("--project is required when kind=scene")
        path = resolve_scene_arg(args.spec, project)
    elif args.kind == "script":
        if project is None:
            raise SystemExit("--project is required when kind=script")
        path = resolve_script_arg(args.spec, project)
    else:
        path = None
        if project is not None:
            try:
                path = resolve_named_file(project, args.spec)
            except SystemExit:
                path = None
        path = path or resolve_generic_readable(args.spec)
        if path is None:
            raise SystemExit(f"Could not resolve path spec: {args.spec}")
    print(path)
    return 0


def command_read(args: argparse.Namespace) -> int:
    project = resolve_project_arg(args.project) if getattr(args, "project", None) else None
    if args.kind == "project":
        path = resolve_project_arg(args.spec)
    elif args.kind == "scene":
        if project is None:
            raise SystemExit("--project is required when kind=scene")
        path = resolve_scene_arg(args.spec, project)
    elif args.kind == "script":
        if project is None:
            raise SystemExit("--project is required when kind=script")
        path = resolve_script_arg(args.spec, project)
    else:
        path = None
        if project is not None:
            try:
                path = resolve_named_file(project, args.spec)
            except SystemExit:
                path = None
        path = path or resolve_generic_readable(args.spec)
        if path is None:
            raise SystemExit(f"Could not resolve readable target: {args.spec}")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(path.read_text(encoding="utf-8"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VN Fusion Workbench")
    sub = parser.add_subparsers(required=True)

    p_paths = sub.add_parser("paths", help="list or resolve ASCII-safe path aliases and project keys")
    p_paths_sub = p_paths.add_subparsers(required=True)

    p_paths_list = p_paths_sub.add_parser("list", help="list path aliases")
    p_paths_list.set_defaults(func=command_paths_list)

    p_paths_projects = p_paths_sub.add_parser("projects", help="list ASCII-safe project keys")
    p_paths_projects.set_defaults(func=command_paths_projects)

    p_paths_scenes = p_paths_sub.add_parser("scenes", help="list scene card filenames for a project key")
    p_paths_scenes.add_argument("--project", required=True, help="project key like P017")
    p_paths_scenes.set_defaults(func=command_paths_scenes)

    p_paths_scripts = p_paths_sub.add_parser("scripts", help="list CSV script filenames for a project key")
    p_paths_scripts.add_argument("--project", required=True, help="project key like P017")
    p_paths_scripts.set_defaults(func=command_paths_scripts)

    p_paths_resolve = p_paths_sub.add_parser("resolve", help="resolve an alias, project key, scene id, or script name")
    p_paths_resolve.add_argument("spec")
    p_paths_resolve.add_argument("--kind", choices=["generic", "project", "scene", "script"], default="generic")
    p_paths_resolve.add_argument("--project", required=False, help="project key like P017 when resolving scene/script names")
    p_paths_resolve.set_defaults(func=command_paths_resolve)

    p_read = sub.add_parser("read", help="read a UTF-8 file through alias/project resolution")
    p_read.add_argument("spec")
    p_read.add_argument("--kind", choices=["generic", "project", "scene", "script"], default="generic")
    p_read.add_argument("--project", required=False, help="project key like P017 when reading scene/script names")
    p_read.set_defaults(func=command_read)

    p_validate = sub.add_parser("validate", help="validate a CSV script")
    p_validate.add_argument("--project", required=True)
    p_validate.add_argument("--script", required=True)
    p_validate.set_defaults(func=command_validate)

    p_context = sub.add_parser("context", help="assemble a scene context pack")
    p_context.add_argument("--project", required=True)
    p_context.add_argument("--scene", required=True)
    p_context.add_argument("--out", required=True)
    p_context.set_defaults(func=command_context)

    p_brief = sub.add_parser("scene-brief", help="assemble a visible method invocation brief before drafting")
    p_brief.add_argument("--project", required=True)
    p_brief.add_argument("--scene", required=True)
    p_brief.add_argument("--out", required=True)
    p_brief.add_argument("--methods", required=False, help="comma-separated method ids; defaults to enabled method cards")
    p_brief.set_defaults(func=command_scene_brief)

    p_session = sub.add_parser("draft-session", help="create a pre-draft invocation bundle with brief, context, manifest, and output contract")
    p_session.add_argument("--project", required=True)
    p_session.add_argument("--scene", required=True)
    p_session.add_argument("--out-dir", required=False)
    p_session.add_argument("--methods", required=False, help="comma-separated method ids; defaults to enabled method cards")
    p_session.add_argument("--draft-name", required=False, help="base filename for intended script/export artifacts")
    p_session.set_defaults(func=command_draft_session)

    p_webgal = sub.add_parser("export-webgal", help="export CSV script to WebGAL .txt")
    p_webgal.add_argument("--project", required=True)
    p_webgal.add_argument("--script", required=True)
    p_webgal.add_argument("--out", required=True)
    p_webgal.set_defaults(func=command_export_webgal)

    p_renpy = sub.add_parser("export-renpy", help="export CSV script to Ren'Py draft")
    p_renpy.add_argument("--project", required=True)
    p_renpy.add_argument("--script", required=True)
    p_renpy.add_argument("--out", required=True)
    p_renpy.set_defaults(func=command_export_renpy)

    p_ink = sub.add_parser("export-ink", help="export CSV script to Ink draft")
    p_ink.add_argument("--project", required=True)
    p_ink.add_argument("--script", required=True)
    p_ink.add_argument("--out", required=True)
    p_ink.set_defaults(func=command_export_ink)

    p_yarn = sub.add_parser("export-yarn", help="export CSV script to Yarn Spinner draft")
    p_yarn.add_argument("--project", required=True)
    p_yarn.add_argument("--script", required=True)
    p_yarn.add_argument("--out", required=True)
    p_yarn.set_defaults(func=command_export_yarn)

    p_godot = sub.add_parser("export-godot-dialogue", help="export CSV script to Godot Dialogue Manager draft")
    p_godot.add_argument("--project", required=True)
    p_godot.add_argument("--script", required=True)
    p_godot.add_argument("--out", required=True)
    p_godot.set_defaults(func=command_export_godot_dialogue)

    p_card = sub.add_parser("export-character-card-v2", help="export project character cards as TavernAI/Character Card V2 JSON")
    p_card.add_argument("--project", required=True)
    p_card.add_argument("--out-dir", required=True)
    p_card.set_defaults(func=command_export_character_card_v2)

    p_char_brief = sub.add_parser("character-brief", help="render project character settings as user-visible Markdown memory points")
    p_char_brief.add_argument("--project", required=True)
    p_char_brief.add_argument("--out", required=True)
    p_char_brief.set_defaults(func=command_character_brief)

    p_readable = sub.add_parser("render-readable", help="render CSV script to a human-readable Galgame Markdown preview")
    p_readable.add_argument("--project", required=True)
    p_readable.add_argument("--script", required=True)
    p_readable.add_argument("--out", required=True)
    p_readable.set_defaults(func=command_render_readable)

    p_deep = sub.add_parser("deep-audit", help="run graph/ref/state/character-control audit on a CSV script")
    p_deep.add_argument("--project", required=True)
    p_deep.add_argument("--script", required=True)
    p_deep.add_argument("--out", required=False)
    p_deep.set_defaults(func=command_deep_audit)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
