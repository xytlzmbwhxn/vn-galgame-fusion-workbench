#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a dependency-free XLSX delivery workbook for a VN workbench project.

This is the public-repo fallback for environments where ``node_modules`` is
ignored or unavailable. It uses only the Python standard library and writes a
plain but valid .xlsx file containing the script, character memory, scene card,
state delta, route map, and build notes.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HEADERS = [
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


def resolve_project(project_arg: str) -> Path:
    project = Path(project_arg)
    if project.is_absolute():
        return project
    if project_arg.startswith("P") and project_arg[1:].isdigit():
        prefix = f"{int(project_arg[1:]):03d}_"
        matches = sorted(p for p in (WORKBENCH_ROOT / "02_projects").iterdir() if p.is_dir() and p.name.startswith(prefix))
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise SystemExit(f"Project key is ambiguous: {project_arg} -> {[p.name for p in matches]}")
    return WORKBENCH_ROOT / "02_projects" / project_arg


def resolve_script(project: Path, script_arg: str | None) -> Path:
    script_dir = project / "02_generated_content" / "scripts" / "csv"
    if script_arg:
        candidate = Path(script_arg)
        if candidate.is_absolute():
            return candidate
        if candidate.exists():
            return candidate
        return script_dir / script_arg
    candidates = sorted(script_dir.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No CSV scripts found under {script_dir}")
    return candidates[0]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(row) for row in reader]
        fieldnames = list(reader.fieldnames or DEFAULT_HEADERS)
    if not rows:
        return []
    return [{key: row.get(key, "") or "" for key in fieldnames} for row in rows]


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def flatten(value: Any, prefix: str = "") -> list[list[str]]:
    rows: list[list[str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{prefix}.{key}" if prefix else str(key)
            rows.extend(flatten(item, child))
    elif isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            rows.append([prefix, " | ".join("" if item is None else str(item) for item in value)])
        else:
            for idx, item in enumerate(value):
                rows.extend(flatten(item, f"{prefix}[{idx}]"))
    else:
        rows.append([prefix, "" if value is None else str(value)])
    return rows


def dict_rows_to_table(rows: list[dict[str, str]]) -> list[list[str]]:
    if not rows:
        return [DEFAULT_HEADERS]
    headers = list(rows[0].keys())
    return [headers] + [[row.get(header, "") for header in headers] for row in rows]


def json_files_table(title: str, files: list[Path]) -> list[list[str]]:
    table = [["section", "file", "key", "value"]]
    for file in files:
        data = read_json(file)
        if data is None:
            continue
        for key, value in flatten(data):
            table.append([title, file.name, key, value])
    if len(table) == 1:
        table.append([title, "(none)", "", ""])
    return table


def safe_sheet_name(name: str, used: set[str]) -> str:
    base = re.sub(r"[\[\]\:\*\?\/\\]", "_", name).strip() or "Sheet"
    base = base[:31]
    candidate = base
    idx = 2
    while candidate in used:
        suffix = f"_{idx}"
        candidate = f"{base[:31 - len(suffix)]}{suffix}"
        idx += 1
    used.add(candidate)
    return candidate


def cell_ref(col: int, row: int) -> str:
    letters = ""
    n = col
    while n:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row}"


def clean_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    text = "".join(ch for ch in text if ch == "\t" or ch == "\n" or ch == "\r" or ord(ch) >= 32)
    return text[:32767]


def worksheet_xml(rows: list[list[Any]]) -> str:
    xml_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            text = clean_cell(value)
            ref = cell_ref(c_idx, r_idx)
            cells.append(
                f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(text)}</t></is></c>'
            )
        xml_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        "</worksheet>"
    )


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = "".join(
        f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        for idx, name in enumerate(sheet_names, start=1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{sheets}</sheets>"
        "</workbook>"
    )


def workbook_rels(sheet_count: int) -> str:
    rels = [
        f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        for idx in range(1, sheet_count + 1)
    ]
    rels.append(
        f'<Relationship Id="rId{sheet_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(rels)}'
        "</Relationships>"
    )


def content_types(sheet_count: int) -> str:
    sheets = "".join(
        f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for idx in range(1, sheet_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        f"{sheets}"
        "</Types>"
    )


def styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        "</styleSheet>"
    )


def package_rels() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )


def core_props() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:creator>VN Workbench</dc:creator>"
        "<cp:lastModifiedBy>VN Workbench</cp:lastModifiedBy>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "</cp:coreProperties>"
    )


def app_props(sheet_names: list[str]) -> str:
    titles = "".join(f"<vt:lpstr>{escape(name)}</vt:lpstr>" for name in sheet_names)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>VN Workbench</Application>"
        f'<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{len(sheet_names)}</vt:i4></vt:variant></vt:vector></HeadingPairs>'
        f'<TitlesOfParts><vt:vector size="{len(sheet_names)}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>'
        "</Properties>"
    )


def write_xlsx(out_path: Path, sheets: list[tuple[str, list[list[Any]]]]) -> None:
    used: set[str] = set()
    named_sheets = [(safe_sheet_name(name, used), rows) for name, rows in sheets]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types(len(named_sheets)))
        zf.writestr("_rels/.rels", package_rels())
        zf.writestr("docProps/core.xml", core_props())
        zf.writestr("docProps/app.xml", app_props([name for name, _ in named_sheets]))
        zf.writestr("xl/workbook.xml", workbook_xml([name for name, _ in named_sheets]))
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels(len(named_sheets)))
        zf.writestr("xl/styles.xml", styles_xml())
        for idx, (_, rows) in enumerate(named_sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", worksheet_xml(rows))


def build(project: Path, script: Path, out_path: Path | None) -> Path:
    rows = read_csv_rows(script)
    scene_id = rows[0].get("scene_id", script.stem) if rows else script.stem
    out = out_path or project / "02_generated_content" / "scripts" / "excel" / f"{script.stem}.xlsx"

    character_files = sorted((project / "00_project_memory" / "cards" / "characters").glob("*.json"))
    runtime_files = sorted((project / "00_project_memory" / "runtime_state" / "characters").glob("*.json"))
    scene_card = project / "01_narrative_design" / "scenes" / "scene_cards" / f"{scene_id}_scene_card.json"
    state_delta = project / "01_narrative_design" / "scenes" / "state_deltas" / f"{scene_id}_state_delta.json"
    route_map = project / "01_narrative_design" / "routes" / "route_map.json"

    notes = [
        ["key", "value"],
        ["project", str(project)],
        ["script", str(script)],
        ["scene_id", scene_id],
        ["generated_at", datetime.now().isoformat(timespec="seconds")],
        ["builder", "build_excel_template_py.py"],
        ["dependency_note", "Python standard library only; safe for public clones without node_modules."],
    ]

    sheets: list[tuple[str, list[list[Any]]]] = [
        ("script_csv", dict_rows_to_table(rows)),
        ("characters", json_files_table("character_card", character_files)),
        ("runtime_state", json_files_table("runtime_state", runtime_files)),
        ("scene_card", [["key", "value"]] + flatten(read_json(scene_card) or {})),
        ("state_delta", [["key", "value"]] + flatten(read_json(state_delta) or {})),
        ("route_map", [["key", "value"]] + flatten(read_json(route_map) or {})),
        ("build_notes", notes),
    ]
    write_xlsx(out, sheets)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Build dependency-free VN delivery XLSX.")
    parser.add_argument("project", help="Project id such as P020 or an absolute project path.")
    parser.add_argument("script", nargs="?", help="CSV filename/path. Defaults to newest generated CSV.")
    parser.add_argument("--out", help="Optional output .xlsx path.")
    args = parser.parse_args()

    project = resolve_project(args.project).resolve()
    script = resolve_script(project, args.script).resolve()
    out_path = Path(args.out).resolve() if args.out else None
    out = build(project, script, out_path)
    print(json.dumps({"ok": True, "out": str(out), "project": str(project), "script": str(script)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
