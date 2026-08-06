#!/usr/bin/env bash
# setup_env.sh — macOS/Linux 原生环境激活（用法：source scripts/setup_env.sh）
# 路径优先级：环境变量 > config/local-tools.json > 本机探测 > 服务器兼容布局。

if [[ -n "${BASH_SOURCE:-}" ]]; then
  _EEA_SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [[ -f "${PWD}/scripts/setup_env.sh" ]]; then
  # zsh 从仓库根 source 时没有 BASH_SOURCE。
  _EEA_SCRIPT_PATH="${PWD}/scripts/setup_env.sh"
else
  echo "[ERROR] 请从仓库根目录执行：source scripts/setup_env.sh" >&2
  return 1 2>/dev/null || exit 1
fi

_EEA_SCRIPT_DIR="$(cd "$(dirname "${_EEA_SCRIPT_PATH}")" && pwd)"
export EEA_REPO_ROOT="$(cd "${_EEA_SCRIPT_DIR}/.." && pwd)"
export EEA_LOCAL_CONFIG="${EEA_LOCAL_CONFIG:-${EEA_REPO_ROOT}/config/local-tools.json}"
export EEA_TOOLS_ROOT="${EEA_TOOLS_ROOT:-$(cd "${EEA_REPO_ROOT}/.." && pwd)/tools}"
export PROJECT_SLUG="${PROJECT_SLUG:-a-share-multifactor-pricing}"
export PYTHONPATH="${EEA_REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

_eea_fail() {
  echo "[ERROR] $1" >&2
}

if command -v python3 >/dev/null 2>&1; then
  _EEA_BOOTSTRAP_PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  _EEA_BOOTSTRAP_PYTHON="$(command -v python)"
elif [[ -x "${EEA_TOOLS_ROOT}/py_env/bin/python" ]]; then
  _EEA_BOOTSTRAP_PYTHON="${EEA_TOOLS_ROOT}/py_env/bin/python"
else
  _eea_fail "未找到系统 Python。请先安装 Python 3.10+。"
  return 1 2>/dev/null || exit 1
fi

if [[ -f "${EEA_LOCAL_CONFIG}" ]]; then
  if ! "${_EEA_BOOTSTRAP_PYTHON}" "${_EEA_SCRIPT_DIR}/read_local_config.py" \
    --config "${EEA_LOCAL_CONFIG}" --validate >/dev/null; then
    _eea_fail "本机工具配置无效：${EEA_LOCAL_CONFIG}"
    return 1 2>/dev/null || exit 1
  fi
fi

_eea_config_value() {
  "${_EEA_BOOTSTRAP_PYTHON}" "${_EEA_SCRIPT_DIR}/read_local_config.py" "$1" \
    --config "${EEA_LOCAL_CONFIG}"
}

_EEA_CONFIG_PYTHON_ENV="$(_eea_config_value python_env)" || {
  return 1 2>/dev/null || exit 1
}
_EEA_CONFIG_R_BIN="$(_eea_config_value r_bin)" || {
  return 1 2>/dev/null || exit 1
}
_EEA_CONFIG_TEXLIVE_BIN="$(_eea_config_value texlive_bin)" || {
  return 1 2>/dev/null || exit 1
}
_EEA_CONFIG_MATLAB_ROOT="$(_eea_config_value matlab_root)" || {
  return 1 2>/dev/null || exit 1
}
_EEA_CONFIG_STATA_CLI="$(_eea_config_value stata_cli)" || {
  return 1 2>/dev/null || exit 1
}

# ── Python：项目 .venv 优先，服务器 tools/py_env 仅作兼容回退 ─────────────
export EEA_PYTHON_ENV="${EEA_PYTHON_ENV:-${_EEA_CONFIG_PYTHON_ENV}}"
if [[ -z "${EEA_PYTHON_ENV}" ]]; then
  if [[ -f "${EEA_REPO_ROOT}/.venv/bin/activate" ]]; then
    export EEA_PYTHON_ENV="${EEA_REPO_ROOT}/.venv"
  elif [[ -f "${EEA_TOOLS_ROOT}/py_env/bin/activate" ]]; then
    export EEA_PYTHON_ENV="${EEA_TOOLS_ROOT}/py_env"
  fi
fi
if [[ -z "${EEA_PYTHON_ENV}" || ! -f "${EEA_PYTHON_ENV}/bin/activate" ]]; then
  _eea_fail "Python 虚拟环境不存在。运行：python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt"
  return 1 2>/dev/null || exit 1
fi
source "${EEA_PYTHON_ENV}/bin/activate"

# ── R 与 TeX：本机配置/PATH 优先，保留当前服务器路径回退 ──────────────────
export EEA_R_BIN="${EEA_R_BIN:-${_EEA_CONFIG_R_BIN}}"
if [[ -z "${EEA_R_BIN}" ]] && command -v Rscript >/dev/null 2>&1; then
  export EEA_R_BIN="$(dirname "$(command -v Rscript)")"
elif [[ -z "${EEA_R_BIN}" && -x "${EEA_TOOLS_ROOT}/R/bin/Rscript" ]]; then
  export EEA_R_BIN="${EEA_TOOLS_ROOT}/R/bin"
fi
if [[ -n "${EEA_R_BIN}" ]]; then
  export PATH="${EEA_R_BIN}:${PATH}"
fi
if ! command -v Rscript >/dev/null 2>&1; then
  _eea_fail "Rscript 未找到；在 config/local-tools.json 填写 r_bin。"
  return 1 2>/dev/null || exit 1
fi

export EEA_TEXLIVE_BIN="${EEA_TEXLIVE_BIN:-${_EEA_CONFIG_TEXLIVE_BIN}}"
if [[ -z "${EEA_TEXLIVE_BIN}" ]] && command -v pdflatex >/dev/null 2>&1; then
  export EEA_TEXLIVE_BIN="$(dirname "$(command -v pdflatex)")"
elif [[ -z "${EEA_TEXLIVE_BIN}" && -x "/usr/local/texlive/2026/bin/x86_64-linux/pdflatex" ]]; then
  export EEA_TEXLIVE_BIN="/usr/local/texlive/2026/bin/x86_64-linux"
fi
if [[ -n "${EEA_TEXLIVE_BIN}" ]]; then
  export PATH="${EEA_TEXLIVE_BIN}:${PATH}"
fi
if ! command -v pdflatex >/dev/null 2>&1; then
  _eea_fail "pdflatex 未找到；在 config/local-tools.json 填写 texlive_bin。"
  return 1 2>/dev/null || exit 1
fi

# ── 可选商业工具：统一导出给本地直连、测试与 MCP 回退使用 ────────────────
export EEA_STATA_EXE="${EEA_STATA_EXE:-${_EEA_CONFIG_STATA_CLI}}"
if [[ -z "${EEA_STATA_EXE}" ]]; then
  for _EEA_STATA_NAME in stata-mp stata-se stata; do
    if command -v "${_EEA_STATA_NAME}" >/dev/null 2>&1; then
      export EEA_STATA_EXE="$(command -v "${_EEA_STATA_NAME}")"
      break
    fi
  done
fi

export EEA_MATLAB_ROOT="${EEA_MATLAB_ROOT:-${_EEA_CONFIG_MATLAB_ROOT}}"
if [[ -z "${EEA_MATLAB_EXE:-}" && -n "${EEA_MATLAB_ROOT}" && -x "${EEA_MATLAB_ROOT}/bin/matlab" ]]; then
  export EEA_MATLAB_EXE="${EEA_MATLAB_ROOT}/bin/matlab"
elif [[ -z "${EEA_MATLAB_EXE:-}" ]] && command -v matlab >/dev/null 2>&1; then
  export EEA_MATLAB_EXE="$(command -v matlab)"
fi

# ── 版本与依赖自检 ─────────────────────────────────────────────────────────
echo "── Empirical-Economics-Agent 环境 ────────────────"
echo "  Repo    : ${EEA_REPO_ROOT}"
echo "  Config  : $([[ -f "${EEA_LOCAL_CONFIG}" ]] && echo "${EEA_LOCAL_CONFIG}" || echo "未创建（自动探测）")"
echo "  Python  : $(python --version 2>&1) [${EEA_PYTHON_ENV}]"
echo "  R       : $(Rscript --version 2>&1)"
echo "  TeX     : $(pdflatex --version | awk 'NR==1 {print; exit}')"
if ! python -c "import numpy, pandas, scipy, statsmodels, linearmodels, sklearn, pyarrow, matplotlib, seaborn, docx, reportlab, lxml, yaml, requests, mcp"; then
  _eea_fail "Python 核心依赖不完整；运行 python -m pip install -r requirements.txt"
  return 1 2>/dev/null || exit 1
fi
echo "  Py deps : OK"
Rscript -e 'p <- c("fixest","did","rdrobust","eventstudyr"); m <- p[!vapply(p, requireNamespace, logical(1), quietly=TRUE)]; cat("  R pkgs  :", if(length(m)) paste("未安装", paste(m, collapse=", ")) else "OK", "\n")'
echo "  Stata   : ${EEA_STATA_EXE:-未配置（可使用 R 降级）}"
echo "  MATLAB  : ${EEA_MATLAB_EXE:-未配置（可使用 Python 降级）}"
echo "──────────────────────────────────────────────────"

unset _EEA_SCRIPT_PATH _EEA_SCRIPT_DIR _EEA_BOOTSTRAP_PYTHON
unset _EEA_CONFIG_PYTHON_ENV _EEA_CONFIG_R_BIN _EEA_CONFIG_TEXLIVE_BIN
unset _EEA_CONFIG_MATLAB_ROOT _EEA_CONFIG_STATA_CLI _EEA_STATA_NAME
unset -f _eea_config_value _eea_fail 2>/dev/null || true
