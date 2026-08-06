# M4 — 渐近理论与证明

> 理论计量论文的心脏：假设体系 → 引理 → 一致性 → 模型特有速率或分布 → 渐近结论，全部绑定假设编号、
> 全部区分已证/候选/缺口。本模块产出决定论文成败，卡点最密。

---

## Requires（前置输入）

- M1 冻结的模型设定 + M3 批准的估计方案
- 项目记号登记表 `proofs/notation_registry.md`

## Produces（产出）

- `projects/{slug}/proofs/assumptions.md` — 假设体系（每条有角色标签）
- `projects/{slug}/proofs/theorem_map.md` — 定理地图（结果 × 假设 × 证明素材 × 状态）
- `projects/{slug}/proofs/proof_*.md` — 各定理证明蓝图与草稿（含 proof gap 清单）
- 附录证明骨架（供 M6 使用）

## 卡点（人裁决）

1. **假设体系批准**：A1–A8 每条的角色与强度确认后才能开始写证明。
2. **定理逐条确认**：每个定理的陈述与证明草稿完成后，人逐条确认状态（candidate → verified by human）。

---

## 执行流程

### 步骤 1：假设体系（八类，逐条标角色）

- **A1 抽样与依赖结构**：独立、聚类、时间或截面依赖的范围；相应 LLN/CLT 的索引与有效样本量。
- **A2 参数空间**：紧；真值在内点（需可微处）；方差有界远离 0 与 ∞。
- **A3 数据与回归元**：矩界、秩条件、外生性或预定性，以及与所用变换的兼容性。
- **A4 扰动项**：条件均值零；支撑 LLN/CLT 的矩条件；截面与时间依赖限制；用三明治时的异方差条件。
- **A5 模型专用正则条件**：仅列当前模型需要的空间可逆性、固定效应、动态初始条件、
  断点截尾、阈值密度或其他非标准结构；不适用时明确记为 N/A。
- **A6 识别**：期望目标在真参数处唯一最优；若含离散结构参数，各候选结构必须可区分。
- **A7 一致收敛**：目标函数在参数空间上满足一致 LLN；若含离散结构参数，
  还须覆盖其允许集合；必要时证明 score/Hessian 的随机等度连续。
- **A8 CLT 与信息矩阵**：score 满足 CLT；Hessian 收敛到非奇异信息矩阵；三明治矩阵有限正定。

对照 `modules/M4-asymptotic-theory/templates/assumptions-checklist.md` 逐项打勾。

### 步骤 2：定理地图

按 `modules/M4-asymptotic-theory/templates/theorem-registry.md` 维护：每行 = 结果 × 陈述 × 引用假设 × 证明素材 × 状态。
典型结构：Lemma 1（确定性或矩阵界）→ Lemma 2（一致 LLN）→ Theorem 1（一致性）
→ Theorem 2（模型特有速率或分布，如适用）→ Theorem 3（常规参数的渐近分布）。
状态词表：`candidate` / `draft` / `proof gap` / `verified by human` / `removed`。

### 步骤 3：证明纪律（每个定理五步法）

```
Step 1 定义目标差  Q_NT(θ,τ) − Q_NT(θ₀,τ₀)
Step 2 确定性漂移（期望目标的识别性）
Step 3 一致随机余项界
Step 4 argmax 定理 / Taylor 展开
Step 5 结论 + Proof gaps 清单
```

蓝图模板：`modules/M4-asymptotic-theory/templates/proof-blueprint.md`。

### 步骤 4：非标准速率与信息速率（本模块最高危区）

- 任何收敛速率都必须从当前目标函数、依赖结构和归一化推出，**禁止套用通用结论**。
- 断点模型还取决于：N/T 哪个发散、断点幅度固定还是收缩、时间依赖、
  \(W_N\) 诱导的截面依赖，以及断点落在斜率、空间参数还是方差。
- 未推导前只能写安全表述：「在固定断点幅度设计下，断点估计量预期相对常规参数超一致；确切随机阶必须由 profile 目标的曲率与似然波动的随机阶推出。」
- 常规参数展开：\(A_{NT}^{-1/2}\partial\ell/\partial\theta \Rightarrow \mathcal{N}(0,\Omega)\)、\(-A_{NT}^{-1}\partial^2\ell/\partial\theta\partial\theta' \to_p J\)；
  **不得未经论证令 \(A_{NT}=NT\)**。

### 步骤 5：数值反例检查（可选但推荐）

用 Python（numpy/scipy）对候选矩阵界、信息矩阵正定性做小规模数值试探——只做反例排查，不替代证明。

### 步骤 6：附录骨架（Gate 4）

按当前定理地图生成：基础引理 → 目标展开 → 一致收敛 → 识别 → 一致性
→ 模型特有速率或分布 → 常规参数渐近结论 → 辅助结果。
检查：每个定理绑假设？随机阶针对 N/T 明确定义？一致收敛写明？proof gap 全列出（同步到 `system/metadata.md` 总账）？

**通过 Gate 4 → 定理逐条过人 → 进入 M5/M6。**

---

## Common Pitfalls

1. 「under regularity conditions」糊弄假设——每条假设必须编号、命名、标角色。
2. 一致收敛只写「由 ULLN 可得」但不核对所引定理的条件。
3. 照抄其他模型的收敛速率；断点模型中常见的是不检查依赖结构就套用既有断点结论。
4. Taylor 展开跨过不可微点（断点目标对 τ 是阶梯函数，对 τ 不能 Taylor）。
5. proof gap 藏在正文里不进总账，M7 审稿时才暴露。

---

## 独立运行说明

M4 可独立运行：常见用法是**审查你已有的证明**——提供证明文本，按五步法逐步核查，输出 proof gap 清单与需补假设。

## 细节流程与模板

- 执行框架：`.cursor/skills/m4-asymptotic-theory/SKILL.md`
- 模板：`modules/M4-asymptotic-theory/templates/assumptions-checklist.md`、`modules/M4-asymptotic-theory/templates/theorem-registry.md`、`modules/M4-asymptotic-theory/templates/proof-blueprint.md`
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的“M4 — 渐近理论”
