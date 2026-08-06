clear all
set more off
capture log close

include "code/config/config.do"
log using "$logs/auto_analysis_test.log", replace text


sysuse auto, clear

* --- 描述统计 ---
tabstat price mpg weight length, stats(mean sd min p25 median p75 max) columns(statistics) format(%9.1f)

* --- 基准回归：价格 ~ mpg + weight ---
regress price mpg weight, robust
estimates store m1

* --- 加更多控制变量 ---
regress price mpg weight length foreign, robust
estimates store m2

* --- esttab 表格输出 ---
capture mkdir "$project_tables"
esttab m1 m2 using "$project_tables/tab_auto.tex", replace ///
    cells("b(star fmt(3)) se(par fmt(3))") ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2, fmt(%12.0fc %8.3f) labels("Obs." "R²")) ///
    title("Table: Determinants of Automobile Price") ///
    mtitles("(1)" "(2)") ///
    booktabs nomtitle nonumber
type "$project_tables/tab_auto.tex"

* --- 经济显著性（1-SD 变化对价格的影响） ---
display _newline as result "=== Economic Significance (1-SD change) ==="
foreach var in mpg weight length foreign {
    quietly summarize `var' if e(sample)
    local sd = r(sd)
    capture noisily regress price mpg weight length foreign, robust
    local b = _b[`var']
    local effect = `b' * `sd'
    display as text "`var': 1-SD change => " as result round(`effect', 0.1) " dollars"
}

* --- 国内外车价格差异 ---
display _newline as result "=== Price by Origin ==="
tab foreign, summarize(price)

display _newline as result "=== T-test: Domestic vs Foreign ==="
ttest price, by(foreign)


log close
exit, STATA
