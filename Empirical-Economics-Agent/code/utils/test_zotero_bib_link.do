/* =============================================================================
   test_zotero_bib_link.do — 测试 Zotero -> Better BibTeX -> Stata 的链接是否生效

   用法：
     do code/utils/test_zotero_bib_link.do
     do code/utils/test_zotero_bib_link.do "E:/path/to/refs.bib"

   默认检查：$paper/refs.bib
============================================================================= */

version 17.0

capture confirm global root
if _rc {
    display as error "global root 未定义。请先 include code/config/config.do"
    error 601
}

args bibfile
if "`bibfile'" == "" {
    local bibfile "$paper/refs.bib"
}

capture confirm file "`bibfile'"
if _rc {
    display as error "未找到 BibTeX 文件：`bibfile'"
    display as error "请先在 Zotero + Better BibTeX 中开启自动导出。"
    error 601
}

file open fh using "`bibfile'", read text
local line ""
local n_entries = 0

display as text "检查文件：`bibfile'"
display as text "前 5 个 citation key："

file read fh line
while r(eof) == 0 {
    local current = trim("`line'")
    if substr("`current'", 1, 1) == "@" {
        local ++n_entries
        if `n_entries' <= 5 {
            local open_brace = strpos("`current'", "{")
            local comma_pos = strpos("`current'", ",")
            if `open_brace' > 0 & `comma_pos' > `open_brace' {
                local citekey = substr("`current'", `open_brace' + 1, `comma_pos' - `open_brace' - 1)
                display as result "  `n_entries'. `citekey'"
            }
        }
    }
    file read fh line
}
file close fh

if `n_entries' == 0 {
    display as error "BibTeX 文件存在，但没有检测到任何条目。"
    display as error "请检查 Better BibTeX 导出设置是否正确。"
    error 459
}

display as result "Zotero -> BibTeX -> Stata 链接正常：共检测到 `n_entries' 个条目。"
display as text "测试建议：在 Zotero 新增 1 篇文献，等待自动导出后重跑本脚本；如果条目数增加或新 key 出现，则自动同步成功。"
