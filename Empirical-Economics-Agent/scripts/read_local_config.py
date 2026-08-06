#!/usr/bin/env python3
"""Read and validate machine-local tool paths for activation scripts."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "local-tools.json"
TOOL_KEYS = {
    "python_env",
    "r_bin",
    "texlive_bin",
    "matlab_root",
    "stata_cli",
}
METADATA_KEYS = {"$schema", "$comment"}


def load_config(path: Path) -> dict[str, Any]:
    """Load a local config and enforce the shared schema's basic contract."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("local-tools.json 顶层必须是 JSON 对象")

    unknown = sorted(set(data) - TOOL_KEYS - METADATA_KEYS)
    if unknown:
        raise ValueError(f"local-tools.json 含未知字段：{', '.join(unknown)}")

    missing = sorted(TOOL_KEYS - set(data))
    if missing:
        raise ValueError(f"local-tools.json 缺少字段：{', '.join(missing)}")

    for key in TOOL_KEYS | (set(data) & METADATA_KEYS):
        if not isinstance(data[key], str):
            raise TypeError(f"{key} 必须是字符串")
    return data


def expanded(value: str) -> str:
    """Expand user and environment markers without resolving missing paths."""
    return os.path.expandvars(os.path.expanduser(value))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="读取 config/local-tools.json 的单个字段，或验证完整配置。"
    )
    parser.add_argument("key", nargs="?", choices=sorted(TOOL_KEYS))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    path = Path(os.path.expandvars(args.config)).expanduser()
    if not path.exists():
        if args.validate:
            print(f"ERROR: 配置不存在：{path}", file=sys.stderr)
            return 1
        return 0

    try:
        data = load_config(path)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"ERROR: 无法读取 {path}：{exc}", file=sys.stderr)
        return 2

    if args.validate:
        print(f"配置有效：{path}")
        return 0
    if args.key is None:
        parser.error("请提供字段名，或使用 --validate")
    print(expanded(data[args.key]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
