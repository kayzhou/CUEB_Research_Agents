# M3 — 模型与实证

> 相对原框架：**全保留**。涵盖描述统计与典型事实、主估计（因果推断/资产定价）、诊断检验、图表输出、实证输出清单。

---

## Requires（前置输入）

- `paper-brief.md`（识别/定价逻辑、范式、引擎）—— 来自 M1，或你直接提供
- 已侦查的干净样本 + codebook —— 来自 M2，或你提供
- 范式与引擎已确定（causal_inference → Stata MCP 或 R；asset_pricing → Python；结构估计可用 MATLAB MCP）

## Produces（产出）

- `empirical-output-checklist.md` — 估计/表/图清单（每条标状态：正文/附录/放弃）
- `stylized-facts.md` — 典型事实记录
- 估计脚本（含头部结构化注释、包搜索结果）
- 结果表图（输出到结果目录）+ 日志
- 实验记录（系数、SE、诊断、规格波动带、claim 链接）

## 卡点（人裁决）

1. **估计计划批准**：正式跑主估计前，输出清单 + 攻防 → 人批准。
2. **典型事实审视**：描述统计后，人确认哪些事实进正文。
3. **实证结果审视**：表图出来后，人审视结果再进入写作。

---

## 执行流程

### 步骤 0：实证输出清单 + 预审攻击（卡点）

- 正式估计前，把估计、表格、图形清单一次性列全，每条对应脚本、用途、依赖顺序、目标位置。
- 以贡献审计的比对矩阵为输入，写 `paper/{project-slug}/estimation-risk-memo.md`：这是 Researcher 的估计风险自检，不冒充独立 Referee；列出攻击点、当前证据和必须预备的检验。
- **等人批准清单。**

### 步骤 1：描述统计与典型事实（卡点）

> 描述统计先于任何回归。不要先跑回归再看描述统计。

至少覆盖四个维度，按研究问题选最相关展开：

- **单变量分布**：均值、标准差、分位数、偏度；必要时分布图。
- **截面模式**：按行业/市值/时间分组统计，看是否与理论预期一致。
- **时序模式**：核心变量时序均值/中位数趋势，标记断点与周期。
- **相关结构**：相关系数矩阵或 binscatter 非参数拟合，标记关键关系方向与线性程度。

每项记录到 `stylized-facts.md`：观察到的模式（fact）→ 可能的解释 → 对后续分析的启发（是否提示固定效应/分组/非线性/工具变量）。
探索阶段可多跑多看，再筛选进正文。**完成后人审视典型事实。**

### 步骤 2：主估计

先回看典型事实——基准规格的变量构造与固定效应选择应与观察到的模式一致。

**因果推断（Stata / R）**：

1. 读对应识别类型规范（DID/IV/RD）与检验清单；可检索 `paper-lib/` 同方法论文核对规格惯例（如 `paperlib_index.py --search 双重差分`）。
2. Stata 脚本先加载 `code/config/config.do`；Python 使用 `from code.config import PATHS`；R 从环境变量或统一配置读取路径。脚本头写输入/输出/说明。
3. **包优先**：Stata 用 reghdfe / ivreghdfe / csdid / rdrobust / eventdd；本机无 Stata 时用 R 的 fixest / did / rdrobust / eventstudyr（引擎路由见 `ENVIRONMENT.md`）；搜索结果写进脚本头。
4. Stata 代码经 MCP `run_stata` 工具执行（见 `ENVIRONMENT.md` §二.4）。

**资产定价（Python）**：

1. 先核查 **look-ahead bias 防范清单**：特征变量是否正确滞后（t-1 月末特征匹配 t 月收益，`.shift(1)`）？动量是否跳过最近一个月（prior 2-12）？年度排组是否等到 6 月末？
2. 用 linearmodels / statsmodels；最终表格 Python 生成 `.tex` 或导出给 esttab。

### 步骤 3：诊断检验

按估计方法路由诊断：

- **DID/Event Study**：平行趋势、事件研究图预趋势、安慰剂检验、交叠处理 TWFE 偏误（必要时换 csdid 等）。
- **IV**：弱工具（一阶段 F）、排他性论证、过度识别检验。
- **RD**：密度检验（操纵）、带宽敏感性、协变量连续性。
- **资产定价**：因子相关性、GRS 检验、风险调整完备性。

逐项记录统计量与判读；未通过项给出处理方案。核心检验进正文，完整诊断进附录。

### 步骤 4：稳健性

按识别威胁组织稳健性检验，覆盖预审攻击 memo 中标记的威胁。
计算通过诊断规格的系数标准差 × 1.5 作为规格波动带。

### 步骤 5：图表输出

- 图形类型：事件研究图 / 系数图 / binscatter / RD 图 / 分布图 / 组合 alpha 条形图。
- 工具：Stata coefplot/twoway 或 R ggplot2（因果），Python matplotlib/seaborn（资产定价）。
- 矢量 PDF + PNG；**必须脚本生成，禁止 GUI 手工保存**。
- 图的 caption/note 由 M4 写作模块负责，本模块只生成图形文件。

### 步骤 6：估计后验证 + 记录（卡点：实证结果审视）

- 断言式安检：样本量/系数方向/R²/参数在合理范围。
- 记录实验：系数、SE、诊断摘要、规格波动带、claim 链接、产出路径；失败实验只记原因。
- 回写 `empirical-output-checklist.md` 状态。**人审视结果后进入 M4。**

---

## Common Pitfalls

1. 在正文直接手写数字（应从结果文件引用）。
2. 脚本不 include config 而硬编码绝对路径。
3. 资产定价：用 t 月末特征直接匹配 t 月收益；动量未跳过最近一月；年度排组未等 6 月末。
4. 包优先违规：有 xtfmb/reghdfe/csdid/rdrobust 还手搓。
5. 描述统计后于回归。
6. 图形 GUI 手工保存，破坏复现。

---

## 独立运行说明

M3 可独立运行：提供 `paper-brief.md`（或口头说明识别策略）+ 干净样本 + 变量定义即可。
若跳过 M1/M2，请在 `system/metadata.md` 标其为 `done(external)` 并说明数据来源与样本侦查是否已在外部完成。

模板见 `templates/`：`empirical-output-checklist-template.md`、`stylized-facts-template.md`、`estimation-risk-memo-template.md`。

---

## 细节流程 Skill 与代码/工具

- **执行框架（细节流程）**：`.cursor/skills/m3-estimation/SKILL.md` —— 因果推断/资产定价两条任务流、look-ahead bias 防范、诊断路由、图形规格、常见陷阱。
- **工具链与引擎路由**：`ENVIRONMENT.md` —— Windows `setup_env.ps1` / macOS/Linux `setup_env.sh` 激活方式、Stata 与 MATLAB 的 MCP/本地直连接入方案、引擎选择决策树。
- **程序层（论文过程的工程化）**：
  - `code/config/config.py` —— 路径配置（`PATHS` 字典），所有脚本第一行引用。
  - `code/analysis/{project-slug}/` —— 主回归、识别策略、机制分析脚本（按论文分包）。
  - `code/output/{project-slug}/` —— 表格/图形最终生成脚本。
  - `code/README.md` —— 程序层运行顺序：config → clean → build → analysis → output → results。
- **Stata MCP 与流水线**：
  - `scripts/master_build.py` —— 当前只做就绪检查；`--strict` 可用于 CI。
  - `scripts/master_build.do` —— 调度模板，阶段调用尚未接入真实项目脚本。
  - `scripts/mcp/stata_mcp_server.py` + `stata_mcp_config.py` —— 内置 Stata MCP 服务器与本机路径配置；更完整的开源方案（SepineTam/mcp-for-stata、hanlulong/stata-mcp）见 `ENVIRONMENT.md`。
  - `code/utils/check_stata_paths.py` —— 运行前检查 Windows 路径引号。
- **验证/汇总工具**：
  - `code/utils/check_table_fonts.py` —— 表格字体检查。
  - `code/utils/experiment_summary.py` —— 实验日志汇总。
  - `code/utils/validate_claims.py` —— 声明-证据链接完整性校验（状态词表见 `system/claim-registry.json` 的 `_schema`）。
  - `code/utils/dependency_check.py` —— 依赖一致性检查。
- **方法基准**：`paper-lib/` —— 同方法已发表论文的规格惯例与诊断套路比对。
