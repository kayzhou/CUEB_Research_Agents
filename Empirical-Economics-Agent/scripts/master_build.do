/* =============================================================================
   master_build.do — 全流水线主控脚本
   用途：按固定顺序运行所有分析脚本，确保全流程可一键复现
   
   运行方式：
     在 Stata 中执行：do ".../scripts/master_build.do"
   
   注意：
     - 此脚本仅负责调度，不含任何数据处理逻辑
     - 如需仅运行部分步骤，注释掉对应的 do 行
     - 每次完整运行前建议清空 results/ 目录（保留子目录结构）
============================================================================= */

// ─── 初始化 ───────────────────────────────────────────────────────────────
clear all
set more off
set linesize 120

// 根据当前 do 文件位置自动识别项目根目录，再加载路径配置
local thisfile = subinstr("`c(filename)'", "\", "/", .)
local marker "/scripts/master_build.do"
local marker_pos = strpos("`thisfile'", "`marker'")

if `marker_pos' == 0 {
  display as error "无法根据当前 do 文件位置识别项目根目录。"
  error 601
}

local root_auto = substr("`thisfile'", 1, `marker_pos' - 1)
global root "`root_auto'"
include "$root/code/config/config.do"

local timestamp = string(year(today()), "%04.0f") + string(month(today()), "%02.0f") + string(day(today()), "%02.0f")
log using "$logs/master_build_`timestamp'.log", replace text

display "=========================================="
display "  Master Build — 开始时间: `c(current_time)'"
display "=========================================="

// ─── 第一阶段：数据清洗 ────────────────────────────────── raw → processed
display _newline "--- [1/4] 数据清洗 ---"
// do "$code/clean/01_clean_stock_data.do"
// do "$code/clean/02_clean_accounting_data.do"

// ─── 第二阶段：样本构建 ──────────────────────────── processed → final
display _newline "--- [2/4] 样本构建 ---"
// do "$code/build/01_merge_datasets.do"
// do "$code/build/02_construct_variables.do"

// ─── 第三阶段：分析估计 ──────────────────────────── final → (中间结果)
display _newline "--- [3/4] 分析估计 ---"
// do "$analysis/01_baseline_regression.do"
// do "$analysis/02_event_study.do"
// do "$analysis/03_heterogeneity.do"
// do "$analysis/04_mechanism.do"

// ─── 第四阶段：输出生成 ─────────────────────────── (中间结果) → results/
display _newline "--- [4/4] 表格与图形输出 ---"
// do "$output/01_tables_main.do"
// do "$output/02_tables_robustness.do"
// do "$output/03_figures_main.do"

display _newline "=========================================="
display "  Master Build — 完成时间: `c(current_time)'"
display "=========================================="

log close
