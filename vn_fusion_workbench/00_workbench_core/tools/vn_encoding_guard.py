from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


WORKBENCH_ROOT = Path(__file__).resolve().parents[2]
PROJECT_RE = re.compile(r"^(?:P)?(\d{1,3})$")

TEXT_EXTENSIONS = {
    ".md",
    ".json",
    ".txt",
    ".csv",
    ".py",
    ".ps1",
    ".cmd",
    ".bat",
    ".yml",
    ".yaml",
}

EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "skills_snapshot",
    "_local",
}

MOJIBAKE_MARKERS = [
    "\ufffd",
    "\u951f",
    "\u9286",
    "\u9340",
    "\u701b",
    "\u95bf",
    "\u9865",
    "\u9429",
    "\u6434\u6953",
    "\u95c6\u3126",
    "\u93ac\u8bf2",
    "\u7470\u55da",
    "\u5bee\u544a",
    "\u5bb8\u63d2",
    "\u93c2\u56e8",
    "\u934a\u6cf0",
    "\u6d60\u8bf2",
    "\u6d93\u5d84",
    "\u6fee\u50db",
    "\u677d",
    "\u9435\u3126",
    "\u7487\u8bf2",
    "\u6d5c\u3084",
    "\u20ac",
]

QUESTION_PLACEHOLDER_RE = re.compile(
    r'(^|[,:\[{]\s*)["\']?\?{2,}["\']?(\s*[,:\]}]|$)'
)
LONG_ASCII_QUESTION_RE = re.compile(r"\?{4,}")


def project_path(project_key: str | None) -> Path:
    if not project_key:
        return WORKBENCH_ROOT
    match = PROJECT_RE.match(project_key.strip())
    if not match:
        candidate = WORKBENCH_ROOT / "02_projects" / project_key
        if candidate.exists():
            return candidate
        raise SystemExit(f"Unknown project key: {project_key}")
    prefix = f"{int(match.group(1)):03d}_"
    matches = [p for p in (WORKBENCH_ROOT / "02_projects").iterdir() if p.name.startswith(prefix)]
    if not matches:
        raise SystemExit(f"Project not found: {project_key}")
    return matches[0]


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in path.parts)


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return None
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) > 3_000_000:
        return None
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def scan_text(path: Path, text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        markers = [marker for marker in MOJIBAKE_MARKERS if marker in line]
        if markers:
            findings.append(
                {
                    "path": str(path),
                    "line": lineno,
                    "kind": "mojibake-marker",
                    "markers": markers,
                    "sample": line[:220],
                }
            )
        if QUESTION_PLACEHOLDER_RE.search(line):
            findings.append(
                {
                    "path": str(path),
                    "line": lineno,
                    "kind": "question-placeholder",
                    "sample": line[:220],
                }
            )
        if LONG_ASCII_QUESTION_RE.search(line):
            findings.append(
                {
                    "path": str(path),
                    "line": lineno,
                    "kind": "long-ascii-question-placeholder",
                    "sample": line[:220],
                }
            )
    return findings


def scan_csv_structured(path: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return findings
            for index, row in enumerate(reader, 2):
                for field in ("speaker", "voice_target", "choice_target", "effects", "memory_refs"):
                    value = (row.get(field) or "").strip()
                    if value == "??" or value.startswith("???"):
                        findings.append(
                            {
                                "path": str(path),
                                "line": index,
                                "kind": "csv-placeholder-field",
                                "field": field,
                                "sample": value,
                            }
                        )
    except Exception as exc:
        findings.append(
            {
                "path": str(path),
                "line": 0,
                "kind": "csv-read-error",
                "sample": str(exc),
            }
        )
    return findings


def scan(root: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for path in root.rglob("*"):
        if should_skip(path) or not path.is_file():
            continue
        text = read_text(path)
        if text is None:
            continue
        findings.extend(scan_text(path, text))
        if path.suffix.lower() == ".csv":
            findings.extend(scan_csv_structured(path))
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan workbench-owned files for real mojibake and placeholder fields.")
    parser.add_argument("--project", help="Project key such as P017. Omit to scan the whole formal workbench.")
    parser.add_argument("--json", action="store_true", help="Print JSON findings.")
    args = parser.parse_args()

    root = project_path(args.project)
    findings = scan(root)
    if args.json:
        print(json.dumps({"root": str(root), "count": len(findings), "findings": findings}, ensure_ascii=False, indent=2))
        return
    print(f"Encoding guard root: {root}")
    print(f"Findings: {len(findings)}")
    for item in findings[:200]:
        location = f"{item['path']}:{item['line']}"
        detail = item.get("field") or ",".join(item.get("markers", []))
        print(f"- [{item['kind']}] {location} {detail} :: {item['sample']}")
    if len(findings) > 200:
        print(f"... {len(findings) - 200} more")


if __name__ == "__main__":
    main()
