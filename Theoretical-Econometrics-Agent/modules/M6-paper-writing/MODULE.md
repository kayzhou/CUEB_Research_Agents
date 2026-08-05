# M6 — 论文写作

> 把 M1–M5 的产出组装成一篇可投稿的理论计量论文：正文六节 + 附录证明。
> 铁律：正文数字来自结果文件；记号/假设/定理/附录标签四处同步；编译零未定义引用。

---

## Requires（前置输入）

- M1–M5 产出：模型设定、文献定位、估计方案、假设与定理地图、模拟表格
- 从中间切入时：你直接提供的等价材料（推导笔记、已有表格均可）

## Produces（产出）

- `projects/{slug}/paper/main.tex` + `sections/` + `appendix/` + `refs.bib`
- 本地验收时由 `latexmk -pdf` 生成并检查 `main.pdf`；发行树只保留 LaTeX/BibTeX 源，不纳入 PDF 或中间文件
- 可选：`projects/{slug}/exports/` 下的 docx（给导师/合作者批注）

## 卡点（人裁决）

1. **章节草稿审阅**：引言 + 模型节先行审阅定调；全稿完成后整体审阅。

---

## 执行流程

### 步骤 1：结构

以下是当前空间面板断点模板的默认文件名，不是所有模型的强制章节或附录：
```text
paper/
├── main.tex
├── sections/
│   ├── 01_introduction.tex     # 四层引言
│   ├── 02_model_likelihood.tex
│   ├── 03_assumptions.tex
│   ├── 04_asymptotic_properties.tex
│   ├── 05_monte_carlo.tex
│   └── 06_conclusion.tex
├── appendix/
│   ├── A_matrix_lemmas.tex
│   ├── B_likelihood_expansion.tex
│   ├── C_consistency.tex
│   ├── D_break_rate.tex
│   └── E_asymptotic_normality.tex
└── refs.bib
```

LaTeX 骨架真源为 `templates/paper-project/paper/`；新项目由 `scripts/init_project.py` 复制到
`projects/{slug}/paper/`。若研究模型不同，须在 Gate 1 后按定理地图重命名或删减章节与附录，
不得保留不适用的空间、断点或渐近结论占位内容。

### 步骤 2：四层引言逻辑

1. 研究背景：说明经济问题与数据结构；
2. 文献缺口：仅使用 M2 已核验的最近文献定位；
3. 技术挑战：由当前模型的识别、估计和渐近问题决定；
4. 贡献清单：只列已建立的模型、估计、理论或计算结果，不把流程本身包装成创新。

### 步骤 3：理论写作标准

- 每条假设编号 + 命名；每个定理显式列出所用假设；禁止「under regularity conditions」。
- 证明未闭合的结果标 **candidate theorem**，并在结论/附录出现 `system/integrity-rules.md` 的终稿警示语。
- 长证明进附录；正文只留陈述 + 证明思路一句话。

### 步骤 4：记号与标签约定

记号以项目 `proofs/notation_registry.md` 为唯一真源。空间权重、断点和 regime 记号仅在当前模型适用时出现。
标签前缀：`sec:` `eq:` `ass:` `lem:` `thm:` `tab:` `app:`（如 `\label{thm:consistency}`）。

### 步骤 5：结果表纪律

模拟表由 M5 脚本生成 `.tex` 片段后 `\input{}` 引用；手写占位表必须显式标 `placeholder`。

### 步骤 6：编译与检查（Gate 6）

```bash
latexmk -pdf main.tex                                        # 英文；中文讨论稿用 xelatex
python scripts/check_latex_notation.py --tex projects/{slug}/paper/main.tex
```

检查：未定义引用 = 0？重复标签 = 0？记号与登记表一致？定理-假设编号对得上？附录证明引用与正文匹配？bib 条目完整？

**通过 Gate 6 → 人审阅全稿 → 进入 M7。**

---

## Common Pitfalls

1. 手抄模拟数字进正文（应 `\input{}` 结果片段）。
2. 附录定理重述与正文陈述不一致（改了一处忘另一处）。
3. `\cite` 了 refs.bib 里不存在或 M2 未核对的文献。
4. 中文稿用 pdflatex 编译导致乱码（应 xelatex + ctex）。
5. 把 candidate theorem 写成无警示的正式定理。

---

## 独立运行说明

M6 可独立运行：提供推导笔记 + 模拟表格（任何格式）即可组稿；缺的上游产出按模板补 stub 并标注。

## 细节流程与模板

- 执行框架：`.cursor/skills/m6-paper-writing/SKILL.md`
- 模板：`templates/paper-project/paper/`（main.tex + sections + appendix + refs.bib 全套骨架，唯一真源）
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的“M6 — 论文写作”；
  示例不提供可投稿论文或已编译成品
