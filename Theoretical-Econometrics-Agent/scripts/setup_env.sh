#!/usr/bin/env bash
# setup_env.sh — macOS/Linux 原生环境激活（用法：source scripts/setup_env.sh）
# 本机路径优先级：环境变量 > config/local-tools.json > 自动探测 > 服务器兼容路径。

_TEA_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export TEA_REPO_ROOT="$(cd "${_TEA_SCRIPT_DIR}/.." && pwd)"
export TEA_LOCAL_CONFIG="${TEA_LOCAL_CONFIG:-${TEA_REPO_ROOT}/config/local-tools.json}"
export PYTHONPATH="${TEA_REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

_tea_fail() {
  echo "[ERROR] $1" >&2
}

_tea_warn() {
  echo "[WARN]  $1" >&2
}

_tea_return() {
  return "$1" 2>/dev/null || exit "$1"
}

if command -v python3 >/dev/null 2>&1; then
  _TEA_BOOTSTRAP_PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  _TEA_BOOTSTRAP_PYTHON="$(command -v python)"
else
  _tea_fail "未找到系统 Python。请先安装 Python 3.10+，再按《使用手册》创建 .venv。"
  _tea_return 1
fi

_tea_config_value() {
  "${_TEA_BOOTSTRAP_PYTHON}" "${_TEA_SCRIPT_DIR}/read_local_config.py" "$1" \
    --config "${TEA_LOCAL_CONFIG}" 2>/dev/null
}

_TEA_CONFIG_PYTHON_ENV="$(_tea_config_value python_env)"
_TEA_CONFIG_R_BIN="$(_tea_config_value r_bin)"
_TEA_CONFIG_TEXLIVE_BIN="$(_tea_config_value texlive_bin)"
_TEA_CONFIG_MATLAB_ROOT="$(_tea_config_value matlab_root)"
_TEA_CONFIG_STATA_CLI="$(_tea_config_value stata_cli)"
_TEA_CONFIG_OCTAVE_CLI="$(_tea_config_value octave_cli)"
_TEA_CONFIG_PANDOC_CLI="$(_tea_config_value pandoc_cli)"

export TEA_PYTHON_ENV="${TEA_PYTHON_ENV:-${_TEA_CONFIG_PYTHON_ENV}}"
if [[ -z "${TEA_PYTHON_ENV}" ]]; then
  if [[ -f "${TEA_REPO_ROOT}/.venv/bin/activate" ]]; then
    export TEA_PYTHON_ENV="${TEA_REPO_ROOT}/.venv"
  elif [[ -f "${TEA_REPO_ROOT}/../tools/py_env/bin/activate" ]]; then
    # 当前服务器布局的兼容回退；迁移到本地后应使用项目内 .venv。
    export TEA_PYTHON_ENV="${TEA_REPO_ROOT}/../tools/py_env"
  fi
fi

if [[ -z "${TEA_PYTHON_ENV}" || ! -f "${TEA_PYTHON_ENV}/bin/activate" ]]; then
  _tea_fail "Python 虚拟环境不存在。运行：python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt"
  _tea_return 1
fi
source "${TEA_PYTHON_ENV}/bin/activate"

export TEA_R_BIN="${TEA_R_BIN:-${_TEA_CONFIG_R_BIN}}"
if [[ -z "${TEA_R_BIN}" && -x "${TEA_REPO_ROOT}/../tools/R/bin/Rscript" ]]; then
  export TEA_R_BIN="${TEA_REPO_ROOT}/../tools/R/bin"
fi
if [[ -n "${TEA_R_BIN}" ]]; then
  export PATH="${TEA_R_BIN}:${PATH}"
fi

export TEA_TEXLIVE_BIN="${TEA_TEXLIVE_BIN:-${_TEA_CONFIG_TEXLIVE_BIN}}"
if [[ -z "${TEA_TEXLIVE_BIN}" && -x "/usr/local/texlive/2026/bin/x86_64-linux/pdflatex" ]]; then
  export TEA_TEXLIVE_BIN="/usr/local/texlive/2026/bin/x86_64-linux"
fi
if [[ -n "${TEA_TEXLIVE_BIN}" ]]; then
  export PATH="${TEA_TEXLIVE_BIN}:${PATH}"
fi

export TEA_MATLAB_ROOT="${TEA_MATLAB_ROOT:-${_TEA_CONFIG_MATLAB_ROOT}}"
export TEA_STATA_CLI="${TEA_STATA_CLI:-${_TEA_CONFIG_STATA_CLI}}"
export TEA_OCTAVE_CLI="${TEA_OCTAVE_CLI:-${_TEA_CONFIG_OCTAVE_CLI}}"
export TEA_PANDOC_CLI="${TEA_PANDOC_CLI:-${_TEA_CONFIG_PANDOC_CLI}}"

echo "── Theoretical-Econometrics-Agent 环境 ─────────────"
echo "  Repo    : ${TEA_REPO_ROOT}"
echo "  Config  : $([[ -f "${TEA_LOCAL_CONFIG}" ]] && echo "${TEA_LOCAL_CONFIG}" || echo "未创建（PATH 自动探测）")"
echo "  Python  : $(python --version 2>&1) [${TEA_PYTHON_ENV}]"
if ! python -c "import numpy, pandas, scipy, statsmodels, linearmodels, matplotlib, seaborn, docx, pypdf, reportlab, yaml, mcp" 2>/dev/null; then
  _tea_fail "Python 依赖不完整：python -m pip install -r requirements.txt"
  _tea_return 1
fi
echo "  Py deps : OK"

if command -v Rscript >/dev/null 2>&1; then
  echo "  R       : $(Rscript --version 2>&1)"
else
  _tea_warn "未找到 Rscript；M1/M3/M4 可运行，M5 的 R 交叉验证不可用。"
fi
if command -v latexmk >/dev/null 2>&1 && command -v pdflatex >/dev/null 2>&1; then
  echo "  TeX     : $(pdflatex --version | awk 'NR==1 {print; exit}')"
else
  _tea_warn "未找到 latexmk/pdflatex；M6 无法编译论文。"
fi
if command -v matlab >/dev/null 2>&1 || [[ -n "${TEA_MATLAB_ROOT}" ]]; then
  echo "  MATLAB  : 已探测（MCP 配置见 ENVIRONMENT.md）"
elif command -v octave >/dev/null 2>&1 || [[ -n "${TEA_OCTAVE_CLI}" ]]; then
  echo "  MATLAB  : 未探测；Octave 可作 M5 降级引擎"
else
  echo "  MATLAB  : 未探测；M5 可用 Python 降级实现"
fi
echo "  Detail  : python scripts/check_environment.py --strict"
echo "──────────────────────────────────────────────────"

unset _TEA_SCRIPT_DIR _TEA_BOOTSTRAP_PYTHON
unset _TEA_CONFIG_PYTHON_ENV _TEA_CONFIG_R_BIN _TEA_CONFIG_TEXLIVE_BIN
unset _TEA_CONFIG_MATLAB_ROOT _TEA_CONFIG_STATA_CLI _TEA_CONFIG_OCTAVE_CLI
unset _TEA_CONFIG_PANDOC_CLI
