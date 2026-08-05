/* =============================================================================
   config.do — 全局路径配置文件
   用途：所有分析脚本的第一行 include 此文件以获得路径变量
   
   使用方法：
     在每个脚本顶部加入：
       include "../../config/config.do"   （根据相对路径调整层级）
     或使用绝对路径：
       include "E:/path/to/project/code/config/config.do"
   
   维护说明：
     修改路径时只需修改本文件，所有脚本自动同步。
     路径使用正斜杠 / 以确保跨平台兼容。
============================================================================= */

version 17.0     // 声明 Stata 版本，确保复现一致性

/* ⚠️ WINDOWS 路径引用规则（必须遵守）
   包含盘符（E:, C:, D: 等）的路径必须用双引号括起。
   正确：include "code/config/config.do"
   正确：use "$final/analysis_sample.dta", clear
   正确：cd "$root"
   错误：cd $root                   ← E: 被 Stata 当命令解析
   错误：include code/config/config.do  ← 若路径含盘符则同样会报错
*/

// ─── 项目根目录：优先读取预设 global root，否则从 c(pwd) 自动识别 ──────────
if "$root" == "" {
  * 注意：不要在中文路径上使用 confirm file，Stata 对 Unicode 路径支持有限。
  * 直接使用 c(pwd) 作为项目根目录（运行脚本前应 cd 到项目根目录）。
  local pwd = subinstr(`"`c(pwd)'"', "\", "/", .)
  global root "`pwd'"
}

// ─── 当前论文项目 slug（小写英文 kebab-case）─────────────────────────────
if "$project_slug" == "" {
  global project_slug "a-share-multifactor-pricing"
}

// ─── 三层数据路径 ─────────────────────────────────────────────────────────
global raw       "$root/data/raw"
global processed "$root/data/processed"
global final     "$root/data/final"

// ─── 结果输出路径 ─────────────────────────────────────────────────────────
global results   "$root/results"
global result    "$root/results"     // 兼容别名，勿在新脚本中使用
global tables    "$root/results/tables"
global figures   "$root/results/figures"
global logs      "$root/results/logs"
global project_tables  "$tables/$project_slug"
global project_figures "$figures/$project_slug"

// ─── 代码路径 ─────────────────────────────────────────────────────────────
global code      "$root/code"
global utils     "$root/code/utils"
global analysis  "$root/code/analysis/$project_slug"
global output    "$root/code/output/$project_slug"
global paper     "$root/paper/$project_slug"

// ─── 知识库路径（期刊范文 PDF 库，只读） ──────────────────────────────────
global paperlib  "$root/paper-lib"

display "✓ 路径配置加载完成（$root；项目：$project_slug）"
