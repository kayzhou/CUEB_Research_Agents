# 论文简报 — paper-brief

> 锁定研究设计。与 paper-screen 口径一致。

## 研究问题（可检验假设）

**核心问题**：FF5 与动量因子能否解释 A 股截面收益差异？现有主流因子集之间是否存在 spanning 关系——即某一组因子是否已包含另一组的定价信息？

- **H1（单变量组合 alpha）**：按 size、BM、盈利（OP/ROE）、投资（INV）、动量（Mom）独立排序形成的 long-short 组合，产生统计显著且经济意义可辨的正（或负）alpha（相对 CAPM 或 FF3）。
- **H2（Fama-MacBeth 风险溢价）**：在 Newey-West 调整下，A 股截面 FMB 回归中，SMB、HML、RMW、CMA、UMD 的风险溢价显著异于零；符号与 Fama-French (2015) / LSY (2019) 方向大体一致或可在讨论中解释差异。
- **H3（GRS spanning）**：以 GRS 检验比较因子集 nest 关系——(i) FF5 vs FF5+Mom；(ii) FF5+Mom vs LSY CH-4；(iii) FF5+Mom vs q-factor。若拒绝 spanning 零假设，表明被检验因子集含有增量定价信息。

## 范式与引擎（卡点：人批准）

- **范式**：资产定价（`asset_pricing`）
- **引擎**：Python（`pandas` + `numpy` + `linearmodels` + `statsmodels`）
- **理由**：
  - 研究问题是截面预期收益差异与因子张成检验，不涉及政策/事件因果识别，不适用 DID/IV/RD。
  - 组合排序、FMB、GRS 在 Python 生态有成熟实现路径；look-ahead bias 控制（特征滞后、动量 skip-month、会计数据披露滞后）用 pandas 时间对齐更透明。
  - 与 `system/metadata.md` 预设一致。

> **状态**：✅ Lead Author 已批准（2026-07-02）。贡献审计接受「中」定位，已进入 M2。

## 核心识别 / 定价逻辑

**方法链**（按执行顺序）：

1. **样本与变量构造**（M2/M3）
   -  universe：A 股普通股，剔除 ST/PT、金融、IPO 6 个月内；月度面板。
   - 因子：MKT, SMB, HML, RMW, CMA, UMD（Carhart 动量）；备选 LSY CH-3/CH-4、HXZ q-factor 构造。
   - Look-ahead 规则：t 月收益匹配 t-1 月末（或 t-1 会计年度披露后）特征；动量用 prior(2,12) skip 1；年度 rebalance 需等到 6 月末（若用年度会计变量）。

2. **Portfolio Sort**
   - 单变量独立排序（5×5 或 2×3×3 视样本量）；计算 value-weighted 组合收益与 long-short spread。
   - 报告 CAPM/FF3 alpha（Newey-West，滞后 6 期）。

3. **Fama-MacBeth (1973)**
   - 第一阶段：每期截面回归 \( r_{i,t} = \lambda_{0,t} + \sum_k \beta_{i,k,t-1} \lambda_{k,t} + \epsilon_{i,t} \)。
   - 第二阶段：时间序列平均风险溢价；NW 标准误。

4. **因子相关与 GRSP spanning (Gibbons-Ross-Shanken 1989)**
   - 比较 nested 因子集：检验「基准因子 + 候选因子」的 alpha 向量是否联合为零。
   - 报告 GRS 统计量、p 值；辅以 MKT-adjusted 组合 alpha 矩阵。

**不做的事**（边界）：
- 不声称发现全新因子（除非 GRS 结果支持且与 LSY/HXZ 有清晰差异）。
- 不在 M1 阶段锁定最终样本起止年——留 M2 样本侦查后由人裁决。

## 数据来源预期

| 项目 | 说明 |
|---|---|
| 主数据源 | CSMAR 股票市场交易 + 财务报表（或 Wind，若 CSMAR 字段不全） |
| 样本期（预期） | 2000-01 — 2024-12（待数据许可与缺失侦查后确认） |
| 频率 | 月度 |
| 标识符 | Stkcd × Yyyymm |
| 关键字段 | 月收益、流通市值、账面市值比、盈利、投资、换手/停牌标记 |
| 存储 | `data/raw/` → `data/processed/` → `data/final/`；双格式 `.parquet` + `.dta` |

## 预期贡献方向（至少一项）

- [x] **市场** — 在统一检验框架下更新 A 股 FF5+动量 vs 中国专用因子 vs q-factor 的相对定价能力。
- [ ] **数据** — 除非使用显著更长样本或新口径变量，否则贡献有限（评级见 contribution-audit）。
- [ ] **识别** — 资产定价语境下为「检验设计」而非因果识别；不主打此项。
- [ ] **机制** — 若仅报告 factor premium 而无行为/摩擦机制检验，机制贡献偏弱；可在 Discussion 轻量讨论，不作主贡献。

**叙事锚点（暂定）**：「在 A 股市场上，系统比较主流多因子模型的 spanning 关系，明确动量是否独立于 FF5，以及 LSY/q-factor 是否已 span FF5+Mom。」

## 主要替代解释预判

1. **微结构 / 流动性**：A 股小市值、高换手导致 size 与 momentum 溢价部分来自流动性补偿而非风险因子——控制 Amihud illiquidity 或使用流动性因子后结果是否稳健？
2. **制度与政策冲击**：涨跌停、停牌、壳价值、注册制改革改变 size/value 分布——子样本（如 2010 前后、2020 注册制）结果是否一致？
3. **因子构造敏感**：BM/盈利/投资的会计定义、breakpoints（NYSE vs 全样本）、value-weight vs equal-weight 改变结论——需 robustness 表格预先规划。
4. **数据 snooping / 多次检验**：多因子集多轮 GRS 比较存在 data mining 风险——主规格预先锁定，其余放附录。
