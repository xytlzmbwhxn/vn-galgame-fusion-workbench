# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = WORKBENCH_ROOT.parent
PROJECTS_ROOT = WORKBENCH_ROOT / "02_projects"

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


def newest_or_largest_readable(project: Path) -> Path:
    delivery_dirs = [p for p in project.iterdir() if p.is_dir() and p.name.startswith("05_")]
    candidates: list[Path] = []
    for delivery in delivery_dirs:
        candidates.extend(delivery.rglob("*.md"))
    if not candidates:
        raise SystemExit(f"No readable Markdown found under delivery dir: {project}")
    # The latest accepted user-facing draft is usually the largest current readable
    # after iterative rewrites. This avoids hard-coding Chinese filenames.
    return sorted(candidates, key=lambda p: (p.stat().st_mtime, p.stat().st_size), reverse=True)[0]


def load_character_names(project: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    cards = project / "00_project_memory" / "cards" / "characters"
    for path in cards.glob("*.json"):
        text = path.read_text(encoding="utf-8-sig")
        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', text)
        cid_match = re.search(r'"id"\s*:\s*"([^"]+)"', text)
        if name_match and cid_match:
            out[name_match.group(1)] = cid_match.group(1)
    return out


def parse_effects(raw: str) -> str:
    raw = raw.strip()
    if not raw.startswith("[") or not raw.endswith("]"):
        return ""
    return raw[1:-1].strip()


def row(scene_id: str, beat: str, row_type: str, **values: str) -> dict[str, str]:
    data = {key: "" for key in HEADERS}
    data["scene_id"] = scene_id
    data["beat_id"] = beat
    data["row_type"] = row_type
    data.update({key: str(value) for key, value in values.items()})
    return data


def parse_readable(path: Path, project: Path, scene_id: str) -> list[dict[str, str]]:
    names = load_character_names(project)
    rows: list[dict[str, str]] = []
    seq = 1
    current_choice = ""

    def beat() -> str:
        nonlocal seq
        value = f"{scene_id}_delivery_{seq:04d}"
        seq += 1
        return value

    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("默认视角"):
            continue
        if re.fullmatch(r"\d{1,4}", line):
            continue

        if line.startswith("@label "):
            label = line.split(maxsplit=1)[1].strip()
            rows.append(row(scene_id, beat(), "command", text=f"label:{label}", qa_notes=f"source={path.name}"))
            continue
        if line.startswith("@merge "):
            label = line.split(maxsplit=1)[1].strip()
            rows.append(row(scene_id, beat(), "command", text=f"label:{label}", qa_notes=f"source={path.name}; merge_rejoin"))
            continue
        if line.startswith("@jump "):
            label = line.split(maxsplit=1)[1].strip()
            rows.append(row(scene_id, beat(), "command", text=f"jumpLabel:{label}", qa_notes=f"source={path.name}"))
            continue
        if line.startswith("@ending "):
            rows.append(row(scene_id, beat(), "command", text="end", effects=line.split(maxsplit=1)[1].strip(), qa_notes=f"source={path.name}"))
            continue
        if line.startswith("@choice "):
            parts = line.split(maxsplit=2)
            current_choice = parts[1] if len(parts) > 1 else f"{scene_id}_CHOICE"
            rows.append(row(scene_id, beat(), "comment", text=line, qa_notes=f"source={path.name}; choice_marker"))
            continue
        if line.startswith("@option "):
            payload = line[len("@option ") :]
            match = re.match(r"(.+?)\s*->\s*([^\s\[]+)\s*(\[.*\])?$", payload)
            if not match:
                rows.append(row(scene_id, beat(), "comment", text=line, qa_notes=f"source={path.name}; unparsed_option"))
                continue
            choice_text = match.group(1).strip()
            target = match.group(2).strip()
            effects = parse_effects(match.group(3) or "")
            rows.append(
                row(
                    scene_id,
                    beat(),
                    "choice",
                    text=choice_text,
                    choice_group=current_choice or f"{scene_id}_CHOICE",
                    choice_text=choice_text,
                    choice_target=target,
                    effects=effects,
                    qa_notes=f"source={path.name}; click_function=branch_state",
                )
            )
            continue

        dialogue = re.match(r"^【([^】]+)】『(.*)』$", line)
        if dialogue:
            display_name, text = dialogue.groups()
            cid = names.get(display_name, display_name)
            rows.append(
                row(
                    scene_id,
                    beat(),
                    "dialogue",
                    speaker=cid,
                    text=text,
                    memory_refs=cid,
                    qa_notes=f"source={path.name}; click_function=reply_pressure",
                )
            )
            continue

        if line.startswith("（") and line.endswith("）"):
            rows.append(
                row(
                    scene_id,
                    beat(),
                    "thought",
                    speaker="CHR_gu_huai",
                    text=line[1:-1],
                    memory_refs="CHR_gu_huai",
                    qa_notes=f"source={path.name}; click_function=private_inference_or_relaxation",
                )
            )
            continue

        rows.append(row(scene_id, beat(), "narration", text=line, qa_notes=f"source={path.name}; click_function=screen_state"))

    if not rows or not rows[0]["text"].startswith("label:"):
        rows.insert(0, row(scene_id, f"{scene_id}_delivery_0000", "command", text=f"label:{scene_id}_START", qa_notes=f"source={path.name}; inserted_start_label"))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a readable Gal preview Markdown file into workbench CSV rows.")
    parser.add_argument("--project", required=True, help="Project key such as P018.")
    parser.add_argument("--input", help="Readable Markdown path. If omitted, use newest/largest delivery Markdown.")
    parser.add_argument("--scene-id", default="S001")
    parser.add_argument("--out", help="Output CSV path. If omitted, writes under 02_generated_content/scripts/csv.")
    args = parser.parse_args()

    project = resolve_project(args.project)
    source = Path(args.input) if args.input else newest_or_largest_readable(project)
    if not source.is_absolute():
        source = (Path.cwd() / source).resolve()
    if not source.exists():
        raise SystemExit(f"Input not found: {source}")

    out = Path(args.out) if args.out else project / "02_generated_content" / "scripts" / "csv" / f"{source.stem}.csv"
    if not out.is_absolute():
        out = (Path.cwd() / out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    rows = parse_readable(source, project, args.scene_id)
    with out.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote CSV: {out}")
    print(f"rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
