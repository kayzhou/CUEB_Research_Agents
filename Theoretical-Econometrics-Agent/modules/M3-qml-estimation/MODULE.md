# M3 — QML 估计方法

> 把 M1 的目标函数变成可执行、数值稳定的估计算法：集中化或 profile、优化、约束与标准误方案。
> 本模块产出同时是 M4 证明的对象和 M5 代码的规格书。

---

## Requires（前置输入）

- M1 冻结的模型设定与 QML 对数似然（`config/model_specification.yaml`）

## Produces（产出）

- `projects/{slug}/estimation/qml_estimation_plan.md` — 参数空间、profile likelihood、估计算法、SE 方案、数值稳定检查、伪代码

## 卡点（人裁决）

1. **估计方案批准**：目标函数、集中化或优化路线、约束与 SE 类型确认后才能进入 M4/M5。

---

## 执行流程

### 步骤 1：估计目标

一般地，
\[
\widehat\theta=\arg\max_{\theta\in\Theta}\ell_n(\theta)
\]
或最小化等价损失。若模型含离散结构参数 \(\eta\)（如断点、类别或模型阶数），
先求 \(\widehat\theta(\eta)\)，再对允许集合 profile：
\[
\widehat\eta=\arg\max_{\eta\in\mathcal H}\ell_n(\widehat\theta(\eta),\eta).
\]
无离散结构的模型不得人为引入网格搜索。

### 步骤 2：集中化似然

仅对可解析消去的参数做集中化，并记录集中化所需的秩、可逆性和内点条件。
对空间杜宾断点专用模型，固定 \(\lambda_j,\tau\)，令
\(\widetilde y_{jt}=S_N(\lambda_j)y_t\)、\(Z_t=[X_t, W_NX_t, D_\alpha]\)、\(\delta_j=(\beta_j',\gamma_j',\alpha_j')'\)，
regime 内最小二乘估计 \(\delta_j\)（与 M1 选定的固定效应处理一致），集中残差方差
\(\widehat\sigma_j^2(\lambda_j,\tau)=\frac{1}{NT_j}\sum_{t\in\mathcal{T}_j(\tau)}\widehat e_{jt}'\widehat e_{jt}\)，集中目标

\[
\ell_c(\lambda_1,\lambda_2,\tau)
=\sum_{j=1}^2\Big[T_j\log|S_N(\lambda_j)|-\frac{NT_j}{2}\log\widehat\sigma_j^2(\lambda_j,\tau)\Big]+C.
\]

### 步骤 3：算法模板

1. 冻结参数空间、约束和数据变换。
2. 解析求解可集中化参数；其余参数采用与目标结构相符的优化方法。
3. 若存在离散结构参数，在允许集合上 profile；断点模型必须使用截尾网格。
4. 在最终结构参数处重估全部待报告参数。
5. 估计协方差矩阵并报告估计值、SE、目标值、收敛状态与边界命中情况。

### 步骤 4：标准误方案（五选一，显式声明）

Hessian 逆 / 三明治 / 聚类稳健 / bootstrap / 仅模拟经验 SE。
理论论文默认：理论部分推 Hessian/三明治，模拟部分同时报告经验 Monte Carlo SD 作对照。

### 步骤 5：数值防线（Gate 3）

- 检查缩放、数值秩、条件数、边界命中、多起点稳定性与 exit flag。
- 含矩阵行列式时使用稳定分解；含空间乘子时拒绝接近奇异的参数。
- 含断点时强制网格截尾；含多峰目标时用网格、全局搜索或多起点作对照。

**通过 Gate 3 → 等人批准估计方案 → M4 与 M5 可并行启动。**

---

## Common Pitfalls

1. 集中化时丢掉仍依赖待估参数的项；空间模型中常见的是漏掉 log-determinant。
2. 离散结构参数的允许集合没有识别或最小样本约束；断点模型中常见的是网格未截尾。
3. SE 方案不声明，模拟里 CP 用了不一致的 SE 公式。
4. 多峰目标只用单起点局部优化。
5. 可缓存的矩阵分解或目标组成部分被重复计算，模拟成本失控。

---

## 独立运行说明

M3 可独立运行：提供模型与似然（或指认 M1 文档）即可，用于给已有模型设计估计算法。

## 细节流程与模板

- 执行框架：`.cursor/skills/m3-qml-estimation/SKILL.md`
- 模板：`modules/M3-qml-estimation/templates/qml-derivation.md`
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的“M3 — QML 估计”
