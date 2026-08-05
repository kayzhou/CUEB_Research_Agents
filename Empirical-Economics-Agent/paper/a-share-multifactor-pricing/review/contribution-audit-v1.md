# 贡献审计 — contribution-audit v1

> 比对矩阵 + 严苛五问。评级「中/低」的维度，引言不得用强声称。
> 审计日期：2026-07-02

## 分层阅读清单

| 文献 | 层级 | 识别/定价设计 | 主要发现 | 与本文关系 |
|---|---|---|---|---|
| Fama & French (2015, JFE) | T1 | FF5 组合排序 + time-series regression | 盈利与投资因子增量解释 US 截面收益 | 方法论母版；本文在 A 股复现并扩展 Mom |
| Liu, Stambaugh & Yuan (2019, JFE) | T1 | A 股 CH-3/CH-4，size/value 异象 | 中国 size/value 与 US 相反或弱化；专用因子更有效 | 最直接竞品；本文需说明与 LSY 的差异（FF5 主线 + GRS nest） |
| Hou, Xue & Zhang (2015, RFS) | T1 | q-factor，Fama-MacBeth + GRS | q-factor 在美国 span FF5 | competing model；A 股适配后纳入 GRS 比较 |
| Carhart (1997, JF) | T2 | 四因子 + UMD | 动量 premium 独立于 FF3 | 动量构造与 alpha 检验参考 |
| Gibbons, Ross & Shanken (1989) | T2 | GRS spanning test | 联合检验 alpha 向量 | 核心检验工具 |
| Fama & MacBeth (1973, JFE) | T3 | 两步截面回归 | 风险溢价估计经典框架 | 方法引用，非贡献对标 |
| Asness, Moskowitz & Pedersen (2013) | T3 | 全球 value/momentum | 新兴市场动量存在 | 支持 A 股动量检验动机 |
| Chui, Titman & Wei (2010) | T3 | 亚洲市场 momentum | 文化/投资者结构影响动量 | 替代解释文献 |

## 比对矩阵（每篇 vs 本文，逐维标差异化程度：高/中/低/无）

| 文献 | 数据 | 识别/检验设计 | 机制 | 市场/样本 |
|---|---|---|---|---|
| Fama & French (2015) | 低（US CRSP） | 低（同框架） | 无 | 高（US vs CN） |
| Liu et al. (2019) | 低（同为 CSMAR 类） | 中（CH 因子 vs FF5 主线） | 低 | 无（同为 A 股） |
| Hou et al. (2015) | 低 | 中（q vs FF nest） | 低 | 高（US vs CN） |
| Carhart (1997) | 低 | 低（Mom 增量） | 无 | 高 |
| GRS (1989) | 无 | 无（纯方法） | 无 | 无 |

**差异化小结**：
- **最强差异轴**：市场（A 股）+ 多模型 GRS 对称比较（FF5+Mom / LSY / q-factor 同一流水线）。
- **最弱差异轴**：数据（CSMAR 标准）、纯方法（FMB/GRS 均为教科书级）。

## 严苛五问

1. **这个想法已经被做过了吗？**
   → **部分是的**。LSY (2019) 已系统讨论 A 股因子；后续大量工作复刻 FF5/CH 因子于 A 股。本文若仅报告「FF5 在 A 股也显著」则贡献不足。可推进条件：必须把 **GRS spanning 的多模型 nest 比较** 作为核心增量，并诚实地与 LSY 结果对话（确认、延伸或限定样本期差异）。

2. **只是换了市场/样本期吗？**
   → **部分是**。A 股市场本身是 valid 贡献来源，但不足以单独支撑顶刊。需叠加：(a) 动量与 FF5 的联合 spanning 结构；(b) 与 LSY、q-factor 的 systematic comparison；(c) 子样本/稳健性（注册制、ST 规则变化）至少一项。

3. **机制是显然的吗？**
   → **对因子 premium 而言，机制往往不是主贡献**。若正文只写「小市值溢价因为流动性」而无额外检验，机制维度弱。引言/讨论可轻量提及替代解释，**不宜强声称「揭示了新机制」**。

4. **系数太小没有经济意义吗？**
   → **需在 M3 描述统计后验证**。A 股 long-short spread 有时幅度大但换手高、交易成本侵蚀 net alpha。M3 必须报告 gross vs net（至少粗略双边成本 30–50 bps）economic magnitude；若 net alpha 不显著，叙事需降级。

5. **方法没有实质新意吗？**
   → **是，方法新意有限**。Portfolio Sort、FMB、GRS 均为标准工具。方法贡献评级应为 **低**。论文卖点在 **检验设计完整性 + 多模型比较**，而非新方法。

## 贡献评级

| 维度 | 评级 | 依据 |
|---|---|---|
| 数据 | **中** | CSMAR 非新；更长样本或严格 look-ahead 处理可支撑「更新」叙事，但非独家 |
| 识别/检验设计 | **中** | GRS 多模型 nest 对称比较有一定组织价值；FMB/GRS 本身不新 |
| 机制 | **低** | 未规划独立机制检验（如投资者结构、卖空限制） |
| 市场 | **高** | A 股独立市场、制度差异、与 US 文献对话——主贡献轴 |
| **整体** | **中** | 可支撑 JFQA / 中文顶刊或 field journal 级「系统检验型」论文；冲击 JFE/RFS 需 M3 出现清晰 spanning 新结论或显著 contradict LSY 的 robust 结果 |

## 结论

**值得推进**，但贡献叙事必须从第一天起 **诚实定位**：

- ✅ 可写强声称：A 股市场上 FF5+Mom vs LSY vs q-factor 的 **相对 spanning 结构**（若 M3 支持）。
- ⚠️ 谨慎写：「发现新因子」「揭示新机制」「数据独家」。
- ❌ 不可写：「首次证明 A 股存在 size/value 异象」（LSY 已覆盖）。

**Lead Author 裁决点**：若接受「整体贡献 = 中、主打市场+检验设计」，批准进入 M2；若要求「整体 = 高」才做，需在 M1 阶段追加机制检验或新变量计划，否则调整目标期刊至 JFQA / 金融研究（中文）等。
