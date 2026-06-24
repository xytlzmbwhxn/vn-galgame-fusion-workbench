#!/usr/bin/env python3
"""Analyze full Ren'Py/VN script corpora without copying script text.

The tool reads complete local script files and exports aggregate metrics only.
It deliberately avoids writing source dialogue, narration, or scene prose into
reports, so licensed works can be studied without becoming a text-dump corpus.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Iterable


LABEL_RE = re.compile(r"^\s*label\s+([A-Za-z_][\w.]*)\s*:")
MENU_RE = re.compile(r"^\s*menu(?:\s+[^:]+)?\s*:")
MENU_OPTION_RE = re.compile(r'^\s*"[^"]+"\s*(?:if\s+[^:]+)?\s*:')
JUMP_RE = re.compile(r"^\s*jump\s+([A-Za-z_][\w.]*)")
CALL_RE = re.compile(r"^\s*call\s+([A-Za-z_][\w.]*)")
RETURN_RE = re.compile(r"^\s*return\b")
SCENE_CMD_RE = re.compile(r"^\s*(scene|show|hide|with|play|stop|queue|voice|pause|window)\b")
DEFINE_RE = re.compile(r"^\s*(define|default)\s+([A-Za-z_][\w.]*)")
PYTHON_RE = re.compile(r"^\s*(\$|python\s*:)")
RABBL_PERFORM_RE = re.compile(r"^\s*perform\s+")
RABBL_CHOICE_RE = re.compile(r"^\s*choice\s+")
QUOTE_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')

COMMAND_KEYWORDS = {
    "add",
    "advance",
    "assert",
    "background",
    "bar",
    "button",
    "call",
    "choice",
    "define",
    "default",
    "elif",
    "else",
    "extend",
    "hide",
    "hotspot",
    "hbox",
    "if",
    "image",
    "imagebutton",
    "init",
    "key",
    "jump",
    "label",
    "menu",
    "old",
    "pause",
    "play",
    "python",
    "queue",
    "return",
    "scroll",
    "scene",
    "screen",
    "show",
    "side",
    "stop",
    "style",
    "style_prefix",
    "text",
    "textbutton",
    "translate",
    "use",
    "variant",
    "vbox",
    "voice",
    "while",
    "window",
    "with",
}

TEXT_COMMAND_PREFIXES = {"extend", "centered", "narrator", "nvl"}


@dataclass
class FileMetrics:
    path: str
    lines: int = 0
    nonblank_lines: int = 0
    labels: int = 0
    menus: int = 0
    menu_options: int = 0
    say_lines: int = 0
    dialogue_lines: int = 0
    narration_lines: int = 0
    scene_commands: int = 0
    jumps: int = 0
    calls: int = 0
    returns: int = 0
    python_lines: int = 0
    defines_defaults: int = 0
    rabbl_performs: int = 0
    rabbl_choices: int = 0


@dataclass
class CorpusMetrics:
    id: str
    title: str
    repo_url: str
    local_path: str
    commit: str
    license_note: str
    study_focus: str
    files: list[FileMetrics] = field(default_factory=list)
    labels: Counter[str] = field(default_factory=Counter)
    speakers: Counter[str] = field(default_factory=Counter)
    scene_commands: Counter[str] = field(default_factory=Counter)
    quote_lengths: list[int] = field(default_factory=list)
    punctuation: Counter[str] = field(default_factory=Counter)

    def totals(self) -> dict:
        total = Counter()
        for file_metric in self.files:
            total.update(
                {
                    "lines": file_metric.lines,
                    "nonblank_lines": file_metric.nonblank_lines,
                    "labels": file_metric.labels,
                    "menus": file_metric.menus,
                    "menu_options": file_metric.menu_options,
                    "say_lines": file_metric.say_lines,
                    "dialogue_lines": file_metric.dialogue_lines,
                    "narration_lines": file_metric.narration_lines,
                    "scene_commands": file_metric.scene_commands,
                    "jumps": file_metric.jumps,
                    "calls": file_metric.calls,
                    "returns": file_metric.returns,
                    "python_lines": file_metric.python_lines,
                    "defines_defaults": file_metric.defines_defaults,
                    "rabbl_performs": file_metric.rabbl_performs,
                    "rabbl_choices": file_metric.rabbl_choices,
                }
            )
        total["files"] = len(self.files)
        lengths = sorted(self.quote_lengths)
        if lengths:
            total["avg_chars_per_textbox_x10"] = round(sum(lengths) * 10 / len(lengths))
            total["median_chars_per_textbox"] = int(median(lengths))
            total["p90_chars_per_textbox"] = lengths[min(len(lengths) - 1, int(len(lengths) * 0.9))]
            total["short_textbox_pct_x10"] = round(sum(1 for n in lengths if n <= 20) * 1000 / len(lengths))
            total["long_textbox_pct_x10"] = round(sum(1 for n in lengths if n >= 100) * 1000 / len(lengths))
        else:
            total["avg_chars_per_textbox_x10"] = 0
            total["median_chars_per_textbox"] = 0
            total["p90_chars_per_textbox"] = 0
            total["short_textbox_pct_x10"] = 0
            total["long_textbox_pct_x10"] = 0
        if total["narration_lines"]:
            total["dialogue_to_narration_x10"] = round(total["dialogue_lines"] * 10 / total["narration_lines"])
        else:
            total["dialogue_to_narration_x10"] = 0
        return dict(total)


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def visible_text_len(raw: str) -> int:
    compact = re.sub(r"\{[^}]+\}", "", raw)
    compact = re.sub(r"\\[nrt]", "", compact)
    compact = re.sub(r"\s+", "", compact)
    return len(compact)


def extract_say(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped.startswith("old ") or stripped.startswith("new "):
        return None
    first_quote = stripped.find('"')
    if first_quote < 0:
        return None
    prefix = stripped[:first_quote].strip()
    if not prefix:
        speaker = ""
    else:
        if prefix.startswith("$") or "=" in prefix or "(" in prefix or ")" in prefix:
            return None
        first = prefix.split()[0]
        if first in COMMAND_KEYWORDS and first not in TEXT_COMMAND_PREFIXES:
            return None
        speaker = first
    match = QUOTE_RE.search(stripped[first_quote:])
    if not match:
        return None
    return speaker, match.group(1)


def iter_script_files(root: Path, entry: dict) -> list[Path]:
    base = root / entry["local_path"]
    seen: set[Path] = set()
    files: list[Path] = []
    excludes = entry.get("exclude_globs", [])
    for pattern in entry.get("script_globs", []):
        for path in base.glob(pattern):
            if not path.is_file() or path in seen:
                continue
            rel = path.relative_to(base).as_posix()
            if any(fnmatch.fnmatch(rel, exclude) for exclude in excludes):
                continue
            seen.add(path)
            files.append(path)
    return sorted(files)


def analyze_file(path: Path, base: Path, corpus: CorpusMetrics) -> FileMetrics:
    text = read_text(path)
    rel = path.relative_to(base).as_posix()
    metrics = FileMetrics(path=rel)

    for raw_line in text.splitlines():
        metrics.lines += 1
        line = raw_line.rstrip("\n")
        stripped = line.strip()
        if stripped:
            metrics.nonblank_lines += 1
        if not stripped or stripped.startswith("#"):
            continue

        if match := LABEL_RE.match(line):
            metrics.labels += 1
            corpus.labels[match.group(1)] += 1
        if MENU_RE.match(line):
            metrics.menus += 1
        if MENU_OPTION_RE.match(line):
            metrics.menu_options += 1
        if JUMP_RE.match(line):
            metrics.jumps += 1
        if CALL_RE.match(line):
            metrics.calls += 1
        if RETURN_RE.match(line):
            metrics.returns += 1
        if match := SCENE_CMD_RE.match(line):
            metrics.scene_commands += 1
            corpus.scene_commands[match.group(1)] += 1
        if DEFINE_RE.match(line):
            metrics.defines_defaults += 1
        if PYTHON_RE.match(line):
            metrics.python_lines += 1
        if RABBL_PERFORM_RE.match(line):
            metrics.rabbl_performs += 1
        if RABBL_CHOICE_RE.match(line):
            metrics.rabbl_choices += 1

        say = extract_say(line)
        if say:
            speaker, quoted = say
            metrics.say_lines += 1
            length = visible_text_len(quoted)
            corpus.quote_lengths.append(length)
            for mark in ("?", "!", "...", "--"):
                if mark in quoted:
                    corpus.punctuation[mark] += 1
            for mark in ("？", "！", "…", "。", "，"):
                if mark in quoted:
                    corpus.punctuation[mark] += 1
            if speaker:
                metrics.dialogue_lines += 1
                if speaker not in TEXT_COMMAND_PREFIXES:
                    corpus.speakers[speaker] += 1
            else:
                metrics.narration_lines += 1

    return metrics


def analyze_corpus(root: Path, entry: dict) -> CorpusMetrics:
    corpus = CorpusMetrics(
        id=entry["id"],
        title=entry["title"],
        repo_url=entry["repo_url"],
        local_path=entry["local_path"],
        commit=entry.get("commit", ""),
        license_note=entry.get("license_note", ""),
        study_focus=entry.get("study_focus", ""),
    )
    base = root / entry["local_path"]
    for path in iter_script_files(root, entry):
        corpus.files.append(analyze_file(path, base, corpus))
    return corpus


def compact_counter(counter: Counter[str], limit: int = 12) -> list[dict[str, int | str]]:
    return [{"key": key, "count": count} for key, count in counter.most_common(limit)]


def corpus_to_dict(corpus: CorpusMetrics) -> dict:
    return {
        "id": corpus.id,
        "title": corpus.title,
        "repo_url": corpus.repo_url,
        "local_path": corpus.local_path,
        "commit": corpus.commit,
        "license_note": corpus.license_note,
        "study_focus": corpus.study_focus,
        "totals": corpus.totals(),
        "top_speakers": compact_counter(corpus.speakers),
        "scene_commands": compact_counter(corpus.scene_commands),
        "top_labels": compact_counter(corpus.labels),
        "punctuation": compact_counter(corpus.punctuation),
        "files": [file_metric.__dict__ for file_metric in corpus.files],
    }


def pct_x10(value: int) -> str:
    return f"{value / 10:.1f}%"


def avg_x10(value: int) -> str:
    return f"{value / 10:.1f}"


def render_markdown(manifest: dict, corpora: list[CorpusMetrics]) -> str:
    lines: list[str] = []
    lines.append("# Legal Full Script Corpus Study")
    lines.append("")
    lines.append("Generated by `00_workbench_core/tools/analyze_full_script_corpus.py`.")
    lines.append("")
    lines.append("## Policy")
    lines.append("")
    lines.append(manifest.get("policy", ""))
    lines.append("")
    lines.append("This report stores aggregate metrics only. It does not reproduce source dialogue, narration, choices, or scene prose.")
    lines.append("")
    lines.append("## Corpus Summary")
    lines.append("")
    lines.append("| Corpus | Files | Lines | Textboxes | Dlg/Nar x | Menus | Options | Labels | Stage Cues | Avg Box Chars | Short Boxes | Long Boxes | License / Use |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for corpus in corpora:
        totals = corpus.totals()
        lines.append(
            "| "
            + " | ".join(
                [
                    corpus.title,
                    str(totals["files"]),
                    str(totals["lines"]),
                    str(totals["say_lines"]),
                    avg_x10(totals["dialogue_to_narration_x10"]),
                    str(totals["menus"]),
                    str(totals["menu_options"]),
                    str(totals["labels"]),
                    str(totals["scene_commands"]),
                    avg_x10(totals["avg_chars_per_textbox_x10"]),
                    pct_x10(totals["short_textbox_pct_x10"]),
                    pct_x10(totals["long_textbox_pct_x10"]),
                    corpus.license_note,
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Per-Corpus Notes")
    lines.append("")
    for corpus in corpora:
        totals = corpus.totals()
        lines.append(f"### {corpus.title}")
        lines.append("")
        lines.append(f"- Source: {corpus.repo_url}")
        lines.append(f"- Local path: `{corpus.local_path}` at `{corpus.commit}`")
        lines.append(f"- Study focus: {corpus.study_focus}")
        lines.append(f"- Structure: {totals['labels']} labels, {totals['menus']} menus, {totals['menu_options']} menu options, {totals['jumps']} jumps, {totals['calls']} calls, {totals['returns']} returns.")
        lines.append(f"- Performance layer: {totals['scene_commands']} staging/audio/window commands across {totals['files']} files.")
        lines.append(f"- System layer: {totals['defines_defaults']} define/default lines, {totals['python_lines']} python-ish script lines, {totals['rabbl_performs']} RABBL perform calls, {totals['rabbl_choices']} RABBL choice calls.")
        if corpus.speakers:
            speaker_names = ", ".join(item["key"] for item in compact_counter(corpus.speakers, 8))
            lines.append(f"- Speaker spread: top speaker symbols include `{speaker_names}`. Names are identifiers only; source lines are not copied.")
        if corpus.scene_commands:
            command_names = ", ".join(f"{item['key']}={item['count']}" for item in compact_counter(corpus.scene_commands, 8))
            lines.append(f"- Common cues: {command_names}.")
        lines.append("")
    lines.append("## Lessons Converted Into Workbench Rules")
    lines.append("")
    lines.append("- Separate master flow from scene prose when a project grows. First Snow and Twofold both centralize scene flow through a master script/RABBL layer while keeping scene text in separate files.")
    lines.append("- Treat choices as replay-safe state changes, not isolated menu labels. RABBL-style `choice` calls and LearnToCodeRPG's stat/day systems both show that choice handling belongs in the system layer.")
    lines.append("- Keep production cues near the text. Large complete scripts repeatedly interleave dialogue/narration with `scene`, `show`, `play`, `with`, and `voice`-style commands; our CSV rows must keep bg/bgm/sfx/expression/body_action populated.")
    lines.append("- Use full-project metrics before drafting. A scene sample should declare target textbox length, dialogue/narration balance, choice density, and staging density based on a selected corpus reference.")
    lines.append("- Do not imitate prose. The reusable artifact is the ratio, flow shape, state ledger, and scene-file organization, not source wording.")
    lines.append("")
    lines.append("## Required Invocation")
    lines.append("")
    lines.append("Before claiming a new script references complete VN scripts, run:")
    lines.append("")
    lines.append("```powershell")
    lines.append("py .\\00_workbench_core\\tools\\analyze_full_script_corpus.py --manifest .\\01_reference_log\\full_script_corpus\\corpus_manifest.json --out-dir .\\01_reference_log\\full_script_corpus")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze complete VN script corpora without exporting source text.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    root = Path(manifest["reference_root"])
    corpora = [analyze_corpus(root, entry) for entry in manifest.get("corpora", [])]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = args.out_dir / "full_script_metrics.json"
    report_path = args.out_dir / "LEGAL_FULL_SCRIPT_CORPUS.md"
    payload = {
        "version": manifest.get("version", ""),
        "reference_root": manifest.get("reference_root", ""),
        "policy": manifest.get("policy", ""),
        "corpora": [corpus_to_dict(corpus) for corpus in corpora],
        "method_sources": manifest.get("method_sources", []),
    }
    metrics_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(render_markdown(manifest, corpora), encoding="utf-8")
    print(f"Wrote {metrics_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
