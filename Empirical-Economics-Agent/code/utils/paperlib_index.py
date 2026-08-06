"""
code/utils/paperlib_index.py — 知识库（paper-lib）索引生成与检索工具

paper-lib/ 存放目标期刊的已发表论文 PDF（如《管理世界》各年各期）。
本脚本扫描全部 PDF，从目录名解析期刊/年份/期号、从文件名解析标题，
生成 paper-lib/index.csv，供 M1 文献调研、M4 写作风格参考、M5 质量评估检索。

用法：
    # 重建索引
    python code/utils/paperlib_index.py --build

    # 按关键词检索（匹配标题，多个关键词为 AND 关系）
    python code/utils/paperlib_index.py --search 数字化 转型
    python code/utils/paperlib_index.py --search 双重差分 --year 2024
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from code.config import PATHS

PAPER_LIB = PATHS["paper_lib"]
INDEX_CSV = PAPER_LIB / "index.csv"
FIELDS = ["journal", "year", "issue", "title", "path"]


def parse_meta(pdf: Path) -> dict[str, str]:
    """从相对路径解析期刊、年份、期号；标题即文件名（去扩展名）。"""
    rel = pdf.relative_to(PAPER_LIB)
    journal = rel.parts[0] if len(rel.parts) > 1 else ""
    year, issue = "", ""
    for part in rel.parts[:-1]:
        m = re.search(r"(\d{4})年(?:(\d{1,2})期)?", part)
        if m:
            year = m.group(1)
            if m.group(2):
                issue = m.group(2)
    # 形如「管理世界2025年1期.pdf」的合刊 PDF，从文件名再解析一次
    m = re.search(r"(\d{4})年(\d{1,2})期", pdf.stem)
    if m:
        year, issue = m.group(1), m.group(2)
    return {
        "journal": journal,
        "year": year,
        "issue": issue,
        "title": pdf.stem,
        "path": str(rel),
    }


def build_index() -> int:
    rows = sorted(
        (parse_meta(p) for p in PAPER_LIB.rglob("*.pdf")),
        key=lambda r: (r["journal"], r["year"], r["issue"].zfill(2), r["title"]),
    )
    with INDEX_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[paperlib_index] 已索引 {len(rows)} 篇 → {INDEX_CSV}")
    return len(rows)


def search(keywords: list[str], year: str | None) -> None:
    if not INDEX_CSV.exists():
        print("索引不存在，先运行 --build")
        sys.exit(1)
    with INDEX_CSV.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    hits = [
        r for r in rows
        if all(k in r["title"] for k in keywords)
        and (year is None or r["year"] == year)
    ]
    for r in hits:
        print(f"{r['journal']} {r['year']}年{r['issue']}期 | {r['title']}")
        print(f"    paper-lib/{r['path']}")
    print(f"\n共 {len(hits)} 篇命中（索引总量 {len(rows)} 篇）")


def main() -> None:
    parser = argparse.ArgumentParser(description="paper-lib 索引生成与检索")
    parser.add_argument("--build", action="store_true", help="重建 index.csv")
    parser.add_argument("--search", nargs="+", metavar="KW", help="按标题关键词检索（AND）")
    parser.add_argument("--year", help="限定年份，如 2024")
    args = parser.parse_args()
    if args.build:
        build_index()
    elif args.search:
        search(args.search, args.year)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
