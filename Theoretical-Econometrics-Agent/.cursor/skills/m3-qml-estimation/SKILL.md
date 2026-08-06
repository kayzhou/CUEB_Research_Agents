---
name: m3-qml-estimation
description: "Derives an auditable QML or M-estimation procedure: concentration or profiling when justified, constrained optimization, standard-error design, discrete-parameter search when applicable, and numerical safeguards."
---

# M3 QML Estimation — QML 估计方法 Skill

## Use This Skill When

1. 需要推导目标函数、profile / 集中化步骤或约束优化算法。
2. 需要制定标准误方案（Hessian / 三明治 / bootstrap …）。
3. 需要审查估计算法的数值稳定性（秩、缩放、边界、多起点；适用时含 log-det）。
4. 需要为 M5 写代码前的算法伪代码规格书。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认 Gate 3。
2. `modules/M3-qml-estimation/MODULE.md`：思维框架——估计目标、集中化公式、算法模板、SE 五选一、数值防线。
3. M1 冻结的 `config/model_specification.yaml`（含固定效应处理选择）。
4. 模板：`modules/M3-qml-estimation/templates/qml-derivation.md`。

## Scope Boundary

1. 只处理估计方法设计与推导；不证明渐近性质（M4）、不写模拟代码（M5）。
2. 估计量的每个计算与理论前提条件必须显式陈述，供 M4 转化为假设。

## Workflow

1. 写出当前模型的估计目标；只有存在离散结构参数时才写 profile 层。
2. 只消去可解析集中化的参数，并记录所需秩与可逆性条件；不得丢掉仍依赖待估参数的项。
3. 写五步算法：数据与约束 → 集中化/优化 → 可选离散搜索 → 最终重估 → 协方差，并给出伪代码。
4. SE 方案五选一并声明理由；理论用 Hessian/三明治，模拟同时报经验 SD。
5. 列数值防线：数值秩、缩放、边界、多起点和 exit flag；空间模型另查近奇异乘子与 log-det，
   断点模型另查截尾网格。
6. 产出 `projects/{slug}/estimation/qml_estimation_plan.md` → Gate 3 自检 → `blocked_on_human` 等人批准。

## Output Expectations

1. `qml_estimation_plan.md` 六段齐全：参数空间 / 目标与可选 profile / 估计算法 / 标准误 / 数值稳定检查 / 伪代码。
2. 每个理论前提（紧性、可逆性、内点）显式标注，供 M4 接手。
3. 计算复杂度说明；若含断点、空间乘子或高维矩阵，应拆分相应网格、优化和分解成本。

## Common Pitfalls

1. 集中化时丢掉参数相关项。
2. 对没有离散结构的模型套用网格；或对断点网格不截尾。
3. SE 方案含糊，M5 的 CP 无法对齐。
4. 多峰目标只用单起点局部优化。
5. 未识别可缓存计算，模拟成本失控。
