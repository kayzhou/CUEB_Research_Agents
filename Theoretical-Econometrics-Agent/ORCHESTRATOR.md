# ORCHESTRATOR — Theoretical-Econometrics-Agent 编排器

> 本文件是框架的唯一入口骨架。每次启动先读本文件确认角色与当前模块，再按需补读对应 `modules/MX-*/MODULE.md`。

---

## 一、角色架构（三角色）

- **Lead Author（人类）**：模型创新点、核心识别逻辑与最终理论结论不可由 AI 单方面确定。负责全部卡点裁决。
- **Researcher（执行者）** → `agents/researcher.md`：推导、编码、写作 + 拓展思考 + 回应攻击。
- **Referee（审稿人）** → `agents/referee.md`：按五视角（理论计量 / 当前模型领域 /
  证明审计 / 模拟审计 / 表达编辑）攻击产出。只攻击不代笔。

轻量任务由主会话直接走「自我攻防」；只有重度子步骤（模型设定、假设体系、核心定理、模拟设计、正式审稿）才建议启动独立 Referee 会话保证独立性。

---

## 二、启动协议

1. 读本文件 → 确认角色与模块路由。
2. 载入本机工具链：Windows PowerShell 必须点调用 `. .\scripts\setup_env.ps1`（点与路径之间有空格），macOS/Linux 执行 `source scripts/setup_env.sh`；路径与引擎路由见 `ENVIRONMENT.md`，Stata/MATLAB 的 MCP 与本地直连见 [`本地化部署说明.md`](本地化部署说明.md)。首次迁移先按 `使用手册.md` 第二篇重建环境。
3. 读 `system/metadata.md` → 确认项目 slug、当前模块、各产出状态。
4. 新项目先 `python scripts/init_project.py --name {slug} --output projects` 初始化工作区。
5. 选运行方式（A 端到端 / B 从某步切入 / C 单模块）。
6. 打开目标模块 `MODULE.md` → 检查 Requires 是否齐全；缺则先用 `templates/paper-project/` 补 stub 并记录。
7. 按模块「执行流程」推进；遇卡点先把状态改为 `blocked_on_human`，再等待裁决。
8. 模块收尾时回写 `system/metadata.md` 的产出状态、冻结输入和下一步。

---

## 三、不可违反规则

1. **不伪造**：文献、定理陈述、页码、证明步骤、模拟结果一律不得虚构（完整清单见 `system/integrity-rules.md`）。
2. **记号纪律**：每个新符号必须登记到项目 `proofs/notation_registry.md`；正文、证明、代码三处记号一致。
3. **假设纪律**：每条假设有明确角色（抽样依赖 / 识别 / 可逆性 / 矩条件 /
   一致收敛 / CLT / 模型专用结构 / 模拟可行性）；每个定理显式引用其使用的假设编号。
4. **证明纪律**：证明缺口显式标 `Proof gap` 并说明缺什么；全文区分 `Confirmed` / `Candidate` / `Needs verification` / `Not yet proved` 四种状态，候选结论不得写成已证定理。
5. **模拟纪律**：DGP 必须与理论模型一致（除非显式声明为稳健性设计）；种子、真值、N/T、重复次数、输出路径必须记录；表格由脚本从保存的原始估计生成，不得手工输入；失败与不收敛必须报告。
6. **速率纪律**：任何收敛速率与有效信息速率均不得套用通用结论，必须从当前目标、
   依赖结构与渐近框架推导；未推导前只能写候选表述。
7. **文献纪律**：所有文献主张必须落在 `literature/library/`、BibTeX 或用户明示批准的外部文献上；「库里没有 ≠ 新颖性成立」，措辞必须保守。
8. **审稿只攻击不代笔**：Referee 与模拟专家只产出意见报告，不改正文/代码；修改走 M7 返修流程。
9. 人卡点不可跳过：模型设定、贡献定位、估计方案、假设体系、模拟设计、章节草稿、返修审定。
10. 全程中文沟通（英文投稿正文除外）。

---

## 四、模块路由

每个模块 = 思维框架（MODULE.md）+ 执行框架（对应 Skill，编号一致）+ 相关模板/工具。
先读 MODULE.md 确定产出与卡点，再读 Skill 获取完整执行步骤。

| 当前任务 | 模块 | 思维框架 | 执行框架 Skill | 主要模板/工具 |
|---------|------|---------|---------------|--------------|
| 模型设定、似然函数、参数空间、记号 | **M1** | `modules/M1-model-specification/MODULE.md` | `.cursor/skills/m1-model-specification/SKILL.md` | `model-specification.yaml`、`notation-registry.md` 模板 |
| 文献检索、文献矩阵、贡献定位 | **M2** | `modules/M2-literature-positioning/MODULE.md` | `.cursor/skills/m2-literature-positioning/SKILL.md` | `literature-matrix.csv` 模板、`scripts/build_rag_index.py`、`paper-lib/` |
| QML 估计算法、集中化或 profile、优化、SE | **M3** | `modules/M3-qml-estimation/MODULE.md` | `.cursor/skills/m3-qml-estimation/SKILL.md` | `qml-derivation.md` 模板 |
| 假设体系、定理地图、证明推导 | **M4** | `modules/M4-asymptotic-theory/MODULE.md` | `.cursor/skills/m4-asymptotic-theory/SKILL.md` | `assumptions-checklist.md`、`theorem-registry.md`、`proof-blueprint.md` 模板 |
| DGP、Monte Carlo、bias/RMSE/CP 表 | **M5** | `modules/M5-monte-carlo/MODULE.md` | `.cursor/skills/m5-monte-carlo/SKILL.md` | `simulation-design.yaml` 模板、MATLAB MCP / 本地直连 / Octave（`ENVIRONMENT.md`） |
| LaTeX 章节、附录证明、编译 | **M6** | `modules/M6-paper-writing/MODULE.md` | `.cursor/skills/m6-paper-writing/SKILL.md` | `templates/paper-project/paper/`、TeX Live、`scripts/check_latex_notation.py` |
| 五视角评审、response 矩阵、终稿检查 | **M7** | `modules/M7-referee-revision/MODULE.md` | `.cursor/skills/m7-referee-revision/SKILL.md` | `referee-report.md`、`reviewer-rubrics.md` 模板、`scripts/summarize_reviews.py` |

### 支撑层

- **`templates/paper-project/`**：论文工作区模板及 `scripts/init_project.py` 的复制源；
  当前内容是空间面板断点默认骨架，其他模型必须在 Gate 1 后替换不适用占位。
- **`examples/`**：一个中性 QML 工作流文档案例；只读，不含实测结果或可投稿论文。
- **`paper-lib/`**：用户提供的领域资料入口。仅保存来源与权限明确的材料，引用前回原文核对。
- **`scripts/`**：环境激活、初始化、RAG 索引、LaTeX 检查、评审汇总、Skill 校验、MCP 配置示例。

---

## 五、最小攻防协议（贯穿各模块）

每个重度子步骤遵循：

```
Researcher 写 PROPOSAL（含拓展思考）
  → Referee 写 ATTACK（按决策级别覆盖维度，标 HIGH/MEDIUM/LOW）
  → Researcher 写 RESPONSE（改 / 辩 / 标局限）
  → Lead Author 裁决 → 批准执行
  → Researcher 执行 → 记录 → Referee 审计
```

| 级别 | 攻击覆盖 | 轮次上限 | 典型子步骤 |
|------|---------|---------|-----------|
| 重度 | 全维度 | 3 | 模型设定、假设体系、核心定理证明、模拟设计、正式审稿 |
| 中度 | 关键维度 + 聚焦 | 2 | 集中化推导、单条引理、文献矩阵、章节草稿 |
| 轻度 | 快速扫 | 1 | 记号统一、表格格式、编译修复 |

轻量任务可省略独立会话，由主会话自审；但 HIGH 级问题必须显式记录与回应。

---

## 六、阶段闸门（Stage Gates）

后一模块的产出不得视为最终结论，除非前面的闸门已通过：

- **Gate 1 模型有效性**（M1 收尾）：维度、信息集、依赖与参数空间清楚？模型专用结构有效？
  目标函数与误差及数据变换兼容？
- **Gate 2 文献落地**（M2 收尾）：引用均可核对？比较区分模型、识别、估计、
  渐近框架与依赖结构？贡献措辞不夸大？
- **Gate 3 估计可行性**（M3 收尾）：目标函数在容许参数域上可计算？优化与约束落实？
  模型专用搜索规则有效？SE 在选定渐近框架下有定义？
- **Gate 4 理论闭合**（M4 收尾）：每个定理绑定假设？随机阶针对 N/T 明确定义？该用一致收敛处写明？proof gap 全部列出？
- **Gate 5 模拟可复现**（M5 收尾）：DGP 与模型一致？真值已记录？种子受控？bias/RMSE/CP 由保存的估计计算？
- **Gate 6 论文一致性**（M6 收尾）：记号 / 假设 / 定理 / 附录标签同步？文献主张有引用？结果表来自可复现输出？编译零未定义引用？

---

## 七、状态机（模块级）

主状态只有四种：

`not_started` → `in_progress` → `blocked_on_human` → `in_progress` → `done`

- `blocked_on_human`：报告和待决问题已落盘，禁止继续执行会受该决定影响的步骤。
- `done`：规范产出齐全、对应 Gate 通过、冻结输入已记录。
- 从中间切入时可用带来源限定的完成态：`done(stub)`、`done(external)`、`done(partial)`；备注中写明缺失项、输入来源和适用边界。
