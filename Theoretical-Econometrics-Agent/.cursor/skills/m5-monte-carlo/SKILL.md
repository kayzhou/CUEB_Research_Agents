---
name: m5-monte-carlo
description: "Implements or audits reproducible Monte Carlo studies for econometric estimators in MATLAB, Octave, Python, or an approved alternative: theory-matched DGPs, seeded replications, saved raw estimates, generated bias/RMSE/coverage tables, failure reporting, and independent cross-checks."
---

# M5 Monte Carlo — 模拟 Skill

## Use This Skill When

1. 需要编写或调试 DGP、QML 估计器、Monte Carlo 主循环（MATLAB/Octave/Python）。
2. 需要设计模拟参数网格与评估指标（bias/RMSE/CP/失败率及模型特有指标）。
3. 需要从原始估计生成汇总表。
4. 需要用 R 交叉验证估计器实现。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认模拟纪律（规则 5）与 Gate 5。
2. `modules/M5-monte-carlo/MODULE.md`：思维框架——核心指标、模型匹配的 DGP、编码标准、指标公式与三级验证。
3. `ENVIRONMENT.md`：引擎决策树（`matlab-mcp` / `matlab-local` / `octave` / `python`）与分平台激活方式（Windows `. .\scripts\setup_env.ps1`；macOS/Linux `source scripts/setup_env.sh`）。
4. `本地化部署说明.md`：MATLAB/Stata 的 MCP 与本地直连；Stata 辅助引擎枚举为 `stata-mcp` / `stata-local` / `r` / `none`。
5. M1 模型 + M3 估计方案 + `projects/{slug}/config/simulation_design.yaml`。
6. 代码骨架：`templates/paper-project/matlab/`（空间面板断点专用，其他模型必须重写）；
   通用流程示例：`examples/generic-qml-workflow/docs/end-to-end-workflow.md`。示例不包含实测结果。

## Scope Boundary

1. 只处理模拟设计、编码、运行与汇总；不改理论（M4）、不写论文正文（M6）。
2. DGP 偏离理论模型必须显式声明为稳健性设计并单独报告。

## Workflow

1. 运行当前操作系统的激活脚本 → `python scripts/check_environment.py` → 按决策树确认主引擎，将 `matlab-mcp` / `matlab-local` / `octave` / `python` 之一写入 metadata 的 `engine` 字段；如用 Stata 做辅助对照，再填写 `stata_engine`。
2. 填/校 `simulation_design.yaml`（真值、样本与参数网格、seed、R_debug/R_final；
   `trim` 仅断点模型适用）→ **等人批准模拟设计**（卡点 1）。
3. 编码：`dgp/`（当前模型的数据生成过程）、`estimation/`（目标函数、优化与 SE）、
   `utils/`（汇总与覆盖率）、`main_run_simulation.m`。
   一文件一函数；`rng(seed+r,'twister')`；raw 估计落盘 `results/raw/`；避免 MATLAB 专有工具箱函数以保 Octave 兼容。
4. 三级验证：smoke test → 当前模型的已知特例 → 第二套独立实现或解析解交叉验证。
   空间模型可用 \(\lambda=0\)、\(\gamma=0\) 特例及 R 空间包；一般模型按实际结构选择工具。
5. final 运行（R=1000）→ `summarize_mc_results` 从 raw 生成表（含 fail_rate）→ 输出 `.tex` 片段供 M6 `\input{}`。
6. Gate 5 自检 → `blocked_on_human` 等人审视结果（卡点 2）。

## Output Expectations

1. 可复现代码：任何人 `run main_run_simulation.m` 得到相同表格。
2. `results/raw/` 保存每次重复的估计、SE、模型特有参数、收敛 flag 与错误信息。
3. 汇总表列齐：`N,T,R,parameter,true,mean,bias,rmse,sd,avg_se,cp95,fail_rate`。
4. 交叉验证记录：R 实现与主引擎在小样本上的估计值比对。

## Common Pitfalls

1. DGP 与理论模型悄悄不一致。
2. CP 用经验 SD 冒充估计 SE。
3. 静默丢弃不收敛的重复。
4. 可缓存的目标组成部分不预计算，导致 final 运行成本失控。
5. 手抄表格数字（必须脚本生成 `.tex` 片段）。
