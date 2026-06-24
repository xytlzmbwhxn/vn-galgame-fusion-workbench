#!/usr/bin/env python3
"""VN learning intake helper.

Converts user-provided learning materials from pending folders into normalized
Markdown under learned folders. This tool deliberately does not "summarize" with
an LLM; it prepares clean text, metadata, and measurable style signals so Codex
or another model can learn from stable files.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import sys
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


SUPPORTED_EXT = {".txt", ".md", ".csv", ".json", ".docx", ".html", ".htm"}
PRIVATE_DIR_NAME = "_local"
CN_SENTENCE_RE = re.compile(r"[^。！？!?…\n]+[。！？!?…]*")
DIALOGUE_MARK_RE = re.compile(r"^\s*(【[^】]+】|「|『|\"|')")
SPEAKER_RE = re.compile(r"【([^】]{1,24})】")
PUNCTUATION = ["。", "，", "、", "？", "！", "…", "：", "；", "「", "」", "『", "』", "（", "）"]
CASUAL_MARKERS = ["欸", "嘛", "啦", "呀", "呢", "吧", "喔", "哎", "啊", "拜托", "好啦", "真的假的"]


@dataclass
class TextMetrics:
    char_count: int
    line_count: int
    nonempty_line_count: int
    sentence_count: int
    avg_sentence_len: float
    dialogue_like_lines: int
    dialogue_like_pct: float
    thought_like_lines: int
    command_like_lines: int
    punctuation_counts: dict[str, int]
    casual_marker_counts: dict[str, int]
    detected_speakers: list[str]


@dataclass
class IntakeRecord:
    kind: str
    source_path: str
    output_path: str
    sha256: str
    processed_at: str
    removed_source: bool
    metrics: TextMetrics


def workbench_root_from(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "00_workbench_core").exists() and (path / "02_projects").exists():
            return path
    raise SystemExit("Run from vn_fusion_workbench or pass --workbench-root.")


def read_text_with_fallback(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "big5", "cp932", "shift_jis", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def extract_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        raw = zf.read("word/document.xml")
    root = ET.fromstring(raw)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paras: list[str] = []
    for p in root.findall(".//w:p", ns):
        parts = [node.text or "" for node in p.findall(".//w:t", ns)]
        text = "".join(parts).strip()
        if text:
            paras.append(text)
    return "\n".join(paras)


def extract_csv(path: Path) -> str:
    text = read_text_with_fallback(path)
    rows: list[list[str]] = []
    try:
        reader = csv.reader(text.splitlines())
        rows = [row for row in reader]
    except csv.Error:
        return text
    return "\n".join(" | ".join(cell.strip() for cell in row) for row in rows)


def extract_json(path: Path) -> str:
    text = read_text_with_fallback(path)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return text
    return json.dumps(obj, ensure_ascii=False, indent=2)


def extract_html(path: Path) -> str:
    text = read_text_with_fallback(path)
    text = re.sub(r"(?is)<(script|style).*?</\1>", "\n", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p\s*>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    return html.unescape(text)


def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".docx":
        return extract_docx(path)
    if ext == ".csv":
        return extract_csv(path)
    if ext == ".json":
        return extract_json(path)
    if ext in {".html", ".htm"}:
        return extract_html(path)
    return read_text_with_fallback(path)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_metrics(text: str) -> TextMetrics:
    lines = text.splitlines()
    nonempty = [line for line in lines if line.strip()]
    sentences = [m.group(0).strip() for m in CN_SENTENCE_RE.finditer(text) if m.group(0).strip()]
    sentence_lengths = [len(re.sub(r"\s+", "", s)) for s in sentences]
    dialogue_like = [line for line in nonempty if DIALOGUE_MARK_RE.search(line)]
    thought_like = [line for line in nonempty if line.strip().startswith(("（", "("))]
    command_like = [line for line in nonempty if line.strip().startswith(("@", "stage:", "scene ", "show ", "play "))]
    punctuation_counts = {p: text.count(p) for p in PUNCTUATION}
    casual_counts = {m: text.count(m) for m in CASUAL_MARKERS if text.count(m)}
    speakers = sorted(set(SPEAKER_RE.findall(text)))[:60]
    avg_len = round(sum(sentence_lengths) / len(sentence_lengths), 2) if sentence_lengths else 0.0
    dialogue_pct = round(len(dialogue_like) * 100 / len(nonempty), 2) if nonempty else 0.0
    return TextMetrics(
        char_count=len(re.sub(r"\s+", "", text)),
        line_count=len(lines),
        nonempty_line_count=len(nonempty),
        sentence_count=len(sentences),
        avg_sentence_len=avg_len,
        dialogue_like_lines=len(dialogue_like),
        dialogue_like_pct=dialogue_pct,
        thought_like_lines=len(thought_like),
        command_like_lines=len(command_like),
        punctuation_counts=punctuation_counts,
        casual_marker_counts=casual_counts,
        detected_speakers=speakers,
    )


def safe_output_name(source: Path) -> str:
    return f"{source.stem}.md"


def render_markdown(kind: str, source: Path, source_hash: str, text: str, metrics: TextMetrics) -> str:
    title = source.stem
    metrics_json = json.dumps(asdict(metrics), ensure_ascii=False, indent=2)
    return (
        "---\n"
        f"kind: {kind}\n"
        f"original_filename: {json.dumps(source.name, ensure_ascii=False)}\n"
        f"source_sha256: {source_hash}\n"
        f"processed_at: {datetime.now().astimezone().isoformat(timespec='seconds')}\n"
        "status: learned_text_normalized\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Intake Metrics\n\n"
        "```json\n"
        f"{metrics_json}\n"
        "```\n\n"
        "## Normalized Text\n\n"
        f"{text}"
    )


def iter_pending_files(pending: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(pending.rglob("*")):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.suffix.lower() not in SUPPORTED_EXT:
            continue
        if path.name.startswith("把") and path.suffix.lower() == ".md":
            continue
        files.append(path)
    return files


def is_private_path(path: Path) -> bool:
    return PRIVATE_DIR_NAME in path.parts


def process_kind(root: Path, kind: str, remove_source: bool) -> list[IntakeRecord]:
    if kind == "tutorials":
        label = "tutorial"
        pending = root / "06_学习输入" / "教程文本" / "待学习"
        learned = root / "06_学习输入" / "教程文本" / "已学习"
    elif kind == "scripts":
        label = "vn_script"
        pending = root / "06_学习输入" / "视觉小说剧本文本" / "待学习"
        learned = root / "06_学习输入" / "视觉小说剧本文本" / "已学习"
    else:
        raise ValueError(kind)

    learned.mkdir(parents=True, exist_ok=True)
    records: list[IntakeRecord] = []
    for source in iter_pending_files(pending):
        source_hash = sha256_file(source)
        text = normalize_text(extract_text(source))
        metrics = collect_metrics(text)
        out_dir = learned / PRIVATE_DIR_NAME if is_private_path(source) else learned
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / safe_output_name(source)
        if out.exists():
            out = learned / f"{source.stem}_{source_hash[:8]}.md"
        out.write_text(render_markdown(label, source, source_hash, text, metrics), encoding="utf-8")
        removed = False
        if remove_source:
            source.unlink()
            removed = True
        records.append(
            IntakeRecord(
                kind=label,
                source_path=str(source),
                output_path=str(out),
                sha256=source_hash,
                processed_at=datetime.now().astimezone().isoformat(timespec="seconds"),
                removed_source=removed,
                metrics=metrics,
            )
        )
    return records


def write_manifest(root: Path, records: list[IntakeRecord]) -> Path:
    has_private = any(PRIVATE_DIR_NAME in Path(record.source_path).parts for record in records)
    logs = root / "06_学习输入" / "_处理日志"
    if has_private:
        logs = logs / PRIVATE_DIR_NAME
    logs.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = logs / f"intake_manifest_{stamp}.json"
    path.write_text(json.dumps([asdict(r) for r in records], ensure_ascii=False, indent=2), encoding="utf-8")
    latest = logs / "latest_intake_manifest.json"
    latest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize pending VN learning materials into Markdown.")
    parser.add_argument("--workbench-root", help="Path to vn_fusion_workbench. Defaults to current/parent search.")
    parser.add_argument("--kind", choices=["all", "tutorials", "scripts"], default="all")
    parser.add_argument("--remove-source", action="store_true", help="Delete source files after successful conversion.")
    args = parser.parse_args(argv)

    root = Path(args.workbench_root).resolve() if args.workbench_root else workbench_root_from(Path.cwd().resolve())
    kinds = ["tutorials", "scripts"] if args.kind == "all" else [args.kind]
    records: list[IntakeRecord] = []
    for kind in kinds:
        records.extend(process_kind(root, kind, args.remove_source))
    manifest = write_manifest(root, records)
    print(f"Processed {len(records)} file(s).")
    print(f"Manifest: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
