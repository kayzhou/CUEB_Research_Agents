# M2 — 文献定位与贡献审计

> 用 RAG 检索与文献矩阵判断当前模型相对最近模型、估计方法和渐近理论的边际贡献。
> 铁律：**「当前文献库没有」≠「文献中没有」**，新颖性措辞必须保守。

---

## Requires（前置输入）

- M1 冻结的模型设定（或你口头描述的等价物）
- `projects/{slug}/literature/library/` 中的文献（PDF 请同时提供转出的 .txt；支持 .txt/.md/.tex/.bib/.csv）

## Produces（产出）

- `projects/{slug}/literature/literature_matrix.csv` — 文献分类矩阵
- `projects/{slug}/literature/positioning.md` — 贡献诊断（最近模型家族 / 最近估计方法 / 最近渐近结果 / 真正可能新的东西 / 新颖性风险 / 待补检索）
- `projects/{slug}/literature/index/` — RAG 轻量索引（`scripts/build_rag_index.py` 生成）

## 卡点（人裁决）

1. **贡献定位批准**：人确认贡献陈述级别（强/中/弱）与新颖性风险后，才能把贡献写进论文。

---

## 执行流程

### 步骤 1：建索引

```bash
python scripts/build_rag_index.py \
  --library projects/{slug}/literature/library \
  --out projects/{slug}/literature/index
```

### 步骤 2：查询计划（八个文献桶，中英双语查询）

查询桶必须由 M1 模型生成，不得把空间或断点文献强加给无关模型：

1. 基础模型家族；2. 识别问题；3. 最近估计方法；4. 渐近框架与主要定理；
5. 数据或依赖结构；6. 模型特有机制（如空间、断点、阈值、动态项，仅在适用时）；
7. 稳健推断与替代估计量；8. Monte Carlo 与计算实现。

例如，一般线性 QML 可检索 `linear model quasi maximum likelihood robust covariance`；
空间面板断点模型可另加 `spatial panel change point QML asymptotic theory`。

### 步骤 3：填文献矩阵

按 `modules/M2-literature-positioning/templates/literature-matrix.csv` 列结构：`paper_id`、`authors_year`、`title`、`model_class`、
`spatial_dependence`、`panel_dimension`、`break_or_threshold`、`estimator`、`main_theory`、`assumptions`、
`simulation_design`、`difference_from_our_model`、`supports_our_assumption`、`novelty_risk`、`citation_status`。
与当前模型无关的专用字段填写 `not applicable`，不得为了填表虚构对应结构。

`citation_status` 只允许：`verified`（回原文核对过）/ `needs PDF` / `user-supplied only`。

### 步骤 4：贡献诊断与措辞分级

- **强**：「本文在 … 条件下建立了 …，[已核对的最近文献] 未覆盖该结果。」
- **中**：「本文将 … 扩展到允许 …。」
- **弱**：「本文把 … 与 … 组合进一个可能有用的框架，新颖性有赖进一步文献核对。」

未核对到原文的比较，只能写：
> 基于当前提供的文献库，我未找到直接匹配的论文。这不构成新颖性证明，需要补充数据库检索。

### 步骤 5：红旗检查（Gate 2）

以下情形必须向人报警：

- 模型只是已知结构的重组，没有新的识别、估计或理论结果；
- 估计量和证明是已有文献的直接重复；
- 新增机制没有独立识别；
- 矩阵漏掉与当前模型最接近的替代模型或估计方法；
- 贡献只剩「我们跑了 MATLAB 模拟」。

**通过 Gate 2 → 等人批准贡献定位 → 进入 M3。**

---

## Common Pitfalls

1. 把「库里检索不到」直接写成「文献中没有人做过」。
2. 引用了没进 library 也没被用户明示批准的文献。
3. 文献比较不区分模型类 / 估计量 / 渐近框架 / 断点类型 / 空间依赖五个维度，笼统一句「不同」。
4. PDF 没转文本就宣称「已检索全库」（索引器只吃 .txt/.md/.tex/.bib/.csv）。

---

## 独立运行说明

M2 可独立运行：提供模型一句话描述 + 文献库即可，用于给一个已有想法做贡献审计。

## 细节流程与模板

- 执行框架：`.cursor/skills/m2-literature-positioning/SKILL.md`
- 模板：`modules/M2-literature-positioning/templates/literature-matrix.csv`
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的“M2 — 文献定位”
- 用户领域资料入口：`paper-lib/`（实际资料放入项目 `literature/library/`，引用前回原文核对）
