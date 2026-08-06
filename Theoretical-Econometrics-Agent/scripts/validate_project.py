#!/usr/bin/env python3
"""Static integrity checks for the complete framework distribution."""

from __future__ import annotations

import fnmatch
import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    "m1-model-specification": "M1-model-specification",
    "m2-literature-positioning": "M2-literature-positioning",
    "m3-qml-estimation": "M3-qml-estimation",
    "m4-asymptotic-theory": "M4-asymptotic-theory",
    "m5-monte-carlo": "M5-monte-carlo",
    "m6-paper-writing": "M6-paper-writing",
    "m7-referee-revision": "M7-referee-revision",
}
REQUIRED = [
    "LICENSE",
    "README.md",
    "ORCHESTRATOR.md",
    "ENVIRONMENT.md",
    "使用手册.md",
    "本地化部署说明.md",
    "requirements.txt",
    "requirements-lock.txt",
    ".gitignore",
    ".cursor/rules/theoretical-econometrics-agent.mdc",
    "agents/researcher.md",
    "agents/referee.md",
    "config/local-tools.example.json",
    "config/local-tools.schema.json",
    "projects/.gitkeep",
    "scripts/setup_env.sh",
    "scripts/setup_env.ps1",
    "scripts/check_environment.py",
    "scripts/configure_local.py",
    "scripts/init_project.py",
    "templates/paper-project/README.md",
    "templates/paper-project/paper/main.tex",
    "modules/M1-model-specification/templates/model-specification.yaml",
    "modules/M1-model-specification/templates/notation-registry.md",
    "modules/M2-literature-positioning/templates/literature-matrix.csv",
    "modules/M3-qml-estimation/templates/qml-derivation.md",
    "modules/M4-asymptotic-theory/templates/assumptions-checklist.md",
    "modules/M4-asymptotic-theory/templates/theorem-registry.md",
    "modules/M4-asymptotic-theory/templates/proof-blueprint.md",
    "modules/M5-monte-carlo/templates/simulation-design.yaml",
    "modules/M7-referee-revision/templates/referee-report.md",
    "modules/M7-referee-revision/templates/reviewer-rubrics.md",
    "modules/M7-referee-revision/templates/final-review.md",
]
STALE_PATTERNS = [
    "theoretical-econometrics-skill-vscode",
    "theoretical-econometrics-skill-package",
    ".github/skills/theoretical-econometrics-research",
]
LATEX_GENERATED_PATTERNS = (
    "*.acn",
    "*.acr",
    "*.alg",
    "*.aux",
    "*.bbl",
    "*.bcf",
    "*.blg",
    "*.dvi",
    "*.fdb_latexmk",
    "*.fls",
    "*.glg",
    "*.glo",
    "*.gls",
    "*.idx",
    "*.ilg",
    "*.ind",
    "*.ist",
    "*.lof",
    "*.log",
    "*.lot",
    "*.maf",
    "*.mtc*",
    "*.nav",
    "*.out",
    "*.ps",
    "*.run.xml",
    "*.snm",
    "*.synctex*",
    "*.toc",
    "*.vrb",
    "*.xdv",
    "*.pdf",
)
LOCAL_ONLY_RELATIVE_PATHS = {
    Path(".cursor/mcp.json"),
    Path("config/local-tools.json"),
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED:
        if not (ROOT / relative).exists():
            fail(errors, f"缺少必需文件：{relative}")

    for skill, module in MODULES.items():
        skill_file = ROOT / ".cursor" / "skills" / skill / "SKILL.md"
        module_file = ROOT / "modules" / module / "MODULE.md"
        if not skill_file.exists():
            fail(errors, f"缺少 Skill：{skill_file.relative_to(ROOT)}")
        if not module_file.exists():
            fail(errors, f"缺少 Module：{module_file.relative_to(ROOT)}")
        if skill_file.exists():
            text = skill_file.read_text(encoding="utf-8")
            match = re.search(r"^name:\s*(.+)$", text, flags=re.MULTILINE)
            if not match or match.group(1).strip().strip("\"'") != skill:
                fail(errors, f"Skill name 与目录不一致：{skill}")

    for path in (ROOT / "scripts" / "mcp").glob("*.json.example"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"MCP JSON 无效：{path.relative_to(ROOT)}：{exc}")
    for path in (ROOT / "config").glob("*.json"):
        if path.name == "local-tools.json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"配置 JSON 无效：{path.relative_to(ROOT)}：{exc}")

    for path in (ROOT / "scripts").glob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(errors, f"Python 语法错误：{path.relative_to(ROOT)}：{exc.msg}")

    duplicate_latex = ROOT / "modules" / "M6-paper-writing" / "templates" / "latex"
    if duplicate_latex.exists():
        fail(errors, "M6 LaTeX 模板必须只有 templates/paper-project/paper/ 一个真源")

    text_extensions = {".md", ".mdc", ".py", ".sh", ".ps1", ".json"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        lower_name = path.name.lower()
        if path.name == ".DS_Store" or "%20" in path.name:
            fail(errors, f"未清理的文件名：{relative}")
        if path.suffix.lower() in {".zip"}:
            fail(errors, f"发行目录不应包含压缩包：{relative}")
        if any(fnmatch.fnmatch(lower_name, pattern) for pattern in LATEX_GENERATED_PATTERNS):
            fail(errors, f"发行目录不应包含 LaTeX/PDF 生成物：{relative}")
        if relative in LOCAL_ONLY_RELATIVE_PATHS or lower_name == "local-tools.json":
            fail(errors, f"发行目录不应包含本机配置：{relative}")
        if path.suffix.lower() not in text_extensions:
            continue
        if path == Path(__file__).resolve():
            continue
        if "paper-lib" in path.parts and path.name == "spatial-panel-break-skill-reference.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in STALE_PATTERNS:
            if pattern in text:
                fail(errors, f"旧路径引用 {pattern}：{path.relative_to(ROOT)}")
        if path.suffix.lower() in {".md", ".mdc"}:
            for raw_link in MARKDOWN_LINK.findall(text):
                link = raw_link.split("#", 1)[0].split("?", 1)[0].strip()
                if (
                    not link
                    or "://" in link
                    or link.startswith(("mailto:", "#"))
                    or "{" in link
                ):
                    continue
                target = (path.parent / link).resolve()
                if not target.exists():
                    fail(
                        errors,
                        f"Markdown 本地链接失效：{path.relative_to(ROOT)} -> {raw_link}",
                    )

    if errors:
        print("项目校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("项目静态完整性校验通过。")
    print(f"- Modules/Skills: {len(MODULES)}/{len(MODULES)}")
    print("- Python scripts: syntax OK")
    print("- Config/MCP examples: JSON OK")
    print("- Required files, release artifacts, and stale-path scan: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
