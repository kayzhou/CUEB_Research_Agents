# M5 — Monte Carlo 模拟

> 用可复现的模拟检查有限样本表现：bias、RMSE、SE 准确性、覆盖率、失败率及模型特有指标。
> 铁律：DGP 必须与理论模型一致；表格由脚本从保存的原始估计生成；失败必须报告。

---

## Requires（前置输入）

- M1 冻结的模型 + M3 批准的估计算法
- `projects/{slug}/config/simulation_design.yaml`（参数真值、网格、种子；模板见 `modules/M5-monte-carlo/templates/simulation-design.yaml`）
- 引擎确认：`matlab-mcp` / `matlab-local` / `octave` / `python`（决策树见 `ENVIRONMENT.md` §三；本地直连见 `本地化部署说明.md`）
- 可选 Stata 对照：`stata-mcp` / `stata-local` / `r` / `none`，登记到 metadata 的 `stata_engine`

## Produces（产出）

- `projects/{slug}/matlab/` — DGP、估计器、主循环、汇总工具（一文件一函数）
- `projects/{slug}/results/raw/` — 每次重复的原始估计（CSV/MAT）
- `projects/{slug}/results/tables/` — bias/RMSE/CP 汇总表（脚本生成）
- 交叉验证记录：R（`spatialreg`/`splm`）独立实现的小样本比对结果

## 卡点（人裁决）

1. **模拟设计批准**：DGP、参数网格、重复次数、评估指标确认后才开跑 final。
2. **结果审视**：汇总表出来后人审视（尤其 CP 偏离 95%、断点直方图形状），再进 M6。

---

## 执行流程

### 步骤 1：模拟设计

核心指标：各参数 bias、RMSE、经验 SD、平均估计 SE、区间覆盖率与收敛失败率。
模型特有指标只在适用时加入，例如断点定位误差、分类准确率、边界命中率或对依赖强度的敏感性。

空间杜宾断点专用模板的默认网格（`simulation-design.yaml`）为：

```text
N ∈ {50, 100}, T ∈ {40, 80}; R = 1000 final / 50 debug
λ: 0.3 → 0.5;  β: [1.0, 0.5] → [1.0, 0.8];  γ: [0.2, 0.1] → [0.2, 0.3]
σ² = 1.0（两 regime）; break_fraction = 0.5; trim = 0.15
```

### 步骤 2：DGP 与模型专用设计

DGP 必须逐项匹配 M1 模型、M3 估计算法与 M4 假设；每个稳健性偏离均须单独标记。
一般模型应明确样本结构、回归元或状态变量、扰动分布、依赖机制与参数真值。

对空间杜宾断点专用模板，
\(y_t=(I_N-\lambda_j W_N)^{-1}(X_t\beta_j+W_NX_t\gamma_j+\alpha+u_t)\)；
此时 W 至少包含一种透明调试设计和一种目标研究设计，并使用与理论一致的标准化。

### 步骤 3：编码标准

- 一文件一函数；估计函数内不硬编码输出路径。
- `rng(seed + r, 'twister')` 控制每次重复；debug 与 final 模式分离。
- 保存：每次重复的估计值、SE、断点估计、收敛 flag → `results/raw/`。
- 表格由 `summarize_mc_results` 从 raw 生成，含 fail_rate 列。
- **Octave 兼容**：不用 MATLAB 专有工具箱函数，让同一套 .m 在 Octave 可跑。

### 步骤 4：指标公式

\(\text{Bias}=R^{-1}\sum_r(\widehat\theta_r-\theta_0)\)；\(\text{RMSE}=[R^{-1}\sum_r(\widehat\theta_r-\theta_0)^2]^{1/2}\)；
\(\text{CP}=R^{-1}\sum_r 1\{\theta_0\in[\widehat\theta_r\pm 1.96\,\widehat{se}_r]\}\)
（必须用估计 SE，不是经验 SD）。断点定位等额外指标只在模型包含相应参数时报告。

表模板列：`N, T, R, parameter, true, mean, bias, rmse, sd, avg_se, cp95, fail_rate`。

### 步骤 5：三级验证（Gate 5）

1. **Smoke test**：R=10、小 N/T，检查维度与收敛。
2. **特例校验**：选择当前模型可退化到的已知特例，与解析解、可信软件或独立实现对照。
   空间杜宾断点模型可检查 \(\lambda=0\) 与 \(\gamma=0\) 特例。
3. **交叉验证**：用第二套独立实现在固定小样本上比对估计值。工具按模型选择；
   空间模型可用 R `spatialreg`/`splm`，一般模型可用 R、Python 或解析解。

**通过 Gate 5 → 人审视结果 → 进入 M6。**

---

## Common Pitfalls

1. DGP 与理论模型悄悄不一致（如 DGP 用了固定效应而似然按 pooled 写）。
2. CP 用经验 SD 冒充估计 SE，覆盖率虚高。
3. 不收敛的重复被静默丢弃，等效于选择性报告。
4. 重复计算可缓存的目标组成部分；空间断点模型常见的是对每个 \((\tau,\lambda)\) 重算 log-det。
5. 手抄表格数字进论文（M6 必须 `\input{}` 脚本生成的 .tex 片段）。

---

## 独立运行说明

M5 可独立运行：提供模型 + 估计算法说明（或指认 M1/M3 文档）+ `simulation_design.yaml` 即可。

## 细节流程与模板

- 执行框架：`.cursor/skills/m5-monte-carlo/SKILL.md`
- 模板：`modules/M5-monte-carlo/templates/simulation-design.yaml`；代码骨架见 `templates/paper-project/matlab/`（仓库根）
- 通用文档示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md` 的
  “M5 — Monte Carlo 设计”；可执行代码须从 `templates/paper-project/matlab/` 按具体模型改写
