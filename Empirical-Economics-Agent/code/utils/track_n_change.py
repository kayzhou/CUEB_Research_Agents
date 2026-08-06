"""
code/utils/track_n_change.py — 样本筛选 N-change 自动追踪

从清洗/构建日志中提取每步前后的观测数变化，生成 sample-construction-log.md
的 N-change 表格，替代手工复制粘贴。

用法：
    python code/utils/track_n_change.py --log-dir results/logs/
    python code/utils/track_n_change.py --log results/logs/clean_stock.log --output data/processed/n-change.md

日志中需包含标准格式的观测数输出（本脚本识别以下模式）：
    Stata:  "N before: XXXX" / "N after: XXXX" 或 "Observations: XXXX"
    Python: "n_before=XXXX" / "n_after=XXXX" 或 "rows: XXXX"
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# 匹配观测数的正则模式
N_PATTERNS = [
    re.compile(r"N\s*(?:before|after)\s*[:=]\s*([\d,]+)", re.IGNORECASE),
    re.compile(r"(?:Observations|obs)\s*[:=]\s*([\d,]+)", re.IGNORECASE),
    re.compile(r"n_(?:before|after)\s*=\s*(\d+)", re.IGNORECASE),
    re.compile(r"(?:rows|samples?)\s*[:=]\s*([\d,]+)", re.IGNORECASE),
    re.compile(r"保留观测[：:]\s*([\d,]+)"),
    re.compile(r"剔除观测[：:]\s*([\d,]+)"),
]


def parse_number(s: str) -> int:
    return int(s.replace(",", ""))


def extract_n_changes(log_path: Path) -> list[dict]:
    """从单个日志文件提取观测数变化序列。"""
    try:
        content = log_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = log_path.read_text(encoding="gbk", errors="replace")

    numbers = []
    for line in content.splitlines():
        for pat in N_PATTERNS:
            m = pat.search(line)
            if m:
                numbers.append(parse_number(m.group(1)))
                break

    if len(numbers) < 2:
        return []

    changes = []
    for i in range(0, len(numbers) - 1, 2):
        before = numbers[i]
        after = numbers[i + 1] if i + 1 < len(numbers) else None
        if after is not None:
            changes.append({"before": before, "after": after, "diff": before - after})

    return changes


def generate_table(log_dir: Path) -> str:
    """生成 N-change markdown 表格。"""
    log_files = sorted(log_dir.rglob("*.log"))
    if not log_files:
        return "无日志文件，无法生成 N-change 表。\n"

    rows = []
    for lf in log_files:
        changes = extract_n_changes(lf)
        for i, ch in enumerate(changes):
            rows.append(
                f"| {lf.stem} | 步骤 {i+1} | {ch['before']:,} | {ch['after']:,} "
                f"| -{ch['diff']:,} |"
            )

    if not rows:
        # 回退：如果在日志中没找到标准 N-change 标记
        return (
            "_未在日志中找到标准观测数标记。_\n\n"
            "请确保清洗脚本按以下格式输出观测数：\n"
            "- Stata: `display \"N before: \" _N` / `display \"N after: \" _N`\n"
            "- Python: `print(f\"n_before={len(df)}\")` / `print(f\"n_after={len(df)}\")`\n"
        )

    header = (
        "| 日志文件 | 步骤 | 筛选前 | 筛选后 | 丢失 |\n"
        "|---|---:|---:|---:|---:|\n"
    )
    return header + "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从清洗日志提取 N-change 表格"
    )
    parser.add_argument(
        "--log-dir", type=Path,
        default=REPO_ROOT / "results" / "logs",
        help="日志文件目录（默认: results/logs/）"
    )
    parser.add_argument(
        "--log", type=Path, nargs="*",
        help="指定单个或多个日志文件"
    )
    parser.add_argument(
        "--output", type=Path,
        help="输出 markdown 文件路径（默认: 打印到 stdout）"
    )
    args = parser.parse_args()

    if args.log:
        log_files = args.log
        table = ""
        for lf in log_files:
            if lf.exists():
                changes = extract_n_changes(lf)
                for i, ch in enumerate(changes):
                    table += (
                        f"| {lf.stem} | 步骤 {i+1} | {ch['before']:,} "
                        f"| {ch['after']:,} | -{ch['diff']:,} |\n"
                    )
        if not table:
            table = generate_table(Path("."))
    else:
        table = generate_table(args.log_dir)

    if args.output:
        args.output.write_text(table, encoding="utf-8")
        print(f"N-change 表已写入 {args.output}")
    else:
        print(table)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
