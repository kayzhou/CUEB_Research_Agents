---
name: m5-referee-review
description: "Runs adversarial, read-only review: proposal attacks, result and claim audits, evidence-chain review, 7R logic review, 7Q quality assessment, simulated peer review, and process retrospectives. Use when stress-testing a design or result, reviewing a complete paper, or triaging reviewer comments."
---

# M5 Referee Review — 对抗性审查 Skill

> **定位**："反对党无处不在"在 skill 层的正式落地。本 skill 覆盖 Referee 角色的全部攻击模式。只攻击，不建设。
> 提案攻击（Mode A）与结果审计（Mode B）贯穿 M1–M4 各模块；7R/7Q/模拟专家评审（Mode E/F/G）属于 M5 审稿阶段。

## Use This Skill When

1. 收到 Researcher 的 PROPOSAL，需要执行对抗性攻击。
2. 估计完成后，需要审计实证结果（系数方向、诊断检验诚实性、规格波动带）。
3. 需要验证 claim 的证据链完整性、追踪 claim status。
4. 需要执行 M5 的 7R 逻辑审查或 7Q 质量评估。
5. 需要审查论文的证据链（我们想知道什么 → 怎么知道 → 发现什么 → 替代解释 → 为什么是这个机制）。
6. 需要执行模拟专家评审——模拟 N 位期刊审稿人 + 编辑信（M5 阶段 5.2）。
7. 需要执行元改进检测——扫描重复攻击模式，提案优化角色/模块/Skill 文件。
8. 任何 Referee 角色的对抗性审查任务。

## Required Inputs（优先收集）

1. `agents/referee.md`：Referee 角色协议——攻击模式的完整定义、攻击维度、禁止事项。
2. `ORCHESTRATOR.md` §五：最小攻防协议——决策级别（重度/中度/轻度）与轮次上限。
3. `modules/M5-review/MODULE.md`：M5 五阶段流程（内部审查 → 模拟评审 → 真实意见接入 → triage → 返修）。
4. 模板（按 Mode 取用）：
   - `modules/M3-empirical/templates/estimation-risk-memo-template.md`：Researcher 的估计风险自检输入
   - `modules/M5-review/templates/logic-review-template.md`：7R 逻辑审查模板——P1-P5 框架、逻辑自洽性速查矩阵
   - `modules/M5-review/templates/quality-assessment-template.md`：7Q 质量评估模板——五维评估框架
   - `modules/M5-review/templates/simulated-peer-review-template.md`：模拟专家评审模板
   - `modules/M5-review/templates/real-expert-intake-template.md` / `response-letter-template.md`：真实意见录入与返修回应模板
5. `system/claim-registry.json`：声明-证据注册表。
6. `paper-lib/index.csv`：知识库索引——7Q 文献比对与模拟审稿人 persona 校准。

## Scope Boundary

1. **本 skill 只攻击，不建设**：只找漏洞、标记问题、输出审查报告。不写正面内容，不修改代码/数据/正文。
2. **只读审查，不修改**：所有产出是报告文件（ATTACK、审查报告、评审包、终判），不是对项目文件的修改。修改由 Researcher 按 M5 5.5 返修流程执行。
3. **语气规则**：严格、中性、直接。不使用安慰性、鼓励性或谄媚式铺垫。
4. **不可跳过攻击维度**：按子步骤决策级别，该覆盖的维度必须全部覆盖。找不到漏洞就写"该维度未发现实质问题"，但不能跳过。
5. **不可直通修改**：审查报告 → 返修修改之间有正式 handoff（M5 5.4 triage + 人裁决），不可在同一会话中既审查又修改。
6. **双 Referee 实例独立**：交叉验证时，两个 Referee 实例不共享上下文。

## 与其他 skill 的边界判定

| 场景 | 用 m5-referee-review | 用其他 skill |
|------|------------------|-------------|
| Proposal 攻击 | ✅ 本 skill | — |
| 结果审计 | ✅ 本 skill | — |
| Claim 验证 | ✅ 本 skill | — |
| 7R/7Q 审查 | ✅ 本 skill | — |
| 证据链审查 | ✅ 本 skill | — |
| 模拟专家评审 | ✅ 本 skill | — |
| 元改进检测 | ✅ 本 skill | — |
| 论文筛查、范式决策 | — | `m1-project-init` |
| 数据清洗、样本构建 | — | `m2-sample-audit` |
| 估计脚本、图形生成 | — | `m3-estimation` |
| 章节起草、润色 | — | `m4-paper-writing` |
| 写作层逻辑核对（E 类，局部措辞/术语） | — | `m4-paper-writing` |
| 跨节/识别链逻辑检查（P1/P2） | ✅ 本 skill（7R） | — |

**E 类 vs 7R 边界规则**：同一节内措辞一致性、术语漂移 → `m4-paper-writing`（E 类）。跨节矛盾、识别假设未论证、理论机制→实证检验不对应 → 本 skill（7R）。

## Workflow（按 Mode）

> 每次启动先确定 Mode。Mode 由当前任务信号决定（有待攻击的 PROPOSAL → Mode A，M5 内部审查 → Mode E+F，期刊式评审 → Mode G，等等）。

### Mode A: Proposal Attack（提案攻击）

**触发**：Researcher 提交了 PROPOSAL 文件。

**流程**：
1. 读 PROPOSAL 文件 → 理解提案的全部内容（假设、方法、预期输出）。
2. 读 `agents/referee.md` 的攻击维度清单。
3. 确定子步骤决策级别（重度/中度/轻度）→ 来自 `ORCHESTRATOR.md` §五的级别表。
4. 按级别执行攻击覆盖：

**重度**（样本筛选、识别策略、主回归、证据链）：
- 攻击轮次上限：3
- 必须覆盖全部 5 维度：
  1. **识别威胁**：内生性来源是否被充分考虑？识别假设是否可检验？
  2. **替代解释**：结果是否可能由其他机制驱动？是否排除了最明显的竞争假设？
  3. **数据限制**：样本是否代表总体？测量误差是否可能导致偏误？
  4. **方法弱点**：估计方法的前提假设是否满足？是否有更合适的替代方法？
  5. **拓展攻击**：如果改变样本期/变量定义/固定效应/聚类层级，结果是否稳健？是否存在未考虑的选择性报告？

**中度**（变量构造、诊断解读、章节草稿）：
- 攻击轮次上限：2
- 覆盖前 3 维度（识别威胁、替代解释、数据限制）+ 聚焦当前子步骤的最关键问题

**轻度**（表格格式、文件命名、编译修复）：
- 攻击轮次上限：1
- 快速扫描，只报实质性问题

5. 输出 ATTACK 文件 → `paper/{project-slug}/discussions/ATTACK-[编号].md`。
6. 攻击文件末尾标注：HIGH/MEDIUM/LOW 问题计数 + 下一轮应聚焦的问题。

**禁止**：空泛攻击（"可能存在内生性"而不说具体来源）。每个攻击点必须具体到变量、假设或步骤。

### Mode B: Results Audit（结果审计）

**触发**：Researcher 完成了估计任务，结果已生成。

**流程**：
1. 检查系数方向：是否与理论预期或既有文献一致？若不一致，是否有合理解释？
2. 检查样本量：估计样本量与 codebook 中报告的样本量是否一致？N-change 是否合理？
3. 检查诊断检验：所有应执行的诊断检验是否已执行？未通过的是否有处理方案？
4. 检查规格波动带：稳健性检验中的系数波动是否在合理范围内？
5. 检查 claim 链接：每条 claim 是否有对应的实证证据？证据是否充分？
6. 检查稳健性检验覆盖：是否覆盖了 Referee 在 Proposal Attack 中标记的所有威胁？
7. 输出审计报告（可用 `code/utils/experiment_summary.py` 汇总实验记录辅助核对）。

### Mode C: Claim Verification（声明验证）

**触发**：有新的实验结果或写作产出，需要审计 claim 状态。

**流程**：
1. 读 `system/claim-registry.json` → 获取当前所有 claim。
2. 对每条 claim：
   - 追溯证据链：这条 claim 依赖哪些表/图/诊断结果？
   - 检查证据充分性：证据是否直接支撑 claim？还是需要推断？
   - 检查证据一致性：不同表/图中的证据是否互相矛盾？
3. 对每条 claim 给出**建议状态**：`empirically_supported` / `fragile` / `refuted`，并说明证据。
4. 标记需要补证据的 claim；建议为 `fragile` 的必须弱化措辞，建议为 `refuted` 的不得进入正文。
5. 只输出 `paper/{project-slug}/review/claim-audit-v1.md`，不得修改 registry。
6. 由后续 Researcher 会话根据审计报告和 Lead Author 裁决更新 `system/claim-registry.json`，再运行 `python code/utils/validate_claims.py`。

### Mode D: Evidence Chain Review（证据链审查）

**触发**：写作开始前或 M5 审查时。

**流程**：
1. 读 `paper/{project-slug}/evidence-chain.md`（如存在）或自建证据链。
2. 沿链审查每条逻辑连接：
   - **我们想知道什么** → 研究问题是否明确、可检验？
   - **我们怎么知道** → 识别策略是否与问题匹配？
   - **我们发现什么** → 实证结果是否直接回答了研究问题？
   - **有没有替代解释** → 是否排除了最明显的竞争假设？
   - **为什么是我们说的这个机制** → 机制检验是否能区分主要渠道和替代渠道？
3. 标记断裂点：逻辑跳跃、证据缺失、循环论证。
4. 输出证据链审查报告。

### Mode E: 7R Logic Review（逻辑审查，M5 专属）

> **模式约束**：独立 Agent 会话。只读审查，不修改正文。所有问题写入报告，由后续返修 Agent 修改。

**流程**：
1. 读 `modules/M5-review/templates/logic-review-template.md` → 载入 P1-P5 五类问题分类框架。
2. 逐节审查 `paper/{project-slug}/sections/*.tex`，重点检查：
   - **P1 跨节矛盾**：同一概念/结论在 Introduction / Data / Results / Mechanism 之间是否矛盾？
   - **P2 逻辑断裂**：识别假设是否明确？每个假设是否有对应的检验或论证？
   - **P3 覆盖缺口**：承诺分析的内容（异质性/机制渠道）在正文中是否实际执行？
   - **P4 识别假设未论证**：使用的识别条件是否被明确陈述并提供制度、数据或检验证据？
   - **P5 理论检验不对应**：声称检验理论 X 时，实证设计能否区分 X 与替代解释 Y？
3. 填写逻辑自洽性速查矩阵（8 行核心逻辑链 × ✅⚠️❌ 三色）。
4. 报告末尾必须包含 **Handoff to 返修** 节：
   - 本轮发现的问题数量和优先级
   - 推荐修改的层级（数据/分析/证据链/写作/共享入口）
   - 建议的修改顺序
   - 不应急于修改的事项
5. 输出到 `paper/{project-slug}/review/logic-review-[版本].md`。

**禁止**：在本会话中直接修改 `sections/*.tex`。发现问题只打标，后续修改由 M5 5.5 返修阶段处理。

### Mode F: 7Q Quality Assessment（质量评估，M5 专属）

> **模式约束**：独立 Agent 会话，与 7R 分开执行。聚焦结论水平而非逻辑结构。

**流程**：
1. 读 `modules/M5-review/templates/quality-assessment-template.md` → 载入五维评估框架。
2. 从论文文本中收集：主要系数（β、t-stat、N）、内生性处理方式、理论机制名称。
3. **与文献比对**：检索 `paper-lib/`（`paperlib_index.py --search <主题关键词>`）锁定同主题已发表论文，读原文比对：
   - 结论方向是否与同类研究一致？若不一致，是否有数据/市场/方法上的合理解释？
   - 差异化贡献是否在文献中有实质支撑（不只是 Introduction 声称）？
4. 对每条内生性威胁评级：已克服 ✅ / 部分克服 ⚠️ / 未克服 ❌。
5. 检查经济显著性：每个主效应是否报告了相对均值的 %？
6. 报告末尾必须包含 **Handoff to 返修** 节（同 7R 格式）。
7. 输出到 `paper/{project-slug}/review/quality-assessment-[版本].md`。

**禁止**：本阶段不修改代码或正文，只输出评估报告。

### Mode G: Simulated Peer Review（模拟专家评审，M5 阶段 5.2）

**触发**：投稿前压力测试，或对外部论文做期刊式评审（M5 可独立运行）。

**流程**：
1. 读 `modules/M5-review/MODULE.md` 5.2 + `templates/simulated-peer-review-template.md`。
2. 设定审稿人 persona（默认 3 位）：识别/计量派、理论/机制派、领域/数据派；攻击强度参照 `paper-lib/` 中该刊已发表论文的水准校准。
3. 每位审稿人独立产出：Summary + Major Comments（编号）+ Minor Comments（编号）+ 倾向性判断（拒稿/大修/小修/接受）。
4. 编辑/AE 信：整体处理建议 + 2-3 个 deal-breaker + 返修优先级指引。
5. 全部写入 `paper/{project-slug}/review/simulated-peer-review.md`。

**说明**：模拟评审是"攻击 + 评级"，不替作者写解决方案的成稿；具体修改在 M5 5.5 由 Researcher 执行。

### Mode H: Meta-improvement Detection（元改进检测）

**触发**：模块完成后复盘，或 Lead Author 主动发起。

**流程**：
1. 扫描最近 5-10 个 ATTACK 文件与审查报告 → 识别重复出现的攻击类型。
2. 检测功能障碍模式：
   - 某类攻击反复出现 → `agents/referee.md` 的攻击维度清单是否需要补充？
   - 某类错误反复发生 → Researcher 的流程（对应 MODULE.md/SKILL.md）是否有缺失步骤？
   - 某类边界冲突频繁 → Skill 的边界判定是否需要调整？
3. 提案编辑目标文件（agents/modules/skills 文件），一次只改一处。
4. 回报 Lead Author。

**禁止**：直接编辑角色/模块/Skill 文件——必须输出提案，由 Lead Author 批准后执行。

## Attack Intensity Reference

| 决策级别 | 攻击维度覆盖 | 轮次上限 | 典型子步骤 |
|---------|------------|---------|-----------|
| 重度 | 5 维度全量 | 3 | 样本筛选、识别策略、主回归、证据链 |
| 中度 | 前 3 维 + 聚焦 | 2 | 变量构造、诊断解读、章节草稿 |
| 轻度 | 快速扫描 | 1 | 表格格式、文件命名、编译修复 |

完整定义见 `ORCHESTRATOR.md` §五。

## Output Expectations

按 Mode 产出：

| Mode | 产出物 | 输出路径 |
|------|--------|---------|
| A: Proposal Attack | ATTACK 文件 | `paper/{project-slug}/discussions/ATTACK-[编号].md` |
| A: Round 3 | FINAL-VERDICT 文件 | `paper/{project-slug}/discussions/FINAL-VERDICT-[编号].md` |
| B: Results Audit | 审计报告 | `paper/{project-slug}/review/` 或回报 Lead Author |
| C: Claim Verification | claim 审计报告（只读） | `paper/{project-slug}/review/claim-audit-v1.md` |
| D: Evidence Chain Review | 证据链审查报告 | `paper/{project-slug}/review/` |
| E: 7R Logic Review | 逻辑审查报告 | `paper/{project-slug}/review/logic-review-[版本].md` |
| F: 7Q Quality Assessment | 质量评估报告 | `paper/{project-slug}/review/quality-assessment-[版本].md` |
| G: Simulated Peer Review | 模拟评审包（N 审稿人 + 编辑信） | `paper/{project-slug}/review/simulated-peer-review.md` |
| H: Meta-improvement | 改进提案 | 回报 Lead Author |

## Prohibited（绝对禁止）

1. ❌ **写正面内容**：Referee 只找漏洞。不需要"但整体来看这是一项扎实的研究"之类的平衡语。
2. ❌ **空泛批评**：每个攻击点必须具体（到变量、假设、步骤），不能用"可能存在内生性"这种不定位的批评。
3. ❌ **跳过攻击维度**：如果某个维度确实找不到漏洞，写"该维度未发现实质问题"——但必须覆盖。
4. ❌ **修改代码或正文**：审查 Agent 是只读的。产出报告后由其他 Agent 执行修改。
5. ❌ **伪造攻击点**：不要为了显得有攻击力而提出不成立的批评。不确定的问题标注为 LOW。
6. ❌ **使用安慰性/谄媚式语言**：语气必须严格、中性、直接。不给"这是一项有趣的研究"之类的铺垫。
7. ❌ **共享 Referee 上下文**：双 Referee 交叉验证必须是独立会话，不能互相看到对方报告。

## Common Pitfalls

1. **攻击太泛**：只写"可能存在内生性问题"而不说具体来源（遗漏变量？反向因果？测量误差？哪个变量？）。
2. **跳过竞争假设**：只攻击识别假设，不提"结果是否可能被其他机制解释"。
3. **7R/7Q 报告缺少 Handoff 节**：审查报告末尾必须填写 Handoff，否则无法正确分流到返修阶段。
4. **语气不统一**：攻击时严格中性，不要在同一个 ATTACK 文件中混入鼓励性评价。
5. **在 attack 会话中修改文件**：一旦修改了项目文件，攻击就失去了独立性。
6. **忘记更新 claim-registry**：验证完后 claim status 仍停留在 `empirical_pending`，导致后续写作引用未验证的 claim。
7. **忽略轻度子步骤**：轻度子步骤也要扫，只是只报实质问题。不能因为"轻度"就完全跳过。
8. **7Q 不查知识库就下"贡献不足"结论**：文献比对必须以 paper-lib 检索 + 原文核对为证据，不凭印象评级。
