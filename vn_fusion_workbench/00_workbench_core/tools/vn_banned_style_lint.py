from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = [
    ("not_x_but_y", re.compile("不是.{0,24}而是")),
    ("split_not_is", re.compile("不是[^。！？\\n]{1,40}[。！？]\\s*[（(]?[^\\n]{0,8}是")),
    ("standalone_bushi", re.compile("不是")),
    ("shibushi_filler", re.compile("是不是")),
    ("thought_is_definition", re.compile("^（.{0,12}是来|^（.{0,12}是个|^（.{0,12}是一个")),
    ("bingfei_but", re.compile("并非.{0,24}而是")),
    ("yuqishuo_buru", re.compile("与其说.{0,24}不如说")),
    ("zhenzheng_de", re.compile("真正的")),
    ("mouzhong_yiyi", re.compile("某种意义")),
    ("turan_yishidao", re.compile("突然意识到")),
    ("zhongyu_mingbai", re.compile("终于明白")),
]


def lint(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    warnings = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for name, pattern in PATTERNS:
            if pattern.search(line):
                warnings.append({"line": line_no, "type": name, "text": line})
    return {"path": str(path), "warning_count": len(warnings), "warnings": warnings}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    result = lint(args.path)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
