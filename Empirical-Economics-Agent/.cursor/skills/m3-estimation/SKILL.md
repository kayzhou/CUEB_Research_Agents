---
name: m3-estimation
description: "Runs M3 empirical analysis in Stata, R, or Python: preregisters outputs, produces descriptive facts, estimates causal or asset-pricing models, runs diagnostics and robustness checks, and generates reproducible tables and figures. Use when the analysis sample is frozen and estimation work begins."
---

# M3 Estimation — 模型与实证 Skill

## Use This Skill When

1. 需要编写或调试估计脚本（DID/IV/RD/Portfolio Sort/FMB/DGTW 等，Stata/R/Python）。
2. 需要设计实证图形（事件研究图、系数图、Binscatter、分布图等）的规格并生成图形。
3. 需要执行诊断检验（平行趋势、弱工具、密度检验、因子相关性等）。
4. 需要管理实证输出清单（`empirical-output-checklist.md`）。
5. 需要执行描述统计和记录典型事实（`stylized-facts.md`）。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认模块路由和不可违反规则（特别是规则 4：包优先）。
2. `system/metadata.md`：确认当前模块、范式和引擎选择。
3. `modules/M3-empirical/MODULE.md`：思维框架——执行流程（清单→描述统计→主估计→诊断→稳健性→出表图）与三个卡点。
4. `paper/{project-slug}/paper-brief.md`：确认研究设计和识别/定价逻辑。
5. `data/final/codebook.md`：确认可用变量、样本范围和变量定义。
6. `ENVIRONMENT.md`：引擎路由（Stata 经 MCP/本地直连 / R / Python）与分平台环境激活。
7. `code/README.md`：程序层规范——运行顺序、路径约定、脚本结构。
8. 模板：`modules/M3-empirical/templates/`（empirical-output-checklist / stylized-facts / estimation-risk-memo）。
9. 方法基准（可选）：`paper-lib/` 检索同方法论文，核对规格与诊断套路（`paperlib_index.py --search 双重差分` 等）。

## Scope Boundary

1. 本 skill 只处理 M3 估计阶段任务——估计代码、诊断检验、图形生成、描述统计、输出清单。
2. 不负责数据清洗或样本构建（那是 `m2-sample-audit` skill 的职责，数据应在进入本 skill 前已冻结）。
3. 不负责论文写作（那是 `m4-paper-writing` skill 的职责）。表图 note/caption 也由 writing skill 负责。
4. 不负责审查或 Proposal 攻击（那是 `m5-referee-review` skill 的职责）。
5. 不负责范式决策（范式已在 M1 由 `m1-project-init` skill 锁定）。

## 与其他 skill 的边界判定

| 场景 | 用 m3-estimation | 用其他 skill |
|------|--------------------------|-------------|
| 估计脚本编写/调试 | ✅ 本 skill | — |
| 诊断检验执行 | ✅ 本 skill | — |
| 图形生成（代码+数据→图形文件） | ✅ 本 skill | — |
| 描述统计与典型事实 | ✅ 本 skill | — |
| 实证输出清单管理 | ✅ 本 skill | — |
| 新项目立项、范式决策 | — | `m1-project-init` |
| 数据清洗、样本构建、样本侦查 | — | `m2-sample-audit` |
| 章节起草、润色、caption/note | — | `m4-paper-writing` |
| 7R/7Q 审查、Proposal 攻击 | — | `m5-referee-review` |
| 图形生成 + note 写作 | 两步：本 skill 生成图 → `m4-paper-writing` 写 note | 两步不同会话 |
| 写作 + 方法选择/结果解释 | `m4-paper-writing` → 本 skill | 串行，两步不同会话 |
| 数据 + 估计 | `m2-sample-audit` → 本 skill | 数据冻结后再进入估计 |

## 引擎与执行环境

- **先激活环境**：Windows 点调用 `. .\scripts\setup_env.ps1`；macOS/Linux 执行 `source scripts/setup_env.sh`。
- **因果推断**：本机有 Stata → 经 Stata MCP 执行（`run_stata` 工具；服务器见 `scripts/mcp/`，推荐的开源 MCP 方案见 `ENVIRONMENT.md`）；无 Stata → R（`fixest`/`did`/`rdrobust`/`eventstudyr`）。
- **资产定价**：Python（pandas + statsmodels/linearmodels）。
- **结构估计/数值方法**：MATLAB 经官方 MCP（`matlab/matlab-mcp-server`，见 `ENVIRONMENT.md`）。

## Workflow（按任务类型）

> 默认先按 `ORCHESTRATOR.md` 确认当前模块与任务路由，再进入以下任务型补充。

### 资产定价代码任务

1. 核查 **look-ahead bias 防范清单**：特征变量是否已正确滞后（t-1 月末特征匹配 t 月收益，`.shift(1)`）？动量是否跳过最近一月（prior 2-12）？年度排组是否等到 6 月末？
2. 用 Python 实施分析：`code/analysis/{project-slug}/` 下按方法命名脚本，头部 `from code.config import PATHS`。
3. 分析脚本生成机器可读中间结果；`code/output/{project-slug}/` 的独立脚本生成最终 `.tex` 表格和 PDF/PNG 图形。

### 因果推断代码任务（Stata / R）

1. 读 `code/README.md` → 熟悉脚本结构规范、编号命名、日志约定。
2. **包优先**：Stata 用 reghdfe / ivreghdfe / csdid / rdrobust / eventdd；R 用 fixest / did / rdrobust / eventstudyr。写代码前先搜包，搜索结果写进脚本头。
3. Stata 脚本第一行 `include config.do`；R/Python 脚本从 `code/config/config.py` 读路径。头部有"输入/输出/说明"三行注释。
4. Stata 代码经 MCP `run_stata` 工具执行，日志自动落 `results/logs/`。

### 识别策略自检任务

1. 读 `modules/M3-empirical/MODULE.md` 步骤 3 → 载入对应识别类型（DID/IV/RD）的检验清单。
2. 系统检查：估计方程 → 识别假设 → 关键检验（平行趋势/F统计量/密度检验）→ 替代解释。
3. 可检索 `paper-lib/` 同方法论文核对该刊的规格惯例与检验套路。
4. 对存疑项打 `[CHECK]` 标注，对未完成检验打 `[TODO]` 标注。
5. **注意**：这是 Researcher 的自我检查，不是 Referee 的 Proposal Attack。正式的对抗性攻击由 `m5-referee-review` skill 执行。

### 诊断检验任务

1. 按估计方法路由诊断（见 `modules/M3-empirical/MODULE.md` 步骤 3）：
   - DID/Event Study：平行趋势、预趋势图、安慰剂检验、交叠处理 TWFE 偏误
   - IV：弱工具（一阶段 F）、排他性论证、过度识别检验
   - RD：密度检验、带宽敏感性、协变量连续性
   - 资产定价：因子相关性、GRS 检验、风险调整完备性
2. 逐项执行该路由的诊断检验，记录检验统计量和判读结果。
3. 未通过的检验：给出处理方案（换估计量/换规格/标注局限）。
4. 核心检验结果写入论文正文（由 writing skill 负责），完整诊断报告写入附录。

### 图形设计任务

1. 明确图形类型：事件研究图 / 系数图（coefplot）/ Binscatter / RD图 / 分布图 / 组合 alpha 条形图。
2. 选择工具：Stata `coefplot` / `twoway`（因果推断图）；R `ggplot2`；Python `matplotlib/seaborn`（资产定价图）。
3. 输出路径：`results/figures/{project-slug}/fig_[名称].pdf`（矢量）+ `.png`（辅助）。
4. 图形必须通过脚本生成，不允许在图形编辑器中手工保存。
5. **注意**：图形的 caption 和 note 由 `m4-paper-writing` skill 负责。本 skill 只生成图形文件。

### 描述统计与典型事实任务

1. 读 `modules/M3-empirical/templates/stylized-facts-template.md` → 确认典型事实记录格式。
2. 描述统计先于任何回归进行——不要先跑回归再看描述统计。
3. 至少覆盖：单变量分布、截面模式、时序趋势、相关结构。
4. 在 `stylized-facts.md` 中记录：观察到的模式 → 可能的解释 → 对后续分析的启发。
5. 完成描述统计后，回到 `empirical-output-checklist.md` 确认哪些典型事实进正文。

### 实验记录（每次估计都执行）

1. 每次模型运行后向 `system/experiments.jsonl` 追加一行 JSON，字段遵循 `system/experiments.schema.json`。干净克隆不预置空 JSONL；首次写入用追加模式自动创建文件。
2. `KEEP`、`FRAGILE`、`DISCARD`、`FAILED` 都要记录；失败实验不进入正式结果，但不得从研究轨迹中删除。
3. 记录规格、样本、系数/标准误/N、诊断、claim 链接和输出路径；首选规格仅允许一条 `is_preferred: true`。
4. 运行 `python code/utils/experiment_summary.py` 检查日志可解析。

## Output Expectations

一次完整的 M3 任务应产出：

1. **资产定价代码任务**：可运行的 `.py` 脚本（portfolio sort / FMB / DGTW），输出到正确路径，含日志，look-ahead bias 规则在注释中说明。
2. **因果推断代码任务**：可运行的 `.do` / `.R` 脚本，输出到正确路径，含日志。
3. **诊断检验任务**：诊断检验结果（日志/报告），未通过项的应对方案。
4. **图形任务**：`results/figures/{project-slug}/` 下的矢量 PDF + PNG 图形文件。
5. **描述统计任务**：`paper/{project-slug}/stylized-facts.md`（典型事实记录）。
6. **实证输出清单**：`paper/{project-slug}/empirical-output-checklist.md`，所有条目标记状态（正文/附录/放弃）。
7. **估计后验证**：断言式安检（样本量/系数/R²/参数）通过。
8. **实验注册**：`system/experiments.jsonl` 已按 schema 追加记录并能被汇总工具读取。

## 任务型提醒

1. 纯写作请求优先交给 `m4-paper-writing` skill，不在当前 skill 重复展开。
2. 资产定价任务优先检查 look-ahead bias，再开始估计。
3. 因果推断任务先确认识别假设与检验设计，再批量出表。
4. 审查任务（7R/7Q/Proposal Attack）优先调用 `m5-referee-review` skill，不在当前 skill 中执行。
5. 数据相关问题（样本变更、变量重新构造）先回到 `m2-sample-audit` skill，不在本 skill 中直接改数据。

## Common Pitfalls

1. 在 `paper/{project-slug}/sections/*.tex` 中直接手写数字（应通过 `\input{results/}` 引用）。
2. 脚本不 include `config.do`（或不 import `config.py`）而直接写绝对路径（其他人无法运行）。
3. **资产定价**：用 t 月末特征直接匹配 t 月收益（应用 t-1 月末特征，即 `.shift(1)`）。
4. **资产定价**：动量变量未跳过最近一个月（prior(2-12) vs prior(1-12)）。
5. **资产定价**：年度排组未等到 6 月末才形成组合（会计数据未充分披露）。
6. **包优先**：禁止在有成熟包（`xtfmb`/`reghdfe`/`csdid`/`rdrobust`/`fixest`/`did`）的情况下手搓估计方法。写代码前先搜包，搜索结果写在脚本头部注释中。
7. **描述统计后于回归**：描述统计和典型事实观察必须在前，回归在后。不要为了赶进度跳过这一步。
8. **图形手工保存**：图形必须通过脚本生成，不允许在 GUI 中手工保存。这会破坏复现链路。
