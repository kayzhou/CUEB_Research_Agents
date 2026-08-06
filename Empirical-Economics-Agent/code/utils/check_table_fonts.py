"""
code/utils/check_table_fonts.py — 编译后表格字体一致性扫描

扫描 results/tables/ 下所有 .tex 片段，检查是否包含与项目全局设定
不一致的字体命令。任何违规都会报告并返回非零退出码。

用法:
    python code/utils/check_table_fonts.py                    # 默认检查 \small
    python code/utils/check_table_fonts.py --font "\footnotesize"
    python code/utils/check_table_fonts.py --dir results/tables/{project-slug}

在 master_build.py 或 latexmk 后运行，作为编译后检查的一环。
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TABLE_DIR = REPO_ROOT / "results" / "tables"
DEFAULT_FONT = r"\small"

FONT_COMMANDS = [
    r"\tiny", r"\scriptsize", r"\footnotesize", r"\small",
    r"\normalsize", r"\large", r"\Large", r"\LARGE", r"\huge", r"\Huge",
]
FONT_PATTERN = re.compile(
    r"\\(?:tiny|scriptsize|footnotesize|small|normalsize|large|Large|LARGE|huge|Huge)\b"
)


def scan_file(tex_path: Path, expected: str) -> list[str]:
    """扫描单个 .tex 文件，返回违规字体命令列表。"""
    try:
        content = tex_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = tex_path.read_text(encoding="gbk")

    found = FONT_PATTERN.findall(content)
    return [f for f in found if f != expected]


def main() -> int:
    parser = argparse.ArgumentParser(description="检查表格 .tex 片段字体一致性")
    parser.add_argument("--font", default=DEFAULT_FONT,
                        help=f"期望的表格字体（默认: {DEFAULT_FONT}）")
    parser.add_argument("--dir", type=Path, default=DEFAULT_TABLE_DIR,
                        help=f"表格目录（默认: {DEFAULT_TABLE_DIR}）")
    args = parser.parse_args()

    table_dir = args.dir
    expected = args.font

    if not table_dir.is_dir():
        print(f"SKIP: {table_dir} 不存在，无需检查")
        return 0

    tex_files = list(table_dir.rglob("*.tex"))
    if not tex_files:
        print("OK: 无 .tex 表格文件，跳过检查")
        return 0

    violations: list[tuple[Path, list[str]]] = []
    for tex_file in tex_files:
        bad = scan_file(tex_file, expected)
        if bad:
            violations.append((tex_file, bad))

    if violations:
        print(f"FONT VIOLATIONS (expected {expected}):")
        for path, fonts in violations:
            rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
            unique = list(dict.fromkeys(fonts))
            print(f"  {rel}: 发现 {unique}")
        print(f"\n共 {len(violations)} 个文件存在字体不一致。")
        print(f"修复: 将所有表格统一为 {expected}，或更新 journal_style.do 的 TABLE_FONT。")
        return 1

    print(f"OK: 全部 {len(tex_files)} 个表格文件使用 {expected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
