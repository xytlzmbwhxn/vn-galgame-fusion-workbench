# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = WORKBENCH_ROOT.parent
PROJECTS_ROOT = WORKBENCH_ROOT / "02_projects"


def resolve_project(project_key: str) -> Path:
    if project_key.startswith("P") and project_key[1:].isdigit():
        prefix = f"{int(project_key[1:]):03d}_"
    else:
        prefix = project_key
    matches = [p for p in PROJECTS_ROOT.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not matches:
        raise SystemExit(f"Project not found: {project_key}")
    if len(matches) > 1:
        raise SystemExit(f"Project key is ambiguous: {project_key} -> {[m.name for m in matches]}")
    return matches[0]


def first_dir(parent: Path, prefix: str) -> Path | None:
    if not parent.exists():
        return None
    matches = [p for p in parent.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    return matches[0] if matches else None


def files(root: Path | None, pattern: str = "*") -> list[Path]:
    if not root or not root.exists():
        return []
    return [p for p in root.rglob(pattern) if p.is_file()]


def count_by_suffix(root: Path | None, suffix: str) -> int:
    return len([p for p in files(root) if p.name.lower().endswith(suffix.lower())])


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a VN project has a complete handoff delivery package.")
    parser.add_argument("--project", required=True, help="Project key such as P018.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if required delivery layers are missing.")
    args = parser.parse_args()

    project = resolve_project(args.project)
    delivery = first_dir(project, "05_")
    generated = project / "02_generated_content"
    internal = first_dir(project, "99_")

    character_cards = files(project / "00_project_memory" / "cards" / "characters", "*.json")
    runtime_states = files(project / "00_project_memory" / "runtime_state" / "characters", "*.json")
    character_memories = files(project / "00_project_memory" / "memory_logs" / "character_memory", "*.md")
    scene_cards = files(project / "01_narrative_design" / "scenes" / "scene_cards", "*.json")
    state_deltas = files(project / "01_narrative_design" / "scenes" / "state_deltas", "*.json")
    route_maps = files(project / "01_narrative_design" / "routes", "*.json")

    delivery_files = files(delivery)
    generated_csv = files(generated / "scripts" / "csv", "*.csv")
    generated_readable = files(generated / "drafts" / "readable", "*.md") + files(generated / "可读剧本", "*.md")
    qa_reports = files(internal / "质检报告" / "当前", "*.md") + files(internal / "质检报告" / "当前", "*.json") if internal else []

    counts = {
        "character_cards": len(character_cards),
        "runtime_states": len(runtime_states),
        "character_memories": len(character_memories),
        "scene_cards": len(scene_cards),
        "state_deltas": len(state_deltas),
        "route_maps": len(route_maps),
        "generated_csv": len(generated_csv),
        "generated_readable": len(generated_readable),
        "delivery_files": len(delivery_files),
        "delivery_readable_md": count_by_suffix(delivery, ".md"),
        "delivery_csv": count_by_suffix(delivery, ".csv"),
        "delivery_excel": count_by_suffix(delivery, ".xlsx"),
        "delivery_webgal": count_by_suffix(delivery, ".txt"),
        "delivery_renpy": count_by_suffix(delivery, ".rpy"),
        "delivery_ink": count_by_suffix(delivery, ".ink"),
        "delivery_yarn": count_by_suffix(delivery, ".yarn"),
        "delivery_godot_dialogue": count_by_suffix(delivery, ".dialogue"),
        "delivery_character_card_v2": len([p for p in delivery_files if p.name.endswith(".card_v2.json")]),
        "qa_reports": len(qa_reports),
    }

    errors: list[str] = []
    warnings: list[str] = []
    required_positive = [
        ("character_cards", "missing stable character cards"),
        ("runtime_states", "missing runtime character states for handoff continuity"),
        ("character_memories", "missing retrievable character memory logs"),
        ("scene_cards", "missing scene card"),
        ("state_deltas", "missing state delta for branch/memory handoff"),
        ("route_maps", "missing route map"),
        ("generated_csv", "missing generated source CSV under 02_generated_content/scripts/csv"),
        ("generated_readable", "missing generated readable source under 02_generated_content"),
        ("delivery_readable_md", "missing public readable Markdown under 05_ delivery"),
        ("delivery_csv", "missing public delivery CSV"),
        ("delivery_excel", "missing public delivery Excel"),
        ("delivery_webgal", "missing WebGAL export"),
        ("delivery_renpy", "missing Ren'Py export"),
        ("delivery_ink", "missing Ink export"),
        ("delivery_yarn", "missing Yarn export"),
        ("delivery_godot_dialogue", "missing Godot Dialogue export"),
        ("delivery_character_card_v2", "missing Character Card V2 delivery export"),
        ("qa_reports", "missing QA/deep audit/quality debt reports"),
    ]
    for key, message in required_positive:
        if counts[key] <= 0:
            errors.append(f"{key}: {message}")

    if counts["runtime_states"] and counts["runtime_states"] < counts["character_cards"]:
        warnings.append("runtime_states fewer than character_cards")
    if counts["character_memories"] and counts["character_memories"] < counts["character_cards"]:
        warnings.append("character_memories fewer than character_cards")
    if counts["delivery_character_card_v2"] and counts["delivery_character_card_v2"] < counts["character_cards"]:
        warnings.append("delivery Character Card V2 exports fewer than character_cards")

    payload = {
        "project": project.name,
        "ok": not errors,
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
