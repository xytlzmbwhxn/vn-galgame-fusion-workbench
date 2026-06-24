#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VN Workbench cleanup helper.

This tool keeps the workbench small after generation runs by removing only
clearly-rebuildable or internal intermediate files. It intentionally protects
canon, generated source scripts, user-facing delivery files, method cards, and
learned/style assets.

Typical use from vn_fusion_workbench:

    py .\00_workbench_core\tools\vn_workspace_cleanup.py --audit
    py .\00_workbench_core\tools\vn_workspace_cleanup.py --clean
    py .\00_workbench_core\tools\vn_workspace_cleanup.py --post-generation

The root node_modules directory is kept by default because this workbench does
not currently include a package.json / lockfile that can rebuild it reliably.
Project-internal node_modules folders are treated as disposable intermediates.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = WORKBENCH_ROOT.parent

CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}

PROTECTED_PARTS = {
    "00_project_memory",
    "01_narrative_design",
    "02_generated_content",
    "05_交付文件",
    "methods",
    "docs",
    "portable_skills",
    "schemas",
    "templates",
    "06_学习输入",
}

INTERNAL_ARTIFACT_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".log",
    ".tmp",
    ".bak",
}

INTERNAL_ARTIFACT_NAME_MARKERS = {
    ".inspect.ndjson",
    "_excel_preview",
    "screenshot",
    "截图",
}


@dataclass
class Candidate:
    kind: str
    path: str
    mb: float
    files: int
    reason: str


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(WORKBENCH_ROOT)).replace("\\", "/")


def assert_inside_workbench(path: Path) -> None:
    resolved = path.resolve()
    root = WORKBENCH_ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise RuntimeError(f"Refusing to touch outside workbench: {resolved}")


def file_count_and_bytes(path: Path) -> tuple[int, int]:
    if path.is_file():
        return 1, path.stat().st_size
    count = 0
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            count += 1
            try:
                total += item.stat().st_size
            except OSError:
                pass
    return count, total


def make_candidate(kind: str, path: Path, reason: str) -> Candidate:
    files, total = file_count_and_bytes(path)
    return Candidate(
        kind=kind,
        path=rel(path),
        mb=round(total / 1024 / 1024, 3),
        files=files,
        reason=reason,
    )


def is_protected(path: Path) -> bool:
    parts = set(path.relative_to(WORKBENCH_ROOT).parts)
    return bool(parts & PROTECTED_PARTS)


def find_safe_candidates(include_internal_artifacts: bool = False) -> list[Candidate]:
    candidates: list[Candidate] = []

    for path in WORKBENCH_ROOT.rglob("*"):
        if not path.is_dir():
            continue

        if path.name in CACHE_DIR_NAMES:
            candidates.append(make_candidate("cache", path, "Python/tool cache; rebuildable."))
            continue

        if path.name == "node_modules":
            parts = path.relative_to(WORKBENCH_ROOT).parts
            if parts == ("node_modules",):
                continue
            if "02_projects" in parts and "99_内部工作" in parts:
                candidates.append(
                    make_candidate(
                        "project_internal_node_modules",
                        path,
                        "Project-internal dependency snapshot; root node_modules is kept instead.",
                    )
                )
            continue

        parts = path.relative_to(WORKBENCH_ROOT).parts
        if len(parts) >= 4 and parts[0] == "02_projects" and "99_内部工作" in parts:
            if path.name in {"表格构建", "excel_build", "screenshots", "截图"}:
                candidates.append(
                    make_candidate(
                        "project_internal_workspace",
                        path,
                        "One-off internal build/screenshot workspace; deliverables live elsewhere.",
                    )
                )

    for path in WORKBENCH_ROOT.rglob("*.inspect.ndjson"):
        if not path.is_file():
            continue
        parts = path.relative_to(WORKBENCH_ROOT).parts
        if "02_projects" in parts and "02_generated_content" in parts:
            candidates.append(
                make_candidate(
                    "generated_inspect_artifact",
                    path,
                    "Spreadsheet inspect trace; rebuildable and not a delivery artifact.",
                )
            )

    if include_internal_artifacts:
        for path in WORKBENCH_ROOT.rglob("*"):
            if not path.is_file():
                continue
            parts = path.relative_to(WORKBENCH_ROOT).parts
            if not ("02_projects" in parts and "99_内部工作" in parts):
                continue
            name = path.name.lower()
            if path.suffix.lower() in INTERNAL_ARTIFACT_SUFFIXES or any(marker in name for marker in INTERNAL_ARTIFACT_NAME_MARKERS):
                if not is_protected(path):
                    candidates.append(
                        make_candidate(
                            "project_internal_artifact",
                            path,
                            "Internal log/screenshot/inspect artifact.",
                        )
                    )

    # Deduplicate nested candidates by keeping the higher-level path.
    candidates.sort(key=lambda c: (c.path.count("/"), c.path))
    kept: list[Candidate] = []
    kept_paths: list[Path] = []
    for candidate in candidates:
        abs_path = WORKBENCH_ROOT / candidate.path
        if any(parent == abs_path or parent in abs_path.parents for parent in kept_paths):
            continue
        kept.append(candidate)
        kept_paths.append(abs_path)
    return kept


def delete_candidate(candidate: Candidate) -> None:
    path = WORKBENCH_ROOT / candidate.path
    assert_inside_workbench(path)
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def write_report(candidates: Iterable[Candidate], cleaned: bool) -> Path:
    report_dir = WORKBENCH_ROOT / "00_workbench_core" / "runtime" / "cleanup"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"workspace_cleanup_{stamp}.json"
    payload = {
        "timestamp": stamp,
        "workbench_root": str(WORKBENCH_ROOT),
        "cleaned": cleaned,
        "total_mb": round(sum(c.mb for c in candidates), 3),
        "candidates": [asdict(c) for c in candidates],
        "protected": sorted(PROTECTED_PARTS),
        "note": "Root node_modules is intentionally kept unless a rebuild manifest is added.",
    }
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and clean VN Workbench intermediate files.")
    parser.add_argument("--audit", action="store_true", help="Only list cleanup candidates.")
    parser.add_argument("--clean", action="store_true", help="Delete safe cleanup candidates.")
    parser.add_argument(
        "--post-generation",
        action="store_true",
        help="Alias for --clean after a generation run; keeps canon/deliverables.",
    )
    parser.add_argument(
        "--include-internal-artifacts",
        action="store_true",
        help="Also remove internal logs/screenshots/inspect files under project 99_内部工作.",
    )
    args = parser.parse_args()

    if not (args.audit or args.clean or args.post_generation):
        args.audit = True

    candidates = find_safe_candidates(include_internal_artifacts=args.include_internal_artifacts)
    should_clean = args.clean or args.post_generation

    if should_clean:
        for candidate in candidates:
            delete_candidate(candidate)

    report_path = write_report(candidates, cleaned=should_clean)
    total_mb = round(sum(c.mb for c in candidates), 3)

    print(json.dumps({
        "mode": "clean" if should_clean else "audit",
        "candidate_count": len(candidates),
        "total_mb": total_mb,
        "report": rel(report_path),
        "candidates": [asdict(c) for c in candidates],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
