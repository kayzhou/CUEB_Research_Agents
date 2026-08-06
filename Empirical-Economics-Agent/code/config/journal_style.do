/* =============================================================================
   journal_style.do — 期刊风格配置
   用途：定义显著性约定、标准误标签、表格格式偏好，一键切换目标期刊风格

   使用方法：
     在每个分析脚本顶部（config.do 之后）加入：
       include "../../config/journal_style.do"

   切换期刊：
     取消注释对应期刊的 local profile，或通过 global journal 控制：
       global journal "JFE"
       include "../../config/journal_style.do"

   维护说明：
     新增期刊时在下方按同样格式追加 profile。
     表格 note 的自明性规范见 modules/M4-writing/templates/table-note-template.md。
   ============================================================================= */

/*
   ─── 经济学 vs 金融的默认格式差异 ─────────────────────────────────────────
   这一差异是学科惯例，不是技术优劣问题。在无本地范文时，按以下默认规则：

   · 经济学（AER / QJE / Econometrica / JPE / ReStud 等）：
     系数下方括号内放 标准误（standard errors）。
     SE_LABEL 示例："Robust standard errors in parentheses"

   · 金融 / 资产定价（JF / JFE / RFS / JFQA / RoF 等）：
     系数下方括号内放 t 统计量（t-statistics）。
     SE_LABEL 示例："t-statistics in parentheses"

   无本地范文时按上述默认；有范文（paper-lib/style-references/）以范文实际格式为准。
   ============================================================================= */

version 17.0

// ─── 期刊选择（默认 JFE，按目标期刊修改）─────────────────────────────────
if "$journal" == "" {
  global journal "JFE"
}

// ─── 按期刊切换风格 ───────────────────────────────────────────────────────
if "$journal" == "JFE" {
  // Journal of Financial Economics
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "t-statistics in parentheses"
  local CLUSTER_LABEL "Standard errors are double-clustered at the firm and year levels."
  local TABLE_FONT  "\small"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

else if "$journal" == "RFS" {
  // Review of Financial Studies
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "t-statistics in parentheses"
  local CLUSTER_LABEL "Standard errors are clustered at the firm level."
  local TABLE_FONT  "\small"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

else if "$journal" == "JF" {
  // Journal of Finance
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "t-statistics in parentheses"
  local CLUSTER_LABEL "Standard errors are heteroskedasticity-consistent and clustered at the firm level."
  local TABLE_FONT  "\footnotesize"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

else if "$journal" == "AER" {
  // American Economic Review
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "Robust standard errors in parentheses"
  local CLUSTER_LABEL "Standard errors are clustered at the [unit] level."
  local TABLE_FONT  "\footnotesize"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

else if "$journal" == "QJE" {
  // Quarterly Journal of Economics
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "Standard errors in parentheses"
  local CLUSTER_LABEL "Standard errors are clustered at the [unit] level."
  local TABLE_FONT  "\footnotesize"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

else if "$journal" == "JoF" {
  // Journal of Finance (alternate)
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "t-statistics in parentheses"
  local CLUSTER_LABEL "Standard errors are heteroskedasticity-consistent and clustered at the firm level."
  local TABLE_FONT  "\footnotesize"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

else {
  // 默认（期刊中性）
  local STAR_PATTERN `"* 0.10 ** 0.05 *** 0.01"'
  local SE_LABEL    "Standard errors in parentheses"
  local CLUSTER_LABEL "Standard errors are clustered at the [unit] level."
  local TABLE_FONT  "\small"
  local SIG_LEVELS  "10%, 5%, and 1%"
}

// ─── 导出给 esttab / estout 使用 ──────────────────────────────────────────
global STAR_PATTERN   `"`STAR_PATTERN'"'
global SE_LABEL       "`SE_LABEL'"
global CLUSTER_LABEL  "`CLUSTER_LABEL'"
global TABLE_FONT     "`TABLE_FONT'"
global SIG_LEVELS     "`SIG_LEVELS'"

// ─── 表格面板布局设置 ────────────────────────────────────────────────────────
// PANEL_ROW_MAX: 单面板最多系数行数，超过则按行竖拆为多个 panel
// PANEL_COL_MAX: 单表最多列数（模型数），超过则按列横拆为 Panel A / Panel B
// TABLE_PANEL_AUTO: 1 = 超阈值自动拆分, 0 = 仅手动 panel_def 拆分
global PANEL_ROW_MAX    30
global PANEL_COL_MAX    6
global TABLE_PANEL_AUTO 1

// ─── esttab 常用预设（可直接在 esttab 调用时参考）─────────────────────────
/*
   esttab m1 m2 m3 m4 m5 m6 using "$project_tables/tab_main.tex", ///
       replace booktabs                                 ///
       star($STAR_PATTERN)                              ///
       se label                                          ///
       mtitles("M1" "M2" "M3" "M4" "M5" "M6")          ///
       addnotes("`CLUSTER_LABEL'" "*, **, and *** indicate significance at the `SIG_LEVELS' levels, respectively.") ///
       nomtitles nonumbers                               ///
       replace
*/

display "✓ 期刊风格加载完成（$journal）"
