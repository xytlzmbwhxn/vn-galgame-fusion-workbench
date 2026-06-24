# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
RUNTIME = ROOT / "00_workbench_core" / "runtime"
RECEIPT = RUNTIME / "last_context_bootstrap.json"


PRIVATE_DIR_NAME = "_local"
PRIVATE_STYLE_ROOT = ROOT / "06_学习输入" / "_风格画像" / PRIVATE_DIR_NAME
PUBLIC_STYLE_ROOT = ROOT / "06_学习输入" / "_风格画像"


def first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None

CORE_FILES = [
    PROJECT / "START_HERE.md",
    PROJECT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "CURRENT_TASK_STATE.md",
    PROJECT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "WORKBENCH_OPERATING_RULES.md",
    PROJECT / "AI_HANDOFF_PACKAGE" / "handoff_notes" / "OTHER_AI_FAILURE_PREVENTION.md",
    ROOT / "00_workbench_core" / "portable_skills" / "portable_skill_manifest.json",
    ROOT / "00_workbench_core" / "methods" / "chinese_vn_generation_hard_gates.md",
    ROOT / "00_workbench_core" / "methods" / "spoken_private_thought_texture.md",
    ROOT / "00_workbench_core" / "methods" / "interior_breath_relaxation.md",
    ROOT / "00_workbench_core" / "methods" / "complete_delivery_package_contract.md",
    ROOT / "00_workbench_core" / "methods" / "dialogue_block_ownership.md",
    ROOT / "00_workbench_core" / "methods" / "vn_style_handprint_fusion.md",
]

OPTIONAL_STYLE_FILES = [
    first_existing(
        PUBLIC_STYLE_ROOT / "VN文风手印融合资产_20260623.md",
        PRIVATE_STYLE_ROOT / "VN文风手印融合资产_20260623.md",
    ),
    first_existing(
        PUBLIC_STYLE_ROOT / "style_profile_cn_gal_tutorial_lessons_20260623.md",
        PRIVATE_STYLE_ROOT / "PRIVATE_SENTENCE_MOVES.md",
    ),
    first_existing(
        PUBLIC_STYLE_ROOT / "vn_style_handprint_fusion_20260623.json",
        PRIVATE_STYLE_ROOT / "vn_style_handprint_fusion_20260623.json",
    ),
]

PORTABLE_SKILL_MANIFEST = ROOT / "00_workbench_core" / "portable_skills" / "portable_skill_manifest.json"


def mandatory_portable_skill_files() -> list[Path]:
    """Load every VN/Gal portable skill from the workbench backup.

    This intentionally avoids host-level Codex / CC Switch skill paths. The
    workbench portable skills are the stable source for every new conversation
    and handoff.
    """
    try:
        data = json.loads(PORTABLE_SKILL_MANIFEST.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    files: list[Path] = []
    for skill in data.get("skills", []):
        skill_id = str(skill.get("id", ""))
        if not (skill_id.startswith("vn") or skill_id.startswith("gal")):
            continue
        rel = skill.get("file")
        if rel:
            files.append(ROOT / "00_workbench_core" / "portable_skills" / rel)
    return files


def read_preview(path: Path, limit: int = 1200) -> str:
    try:
        text = path.read_text(encoding="utf-8")
        return text[:limit]
    except Exception as exc:
        return f"READ_ERROR: {exc}"


def resolve_project(project_key: str | None) -> Path | None:
    if not project_key:
        return None
    projects = ROOT / "02_projects"
    if not projects.exists():
        return None
    if project_key.startswith("P") and project_key[1:].isdigit():
        suffix = project_key[1:].lstrip("0") or "0"
        candidates = []
        for p in projects.iterdir():
            if p.is_dir():
                name = p.name
                if name.startswith(project_key[1:] + "_") or name.startswith(suffix.zfill(3) + "_"):
                    candidates.append(p)
        return sorted(candidates)[-1] if candidates else None
    direct = projects / project_key
    return direct if direct.exists() else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Load and record mandatory VN workbench context.")
    parser.add_argument("--project", default=None, help="Project key such as P018.")
    parser.add_argument("--task", default="draft", help="draft/rewrite/review/learning")
    args = parser.parse_args()

    RUNTIME.mkdir(parents=True, exist_ok=True)

    project_path = resolve_project(args.project)
    project_files = []
    if project_path:
        for rel in [
            "00_project_memory/cards/characters",
            "00_project_memory/runtime_state/characters",
            "00_project_memory/memory_logs/character_memory",
            "01_narrative_design/routes/route_map.json",
        ]:
            p = project_path / rel
            if p.is_dir():
                project_files.extend(sorted([x for x in p.rglob("*") if x.is_file()])[:20])
            elif p.exists():
                project_files.append(p)

    portable_skill_files = mandatory_portable_skill_files()
    optional_style_files = [p for p in OPTIONAL_STYLE_FILES if p is not None and p.exists()]
    required = CORE_FILES + portable_skill_files + project_files
    load_targets = required + optional_style_files
    missing = [str(p) for p in required if not p.exists()]
    loaded = []
    for p in load_targets:
        if p.exists():
            loaded.append({
                "path": str(p),
                "size": p.stat().st_size,
                "preview": read_preview(p),
            })

    receipt = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project": args.project,
        "project_path": str(project_path) if project_path else None,
        "task": args.task,
        "missing": missing,
        "loaded_count": len(loaded),
        "loaded": loaded,
        "optional_style_assets": [
            str(p) for p in optional_style_files
        ],
        "mandatory_portable_skills": [
            str(p) for p in portable_skill_files
        ],
        "required_principles": [
            "Start from character truth, not bans.",
            "Use dialogue ownership plan; avoid long pure ping-pong.",
            "Thought rows must use viewpoint character private voice.",
            "Run vn_handoff_guard.py before user-facing delivery.",
            "Reply to user in Chinese unless asked otherwise.",
        ],
    }

    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")

    print("# VN Context Bootstrap")
    print(f"- receipt: {RECEIPT}")
    print(f"- loaded_count: {len(loaded)}")
    print(f"- missing_count: {len(missing)}")
    if project_path:
        print(f"- project_path: {project_path}")
    if missing:
        print("ERROR missing required context:")
        for item in missing:
            print("- " + item)
        return 1

    print("BOOTSTRAP_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
