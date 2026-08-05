# M5 — 审稿与返修

> 相对原框架：**全保留**内部审查（7R 逻辑 + 7Q 质量），并**新增**：
> （1）模拟专家评审阶段——模拟期刊同行评审，产出多位审稿人意见 + 编辑信；
> （2）人工真实意见接入——可人工录入真实专家/审稿人意见，与模拟意见合并；
> （3）返修产出——输出逐条回应（response letter / 返修意见）+ 最终优化稿。

---

## Requires（前置输入）

- **论文全文**（本框架 M4 产出，或一篇外部已有论文——M5 可对外部论文独立运行）
- 结果表图与实验记录（可选；有则审计更扎实）
- 文献索引（可选；7Q 与文献比对用）

## Produces（产出）

- 内部审查报告：`paper/{project-slug}/review/logic-review-v1.md` + `quality-assessment-v1.md`
- **模拟专家评审包**：`paper/{project-slug}/review/simulated-peer-review.md`
- **真实意见摄入**：`paper/{project-slug}/review/real-expert-intake.md`
- **返修意见**：`paper/{project-slug}/review/response-letter.md`
- **最终优化稿**：修订后的 `sections/` + `paper/{project-slug}/review/changelog.md`

## 卡点（人裁决）

1. **评审意见裁决**：模拟 + 真实意见合并后，由人确认哪些必改、哪些辩驳、哪些标局限。
2. **返修稿审定**：最终优化稿由人审定后才算定稿。

---

## 五个阶段

```
5.1 内部审查（7R 逻辑 + 7Q 质量）
      ↓
5.2 模拟专家评审（N 审稿人 + 编辑信）        ← 新增
      ↓
5.3 真实专家意见接入（人工录入，可选但推荐）   ← 新增
      ↓
5.4 意见合并与返修 triage（卡点：人裁决）
      ↓
5.5 返修执行 → response letter + 最终优化稿（卡点：审定）
```

每个阶段可独立运行。例如只想要模拟评审 → 跑 5.2；已有真实审稿意见要返修 → 从 5.3 切入。

---

## 5.1 内部审查（保留）

独立、只读，产出报告，不改正文。

**7R 逻辑审查**：逐节查四条逻辑链（研究问题→识别策略、识别假设→检验证据、理论机制→实证检验、各章节互不矛盾），按 P1-P5 分类标问题，填逻辑自洽性速查矩阵。输出 `review/logic-review-v1.md`。

**7Q 质量评估**：五维（问题重要性、贡献超越文献、方法前沿适当、数据样本充分、写作清晰）。重点：结论方向与文献是否一致（比对对象优先从 `paper-lib/` 检索同主题已发表论文）、每个主效应是否报经济显著性、内生性威胁逐项评级（✅/⚠️/❌）。输出 `review/quality-assessment-v1.md`。

> 7R 与 7Q 用独立会话、互不共享上下文。报告末尾填 Handoff 节（问题数、推荐修改层级、修改顺序、不应急于改的事项）。

---

## 5.2 模拟专家评审（新增）

> 目标：在投稿前，用一个模拟的期刊同行评审流程压力测试论文。模拟 2-3 位独立审稿人 + 一位 AE/编辑。

### 执行步骤

1. **设定审稿人 persona**（默认 3 位，可调）：每位有不同侧重，模拟真实评审组的多样性；攻击强度参照 `paper-lib/` 中目标期刊已发表论文的水准校准。
   - **审稿人 1（识别/计量派）**：盯识别策略、内生性、稳健性、计量细节。
   - **审稿人 2（理论/机制派）**：盯理论贡献、机制是否讲清、与文献的对话、经济显著性。
   - **审稿人 3（领域/数据派）**：盯数据质量、样本代表性、制度背景、外部有效性、政策含义。
2. **每位审稿人独立产出评审意见**（用 `templates/simulated-peer-review-template.md`）：
   - 一段 Summary（这篇论文做了什么——证明审稿人读懂了）
   - **Major Comments**（影响能否发表的问题，编号）
   - **Minor Comments**（次要问题，编号）
   - 倾向性判断（拒稿 / 大修 / 小修 / 接受）+ 一句理由
   - 语气严格、中性、专业，不安慰性铺垫。
3. **编辑/AE 信**：综合 3 位意见，给出：
   - 整体处理建议（Reject / Major Revision / Minor Revision / Accept）
   - 编辑视角最关键的 2-3 个 deal-breaker
   - 给作者的返修优先级指引
4. 全部写入 `simulated-peer-review.md`。

> 说明：模拟评审是「攻击 + 评级」，不替作者写解决方案的成稿；具体修改在 5.5 由作者（Researcher）执行。

### 独立运行（对外部论文）

只跑 5.2 时，输入只需论文全文（PDF/tex/文本均可）。模拟评审不依赖本框架前序产出。

---

## 5.3 真实专家意见接入（新增）

> 当你拿到**真实**的合作者批注、导师意见、或期刊审稿意见时，在此结构化录入，与模拟意见同等对待进入返修。

1. 人工把真实意见原文粘贴进来（可以是邮件、批注、审稿报告）。
2. 逐条录入 `real-expert-intake.md`（用 `templates/real-expert-intake-template.md`）：来源、原文、摘要、初步影响层级（数据/分析/证据链/写作）。
3. 真实意见**优先级高于**模拟意见——冲突时以真实意见为准。
4. 标注哪些真实意见与 5.1/5.2 已发现的问题重合（合并去重）。

> 真实意见可在任何时候接入；没有真实意见时本阶段可跳过，仅用模拟评审驱动返修。

---

## 5.4 意见合并与返修 triage（卡点）

1. **合并去重**：把 7R + 7Q + 模拟评审 + 真实意见汇总成一张问题清单，去重、按严重性排序（HIGH/MEDIUM/LOW；真实审稿人的 Major 默认 HIGH）。
2. **triage 四问**（每条问题）：本轮改什么？触及哪一层（数据/分析/证据链/写作）？哪些上游必须重开？哪些明确不动？
3. **人裁决**：逐条确定处置——必改 / 辩驳（不改但要在 response 里解释）/ 标为局限。
4. 输出合并清单 + triage 结论。**等人裁决后进入 5.5。**

---

## 5.5 返修执行 → response letter + 最终优化稿（卡点：审定）

1. **执行修改**（由 Researcher 角色，遵守 M2-M4 各自规则）：
   - 触及数据 → 回 M2 流程；触及方法/识别 → 回 M3 流程；纯写作 → M4 流程。
   - 自上而下回填上游文档（codebook / checklist / evidence-chain / section-brief），不留「口头已改文档未更新」。
2. **写 response letter**（`templates/response-letter-template.md`）——逐条 point-by-point：
   - 重述每条意见（We thank the reviewer for...）
   - 回应类型：已修改（指出改在哪、第几节/表）/ 解释说明（为何这样处理）/ 已作为局限说明。
   - 引用修订稿的具体位置（页/节/表号）。
   - 真实审稿意见用礼貌专业的投稿口吻；内部/模拟意见可用简洁中文。
3. **产出最终优化稿**：修订后的 `sections/`（及对应 `sections_cn/`），所有 `[TODO]/[CHECK]` 清零。
4. **更新 changelog**：本轮轮次、影响范围、已处理问题、未关闭问题去向。
5. **人审定**：最终优化稿 + response letter 由人审定后定稿。

---

## 关键约束

1. 审查阶段（5.1/5.2）只读、只产出意见，不改正文——保证审查独立性。
2. 修改阶段（5.5）才动正文，且走 triage 批准的切片，不直接从手头文件开改。
3. 真实意见优先于模拟意见；冲突以真实意见为准。
4. 同一会话不可既审查又修改（审查与修改分会话）。

---

## 独立运行说明

- **只要内部审查**：跑 5.1。
- **只要模拟专家评审**（含对外部论文）：跑 5.2，输入论文全文即可。
- **已有真实审稿意见要返修**：从 5.3 切入 → 5.4 → 5.5。
- **完整审稿到返修**：5.1 → 5.5 全跑。

模板见 `templates/`：`logic-review-template.md`、`quality-assessment-template.md`、`simulated-peer-review-template.md`、`real-expert-intake-template.md`、`response-letter-template.md`。

---

## 细节流程 Skill 与代码/工具

- **执行框架（细节流程）**：`.cursor/skills/m5-referee-review/SKILL.md` —— 8 种攻击 Mode（Proposal Attack / Results Audit / Claim Verification / Evidence Chain / 7R / 7Q / Simulated Peer Review / Meta-improvement）、攻击强度参考表、禁止事项。
- **知识库**：`paper-lib/` —— 7Q 文献比对与模拟审稿人 persona 校准的证据来源。
- **相关代码/工具**：
  - `paper/exports/` —— 把审查/返修稿导出 docx（python-docx）供合作者批注。
  - `code/utils/experiment_summary.py` —— Results Audit 时汇总实验记录，核对系数/样本量/诊断。
- **设计理念（重要）**：`discussions/V3.0-discussion-2-opposition-party.md` —— 「反对党无处不在」的对抗式审查设计原理；`discussions/V3.0-autoscientists-study.md` —— 自动化科研的背景讨论。模拟专家评审正是这一理念在投稿前的延伸。
