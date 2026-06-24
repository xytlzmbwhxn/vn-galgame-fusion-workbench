#!/usr/bin/env python3
"""VN Control Room.

File-first control plane for the VN Fusion Workbench.

This tool adapts AI-native workflow ideas into the local visual-novel workbench:
project status projection, command ledger, method/style contract compilation,
context trace, and VN-specific quality debt reporting.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PORTABLE_ROOT = WORKBENCH_ROOT.parent
CORE_DIR = WORKBENCH_ROOT / "00_workbench_core"
PROJECTS_DIR = WORKBENCH_ROOT / "02_projects"
METHOD_INDEX = CORE_DIR / "methods" / "method_index.json"
VN_TOOL = CORE_DIR / "tools" / "vn_workbench.py"
RUNTIME_DIR = CORE_DIR / "runtime"
COMMAND_DIR = RUNTIME_DIR / "commands"
COMMAND_LEDGER = COMMAND_DIR / "command_ledger.jsonl"
PROJECT_KEY_RE = re.compile(r"^(?:P)?(\d{1,3})$")

QUALITY_DEBT_TYPES = {
    "click_unit_low_payload": "点击单位信息量不足",
    "click_unit_overfragmented": "对话被切得过碎",
    "thought_missing": "心理行缺位",
    "thought_misclassified_narration": "把可见叙述误当心理",
    "flat_voice": "角色口吻偏平",
    "punctuation_energy_loss": "标点与语气能量不足",
    "preachy_dialogue": "对白像说明或说教",
    "performance_cue_gap": "演出提示不足",
    "theme_not_playable": "主题没有变成可操作压力",
    "state_unremembered": "选择或信息没有被状态记住",
}

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

VISIBLE_ACTION_WORDS = re.compile(r"(看见|看到|拿起|放下|推开|关上|走到|按下|递给|收进|折起|打印|扫描|贴上|抬头|低头)")
ENERGY_RE = re.compile(r"[?!？！…—]")
CASUAL_RE = re.compile(r"(嘛|啦|欸|诶|哎|呀|吧|哟|呗|喂|哈|拜托|算我求你|好嘛|行吧)")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(WORKBENCH_ROOT.resolve()))
    except Exception:
        return str(path)


def visible_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text or ""))


def project_path(project_id: str) -> Path:
    if not project_id or "/" in project_id or "\\" in project_id or ".." in project_id:
        raise SystemExit(f"Invalid project id: {project_id}")
    key_match = PROJECT_KEY_RE.fullmatch(project_id.strip())
    if key_match:
        prefix = f"{int(key_match.group(1)):03d}_"
        matches = sorted(p for p in PROJECTS_DIR.iterdir() if p.is_dir() and p.name.startswith(prefix)) if PROJECTS_DIR.exists() else []
        if len(matches) == 1:
            return matches[0].resolve()
        if len(matches) > 1:
            match_list = "\n".join(f"- {p}" for p in matches)
            raise SystemExit(f"Ambiguous project key {project_id}:\n{match_list}")
        raise SystemExit(f"Project key not found: {project_id}")
    project = (PROJECTS_DIR / project_id).resolve()
    if not project.exists() or PROJECTS_DIR.resolve() not in project.parents:
        raise SystemExit(f"Project not found: {project_id}")
    return project


def list_files(path: Path, pattern: str) -> list[Path]:
    return sorted(p for p in path.glob(pattern) if p.is_file()) if path.exists() else []


def list_files_recursive(path: Path, pattern: str) -> list[Path]:
    return sorted(p for p in path.rglob(pattern) if p.is_file()) if path.exists() else []


def quality_reports_dir(project: Path) -> Path:
    return project / "99_内部工作" / "质检报告" / "当前"


def quality_reports_root(project: Path) -> Path:
    return project / "99_内部工作" / "质检报告"


def internal_context_dir(project: Path) -> Path:
    return project / "99_内部工作" / "上下文包" / "当前"


def internal_context_root(project: Path) -> Path:
    return project / "99_内部工作" / "上下文包"


def engine_exports_dir(project: Path) -> Path:
    return project / "05_交付文件" / "引擎导出"


def character_exports_dir(project: Path) -> Path:
    return project / "05_交付文件" / "角色设定" / "角色卡导出"


def latest_file(files: list[Path]) -> Path | None:
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def read_csv_rows(script: Path) -> list[dict[str, str]]:
    with script.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            clean = {str(k): (str(v) if v is not None else "").strip() for k, v in row.items() if k is not None}
            if any(clean.values()):
                rows.append(clean)
        return rows


def project_surfaces(project: Path) -> dict[str, list[Path]]:
    return {
        "character_cards": list_files(project / "00_project_memory" / "cards" / "characters", "*.json"),
        "character_states": list_files(project / "00_project_memory" / "runtime_state" / "characters", "*.json"),
        "character_memories": list_files(project / "00_project_memory" / "memory_logs" / "character_memory", "*.md"),
        "scene_cards": list_files(project / "01_narrative_design" / "scenes" / "scene_cards", "*.json"),
        "state_deltas": list_files(project / "01_narrative_design" / "scenes" / "state_deltas", "*.json"),
        "csv_scripts": list_files(project / "02_generated_content" / "scripts" / "csv", "*.csv"),
        "readable_drafts": list_files(project / "02_generated_content" / "drafts" / "readable", "*.md"),
        "excel_scripts": list_files(project / "02_generated_content" / "scripts" / "excel", "*.xlsx"),
        "qa_reports": list_files_recursive(quality_reports_root(project), "*_qa.md") + list_files(project / "04_quality" / "reports", "*_qa.md"),
        "deep_audits": list_files_recursive(quality_reports_root(project), "*_deep_audit.md") + list_files(project / "04_quality" / "reports", "*_deep_audit.md"),
        "context_exports": list_files_recursive(internal_context_root(project), "*") + list_files(project / "03_exports" / "context", "*"),
        "webgal_exports": list_files(engine_exports_dir(project) / "webgal", "*.txt") + list_files(project / "03_exports" / "webgal", "*.txt"),
        "renpy_exports": list_files(engine_exports_dir(project) / "renpy", "*.rpy") + list_files(project / "03_exports" / "renpy", "*.rpy"),
        "ink_exports": list_files(engine_exports_dir(project) / "ink", "*.ink") + list_files(project / "03_exports" / "ink", "*.ink"),
        "yarn_exports": list_files(engine_exports_dir(project) / "yarn", "*.yarn") + list_files(project / "03_exports" / "yarn", "*.yarn"),
        "godot_exports": list_files(engine_exports_dir(project) / "godot_dialogue", "*.dialogue") + list_files(project / "03_exports" / "godot_dialogue", "*.dialogue"),
    }


def recommend_next(status: dict[str, Any]) -> dict[str, str]:
    counts = status["counts"]
    latest = status["latest"]
    if counts["character_cards"] == 0:
        return {
            "action": "prepare_characters",
            "reason": "没有角色卡，不能稳定口吻和长期状态。",
            "command": "character-brief",
        }
    if counts["scene_cards"] == 0:
        return {
            "action": "prepare_scene_card",
            "reason": "没有场景卡，无法形成可审计的场景目标、压力和选择。",
            "command": "create scene card manually, then run draft-session",
        }
    if not any("draft_session" in item for item in status["surfaces"]["context_exports"]):
        return {
            "action": "draft_session",
            "reason": "还没有本轮写作上下文包，不能证明方法卡、角色状态和输出路径被加载。",
            "command": "vn_control_room.py command create --action draft_session",
        }
    if counts["csv_scripts"] == 0:
        return {
            "action": "draft_csv",
            "reason": "还没有 CSV 剧本源，后续 readable、QA 和导出都缺源头。",
            "command": "write CSV under 02_generated_content/scripts/csv",
        }
    if counts["readable_drafts"] == 0:
        return {
            "action": "render_readable",
            "reason": "已有 CSV，但没有给人看的 Gal 可读稿。",
            "command": "vn_control_room.py command create --action render_readable",
        }
    if counts["qa_reports"] == 0:
        return {
            "action": "validate",
            "reason": "已有剧本，但还没有 Gal textbox QA 报告。",
            "command": "vn_control_room.py command create --action validate",
        }
    if counts["deep_audits"] == 0:
        return {
            "action": "deep_audit",
            "reason": "已有普通 QA，但还没有图结构、状态和角色控制审计。",
            "command": "vn_control_room.py command create --action deep_audit",
        }
    if counts["webgal_exports"] == 0 or counts["renpy_exports"] == 0:
        return {
            "action": "export_all",
            "reason": "剧本已经通过基础检查，下一步应生成多引擎交接文件。",
            "command": "vn_control_room.py command create --action export_all",
        }
    if latest.get("quality_debt") is None:
        return {
            "action": "quality_debt",
            "reason": "已有可交付产物，建议补一份 VN 专属质量债务分析。",
            "command": "vn_control_room.py quality-debt",
        }
    return {
        "action": "ready_for_next_scene",
        "reason": "当前项目主要产物已齐，可以继续下一个场景或做人工修订。",
        "command": "create or select next scene card",
    }


def build_status(project: Path) -> dict[str, Any]:
    surfaces = project_surfaces(project)
    method_index = read_json(METHOD_INDEX, {"methods": []})
    latest_quality_debt = latest_file(list_files_recursive(quality_reports_root(project), "*_quality_debt.md") + list_files(project / "04_quality" / "reports", "*_quality_debt.md"))
    latest = {
        key: rel(value) if value else None
        for key, value in {name: latest_file(files) for name, files in surfaces.items()}.items()
    }
    latest["quality_debt"] = rel(latest_quality_debt) if latest_quality_debt else None
    status = {
        "project_id": project.name,
        "project_path": rel(project),
        "generated_at": now_iso(),
        "method_count": len(method_index.get("methods", [])),
        "counts": {name: len(files) for name, files in surfaces.items()},
        "surfaces": {name: [rel(p) for p in files] for name, files in surfaces.items()},
        "latest": latest,
    }
    status["recommendation"] = recommend_next(status)
    return status


def render_status_markdown(status: dict[str, Any]) -> str:
    lines = [
        f"# VN Control Room Status: {status['project_id']}",
        "",
        f"- Generated: {status['generated_at']}",
        f"- Project path: `{status['project_path']}`",
        f"- Method cards available: {status['method_count']}",
        "",
        "## Counts",
        "",
    ]
    for key, value in status["counts"].items():
        lines.append(f"- `{key}`: {value}")
    rec = status["recommendation"]
    lines += [
        "",
        "## Recommended Next Step",
        "",
        f"- Action: `{rec['action']}`",
        f"- Reason: {rec['reason']}",
        f"- Command hint: `{rec['command']}`",
        "",
        "## Latest Artifacts",
        "",
    ]
    for key, value in status["latest"].items():
        lines.append(f"- `{key}`: `{value or ''}`")
    return "\n".join(lines) + "\n"


def append_ledger(record: dict[str, Any]) -> None:
    COMMAND_DIR.mkdir(parents=True, exist_ok=True)
    with COMMAND_LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_ledger() -> list[dict[str, Any]]:
    if not COMMAND_LEDGER.exists():
        return []
    records = []
    for line in COMMAND_LEDGER.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def command_id(action: str, project_id: str) -> str:
    seed = f"{now_iso()}|{project_id}|{action}|{time.perf_counter()}".encode("utf-8")
    return hashlib.sha1(seed).hexdigest()[:12]


def create_command(args: argparse.Namespace) -> dict[str, Any]:
    project = project_path(args.project)
    record = {
        "id": command_id(args.action, project.name),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "queued",
        "project_id": project.name,
        "action": args.action,
        "scene": args.scene,
        "script": args.script,
        "draft_name": args.draft_name,
        "note": args.note or "",
        "result": None,
    }
    append_ledger(record)
    return record


def update_command(record_id: str, patch: dict[str, Any]) -> dict[str, Any]:
    records = load_ledger()
    next_records = []
    updated = None
    for record in records:
        if record.get("id") == record_id:
            record = {**record, **patch, "updated_at": now_iso()}
            updated = record
        next_records.append(record)
    if updated is None:
        raise SystemExit(f"Command not found: {record_id}")
    COMMAND_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    COMMAND_LEDGER.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in next_records),
        encoding="utf-8",
    )
    return updated


def latest_script(project: Path, requested: str | None = None) -> Path:
    if requested:
        candidate = (WORKBENCH_ROOT / requested).resolve() if not Path(requested).is_absolute() else Path(requested).resolve()
        if candidate.exists():
            return candidate
    scripts = project_surfaces(project)["csv_scripts"]
    if not scripts:
        raise SystemExit("No CSV script found.")
    return latest_file(scripts) or scripts[-1]


def latest_scene(project: Path, requested: str | None = None) -> Path:
    if requested:
        candidate = (WORKBENCH_ROOT / requested).resolve() if not Path(requested).is_absolute() else Path(requested).resolve()
        if candidate.exists():
            return candidate
    scenes = project_surfaces(project)["scene_cards"]
    if not scenes:
        raise SystemExit("No scene card found.")
    return scenes[0]


def run_subprocess(args: list[str], timeout: int = 240) -> dict[str, Any]:
    started = time.time()
    proc = subprocess.run(
        [sys.executable, str(VN_TOOL), *args],
        cwd=str(WORKBENCH_ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "seconds": round(time.time() - started, 2),
        "command": [sys.executable, str(VN_TOOL), *args],
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def execute_action(project: Path, action: str, scene: str | None, script: str | None, draft_name: str | None) -> dict[str, Any]:
    if action == "draft_session":
        scene_path = latest_scene(project, scene)
        return run_subprocess([
            "draft-session",
            "--project",
            str(project),
            "--scene",
            str(scene_path),
            "--draft-name",
            draft_name or scene_path.stem,
        ])
    if action == "validate":
        script_path = latest_script(project, script)
        return run_subprocess(["validate", "--project", str(project), "--script", str(script_path)])
    if action == "deep_audit":
        script_path = latest_script(project, script)
        return run_subprocess(["deep-audit", "--project", str(project), "--script", str(script_path)])
    if action == "render_readable":
        script_path = latest_script(project, script)
        out = project / "02_generated_content" / "drafts" / "readable" / f"{script_path.stem}.md"
        return run_subprocess(["render-readable", "--project", str(project), "--script", str(script_path), "--out", str(out)])
    if action == "character_brief":
        out = internal_context_dir(project) / f"{project.name}_character_brief.md"
        return run_subprocess(["character-brief", "--project", str(project), "--out", str(out)])
    if action == "export_all":
        script_path = latest_script(project, script)
        stem = script_path.stem
        exports = [
            ("export-webgal", engine_exports_dir(project) / "webgal" / f"{stem}.txt"),
            ("export-renpy", engine_exports_dir(project) / "renpy" / f"{stem}.rpy"),
            ("export-ink", engine_exports_dir(project) / "ink" / f"{stem}.ink"),
            ("export-yarn", engine_exports_dir(project) / "yarn" / f"{stem}.yarn"),
            ("export-godot-dialogue", engine_exports_dir(project) / "godot_dialogue" / f"{stem}.dialogue"),
        ]
        results = [run_subprocess([cmd, "--project", str(project), "--script", str(script_path), "--out", str(out)]) for cmd, out in exports]
        return {"ok": all(item["ok"] for item in results), "results": results}
    if action == "quality_debt":
        script_path = latest_script(project, script)
        report = build_quality_debt(project, script_path)
        return {"ok": True, "report": report}
    if action == "style_contract":
        scene_path = latest_scene(project, scene)
        contract = build_style_contract(project, scene_path, None, draft_name or scene_path.stem)
        return {"ok": True, "contract": contract}
    raise SystemExit(f"Unknown action: {action}")


def run_command(args: argparse.Namespace) -> dict[str, Any]:
    records = load_ledger()
    record = next((item for item in records if item.get("id") == args.id), None)
    if not record:
        raise SystemExit(f"Command not found: {args.id}")
    project = project_path(record["project_id"])
    update_command(record["id"], {"status": "running"})
    try:
        result = execute_action(project, record["action"], record.get("scene"), record.get("script"), record.get("draft_name"))
        status = "succeeded" if result.get("ok") else "failed"
        return update_command(record["id"], {"status": status, "result": result})
    except Exception as error:
        return update_command(record["id"], {"status": "failed", "result": {"ok": False, "error": str(error)}})


def select_methods(methods_arg: str | None) -> list[dict[str, Any]]:
    index = read_json(METHOD_INDEX, {"methods": []})
    methods = index.get("methods", [])
    if methods_arg:
        wanted = {item.strip() for item in methods_arg.split(",") if item.strip()}
        return [item for item in methods if item.get("id") in wanted]
    return [item for item in methods if item.get("default_enabled")]


def method_category(method_id: str) -> str:
    if any(token in method_id for token in ["character", "voice", "presence", "memory"]):
        return "character"
    if any(token in method_id for token in ["click", "rhythm", "textbox", "dialogue", "interiority", "punctuation"]):
        return "rhythm"
    if any(token in method_id for token in ["theme", "choice", "branch", "storylet", "state", "route"]):
        return "narrative"
    if any(token in method_id for token in ["ai", "preachy", "line_energy"]):
        return "anti_ai"
    return "language"


def compact_method_text(path: Path, limit: int = 1800) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[trimmed in style contract]"


def build_style_contract(project: Path, scene: Path, methods_arg: str | None, draft_name: str) -> dict[str, Any]:
    selected = select_methods(methods_arg)
    blocks: dict[str, list[dict[str, str]]] = {
        "narrative": [],
        "character": [],
        "language": [],
        "rhythm": [],
        "anti_ai": [],
        "self_check": [],
    }
    for item in selected:
        method_id = item["id"]
        method_file = CORE_DIR / "methods" / item["file"]
        block = {
            "id": method_id,
            "title": item.get("title", method_id),
            "invocation": item.get("invocation", ""),
            "output_contract": item.get("output_contract", ""),
            "text": compact_method_text(method_file) if method_file.exists() else "",
        }
        blocks[method_category(method_id)].append(block)
    blocks["self_check"].append({
        "id": "vn_control_room_self_check",
        "title": "VN Control Room Self Check",
        "invocation": "Run after drafting or revising.",
        "output_contract": "Check click payload, thought rows, voice separation, punctuation energy, theme-through-play, and state memory before delivery.",
        "text": "\n".join(f"- {name}: {label}" for name, label in QUALITY_DEBT_TYPES.items()),
    })
    contract = {
        "project_id": project.name,
        "scene": rel(scene),
        "generated_at": now_iso(),
        "draft_name": draft_name,
        "source": "workbench-owned method cards compiled into VN style contract",
        "method_ids": [item["id"] for item in selected],
        "blocks": blocks,
    }
    out_dir = internal_context_dir(project)
    json_path = out_dir / f"{draft_name}_style_contract.json"
    md_path = out_dir / f"{draft_name}_style_contract.md"
    write_json(json_path, contract)
    lines = [
        f"# VN Style Contract: {draft_name}",
        "",
        f"- Project: `{project.name}`",
        f"- Scene: `{rel(scene)}`",
        f"- Generated: {contract['generated_at']}",
        "",
    ]
    for block_name, entries in blocks.items():
        lines += [f"## {block_name}", ""]
        for entry in entries:
            lines += [
                f"### {entry['id']} - {entry['title']}",
                "",
                f"- Invocation: {entry['invocation']}",
                f"- Output contract: {entry['output_contract']}",
                "",
                entry["text"],
                "",
            ]
    write_text(md_path, "\n".join(lines))
    return {**contract, "json_path": rel(json_path), "markdown_path": rel(md_path)}


def add_debt(debts: dict[str, list[dict[str, Any]]], debt_type: str, row: dict[str, str] | None, reason: str) -> None:
    item = {
        "beat_id": row.get("beat_id", "") if row else "",
        "speaker": row.get("speaker", "") if row else "",
        "excerpt": (row.get("text", "") if row else "")[:120],
        "reason": reason,
    }
    debts.setdefault(debt_type, []).append(item)


def build_quality_debt(project: Path, script: Path) -> dict[str, Any]:
    rows = read_csv_rows(script)
    debts: dict[str, list[dict[str, Any]]] = {}
    dialogue_rows = [row for row in rows if row.get("row_type") == "dialogue"]
    thought_rows = [row for row in rows if row.get("row_type") == "thought"]
    choice_rows = [row for row in rows if row.get("row_type") == "choice"]

    for row in dialogue_rows:
        text = row.get("text", "")
        length = visible_len(text)
        if length < 8:
            add_debt(debts, "click_unit_low_payload", row, "对白点击单位过短，除非配合强演出，否则玩家点击收益偏低。")
        has_energy = bool(ENERGY_RE.search(text) or CASUAL_RE.search(text))
        has_performance_support = bool(row.get("expression") or row.get("body_action") or row.get("sfx"))
        if length >= 18 and not has_energy and not has_performance_support:
            add_debt(debts, "punctuation_energy_loss", row, "较长对白缺少可表演的停顿、追问、打断、语气词或演出承托。")
        if length >= 18 and not (row.get("expression") or row.get("body_action") or row.get("sfx")):
            add_debt(debts, "performance_cue_gap", row, "长对白缺少立绘、动作或音效承托。")
        if any(pattern.search(text) for pattern in AI_PHRASE_PATTERNS):
            add_debt(debts, "preachy_dialogue", row, "命中了常见 AI/说教式表达。")

    for first, second in zip(dialogue_rows, dialogue_rows[1:]):
        if first.get("speaker") == second.get("speaker") and visible_len(first.get("text", "")) < 12 and visible_len(second.get("text", "")) < 12:
            add_debt(debts, "click_unit_overfragmented", second, "同一角色连续短句可能应合并为一个更有负载的点击单位。")

    if len(rows) >= 12 and not thought_rows:
        add_debt(debts, "thought_missing", None, "场景没有心理行；如果需要玩家代入，应补私下推断、隐瞒动机或选择压力。")
    for row in thought_rows:
        text = row.get("text", "")
        if VISIBLE_ACTION_WORDS.search(text) and "我" not in text:
            add_debt(debts, "thought_misclassified_narration", row, "这行更像摄像机可见动作或物件叙述，不像私密心理。")

    by_speaker: dict[str, list[dict[str, str]]] = {}
    for row in dialogue_rows:
        by_speaker.setdefault(row.get("speaker") or "UNKNOWN", []).append(row)
    for speaker, speaker_rows in by_speaker.items():
        if len(speaker_rows) >= 3:
            energetic = sum(1 for row in speaker_rows if ENERGY_RE.search(row.get("text", "")) or CASUAL_RE.search(row.get("text", "")))
            acted = sum(1 for row in speaker_rows if row.get("body_action") or row.get("expression"))
            if energetic == 0 or acted == 0:
                add_debt(debts, "flat_voice", speaker_rows[0], f"`{speaker}` 的句形、语气或动作手迹不足。")

    if not choice_rows:
        add_debt(debts, "theme_not_playable", None, "没有 choice 行；若这是交互测试片段，主题压力还没有变成玩家行为。")
    for row in choice_rows:
        if not row.get("effects") and not row.get("memory_refs"):
            add_debt(debts, "state_unremembered", row, "选择没有 effects 或 memory_refs，后续难以记住玩家行为。")

    summary = {
        "script": rel(script),
        "project_id": project.name,
        "generated_at": now_iso(),
        "row_count": len(rows),
        "dialogue_count": len(dialogue_rows),
        "thought_count": len(thought_rows),
        "choice_count": len(choice_rows),
        "debt_counts": {key: len(value) for key, value in debts.items()},
        "blocking": [key for key in debts if key in {"state_unremembered", "theme_not_playable"}],
        "debts": debts,
    }
    out_json = quality_reports_dir(project) / f"{script.stem}_quality_debt.json"
    out_md = quality_reports_dir(project) / f"{script.stem}_quality_debt.md"
    write_json(out_json, summary)
    lines = [
        f"# VN Quality Debt: {script.stem}",
        "",
        f"- Project: `{project.name}`",
        f"- Script: `{rel(script)}`",
        f"- Rows: {len(rows)}",
        f"- Dialogue / Thought / Choice: {len(dialogue_rows)} / {len(thought_rows)} / {len(choice_rows)}",
        "",
        "## Debt Summary",
        "",
    ]
    if not debts:
        lines.append("No VN-specific quality debt detected by this deterministic pass.")
    for key, items in debts.items():
        lines += [f"- `{key}` {QUALITY_DEBT_TYPES[key]}: {len(items)}"]
    for key, items in debts.items():
        lines += ["", f"## {key} - {QUALITY_DEBT_TYPES[key]}", ""]
        for item in items[:20]:
            lines.append(f"- `{item['beat_id']}` {item['speaker']}: {item['reason']} `{item['excerpt']}`")
        if len(items) > 20:
            lines.append(f"- ... {len(items) - 20} more")
    write_text(out_md, "\n".join(lines) + "\n")
    return {**summary, "json_path": rel(out_json), "markdown_path": rel(out_md)}


def build_context_trace(project: Path, scene: Path, draft_name: str) -> dict[str, Any]:
    surfaces = project_surfaces(project)
    selected_methods = select_methods(None)
    trace = {
        "project_id": project.name,
        "scene": rel(scene),
        "generated_at": now_iso(),
        "draft_name": draft_name,
        "required_order": [
            "portable operating rules",
            "method index",
            "project bible",
            "scene card",
            "route and interactive design",
            "character cards",
            "runtime character states",
            "episodic memories",
            "style contract",
            "recent script tail",
            "user instruction",
        ],
        "method_ids": [item["id"] for item in selected_methods],
        "loaded_files": {name: [rel(path) for path in files] for name, files in surfaces.items()},
    }
    out = internal_context_dir(project) / f"{draft_name}_context_trace.json"
    write_json(out, trace)
    return {**trace, "json_path": rel(out)}


def command_status(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    status = build_status(project)
    if args.out:
        out = Path(args.out)
        if out.suffix.lower() == ".json":
            write_json(out, status)
        else:
            write_text(out, render_status_markdown(status))
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(render_status_markdown(status))
    return 0


def command_create(args: argparse.Namespace) -> int:
    record = create_command(args)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def command_list(args: argparse.Namespace) -> int:
    records = load_ledger()
    if args.project:
        records = [item for item in records if item.get("project_id") == args.project]
    print(json.dumps(records[-args.limit :], ensure_ascii=False, indent=2))
    return 0


def command_run(args: argparse.Namespace) -> int:
    record = run_command(args)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if record.get("status") == "succeeded" else 1


def command_style_contract(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    scene = latest_scene(project, args.scene)
    result = build_style_contract(project, scene, args.methods, args.draft_name or scene.stem)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_quality_debt(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    script = latest_script(project, args.script)
    result = build_quality_debt(project, script)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_context_trace(args: argparse.Namespace) -> int:
    project = project_path(args.project)
    scene = latest_scene(project, args.scene)
    result = build_context_trace(project, scene, args.draft_name or scene.stem)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VN Control Room")
    sub = parser.add_subparsers(required=True)

    p_status = sub.add_parser("status", help="project status projection and next-step recommendation")
    p_status.add_argument("--project", required=True)
    p_status.add_argument("--json", action="store_true")
    p_status.add_argument("--out")
    p_status.set_defaults(func=command_status)

    p_create = sub.add_parser("command-create", help="create a controlled workbench command")
    p_create.add_argument("--project", required=True)
    p_create.add_argument("--action", required=True, choices=[
        "draft_session",
        "validate",
        "deep_audit",
        "render_readable",
        "export_all",
        "character_brief",
        "style_contract",
        "quality_debt",
    ])
    p_create.add_argument("--scene")
    p_create.add_argument("--script")
    p_create.add_argument("--draft-name", default="")
    p_create.add_argument("--note")
    p_create.set_defaults(func=command_create)

    p_list = sub.add_parser("command-list", help="list recent command ledger records")
    p_list.add_argument("--project")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.set_defaults(func=command_list)

    p_run = sub.add_parser("command-run", help="run a queued command by id")
    p_run.add_argument("--id", required=True)
    p_run.set_defaults(func=command_run)

    p_style = sub.add_parser("style-contract", help="compile method cards into a VN writing contract")
    p_style.add_argument("--project", required=True)
    p_style.add_argument("--scene")
    p_style.add_argument("--methods")
    p_style.add_argument("--draft-name")
    p_style.set_defaults(func=command_style_contract)

    p_debt = sub.add_parser("quality-debt", help="classify VN-specific quality debt from a CSV script")
    p_debt.add_argument("--project", required=True)
    p_debt.add_argument("--script")
    p_debt.set_defaults(func=command_quality_debt)

    p_trace = sub.add_parser("context-trace", help="write a context trace for a scene drafting run")
    p_trace.add_argument("--project", required=True)
    p_trace.add_argument("--scene")
    p_trace.add_argument("--draft-name", default="S001_context_trace")
    p_trace.set_defaults(func=command_context_trace)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
