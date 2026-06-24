#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check that required VN/workbench skills are usable and backed up for handoff.

Public clones should not require the private host-level skill snapshot. The
handoff guarantee is:

1. the visible top-level ``skills/`` directory;
2. the workbench copy under ``00_workbench_core/portable_skills``;
3. the mirror under ``AI_HANDOFF_PACKAGE/portable_skills``.
"""

from __future__ import annotations

import json
from pathlib import Path


WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = WORKBENCH_ROOT.parent
HOST_SKILL_ROOTS = [
    Path.home() / ".cc-switch" / "skills",
    Path.home() / ".codex" / "skills",
]

SCREEN_SKILLS = {
    "galgame-workbench-loader": ["galgame-workbench-loader"],
    "game-gdd-excel-shape-sanitized": ["game-gdd-excel-shape-sanitized", "GDDskill"],
    "unity-skills": ["unity-skills"],
    "vn-character-memory": ["vn-character-memory"],
    "vn-fusion-writer": ["vn-fusion-writer"],
    "vn-presence-revision": ["vn-presence-revision"],
    "vn-scene-drafting": ["vn-scene-drafting"],
}

PORTABLE_REQUIRED = {
    "galgame-workbench-loader",
    "vn-character-memory",
    "vn-fusion-writer",
    "vn-presence-revision",
    "vn-scene-drafting",
}


def find_dir(roots: list[Path], aliases: list[str]) -> Path | None:
    for root in roots:
        if not root.exists():
            continue
        for alias in aliases:
            direct = root / alias
            if direct.exists():
                return direct
        for path in root.rglob("*"):
            if path.is_dir() and path.name in aliases:
                return path
    return None


def has_readable_skill(path: Path | None) -> bool:
    if not path:
        return False
    skill = path / "SKILL.md"
    if not skill.exists():
        return False
    try:
        text = skill.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = skill.read_text(encoding="utf-8", errors="replace")
    return bool(text.strip())


def manifest_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return {item.get("id", "") for item in data.get("skills", [])}


def main() -> int:
    top_level_skills = PROJECT_ROOT / "skills"
    core_portable = WORKBENCH_ROOT / "00_workbench_core" / "portable_skills"
    handoff_portable = PROJECT_ROOT / "AI_HANDOFF_PACKAGE" / "portable_skills"
    snapshot = PROJECT_ROOT / "AI_HANDOFF_PACKAGE" / "skills_snapshot" / "cc_switch_skills"

    top_manifest = manifest_ids(top_level_skills / "portable_skill_manifest.json")
    core_manifest = manifest_ids(core_portable / "portable_skill_manifest.json")
    handoff_manifest = manifest_ids(handoff_portable / "portable_skill_manifest.json")

    rows = []
    for skill_id, aliases in SCREEN_SKILLS.items():
        host = find_dir(HOST_SKILL_ROOTS, aliases)
        snapshot_dir = find_dir([snapshot], [skill_id] + aliases)
        top_dir = top_level_skills / skill_id
        core_dir = core_portable / skill_id
        handoff_dir = handoff_portable / skill_id

        rows.append(
            {
                "skill": skill_id,
                "host_readable": has_readable_skill(host),
                "host_path": str(host) if host else None,
                "snapshot_readable": has_readable_skill(snapshot_dir),
                "snapshot_path": str(snapshot_dir) if snapshot_dir else None,
                "portable_required": skill_id in PORTABLE_REQUIRED,
                "top_level_readable": has_readable_skill(top_dir),
                "core_portable_readable": has_readable_skill(core_dir),
                "handoff_portable_readable": has_readable_skill(handoff_dir),
                "top_level_manifest": skill_id in top_manifest,
                "core_manifest": skill_id in core_manifest,
                "handoff_manifest": skill_id in handoff_manifest,
            }
        )

    failures = []
    warnings = []
    for row in rows:
        if not row["host_readable"] and not row["portable_required"]:
            warnings.append(f"{row['skill']}: host skill missing/unreadable on this machine")
        if not row["snapshot_readable"] and not row["portable_required"]:
            warnings.append(f"{row['skill']}: optional host skill has no public portable backup in this VN repository")
        if row["portable_required"]:
            for key in [
                "top_level_readable",
                "core_portable_readable",
                "handoff_portable_readable",
                "top_level_manifest",
                "core_manifest",
                "handoff_manifest",
            ]:
                if not row[key]:
                    failures.append(f"{row['skill']}: {key} failed")

    print(json.dumps({"ok": not failures, "failures": failures, "warnings": warnings, "skills": rows}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
