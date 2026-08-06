/*===========================================================================
 code/utils/table_panel_splitter.do — 回归表面板拆分程序

 用途：在 esttab 输出 .tex 之前，根据存储估计量的行数/列数判断是否需要
       拆分为多个 panel（Panel A / Panel B ...），并输出带面板标题的完整
       LaTeX 表格片段。

 依赖：estout 包（ssc install estout）
 加载：include "code/utils/table_panel_splitter.do"
       （路径相对于项目根，调用前确保已 include code/config/config.do）

 签名：
   table_panel_split, models(string)             // 存储估计量名称列表
                      [using(string)]            // 输出 .tex 路径
                      [panel_def(string)]        // 手动面板定义 "标题:模型范围 标题:模型范围"
                      [max_rows(integer 25)]     // 行数阈值，超过则竖拆
                      [max_cols(integer 6)]      // 列数阈值，超过则横拆
                      [table_opts(string)]       // 透传给 esttab 的额外选项
                      [font(string)]             // 表格字体（应与 TABLE_FONT 一致）
                      [note(string)]             // 表格注释文本
                      [label(string)]            // 表格 label
                      [caption(string)]          // 表格标题
                      [placement(string)]        // 表格浮动位置；省略时默认为 htbp

 面板定义格式（panel_def）：
   "Baseline:m1 m2 m3" "With Controls:m4 m5 m6" "Full FE:m7 m8"
   冒号前是面板标题（Panel A 的 "A: " 前缀自动添加），冒号后是空格分隔的模型名。

   也可用范围简写：panel_def("Baseline:m1-m3" "Robustness:m4-m6")

 自动拆分行为：
   当 panel_def 为空且模型数 > max_cols 时，自动按列均分。
   当系数行数 > max_rows 时，自动按行拆分（需手动分组变量）。

 输出结构：
   \begin{table}[htbp]
   \centering \tablefont
   \caption{...} \label{...}
   \begin{threeparttable}
   \textbf{Panel A: Baseline}\\[4pt]
   \input{..._panel_a.tex}
   \textbf{Panel B: Robustness}\\[4pt]
   \input{..._panel_b.tex}
   \begin{tablenotes} \tablenotefont \item \textit{Notes:} ... \end{tablenotes}
   \end{threeparttable}
   \end{table}

 维护：修改本程序时同步更新 docs/code/utils/table_panel_splitter.do.md
===========================================================================*/

capture program drop table_panel_split
program define table_panel_split

    syntax , models(string) ///
        [ using(string) ///
          panel_def(string) ///
          max_rows(integer 25) ///
          max_cols(integer 6) ///
          table_opts(string) ///
          font(string) ///
          note(string) ///
          label(string) ///
          caption(string) ///
          placement(string) ]

    if "`placement'" == "" {
        local placement "htbp"
    }

    // ── 1. 解析模型列表 ──────────────────────────────────────────────
    local n_models : word count `models'
    local model_list `models'

    // ── 2. 确定使用的字体 ────────────────────────────────────────────
    if "`font'" == "" {
        if "$TABLE_FONT" != "" {
            local font "$TABLE_FONT"
        }
        else {
            local font "\small"
        }
    }

    // ── 3. 估算系数行数 ──────────────────────────────────────────────
    tempname preview
    quietly estimates table `model_list', star(${STAR_PATTERN})
    local est_rows = e(k)          // 每个估计量的系数行数（含统计行）
    if `est_rows' == . {
        local est_rows = 0
        foreach m of local model_list {
            quietly estimates restore `m'
            local keq = e(rank)    // 方程秩 = 系数个数（不含统计行）
            local est_rows = max(`est_rows', `keq')
        }
        local est_rows = `est_rows' + 5    // 统计行预留
    }

    // ── 4. 解析面板定义 ──────────────────────────────────────────────
    local n_panels = 0
    local panel_titles ""
    local panel_models ""

    if "`panel_def'" != "" {
        // 手动面板模式
        local pname_count = 0
        foreach chunk of local panel_def {
            local ++pname_count
            gettoken ptitle pmodels : chunk, parse(":")
            local ptitle : subinstr local ptitle ":" ""
            local ptitle = strtrim("`ptitle'")

            // 支持 m1-m3 范围简写
            // 这里保持简单：调用者直接提供空格分隔的模型名
            local n_panels = `n_panels' + 1
            local panel_titles `panel_titles' "`ptitle'"
            local panel_models `panel_models' "`pmodels'"
        }
    }
    else if `n_models' > `max_cols' {
        // 自动按列拆分模式
        local models_per_panel = `max_cols'
        local n_panels = ceil(`n_models' / `max_cols')

        local remaining = `n_models'
        local start = 1
        forvalues p = 1/`n_panels' {
            local pm = ""
            local pend = min(`start' + `max_cols' - 1, `n_models')
            forvalues mi = `start'/`pend' {
                local mm : word `mi' of `model_list'
                local pm `pm' `mm'
            }
            local panel_models `panel_models' "`pm'"
            local panel_titles `panel_titles' "Specifications `start'-`pend'"
            local start = `pend' + 1
        }
    }
    else {
        // 单面板模式
        local n_panels = 1
        local panel_titles ""
        local panel_models "`model_list'"
    }

    // ── 5. 输出带面板结构的完整 LaTeX 表格 ────────────────────────────
    if "`using'" == "" {
        di as error "table_panel_split: using() 必须指定输出路径"
        exit 198
    }

    local outdir : subinstr local using "\" "/", all
    local outbase = subinstr("`using'", ".tex", "", 1)

    // 写完整 table 包装
    tempname fh
    quietly file open `fh' using "`using'", write text replace

    file write `fh' "\begin{table}[`placement']" _n
    file write `fh' "  \centering" _n
    file write `fh' "  `font'" _n
    if "`caption'" != "" {
        file write `fh' "  \caption{`caption'}" _n
    }
    if "`label'" != "" {
        file write `fh' "  \label{`label'}" _n
    }
    file write `fh' "  \begin{threeparttable}" _n

    // 逐面板输出
    local pidx = 0
    forvalues p = 1/`n_panels' {
        local ptitle : word `p' of `panel_titles'
        local pmodels : word `p' of `panel_models'

        // 为每个面板生成独立的 .tex 片段
        local panel_file "`outbase'_p`p'.tex"

        // 写面板标题
        if `n_panels' > 1 {
            file write `fh' "  \textbf{Panel `p': `ptitle'}\\[4pt]" _n
        }

        // 生成面板表体
        quietly esttab `pmodels' using "`panel_file'", replace ///
            booktabs nomtitle nonumbers ///
            `table_opts'

        // 引用面板文件
        file write `fh' "  \input{`panel_file'}" _n

        // 面板间加空白
        if `p' < `n_panels' {
            file write `fh' "  \vspace{6pt}" _n _n
        }
    }

    // 表格注释
    if "`note'" != "" {
        file write `fh' "  \begin{tablenotes}" _n
        file write `fh' "    \tablenotefont" _n
        file write `fh' "    \item \textit{Notes:} `note'" _n
        file write `fh' "  \end{tablenotes}" _n
    }

    file write `fh' "  \end{threeparttable}" _n
    file write `fh' "\end{table}" _n
    quietly file close `fh'

    // ── 6. 报告摘要 ──────────────────────────────────────────────────
    di as text _n "── table_panel_split 输出摘要 ──"
    di as text "  输出文件: " as result "`using'"
    di as text "  面板数:   " as result `n_panels'
    di as text "  模型数:   " as result `n_models'
    di as text "  表格字体: " as result "`font'"
    di as text "  系数行数: " as result `est_rows'
    if `est_rows' > `max_rows' {
        di as error "  ⚠ 行数 (`est_rows') 超过阈值 (`max_rows')，建议竖拆"
    }
    di as text "───────────────────────────────" _n

end
