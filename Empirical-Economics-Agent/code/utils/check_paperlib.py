"""Check whether the local paper-lib PDFs match index.csv."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from code.config import PATHS

PAPER_LIB = PATHS["paper_lib"]
INDEX = PAPER_LIB / "index.csv"


def main() -> int:
    if not INDEX.exists():
        print("[FAIL] paper-lib/index.csv 不存在；先运行 paperlib_index.py --build。")
        return 1

    with INDEX.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "path" not in reader.fieldnames:
            print("[FAIL] paper-lib/index.csv 缺少 path 列。")
            return 1
        rows = list(reader)

    if not rows:
        print("[BLOCKED] paper-lib/index.csv 为空，知识库尚未同步或建立索引。")
        return 1

    missing = [row["path"] for row in rows if not (PAPER_LIB / row["path"]).is_file()]
    pdf_count = sum(1 for _ in PAPER_LIB.rglob("*.pdf"))

    print(f"索引记录: {len(rows)}")
    print(f"本地 PDF: {pdf_count}")
    print(f"索引缺失文件: {len(missing)}")
    if pdf_count == 0:
        print("[BLOCKED] 本地没有 PDF，不能执行原文核对。")
        return 1
    if missing:
        for path in missing[:10]:
            print(f"  - {path}")
        if len(missing) > 10:
            print(f"  ... 另有 {len(missing) - 10} 个")
        print("[BLOCKED] 不能执行要求回 PDF 原文核对的任务。")
        return 1

    print("[OK] paper-lib 已就绪，索引与本地 PDF 一致。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
