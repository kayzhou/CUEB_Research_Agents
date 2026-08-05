"""
脚本名称：utils/experiment_summary.py
用途说明：读取 system/experiments.jsonl 并输出汇总统计
输入文件：system/experiments.jsonl
输出文件：打印汇总报告到 stdout
方法来源：V3.0 结构化实验日志协议
关键决策：按 outcome_code 分类统计、按 method 分组、追踪 champion 提升
作者：V3.0 模板  日期：2026-06-07
"""

import json
import sys
from collections import Counter
from pathlib import Path

# Windows 控制台编码兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_log():
    path = PROJECT_ROOT / "system" / "experiments.jsonl"
    if not path.exists():
        print("⚠ system/experiments.jsonl 尚未由 M3 运行创建，跳过汇总。")
        return []
    experiments = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    experiments.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return experiments


def summarize(experiments):
    if not experiments:
        print("⚠ 无实验记录。")
        return

    total = len(experiments)
    outcomes = Counter(e.get("outcome_code", "?") for e in experiments)
    methods = Counter(e.get("method", "?") for e in experiments)
    keeps = [e for e in experiments if e.get("outcome_code") == "KEEP"]
    preferred = [e for e in experiments if e.get("is_preferred")]

    print(f"实验日志汇总")
    print(f"============")
    print(f"总实验数: {total}")
    print(f"KEEP: {outcomes.get('KEEP', 0)}  DISCARD: {outcomes.get('DISCARD', 0)}  FRAGILE: {outcomes.get('FRAGILE', 0)}")
    print(f"首选规格数: {len(preferred)}")
    print()

    if methods:
        print("按方法分布:")
        for method, count in methods.most_common():
            print(f"  {method}: {count}")

    if keeps:
        print()
        print("KEEP 记录:")
        for k in keeps[-10:]:  # 最近 10 条
            eid = k.get("exp_id", "?")
            method = k.get("method", "?")
            coef = k.get("coef", "?")
            band = k.get("specification_band", "?")
            print(f"  {eid} | {method} | coef={coef} | band={band}")


def main():
    experiments = load_log()
    summarize(experiments)


if __name__ == "__main__":
    main()
