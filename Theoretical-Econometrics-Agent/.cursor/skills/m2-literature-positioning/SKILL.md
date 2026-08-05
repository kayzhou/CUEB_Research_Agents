---
name: m2-literature-positioning
description: "Positions a theoretical econometrics model against its closest model, identification, estimation, asymptotic, and computation literatures using a local RAG index and a structured matrix. Produces conservative, source-verifiable novelty statements."
---

# M2 Literature Positioning — 文献定位与贡献审计 Skill

## Use This Skill When

1. 需要判断模型相对已有文献的边际贡献。
2. 需要构建文献矩阵、贡献诊断或「最近文献」比较。
3. 需要为 literature/library 建 RAG 索引并执行查询计划。
4. 需要审查论文引言中的贡献陈述是否夸大。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认文献纪律（规则 7）与 Gate 2。
2. `modules/M2-literature-positioning/MODULE.md`：思维框架——模型自适应的八个文献桶、矩阵列、措辞分级与红旗清单。
3. M1 冻结的模型设定（或用户口头描述）。
4. `projects/{slug}/literature/library/` 内容清单（PDF 需配套 .txt 才能被索引）。
5. 模板：`modules/M2-literature-positioning/templates/literature-matrix.csv`。
6. 用户领域资料入口：`paper-lib/README.md`；实际资料以项目 `literature/library/` 为准。

## Scope Boundary

1. 只做检索、分类、比较与贡献诊断；不改模型（M1）、不写引言正文（M6）。
2. 只使用 library、BibTeX 或用户明示批准的外部文献；不引用凭记忆的文献。

## Workflow

1. `python scripts/build_rag_index.py --library projects/{slug}/literature/library --out projects/{slug}/literature/index`。
2. 从 M1 模型生成八类中英双语查询，逐桶检索并记录空桶；仅在适用时加入空间、断点或阈值桶。
3. 填文献矩阵（16 列，含 `notes`；`citation_status` 只允许 verified / needs PDF / user-supplied only）。
4. 写贡献诊断六段：最近模型家族 / 最近估计方法 / 最近渐近结果 / 看似增量的部分 / 可能真正新的部分 / 待补检索。
5. 贡献措辞按强/中/弱分级；库中未命中一律用保守句式（「不构成新颖性证明」）。
6. 跑红旗清单 → 状态 `blocked_on_human` 等人裁决贡献定位。

## Output Expectations

1. `literature_matrix.csv`：每行可回溯到 library 中的具体文件。
2. `positioning.md`：贡献诊断 + 措辞分级 + 新颖性风险 + 待补检索清单。
3. 明确列出哪些比较基于 verified 文献、哪些只是候选。

## Common Pitfalls

1. 「库里没有」写成「文献中没有」。
2. PDF 未转文本却宣称检索过全库。
3. 比较不区分模型类、识别、估计量、渐近框架与数据依赖结构。
4. 套用固定查询桶，遗漏当前模型真正接近的替代方法。
5. 把「我们做了 MATLAB 模拟」当成贡献。
