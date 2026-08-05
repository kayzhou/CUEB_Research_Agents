# M1 — 模型设定与似然函数

> 把一个粗糙的模型想法变成精确、可证明、可模拟的数学对象。这是全流程的地基：
> 后面所有模块（估计、证明、模拟、写作）都以本模块冻结的模型为准。

---

## Requires（前置输入）

- 模型想法（口头描述即可）：研究对象、样本结构、条件均值或分布、依赖结构、估计方法与理论目标
- 可选专用结构：空间权重、固定效应、动态项、断点、阈值、多重 regime 或参数异质性
- 可选：已有 LaTeX 草稿或矩阵表达式

## Produces（产出）

- `projects/{slug}/config/model_specification.yaml` — 结构化模型设定
- `projects/{slug}/proofs/notation_registry.md` — 记号登记表（首版）
- 模型设定文档：结构方程、简化式、参数空间、QML 对数似然、识别性讨论、开放选择与证明风险清单

## 卡点（人裁决）

1. **模型设定批准**：模型方程、断点结构、固定效应处理、参数空间确认后才能冻结进入 M2/M3。

---

## 执行流程

### 步骤 1：任务识别与默认基准

先判断用户输入属于：全新设定 / 修改已有设定 / 审查已有推导。
不为用户擅自加入空间依赖、断点、动态项或固定效应。信息不全时，先用
\(y_i=x_i'\beta+u_i\) 作为纯格式示例，并将所有未确认选择标为 `editable`。

若用户明确选择带单一未知时间断点的空间杜宾面板，可采用以下专用基准：

\[
y_t = \lambda_j W_N y_t + X_t\beta_j + W_N X_t\gamma_j + \alpha + u_t,
\qquad t\in\mathcal{T}_j(\tau_0),\quad j=1,2,
\]

等价地 \(S_N(\lambda_j)y_t = X_t\beta_j + W_N X_t\gamma_j + \alpha + u_t\)，其中 \(S_N(\lambda)=I_N-\lambda W_N\)。
SAR 特例：\(\gamma_j=0\)；无空间滞后特例：\(\lambda_j=0\)。

### 步骤 2：逐项产出（14 项，缺一不可）

1. 研究目标；2. 样本、指标、维度与渐近框架；3. 变量与信息集；
4. 结构方程或条件矩限制；5. 扰动过程与依赖结构；6. 参数向量与参数空间；
7. 变换、简化式或约化式（如适用）；8. 目标函数或 QML 对数似然；
9. 集中化目标（如适用）；10. 识别性讨论；11. 估计所需数值约束；
12. 模型专用结构（空间权重、固定效应、动态项、断点或阈值，仅在适用时填写）；
13. 记号登记表更新；14. 开放选择与证明风险。

### 步骤 3：QML 对数似然

先从用户模型与工作分布推导目标函数，不得套用无关模型的 Jacobian、方差或 regime 项。
对上述空间杜宾断点专用基准，在 regime 内同方差时：

\[
\ell_{NT}(\theta_1,\theta_2,\tau)
=\sum_{j=1}^2\Big[
T_j(\tau)\log|S_N(\lambda_j)|
-\tfrac{NT_j(\tau)}{2}\log(2\pi\sigma_j^2)
-\tfrac{1}{2\sigma_j^2}\textstyle\sum_{t\in\mathcal{T}_j(\tau)} e_{jt}(\theta_j)'e_{jt}(\theta_j)
\Big],
\]

其中 \(e_{jt}(\theta_j)=S_N(\lambda_j)y_t-X_t\beta_j-W_NX_t\gamma_j-\alpha_j\)，\(T_1(\tau)=\tau\)、\(T_2(\tau)=T-\tau\)。
共同方差时以 \(\sigma^2\) 替换并合并残差平方和。

### 步骤 4：固定效应处理（仅面板模型适用）

若模型包含固定效应，必须显式选择直接估计、组内变换、准去均值或双向效应等处理方式，
并使似然与变换一致。动态项只有在同时给出相应偏误修正与渐近框架时才能加入。

### 步骤 5：自检清单（Gate 1）

- 样本结构、信息集、外生性与误差依赖是否明确？
- 目标函数是否由当前模型推出，参数空间是否与识别条件相容？
- 渐近框架和有效样本量是否明确？
- 若含 \(W_N\)：标准化、随机性、稀疏性与空间乘子可逆性是否明确？
- 若含断点或阈值：变化参数、截尾集、共同性与 regime 方差是否明确？
- 若含固定效应或动态项：变换、似然和偏误修正是否一致？

**通过 Gate 1 → 等人批准 → 冻结模型，写入 metadata。**

---

## Common Pitfalls

1. 记号未登记就往下推导，后期正文/证明/代码三处打架。
2. 固定效应处理与似然不匹配（去均值后仍用原似然）。
3. 参数空间 \(\Lambda=[-1,1]\) 当成定理使用——行标准化 + 谱半径界只是默认惯例。
4. 用户给了已有推导时直接重写而不是先判断对错。
5. 一次性生成最终定理（那是 M4 的事，本模块只标证明风险）。

---

## 独立运行说明

M1 可独立运行：只需一句模型想法。产出的 `model_specification.yaml` + 记号登记表即是 M2–M6 的输入契约。

## 细节流程与模板

- 执行框架：`.cursor/skills/m1-model-specification/SKILL.md`
- 模板：`modules/M1-model-specification/templates/model-specification.yaml`、`modules/M1-model-specification/templates/notation-registry.md`
- 输入/输出示例：`modules/M1-model-specification/examples/model-request-example.md`、`modules/M1-model-specification/examples/expected-output-outline.md`
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的“M1 — 模型设定”
