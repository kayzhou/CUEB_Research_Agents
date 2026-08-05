---
name: m7-referee-revision
description: "Runs multi-round expert review of a theoretical econometrics paper from five roles (theory referee, model-appropriate domain specialist, proof auditor, simulation auditor, exposition editor), builds the response matrix, and performs final consistency checks."
---

# M7 Referee & Revision — 审稿与返修 Skill

## Use This Skill When

1. 需要对论文（本框架产出或外部论文）做五视角模拟评审。
2. 需要把评审意见转成 response-to-review 矩阵并管理返修。
3. 需要做投稿前的终稿一致性检查。
4. 需要针对真实审稿意见撰写 response letter。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认「审稿只攻击不代笔」（规则 8）。
2. `modules/M7-referee-revision/MODULE.md`：思维框架——五视角、四轮次序、response 矩阵、五维一致性检查。
3. `agents/referee.md`：persona 定义与常用攻击清单。
4. 论文全稿 + （内部评审时）`proofs/`、`results/`、metadata 的 proof gap 总账。
5. 模板：`modules/M7-referee-revision/templates/{referee-report.md, reviewer-rubrics.md, final-review.md}`。

## Scope Boundary

1. Referee 会话只产出评审报告，**不修改**证明、代码或正文；返修由 Researcher 会话按裁决执行。
2. 评审意见必须可定位（公式编号 / 假设编号 / 页码 / 代码行）；不可定位的意见无效。
3. 对外部论文：不虚构原文内容，无法核实处标 `cannot verify`。

## Workflow

### 评审任务（Referee 角色）

1. 确认轮次（R1 模型与贡献 / R2 证明与估计 / R3 模拟与可复现 / R4 全稿连贯）。
2. 按该轮相关 persona 逐个出报告：1–5 评分 × 九维度 + Major / Minor / Required revisions / Proof gaps or code risks / Recommendation。
3. `python scripts/summarize_reviews.py --reviews projects/{slug}/reviews` 汇总 → **等人裁决意见**（卡点 1）。

### 返修任务（Researcher 角色）

1. 按裁决把每条意见填入 response 矩阵（resolved / partially resolved / deferred / rejected with reason / requires human verification）。
2. 逐条修改并回填 File changed；未解决的 proof gap 保留显式标注，**不得抹掉**。
3. 所有 major concern 闭环后进下一轮或终检。

### 终稿检查任务

1. 五维一致性：模型四处一致 / 理论绑定 / 模拟可溯 / 文献不夸大 / LaTeX 干净。
2. 用 `modules/M7-referee-revision/templates/final-review.md` 生成 `reviews/final_review.md`，核对最终交付清单（MODULE.md 步骤 5）→ **等人审定终稿**（卡点 2）。

## Output Expectations

1. 每份评审报告遵循 referee-report 模板，评分有据、意见可定位。
2. `revision_log.md`：response 矩阵完整，逐条指向具体文件修改。
3. proof gap 未清零的终稿带警示语。

## Common Pitfalls

1. Referee 顺手改正文。
2. 「已修改」式空洞 response。
3. 四轮一次跑完再返修。
4. 终检只看编译不查模型一致性。
5. 评审外部论文时虚构页码引文。
