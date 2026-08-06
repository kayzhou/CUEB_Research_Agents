---
name: m4-asymptotic-theory
description: "Builds or audits asymptotic theory for econometric estimators: model-specific assumptions with roles, theorem maps, five-step proof blueprints, convergence rates and limiting distributions, with explicit proof gaps and no imported rate claims."
---

# M4 Asymptotic Theory — 渐近理论与证明 Skill

## Use This Skill When

1. 需要搭建假设体系（A1–A8）与定理地图。
2. 需要写一致性、模型特有收敛速率或渐近分布的证明蓝图或草稿。
3. 需要审查用户已有证明，找 proof gap、随机阶错误、维度错误、假设缺失。
4. 需要生成附录证明骨架。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认证明纪律（规则 4）、速率纪律（规则 6）与 Gate 4。
2. `modules/M4-asymptotic-theory/MODULE.md`：思维框架——模型自适应假设、定理地图、五步法与非标准速率高危区。
3. M1 模型设定 + M3 估计方案 + 项目记号登记表。
4. 模板：`modules/M4-asymptotic-theory/templates/{assumptions-checklist.md, theorem-registry.md, proof-blueprint.md}`。

## Scope Boundary

1. 只处理假设、引理、定理与证明；不改模型设定（M1）、不改算法（M3）、不排版论文（M6）。
2. 审查已有证明时逐步核查并输出意见，不直接重写整个证明（除非用户要求）。
3. 数值试探只做反例排查，不作为证明依据。

## Workflow

1. 按当前模型起草 A1–A8，每条标角色（抽样依赖 / 识别 / 可逆性 / 矩条件 /
   一致收敛 / CLT / 模型专用条件），对照 assumptions-checklist 打勾。
2. 建定理地图：基础引理与一致 LLN → 一致性 → 模型特有速率或分布 → 常规参数渐近结论；
   不适用的结果不得保留占位定理。
3. **等人批准假设体系**（卡点 1）后逐个定理走五步法：目标差 → 确定性漂移 → 一致随机界 → argmax/Taylor → 结论 + proof gaps。
4. 任意速率与 \(A_n\) 或 \(A_{NT}\) 都严禁套用通用结论；未推导前使用 MODULE.md 的安全表述。
5. 可选：numpy/scipy 小规模数值试探候选矩阵界与信息矩阵正定性。
6. 生成附录骨架（矩阵引理 → … → 辅助结果）→ proof gap 同步 metadata 总账 → Gate 4 → 定理逐条过人（卡点 2）。

## Output Expectations

1. `proofs/assumptions.md`：每条假设编号、命名、角色齐全。
2. `proofs/theorem_map.md`：状态只用 candidate / draft / proof gap / verified by human / removed。
3. `proofs/proof_*.md`：五步法结构 + 显式 proof gaps 清单。
4. 全文区分 Confirmed / Candidate / Needs verification / Not yet proved。

## Common Pitfalls

1. 「under regularity conditions」糊弄；假设不编号不标角色。
2. 引用 ULLN/CLT 不核对条件。
3. 对不可微或离散结构参数直接做 Taylor 展开。
4. 直接令 \(A_{NT}=NT\)，或照抄依赖结构不同的文献速率。
5. proof gap 藏正文不进总账。
