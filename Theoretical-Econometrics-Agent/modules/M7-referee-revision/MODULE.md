# M7 — 审稿与返修

> 投稿前的最后防线：五视角专家评审（四轮）→ response 矩阵 → 返修 → 终稿一致性检查。
> 也可单独用于**外部论文**：只提供论文全文即可做模拟审稿。

---

## Requires（前置输入）

- 论文全稿（本框架 M6 产出，或外部论文 PDF/LaTeX）
- 可选：真实审稿意见（做真实返修时）

## Produces（产出）

- `projects/{slug}/reviews/referee_report_round{k}_{persona}.md` — 各视角评审报告
- `projects/{slug}/reviews/revision_log.md` — response-to-review 矩阵与修改记录
- 终稿一致性检查报告 + 更新后的终稿

## 卡点（人裁决）

1. **评审意见裁决**：每轮评审后人决定哪些意见接受、哪些抗辩、哪些延后。
2. **返修稿审定**：response 矩阵闭环后人审定终稿。

---

## 执行流程

### 步骤 1：五视角评审（persona 定义见 `agents/referee.md`）

A 理论计量审稿人 / B 当前模型的领域专家（空间、面板、时间序列、微观计量等）/
C 数学证明审计员 / D 模拟审计员 / E 表达编辑。
评分 1–5（5 = 可发表/技术闭合 … 1 = 当前不可行），九个维度：模型有效性、识别、估计方法、
假设、证明完整性、文献定位、模拟设计、可复现性、写作清晰度。
报告格式用 `modules/M7-referee-revision/templates/referee-report.md`，评分细则用 `modules/M7-referee-revision/templates/reviewer-rubrics.md`。

### 步骤 2：四轮次序

- Round 1：模型与贡献；Round 2：证明与估计；Round 3：模拟与可复现性；Round 4：全稿连贯性。
- 每轮之间走返修（步骤 3），所有 major concern 有回应前不得标记完成。
- 汇总工具：`python scripts/summarize_reviews.py --reviews projects/{slug}/reviews`。

### 步骤 3：response 矩阵（返修由 Researcher 执行，Referee 不代笔）

| Reviewer | Concern | Severity | Action taken | File changed | Status |
|---|---|---|---|---|---|

Status 词表：`resolved` / `partially resolved` / `deferred` / `rejected with reason` / `requires human verification`。

### 步骤 4：终稿一致性检查（五个维度）

- **模型**：模型节、理论节、模拟与代码中的方程、参数、数据变换及专用结构一致。
- **理论**：假设编号且被使用；定理引用假设；附录证明与定理陈述匹配；无定理依赖未列假设。
- **模拟**：DGP 与模型一致；真值与正文一致；表格来自保存输出；CP 用估计 SE；收敛失败已报告。
- **文献**：主张有依据；最近文献已讨论；贡献不夸大。
- **LaTeX**：编译通过；无未定义引用；无重复标签；记号统一。

### 步骤 5：终稿交付

最终项目应包含：`paper/main.tex`、`paper/refs.bib`、`proofs/assumptions.md`、`proofs/theorem_map.md`、
`literature/literature_matrix.csv`、`matlab/main_run_simulation.m`、`results/tables/*.csv`、
`reviews/final_review.md`、`reviews/revision_log.md`。
`main.pdf` 仅作为本地终检产物按需再生，不纳入发行树。

**proof gap 未清零时，终稿必须带 `system/integrity-rules.md` 规定的警示语。**

---

## Common Pitfalls

1. Referee 顺手改正文——违反「只攻击不代笔」，修改必须走 Researcher。
2. major concern 用一句「已修改」搪塞，response 矩阵不指向具体文件与位置。
3. 四轮评审一次性跑完再统一返修，后轮意见全部作废。
4. 终稿检查只看 LaTeX 编译，不查模型四处一致性。
5. 对外部论文评审时虚构「文中第 X 页说」——引用必须可定位。

---

## 独立运行说明

M7 可独立运行（方式 C 的典型场景）：对一篇外部论文做五视角模拟评审 + 帮助撰写 response letter。
此时不依赖本框架前序产出，只需论文全文；产出落在 `projects/{slug}/reviews/`（slug 可临时新建）。

## 细节流程与模板

- 执行框架：`.cursor/skills/m7-referee-revision/SKILL.md`
- 模板：`modules/M7-referee-revision/templates/referee-report.md`、`modules/M7-referee-revision/templates/reviewer-rubrics.md`、`modules/M7-referee-revision/templates/final-review.md`
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的“M7 — 审稿与返修”
