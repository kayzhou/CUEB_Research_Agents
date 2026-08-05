/* =============================================================================
   install_packages.do — Stata 依赖包安装脚本
   用途：在新的电脑上首次运行项目前，执行此脚本安装所有所需 Stata 包。
   用法：在 Stata 中运行：do "code/config/install_packages.do"

   维护：每新增一个 ssc/rnn 包依赖，在此文件中追加一行。
============================================================================= */

* 必须从仓库根目录运行，以便加载统一路径配置。
include "code/config/config.do"
capture log close
log using "$logs/install_packages.log", replace text

display "======================================================"
display "  Stata 依赖包安装"
display "  时间：$S_DATE $S_TIME"
display "======================================================"

// ─── 因果推断必备包 ──────────────────────────────────────────────────────────
capture ssc install reghdfe,      replace    // 高维固定效应
capture ssc install ftools,       replace    // reghdfe 依赖
capture ssc install ivreghdfe,    replace    // IV + 高维 FE
capture ssc install ivreg2,       replace    // IV/2SLS 全套诊断（弱工具变量、过度识别检验）
capture ssc install ranktest,     replace    // Kleibergen-Paap 弱 IV 秩检验（配 ivreg2 用）
capture ssc install rdrobust,     replace    // 断点回归

// ─── 现代 DID 方法 ────────────────────────────────────────────────────────────
capture ssc install csdid,        replace    // Callaway & Sant'Anna (2021) 交错 DID 估计量
capture ssc install drdid,        replace    // csdid 的辅助包
capture ssc install did_multiplegt_din, replace // de Chaisemartin & D'Haultfoeuille 多期 DID
capture ssc install bacondecomp,  replace    // Goodman-Bacon 交错 DID 分解
capture ssc install eventdd,      replace    // DID 事件研究图

// ─── 合成对照法 ───────────────────────────────────────────────────────────────
capture ssc install synth,        replace    // Abadie et al. 合成对照法
capture ssc install synth_runner, replace    // 合成对照的统计推断 + 安慰剂图

// ─── 稳健标准误与推断 ─────────────────────────────────────────────────────────
capture ssc install boottest,     replace    // Wild bootstrap 簇标准误（少聚类时更准确）

// ─── 输出与图形 ──────────────────────────────────────────────────────────────
capture ssc install coefplot,     replace    // 系数图
capture ssc install binscatter,   replace    // 分组散点图（Cattaneo et al.，顶刊常用）
capture ssc install estout,       replace    // esttab 表格输出
capture ssc install outreg2,      replace    // 表格输出（备选方案）

// ─── 资产定价辅助包 ──────────────────────────────────────────────────────────
capture ssc install newey,        replace    // Newey-West 标准误
capture ssc install asreg,        replace    // Fama-MacBeth 截面回归（含 Newey 校正）

// ─── 多重假设检验（资产定价多因子情景必备）─────────────────────────────────────
capture ssc install mhtexp,       replace    // Bonferroni / Holm / Romano-Wolf 多重检验校正

// ─── 数据处理工具 ─────────────────────────────────────────────────────────────
capture ssc install gtools,       replace    // 快速排序/合并/分组计算
capture ssc install winsor2,      replace    // 缩尾处理
capture ssc install distinct,     replace    // 计数唯一个体
capture ssc install unique,       replace    // 唯一个体 ID
capture ssc install fre,          replace    // 频率表（含缺失值百分比）
capture ssc install mmerge,       replace    // 灵活合并（合并前诊断 + 合并后校验）

display "======================================================"
display "  安装完成。请检查上方是否有红色错误信息。"
display "  日志：$logs/install_packages.log"
display "======================================================"

log close
