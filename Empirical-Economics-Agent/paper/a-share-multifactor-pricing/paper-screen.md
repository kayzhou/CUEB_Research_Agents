# 论文筛查 — a-share-multifactor-pricing

> 立项第一关：能否、值不值得继续推进。先于大规模投入。

## 研究问题（一句话）

中国 A 股市场上，Fama-French 五因子与动量因子能否充分解释个股截面收益差异？更简约或更丰富的因子集能否 span 现有主流因子模型？

## 对标期刊（1-3 本）

1. **Journal of Financial Economics (JFE)** — 因子模型与资产定价检验的主战场；LSY (2019) 等中国因子文献常以此为标杆。
2. **Review of Financial Studies (RFS)** — 截面回归、spanning 检验与 robustness 规格的标准发表渠道。
3. **Journal of Financial and Quantitative Analysis (JFQA)** — 新兴市场/中国市场因子复制的常见区间；若 GRS 与 FMB 结果稳健，可作为务实备选。

## 最接近文献（3-5 篇）

| 文献 | 主要发现 | 与本文最接近之处 | 本文的差异 |
|---|---|---|---|
| Fama & French (2015, JFE) | 提出 FF5（MKT, SMB, HML, RMW, CMA），在美国市场显著改善截面定价 | 本文沿用 FF5 构造逻辑与 FMB/GRS 检验框架 | 样本换为中国 A 股；加入 Carhart 动量；系统比较 FF5+Mom vs LSY 中国因子 vs q-factor 的 spanning |
| Liu, Stambaugh & Yuan (2019, JFE) | 中国 size/value 异象与 US 不同；提出中国市场专用因子（CH-3/CH-4） | 同样聚焦 A 股截面定价与中国因子有效性 | 本文以 FF5+动量为基准，而非以 CH 因子为唯一主线；强调 GRS spanning 与多模型 nest 比较 |
| Hou, Xue & Zhang (2015, RFS) | q-factor 模型（投资、盈利驱动）在美国表现优于 FF5 | 本文将 q-factor 作为 competing model 纳入 spanning 检验 | 在 A 股样本上复现/适配 q-factor，并与 FF5、LSY 因子做同一套 GRS 比较 |
| Carhart (1997, JF) | 四因子模型加入动量（UMD），改善组合 alpha | 动量因子构造与组合排序逻辑 | 本文在 FF5 基础上叠加动量，检验 A 股动量 premium 是否独立于 FF5 |
| Gibbons, Ross & Shanken (1989, Econometrica) | GRS 检验：候选因子是否张成随机折扣因子 | 本文核心检验工具之一 | 应用对象为中国 A 股多组因子集，而非美国经典因子 |

## 推进判断

- **为什么值得做**：
  - A 股是独立于 US 的大样本新兴市场，size/value/profitability/investment/momentum 异象幅度与 US 不同（LSY 2019 已证），FF5 在中国是否仍是最优基准、动量是否增量有效，仍有更新样本与统一检验框架的空间。
  - 现有文献多分别讨论 CH 因子或 FF5 在 A 股的适配，较少在同一套 Portfolio Sort → FMB → GRS 流水线中，对 FF5+Mom、LSY、q-factor 做对称的 spanning 比较。
  - 方法链清晰、可复现，符合本框架资产定价范式（Python + 成熟包），适合作为当前端到端研究项目推进。

- **与最接近文献的核心差异**：
  - 不是单一复刻 FF5 或 LSY，而是**多模型 nest 比较 + GRS spanning** 的统一框架。
  - 显式检验动量在 FF5 之上的增量定价能力（H3 层级的组合 alpha 与 GRS 联合检验）。
  - 若 LSY 或 q-factor 在 A 股 span FF5+Mom，需在贡献叙事中诚实降级为「确认/延伸」而非「新因子发现」。

## 数据可行性初判

| 检查项 | 初判 |
|---|---|
| 核心变量是否可得 | **可得**。CSMAR 提供 A 股月度收益、流通市值、BM（或账面价值）、盈利（ROE/OP）、投资（资产增长）、足够构造动量（prior 2–12 月收益，跳过最近 1 月） |
| 样本期是否覆盖 | **可覆盖**。建议 2000-01 至 2024-12（或数据许可上限）；IPO 后至少 6 个月、剔除 ST/PT、金融股——与 LSY/Fama-French 惯例一致 |
| 标识符 | Stkcd + Trdmnt（或 Yyyymm）面板键；需确认 CSMAR 字段名与编码（GBK） |
| 初步结论 | **可推进** — 数据需求标准、无 exotic 变量；主要风险是因子构造细节（尤其是 A 股 BM、盈利、投资的会计时点与 look-ahead bias）需在 M2/M3 严格按 `asset-pricing-standards` 处理 |
