#!/usr/bin/env python3
"""Cross-platform environment diagnostics for local installations."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG = REPO_ROOT / "config" / "local-tools.json"
PYTHON_MODULES = {
    "numpy": "numpy",
    "scipy": "scipy",
    "pandas": "pandas",
    "statsmodels": "statsmodels",
    "linearmodels": "linearmodels",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "PyYAML": "yaml",
    "python-docx": "docx",
    "pypdf": "pypdf",
    "reportlab": "reportlab",
    "mcp": "mcp",
}


def load_config() -> dict[str, str]:
    if not CONFIG.exists():
        return {}
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    return {key: value for key, value in data.items() if isinstance(value, str)}


def first_executable(configured: str, *names: str) -> str:
    if configured:
        path = Path(configured).expanduser()
        if path.is_dir():
            for name in names:
                candidate = path / name
                if candidate.is_file():
                    return str(candidate)
        elif path.is_file():
            return str(path)
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return ""


def version(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"ERROR: {exc}"
    text = (result.stdout or result.stderr).strip().splitlines()
    return text[0] if text else f"exit={result.returncode}"


def status(ok: bool) -> str:
    return "OK" if ok else "MISSING"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Python 依赖、R、latexmk/pdflatex 任一缺失时返回非零状态",
    )
    args = parser.parse_args()
    config = load_config()
    failures: list[str] = []

    print("Theoretical-Econometrics-Agent 环境检查")
    print(f"Repository : {REPO_ROOT}")
    print(f"Platform   : {sys.platform}")
    print(f"Config     : {CONFIG if CONFIG.exists() else '(未创建，使用 PATH 自动探测)'}")
    print(f"Python     : {sys.executable}")
    print(f"Version    : {sys.version.split()[0]}")
    print(f"Virtualenv : {sys.prefix != getattr(sys, 'base_prefix', sys.prefix)}")

    missing_modules = []
    for label, module in PYTHON_MODULES.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(label)
    print(f"Python deps: {status(not missing_modules)}")
    if missing_modules:
        print(f"  缺少：{', '.join(missing_modules)}")
        failures.append("Python dependencies")

    rscript = first_executable(
        config.get("r_bin", ""), "Rscript.exe" if os.name == "nt" else "Rscript", "Rscript"
    )
    print(f"Rscript    : {rscript or 'MISSING'}")
    if rscript:
        print(f"  {version([rscript, '--version'])}")
    else:
        failures.append("Rscript")

    tex_bin = config.get("texlive_bin", "")
    latexmk = first_executable(tex_bin, "latexmk.exe" if os.name == "nt" else "latexmk", "latexmk")
    pdflatex = first_executable(
        tex_bin, "pdflatex.exe" if os.name == "nt" else "pdflatex", "pdflatex"
    )
    xelatex = first_executable(
        tex_bin, "xelatex.exe" if os.name == "nt" else "xelatex", "xelatex"
    )
    print(f"latexmk    : {latexmk or 'MISSING'}")
    print(f"pdflatex   : {pdflatex or 'MISSING'}")
    print(f"xelatex    : {xelatex or 'MISSING'}")
    if not (latexmk and pdflatex):
        failures.append("TeX Live")

    matlab_root = config.get("matlab_root", "")
    matlab = first_executable(
        str(Path(matlab_root) / "bin") if matlab_root else "",
        "matlab.exe" if os.name == "nt" else "matlab",
        "matlab",
    )
    octave = first_executable(
        config.get("octave_cli", ""),
        "octave-cli.exe" if os.name == "nt" else "octave-cli",
        "octave.exe" if os.name == "nt" else "octave",
        "octave",
    )
    stata_names = (
        (
            "StataMP-64.exe",
            "StataSE-64.exe",
            "StataBE-64.exe",
            "Stata-64.exe",
            "StataMP.exe",
            "StataSE.exe",
            "StataBE.exe",
            "Stata.exe",
        )
        if os.name == "nt"
        else ("stata-mp", "stata-se", "stata")
    )
    stata = first_executable(config.get("stata_cli", ""), *stata_names)
    pandoc = first_executable(config.get("pandoc_cli", ""), "pandoc.exe" if os.name == "nt" else "pandoc")
    print(f"MATLAB     : {matlab or 'not configured (optional)'}")
    print(f"Octave     : {octave or 'not configured (optional)'}")
    print(f"Stata      : {stata or 'not configured (optional)'}")
    print(f"Pandoc     : {pandoc or 'not configured (optional)'}")

    if failures:
        print("\n需要处理：" + "、".join(failures))
        print("安装与路径配置见《使用手册》“本地迁移”章节和 ENVIRONMENT.md。")
        return 1 if args.strict else 0
    print("\n核心环境检查通过。MATLAB、Stata、Octave、Pandoc 按研究需要选装。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
