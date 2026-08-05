"""简明 Stata 实证分析测试 — 只使用内置命令，不依赖外部包."""

import subprocess
import os
from pathlib import Path

# 优先读取兼容本机配置；也可使用 setup_env 导出的 EEA_STATA_EXE。
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from stata_mcp_config_local import STATA_EXE  # type: ignore[import-not-found]
except ImportError:
    STATA_EXE = os.environ.get("EEA_STATA_EXE") or os.environ.get("STATA_EXE", "")
if not STATA_EXE:
    raise SystemExit(
        "请运行 scripts/configure_local.py 并激活环境，"
        "或创建 scripts/mcp/stata_mcp_config_local.py。"
    )
REPO_ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = REPO_ROOT / "results" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

analysis_code = r"""

display as result "=========================================="
display as result "  实证分析：汽车价格的决定因素"
display as result "  数据：1978 Automobile Data (auto.dta)"
display as result "=========================================="

sysuse auto, clear

display _newline(2) as result "=== 1. 描述统计 ==="
summarize price mpg weight length foreign, detail

display _newline(2) as result "=== 2. 基准回归：price ~ mpg + weight ==="
regress price mpg weight
display _newline as result "--- Robust SE ---"
regress price mpg weight, robust

display _newline(2) as result "=== 3. 多变量回归 ==="
regress price mpg weight length foreign
display _newline as result "--- Robust SE ---"
regress price mpg weight length foreign, robust

display _newline(2) as result "=== 4. 经济显著性（1个SD的变化对价格的影响）==="
regress price mpg weight length foreign
foreach var in mpg weight length foreign {
    quietly summarize `var'
    local sd = r(sd)
    local b = _b[`var']
    local effect = `b' * `sd'
    display as text "`var' (sd=" %6.2f `sd' "): 1-SD change =" as result %9.1f `effect' " dollars"
}

display _newline(2) as result "=== 5. 国产 vs 进口价格差异 ==="
tab foreign, summarize(price)
ttest price, by(foreign)

display _newline(2) as result "=== 6. 回归诊断：残差分布 ==="
predict res, residual
summarize res, detail
drop res

display _newline(2) as result "=== 完成 ==="
"""

log_file = LOG_DIR / "auto_analysis_final.log"
do_file = Path(__file__).resolve().parent / "_stata_analysis_final.do"

do_file.write_text(
    f"clear all\nset more off\ncapture log close\n"
    f'log using "{log_file.as_posix()}", replace text\n\n'
    f"{analysis_code}\n\nlog close\nexit, STATA\n",
    encoding="utf-8",
)

print("Running Stata...")
result = subprocess.run(
    (
        [STATA_EXE, "/e", "do", do_file.as_posix()]
        if sys.platform == "win32"
        else [STATA_EXE, "-b", "do", do_file.as_posix()]
    ),
    capture_output=True, text=True, timeout=120,
    cwd=REPO_ROOT,
)
print(f"Return code: {result.returncode}")

if log_file.exists():
    raw = log_file.read_bytes()
    text = raw.decode("gbk", errors="replace")
    # Print only the results (skip Stata technical lines)
    for line in text.splitlines():
        # Skip purely technical lines
        if line.startswith(".") and len(line) < 3:
            continue
        print(line.encode("ascii", errors="replace").decode("ascii"))
else:
    print("NO LOG")
    print(result.stdout[:2000])
