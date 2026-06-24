#!/usr/bin/env python3
"""Compile normalized learned texts into a compact VN style profile."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


METRIC_BLOCK_RE = re.compile(r"## Intake Metrics\s+```json\s+(.*?)\s+```", re.S)
TEXT_BLOCK_RE = re.compile(r"## Normalized Text\s+(.*)", re.S)
SENTENCE_RE = re.compile(r"[^。！？!?…\n]+[。！？!?…]*")
PRIVATE_DIR_NAME = "_local"


@dataclass
class LearnedDoc:
    path: Path
    text: str
    metrics: dict


def workbench_root_from(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "00_workbench_core").exists() and (path / "06_学习输入").exists():
            return path
    raise SystemExit("Run from vn_fusion_workbench or pass --workbench-root.")


def load_learned_doc(path: Path) -> LearnedDoc:
    raw = path.read_text(encoding="utf-8", errors="replace")
    metric_match = METRIC_BLOCK_RE.search(raw)
    metrics = {}
    if metric_match:
        try:
            metrics = json.loads(metric_match.group(1))
        except json.JSONDecodeError:
            metrics = {}
    text_match = TEXT_BLOCK_RE.search(raw)
    text = text_match.group(1).strip() if text_match else raw
    return LearnedDoc(path=path, text=text, metrics=metrics)


def learned_dir(root: Path, kind: str) -> Path:
    if kind == "tutorials":
        return root / "06_学习输入" / "教程文本" / "已学习"
    if kind == "scripts":
        return root / "06_学习输入" / "视觉小说剧本文本" / "已学习"
    raise ValueError(kind)


def collect_docs(root: Path, kind: str) -> list[LearnedDoc]:
    base = learned_dir(root, kind)
    docs = []
    paths = list(base.glob("*.md"))
    private_base = base / PRIVATE_DIR_NAME
    if private_base.exists():
        paths.extend(private_base.glob("*.md"))
    for path in sorted(paths):
        if path.name.startswith("."):
            continue
        docs.append(load_learned_doc(path))
    return docs


def contains_private_docs(docs: list[LearnedDoc]) -> bool:
    return any(PRIVATE_DIR_NAME in doc.path.parts for doc in docs)


def top_counts(counter: dict[str, int], limit: int = 12) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:limit])


def merge_counts(docs: list[LearnedDoc], key: str) -> dict[str, int]:
    merged: dict[str, int] = {}
    for doc in docs:
        counts = doc.metrics.get(key, {})
        if isinstance(counts, dict):
            for k, v in counts.items():
                if isinstance(v, int):
                    merged[k] = merged.get(k, 0) + v
    return top_counts(merged)


def aggregate_numeric(docs: list[LearnedDoc], key: str) -> float:
    vals = [doc.metrics.get(key) for doc in docs if isinstance(doc.metrics.get(key), (int, float))]
    return round(sum(vals) / len(vals), 2) if vals else 0.0


def extract_line_examples(docs: list[LearnedDoc], patterns: list[str], limit: int = 10) -> list[str]:
    examples: list[str] = []
    regexes = [re.compile(p) for p in patterns]
    for doc in docs:
        for line in doc.text.splitlines():
            clean = line.strip()
            if not clean or len(clean) > 90:
                continue
            if any(rx.search(clean) for rx in regexes):
                examples.append(clean)
            if len(examples) >= limit:
                return examples
    return examples


def compile_profile(root: Path, kind: str, name: str) -> Path:
    docs = collect_docs(root, kind)
    out_dir = root / "06_学习输入" / "_风格画像"
    if contains_private_docs(docs):
        out_dir = out_dir / PRIVATE_DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = out_dir / f"style_profile_{name or kind}_{stamp}.md"

    total_chars = sum(int(doc.metrics.get("char_count", len(doc.text))) for doc in docs)
    total_lines = sum(int(doc.metrics.get("nonempty_line_count", 0)) for doc in docs)
    avg_sentence_len = aggregate_numeric(docs, "avg_sentence_len")
    dialogue_pct = aggregate_numeric(docs, "dialogue_like_pct")
    punctuation = merge_counts(docs, "punctuation_counts")
    casual = merge_counts(docs, "casual_marker_counts")
    speakers = sorted({sp for doc in docs for sp in doc.metrics.get("detected_speakers", [])})[:80]

    question_examples = extract_line_examples(docs, [r"[？?]"])
    pause_examples = extract_line_examples(docs, [r"…|——|--"])
    dialogue_examples = extract_line_examples(docs, [r"^\s*【[^】]+】", r"^\s*『", r"^\s*「"])

    content = [
        f"# Style Profile: {name or kind}",
        "",
        "## Corpus",
        "",
        f"- kind: `{kind}`",
        f"- files: {len(docs)}",
        f"- total_chars: {total_chars}",
        f"- total_nonempty_lines: {total_lines}",
        f"- generated_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## Metrics",
        "",
        "```json",
        json.dumps(
            {
                "avg_sentence_len": avg_sentence_len,
                "dialogue_like_pct": dialogue_pct,
                "punctuation_counts": punctuation,
                "casual_marker_counts": casual,
                "detected_speakers": speakers,
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## Sentence Engine",
        "",
        "- Fill manually after AI reads the learned Markdown.",
        "- Extract how lines are built, not only what the text talks about.",
        "",
        "## Display Rules",
        "",
        "- Fill with dialogue marks, thought marks, stage cue habits, and textbox split/merge rules.",
        "",
        "## Dialogue Examples To Inspect",
        "",
        *[f"- {line}" for line in dialogue_examples[:10]],
        "",
        "## Question / Pressure Examples",
        "",
        *[f"- {line}" for line in question_examples[:10]],
        "",
        "## Pause / Cut Examples",
        "",
        *[f"- {line}" for line in pause_examples[:10]],
        "",
        "## Do / Do Not / Repair",
        "",
        "- Fill manually after comparing examples against current workbench style rules.",
        "",
        "## QA Checklist",
        "",
        "- [ ] Convert prose style into VN textbox rules.",
        "- [ ] Identify dialogue continuity lessons.",
        "- [ ] Identify valid thought-row functions.",
        "- [ ] Identify punctuation that belongs to character pressure.",
        "- [ ] Add reusable lessons to methods only after rewriting in workbench-owned wording.",
        "",
    ]
    out.write_text("\n".join(content), encoding="utf-8")
    print(out)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile learned Markdown into a compact style profile.")
    parser.add_argument("--workbench-root")
    parser.add_argument("--kind", choices=["tutorials", "scripts"], required=True)
    parser.add_argument("--name", default="")
    args = parser.parse_args(argv)
    root = Path(args.workbench_root).resolve() if args.workbench_root else workbench_root_from(Path.cwd().resolve())
    compile_profile(root, args.kind, args.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
