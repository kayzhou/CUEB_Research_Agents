---
name: m6-paper-writing
description: "Assembles a submission-ready theoretical econometrics paper in LaTeX: four-layer introduction, model and assumptions sections, theorem statements bound to assumptions, appendix proofs, simulation tables input from generated files, compiled with TeX Live. Use when drafting or polishing the manuscript."
---

# M6 Paper Writing — 论文写作 Skill

## Use This Skill When

1. 需要起草或修改 LaTeX 章节（引言 / 模型 / 假设 / 渐近性质 / 模拟 / 结论 / 附录证明）。
2. 需要组装 M1–M5 产出为全稿并编译。
3. 需要检查记号 / 标签 / 引用一致性。
4. 需要导出 docx 给导师批注。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认 Gate 6。
2. `modules/M6-paper-writing/MODULE.md`：思维框架——目录结构、四层引言、理论写作标准、标签约定、结果表纪律。
3. `ENVIRONMENT.md` + 当前系统的激活脚本：TeX Live/MacTeX（英文 latexmk -pdf / 中文 xelatex）。
4. 上游产出：模型设定、positioning.md、assumptions.md、theorem_map.md、results/tables/。
5. LaTeX 骨架真源：`templates/paper-project/paper/`；其默认内容属于空间面板断点模型，
   其他模型必须依据 M1 与 M4 删除或替换不适用占位。
6. 记号真源：项目 `proofs/notation_registry.md`。

## Scope Boundary

1. 只处理写作、组稿、编译与一致性检查；不新增定理（M4）、不重跑模拟（M5）。
2. 引言的贡献陈述必须逐句来自 M2 批准的 positioning.md，不得升级措辞。

## Workflow

1. 新项目用 `scripts/init_project.py` 生成骨架，并先按冻结模型与定理地图清理默认占位；
   已有项目直接编辑 `projects/{slug}/paper/`。先写引言 + 模型节 → **等人审阅定调**（卡点）。
2. 假设与定理节从 `proofs/` 转写：每条假设编号命名，每个定理列所用假设；candidate theorem 显式标注。
3. 模拟节 `\input{}` M5 生成的 `.tex` 表格片段；占位表标 `placeholder`。
4. 附录证明从 `proofs/proof_*.md` 转写，保留 proof gap 标注。
5. 编译：`latexmk -pdf main.tex`（中文稿 xelatex + ctex）→ `python scripts/check_latex_notation.py --tex .../main.tex`。
6. Gate 6 六项检查（未定义引用 / 重复标签 / 记号 / 定理-假设 / 附录匹配 / bib）→ 全稿 `blocked_on_human` 等人审阅。
7. 需要 docx 时用 python-docx / pandoc 导出到 `projects/{slug}/exports/`。

## Output Expectations

1. 本地生成的 `main.pdf` 编译通过，零未定义引用、零重复标签；交付发行树只保留 LaTeX/BibTeX 源。
2. 正文数字全部来自结果文件或显式 placeholder。
3. proof gap 未清零时结论/附录带终稿警示语（`system/integrity-rules.md`）。
4. 标签遵循 `sec:/eq:/ass:/lem:/thm:/tab:/app:` 前缀约定。

## Common Pitfalls

1. 手抄模拟数字。
2. 正文与附录定理陈述不同步。
3. `\cite` 未核对文献。
4. 中文稿误用 pdflatex。
5. candidate theorem 冒充正式定理、贡献措辞私自升级。
