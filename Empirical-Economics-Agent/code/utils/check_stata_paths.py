"""
脚本名称：utils_check_stata_paths.py
用途说明：扫描 .do 文件中未加引号的盘符路径，防止 "command X not defined by X.ado" 错误
输入文件：一个或多个 .do 文件或目录
输出文件：无（stdout 报告 + 非零退出码表示发现问题）
方法来源：自建——基于 Stata for Windows 已知解析行为
关键决策：仅检查 Stata 路径命令（do/include/cd/use/save/log using/esttab using/graph export 等）
作者：    日期：2026-05-29
"""

import re
import sys
from pathlib import Path

# Stata 命令（接收路径参数的命令，按危险程度排序）
# 格式: (命令名, 路径在第几个参数位, 是否必须在行首检测)
PATH_COMMANDS = [
    # 最危险的——路径在行首被解析为命令名
    ("do", 1),
    ("include", 1),
    ("run", 1),
    ("cd", 1),
    # 次危险——盘符虽然不在行首，但 do/run/include 本身就能触发
    ("use", 1),
    ("save", 1),
    ("log using", 2),  # "log using path", not "log"
    ("esttab using", 2),
    ("estout using", 2),
    ("graph export", 2),
    ("graph save", 2),
    ("graph use", 2),
    ("estimates save", 2),
    ("estimates use", 2),
    ("import delimited using", 3),
    ("import excel using", 3),
    ("export delimited using", 3),
    ("export excel using", 3),
    ("append using", 2),
    ("merge using", 2),
    ("joinby using", 2),
    ("cross using", 2),
]

# 检测盘符 + 路径的模式
DRIVE_PATH_RE = re.compile(r'[A-Za-z]:[/\\]')


def strip_comments(line: str) -> str:
    """移除 Stata 注释，返回可检查的代码部分。"""
    # 整行注释
    if line.strip().startswith("*"):
        return ""
    # // 注释（不在字符串内的）
    if "//" in line:
        line = line[: line.index("//")]
    # /* 注释 */
    while "/*" in line:
        start = line.index("/*")
        end = line.find("*/", start + 2)
        if end == -1:
            line = line[:start]
        else:
            line = line[:start] + line[end + 2:]
    return line


def line_has_quoted_path(line: str, path_start_col: int) -> bool:
    """检查从 path_start_col 开始的位置是否在双引号内。"""
    # 简化逻辑：检查 path_start_col 之前是否有奇数个未转义的双引号
    before = line[:path_start_col]
    in_quote = False
    i = 0
    while i < len(before):
        if before[i] == '"' and (i == 0 or before[i - 1] != '`'):
            in_quote = not in_quote
        i += 1
    return in_quote


def check_file(filepath: Path) -> list[str]:
    """检查单个 .do 文件，返回问题列表。"""
    issues: list[str] = []
    try:
        lines = filepath.read_text(encoding="utf-8").split("\n")
    except UnicodeDecodeError:
        try:
            lines = filepath.read_text(encoding="gbk").split("\n")
        except Exception:
            issues.append(f"{filepath}: 无法读取文件（编码错误）")
            return issues

    in_block_comment = False

    for lineno, raw_line in enumerate(lines, 1):
        # 处理 /* */ 跨行注释
        if in_block_comment:
            if "*/" in raw_line:
                in_block_comment = False
            continue
        if "/*" in raw_line and "*/" not in raw_line:
            in_block_comment = True
            continue

        line = strip_comments(raw_line)
        if not line.strip():
            continue

        # 检查每个命令
        for cmd, path_pos in PATH_COMMANDS:
            # 在行中查找命令
            cmd_pattern = re.compile(r'(?:^|\s)' + re.escape(cmd) + r'\s+', re.IGNORECASE)
            for m in cmd_pattern.finditer(line):
                # 获取命令后的参数
                after_cmd = line[m.end():].strip()

                # 如果参数以引号开头，跳过
                if after_cmd.startswith('"'):
                    continue

                # 如果参数使用宏引用且带引号，跳过
                # "$macro" 形式
                if after_cmd.startswith('$'):
                    # 检查整个表达式是否被引号包裹
                    continue  # 使用宏通常已经在 config 里加了引号

                # 如果参数以 ` 开头（local macro），跳过
                if after_cmd.startswith('`'):
                    continue

                # 检查参数中是否有盘符路径
                drive_match = DRIVE_PATH_RE.search(after_cmd)
                if drive_match:
                    pos = m.start() + len(cmd) + 1 + drive_match.start()
                    if not line_has_quoted_path(line, pos):
                        # 提取路径片段用于报告
                        path_fragment = after_cmd[:80].rstrip()
                        issues.append(
                            f"{filepath.name}:{lineno} — "
                            f"{cmd} {path_fragment}\n"
                            f"  → 应改为 {cmd} \"{path_fragment.split()[0]}\" ..."
                        )
                        break  # 该命令只报告一次

    return issues


def main():
    if len(sys.argv) < 2:
        print("用法: python check_stata_paths.py <file.do|dir/> [...]")
        sys.exit(1)

    targets = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.do")))
        elif p.is_file():
            targets.append(p)
        else:
            print(f"跳过（不存在）: {arg}")

    if not targets:
        print("未找到 .do 文件")
        sys.exit(0)

    all_issues: list[str] = []
    for fp in targets:
        issues = check_file(fp)
        all_issues.extend(issues)

    if all_issues:
        print(f"\n发现 {len(all_issues)} 个路径引号问题:\n")
        for issue in all_issues:
            print(f"  ⚠️  {issue}\n")
        print(
            f"共 {len(all_issues)} 个问题。"
            "请在运行脚本前给所有盘符路径加上双引号。"
        )
        print("详细规则见 code/config/config.do 头部的 Windows 路径引用规则")
        sys.exit(1)

    print(f"检查通过 ✓（{len(targets)} 个 .do 文件）")
    sys.exit(0)


if __name__ == "__main__":
    main()
