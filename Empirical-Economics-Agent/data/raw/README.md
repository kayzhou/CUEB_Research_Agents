# data/raw/ — 原始数据（只读）

将 CSMAR（或 Wind）导出文件放在此目录。**Agent 不得直接修改 raw 内文件**；清洗输出写入 `data/processed/` 与 `data/final/`。

## a-share-multifactor-pricing 建议文件

| 文件/目录 | 内容 | 用途 |
|-----------|------|------|
| `csmar_trdmonth/` | 月度个股收益、流通市值、交易状态 | ret, size, ST 标记 |
| `csmar_fina/` | 财务报表（总资产、股东权益、净利润等） | BM, OP, INV 构造 |
| `csmar_stkinfo/` | 上市日期、行业、股票类型 | universe 筛选 |

## 最低字段要求（见 `paper/a-share-multifactor-pricing/paper-brief.md`）

- 标识：`Stkcd` + 年月
- 收益：月度个股收益（或价格算收益）
- 市值：流通市值或总市值
- 会计：账面价值、盈利、投资（资产增长）——用于 FF5 特征

放入数据后，在 Chat 中说明路径，例如：

> 「把 system/metadata.md 的 m2_mode 改为 full_pipeline。CSMAR 已放入 data/raw/，请按 m2-sample-audit 步骤 1-5 清洗+构建，然后做步骤 6 样本侦查」
