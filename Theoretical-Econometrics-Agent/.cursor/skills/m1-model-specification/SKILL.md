---
name: m1-model-specification
description: "Turns a rough theoretical econometrics idea into a precise, auditable model: variables, sample structure, dependence, parameter space, objective or QML log-likelihood, identification, and notation registry. Supports spatial, panel, break, threshold, and general QML settings without adding structures the user did not request."
---

# M1 Model Specification — 模型设定与似然函数 Skill

## Use This Skill When

1. 用户给出一个新的理论计量模型想法（一般 QML、面板、空间、断点或阈值）需要形式化。
2. 需要推导或修改 QML 对数似然、集中化目标。
3. 需要审查已有模型设定的维度、可逆性、固定效应处理。
4. 需要建立或更新记号登记表。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认角色、规则与阶段闸门（Gate 1）。
2. `modules/M1-model-specification/MODULE.md`：思维框架——14 项产出、默认基准模型、自检清单。
3. `system/metadata.md`：项目 slug 与状态。
4. 模板：`modules/M1-model-specification/templates/{model-specification.yaml, notation-registry.md}`。
5. 输入示例：`modules/M1-model-specification/examples/`。

## Scope Boundary

1. 本 skill 只处理模型设定与似然推导；不生成最终定理（M4）、不写估计算法细节（M3）、不写论文（M6）。
2. 用户提供了已有推导时，先判断推导是否成立，而不是直接重写。

## Workflow

1. 识别任务类型：全新设定 / 修改设定 / 审查推导。
2. 不擅自加入空间依赖、断点、动态项或固定效应；信息不全时用最小线性模型作格式示例，
   并把未确认选择标为 `editable`。
3. 按 MODULE.md 的 14 项逐项产出：目标 → 样本与维度 → 变量与信息集 → 模型/矩限制 →
   扰动与依赖 → 参数空间 → 变换/约化式 → 目标函数 → 集中化 → 识别 → 数值约束 →
   适用的专用结构 → 记号更新 → 开放选择与证明风险。
4. 仅在模型需要时加入空间权重、断点、固定效应或动态项，并确保目标函数与所选结构一致。
5. 结果写入 `projects/{slug}/config/model_specification.yaml` 与 `proofs/notation_registry.md`。
6. 跑 Gate 1 自检清单 → 状态改 `blocked_on_human` 等人批准 → 批准后冻结并回写 metadata。

## Output Expectations

1. 结构化模型设定文档（14 项齐全），默认选择清晰标注 `editable`。
2. `model_specification.yaml` 与记号登记表同步更新。
3. 开放选择与证明风险清单（供 M4 提前知道雷区）。
4. 不含任何最终定理陈述。

## Common Pitfalls

1. 引入符号不登记；后期正文/证明/代码记号打架。
2. 参数空间 \(\Lambda=[-c,c], c<1\) 当定理用——那只是行标准化下的默认惯例。
3. 断点集不截尾。
4. 去均值后仍用未变换的似然。
5. 一次性替用户决定模型创新点（那是 Lead Author 的卡点）。
