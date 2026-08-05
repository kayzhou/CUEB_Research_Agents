"""
code/config/config.py
Python 全局路径配置（对应 Stata 的 config.do）

从仓库根运行脚本，统一使用：
    from code.config import REPO_ROOT, PATHS, PROJECT_SLUG, TOOLS
"""

from pathlib import Path
import os

# ── 仓库根目录（自动推断，不依赖绝对路径）
REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_SLUG = os.environ.get("PROJECT_SLUG", "a-share-multifactor-pricing")
TOOLS_ROOT = Path(
    os.environ.get("EEA_TOOLS_ROOT", REPO_ROOT.parent / "tools")
).expanduser()
_DEFAULT_PYTHON_ENV = (
    REPO_ROOT / ".venv"
    if (REPO_ROOT / ".venv").is_dir()
    else TOOLS_ROOT / "py_env"
)
PYTHON_ENV = Path(
    os.environ.get("EEA_PYTHON_ENV", _DEFAULT_PYTHON_ENV)
).expanduser()
R_BIN = Path(
    os.environ.get("EEA_R_BIN", TOOLS_ROOT / "R" / "bin")
).expanduser()
TEXLIVE_BIN = Path(
    os.environ.get("EEA_TEXLIVE_BIN", "/usr/local/texlive/2026/bin/x86_64-linux")
).expanduser()

# ── 数据层路径（与 Stata config.do 保持一致）
PATHS = {
    "raw":       REPO_ROOT / "data" / "raw",
    "processed": REPO_ROOT / "data" / "processed",
    "final":     REPO_ROOT / "data" / "final",
    # 结果层
    "tables":    REPO_ROOT / "results" / "tables",
    "figures":   REPO_ROOT / "results" / "figures",
    "logs":      REPO_ROOT / "results" / "logs",
    "project_tables":  REPO_ROOT / "results" / "tables" / PROJECT_SLUG,
    "project_figures": REPO_ROOT / "results" / "figures" / PROJECT_SLUG,
    # 代码层
    "code":      REPO_ROOT / "code",
    "utils":     REPO_ROOT / "code" / "utils",
    "analysis":  REPO_ROOT / "code" / "analysis" / PROJECT_SLUG,
    "output":    REPO_ROOT / "code" / "output" / PROJECT_SLUG,
    # 知识库（期刊范文 PDF 库，只读）
    "paper_lib":   REPO_ROOT / "paper-lib",
    "style_pdfs":  REPO_ROOT / "paper-lib" / "style-references" / "pdfs",
    # 论文层
    "paper":     REPO_ROOT / "paper" / PROJECT_SLUG,
    "exports":   REPO_ROOT / "paper" / "exports",
}

# ── 本机工具链（详见仓库根目录 ENVIRONMENT.md；不存在时脚本应自行降级）
_PYTHON_RELATIVE = Path("Scripts/python.exe") if os.name == "nt" else Path("bin/python")
_RSCRIPT_NAME = "Rscript.exe" if os.name == "nt" else "Rscript"
TOOLS = {
    "r_bin":       R_BIN,
    "texlive_bin": TEXLIVE_BIN,
    "py_env":      PYTHON_ENV,
    "python":      PYTHON_ENV / _PYTHON_RELATIVE,
    "rscript":     R_BIN / _RSCRIPT_NAME,
}

# ── 独立变量导出（兼容模板中的 from config import RAW, PROCESSED, ...）
RAW       = PATHS["raw"]
PROCESSED = PATHS["processed"]
FINAL     = PATHS["final"]
TABLES    = PATHS["tables"]
FIGURES   = PATHS["figures"]
LOGS      = PATHS["logs"]
CODE      = PATHS["code"]
UTILS     = PATHS["utils"]
PAPER_LIB = PATHS["paper_lib"]

# ── 使用示例
# 字典方式：raw_dir = PATHS["raw"] / "csmar_stock"
# 独立变量：raw_dir = RAW / "csmar_stock"
# output_dir = TABLES / PROJECT_SLUG
# output_dir.mkdir(parents=True, exist_ok=True)
