"""
脚本名称：utils_dependency_check.py
用途说明：根据 dependency_manifest.yaml，当脚本变更时列出受影响的下游输出
输入文件：code/config/dependency_manifest.yaml
输出文件：无（stdout 报告）
方法来源：自建
作者：    日期：2026-05-29
"""

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parents[2]
MANIFEST_PATH = PROJECT_ROOT / "code" / "config" / "dependency_manifest.yaml"


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        print(f"Manifest 不存在: {MANIFEST_PATH}")
        print("请先创建 code/config/dependency_manifest.yaml")
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def find_affected(manifest: dict, changed: str) -> list[str]:
    """找出受变更影响的所有输出文件。"""
    outputs = manifest.get("outputs") or {}
    affected: list[str] = []

    for output_path, entry in outputs.items():
        script = entry.get("script", "")
        upstream = entry.get("upstream", [])

        # 检查是否是直接变更的脚本，或上游依赖中包含变更的脚本
        if script == changed or changed in upstream:
            affected.append(output_path)
            # 递归：该输出可能会影响更下游
            deeper = find_affected(manifest, script)
            affected.extend(deeper)

    return sorted(set(affected))


def main():
    if len(sys.argv) < 2:
        print("用法: python dependency_check.py --changed <script_path>")
        print("      python dependency_check.py --list                    # 列出全部依赖")
        sys.exit(1)

    manifest = load_manifest()
    if not manifest:
        sys.exit(1)

    outputs = manifest.get("outputs") or {}

    if "--list" in sys.argv:
        print(f"已登记 {len(outputs)} 条依赖:\n")
        for out_path, entry in outputs.items():
            script = entry.get("script", "?")
            inputs = entry.get("inputs", [])
            print(f"  {out_path}")
            print(f"    ← {script}")
            for inp in inputs:
                print(f"      ← {inp}")
            print()
        sys.exit(0)

    if "--changed" in sys.argv:
        idx = sys.argv.index("--changed")
        if idx + 1 >= len(sys.argv):
            print("错误：--changed 后必须提供脚本路径。")
            sys.exit(2)
        changed = sys.argv[idx + 1]
        affected = find_affected(manifest, changed)

        if not affected:
            print(f"变更 '{changed}' 不影响任何已登记的输出。")
        else:
            print(f"变更 '{changed}' 影响以下 {len(affected)} 个输出文件需要重跑:")
            for f in affected:
                print(f"  {f}")
        sys.exit(0)


if __name__ == "__main__":
    main()
