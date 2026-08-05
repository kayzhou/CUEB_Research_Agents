#!/usr/bin/env python3
"""Create config/local-tools.json from explicit paths or PATH discovery."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "config" / "local-tools.json"


def executable_dir(*names: str) -> str:
    for name in names:
        found = shutil.which(name)
        if found:
            # Keep the directory exposed on PATH. Resolving TeX Live wrapper
            # symlinks can jump into texmf-dist/scripts, which is not a bin dir.
            return str(Path(found).absolute().parent)
    return ""


def executable_path(*names: str) -> str:
    for name in names:
        found = shutil.which(name)
        if found:
            return str(Path(found).absolute())
    return ""


def discover_matlab_root() -> str:
    found = shutil.which("matlab")
    if not found:
        return ""
    path = Path(found).resolve()
    return str(path.parent.parent) if path.parent.name.lower() == "bin" else ""


def default_python_env() -> str:
    local = REPO_ROOT / ".venv"
    if local.exists():
        return str(local.resolve())
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return str(Path(sys.prefix).resolve())
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="生成本机工具路径配置；未指定的字段自动从 PATH 探测。"
    )
    parser.add_argument("--python-env", default=None)
    parser.add_argument("--r-bin", default=None)
    parser.add_argument("--texlive-bin", default=None)
    parser.add_argument("--matlab-root", default=None)
    parser.add_argument("--stata-cli", default=None)
    parser.add_argument("--octave-cli", default=None)
    parser.add_argument("--pandoc-cli", default=None)
    parser.add_argument("--force", action="store_true", help="覆盖已有配置")
    args = parser.parse_args()

    if OUTPUT.exists() and not args.force:
        print(f"ERROR: {OUTPUT} 已存在；确认覆盖时加 --force。", file=sys.stderr)
        return 1

    config = {
        "$schema": "./local-tools.schema.json",
        "$comment": "本机生成的绝对路径配置；不提交版本库。",
        "python_env": args.python_env if args.python_env is not None else default_python_env(),
        "r_bin": args.r_bin if args.r_bin is not None else executable_dir("Rscript", "Rscript.exe"),
        "texlive_bin": (
            args.texlive_bin
            if args.texlive_bin is not None
            else executable_dir("latexmk", "latexmk.exe", "pdflatex", "pdflatex.exe")
        ),
        "matlab_root": (
            args.matlab_root if args.matlab_root is not None else discover_matlab_root()
        ),
        "stata_cli": (
            args.stata_cli
            if args.stata_cli is not None
            else executable_path(
                "stata-mp",
                "stata-se",
                "stata",
                "StataMP-64.exe",
                "StataSE-64.exe",
                "StataBE-64.exe",
                "Stata-64.exe",
                "StataMP.exe",
                "StataSE.exe",
                "StataBE.exe",
                "Stata.exe",
            )
        ),
        "octave_cli": (
            args.octave_cli
            if args.octave_cli is not None
            else executable_path("octave-cli", "octave", "octave-cli.exe", "octave.exe")
        ),
        "pandoc_cli": (
            args.pandoc_cli
            if args.pandoc_cli is not None
            else executable_path("pandoc", "pandoc.exe")
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(config, ensure_ascii=False, indent=2) + os.linesep, encoding="utf-8")
    print(f"已写入：{OUTPUT}")
    for key, value in config.items():
        if not key.startswith("$"):
            print(f"  {key:13}: {value or '(未探测到，可手工填写)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
