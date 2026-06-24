from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DIALOGUE_RE = re.compile(r"^【([^】]+)】")


def read_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        stripped = line.strip()
        m = DIALOGUE_RE.match(stripped)
        if m:
            rows.append({"line_no": line_no, "speaker": m.group(1), "kind": "dialogue", "text": stripped})
        elif not stripped:
            rows.append({"line_no": line_no, "speaker": None, "kind": "blank", "text": stripped})
        elif stripped.startswith("@") or stripped.startswith("#"):
            rows.append({"line_no": line_no, "speaker": None, "kind": "stage", "text": stripped})
        elif re.match(r"^\d+(_[A-Z])?(\.\d+)?$", stripped):
            rows.append({"line_no": line_no, "speaker": None, "kind": "id", "text": stripped})
        elif stripped.startswith("（") and stripped.endswith("）"):
            rows.append({"line_no": line_no, "speaker": None, "kind": "thought", "text": stripped})
        else:
            rows.append({"line_no": line_no, "speaker": None, "kind": "narration", "text": stripped})
    return rows


def dialogue_blocks(rows: list[dict]) -> list[list[dict]]:
    blocks: list[list[dict]] = []
    cur: list[dict] = []
    for r in rows:
        if r["kind"] == "dialogue":
            cur.append(r)
        elif r["kind"] in {"id", "blank"}:
            continue
        else:
            if cur:
                blocks.append(cur)
                cur = []
    if cur:
        blocks.append(cur)
    return blocks


def same_speaker_runs(block: list[dict]) -> list[int]:
    out: list[int] = []
    last = None
    n = 0
    for r in block:
        sp = r["speaker"]
        if sp == last:
            n += 1
        else:
            if n:
                out.append(n)
            last = sp
            n = 1
    if n:
        out.append(n)
    return out


def lint(path: Path) -> dict:
    rows = read_rows(path)
    blocks = dialogue_blocks(rows)
    warnings = []
    for idx, block in enumerate(blocks, 1):
        if len(block) < 6:
            continue
        runs = same_speaker_runs(block)
        speakers = [r["speaker"] for r in block]
        changes = sum(1 for a, b in zip(speakers, speakers[1:]) if a != b)
        same = sum(1 for a, b in zip(speakers, speakers[1:]) if a == b)
        longest_run = max(runs) if runs else 0
        if longest_run < 2:
            warnings.append(
                {
                    "type": "long_pingpong_no_same_speaker_run",
                    "block_index": idx,
                    "start_line": block[0]["line_no"],
                    "end_line": block[-1]["line_no"],
                    "dialogue_rows": len(block),
                    "speakers": sorted(set(speakers)),
                    "message": "Risk: long dialogue block has no same-speaker run. This may be valid for comic spar, argument, interrogation, confession, group chaos, or route-lock negotiation, but the draft must declare its long dialogue function and pressure escalation.",
                }
            )
        elif len(block) >= 10 and changes > same * 4:
            warnings.append(
                {
                    "type": "pingpong_dominant_long_block",
                    "block_index": idx,
                    "start_line": block[0]["line_no"],
                    "end_line": block[-1]["line_no"],
                    "dialogue_rows": len(block),
                    "longest_same_speaker_run": longest_run,
                    "message": "Risk: long block is dominated by speaker alternation. Keep it only if it has a clear long dialogue function, interruption rhythm, and changed state by the end.",
                }
            )

    return {
        "path": str(path),
        "dialogue_blocks": len(blocks),
        "long_blocks_checked": sum(1 for b in blocks if len(b) >= 6),
        "warnings": warnings,
        "warning_count": len(warnings),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    result = lint(args.path)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
