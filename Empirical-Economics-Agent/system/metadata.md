# 项目状态 — Empirical-Economics-Agent

> 本文件追踪当前在哪个模块、各产出就绪状态。每个模块收尾时回写。

---

## 基本信息

```yaml
project: a-share-multifactor-pricing
title: "中国 A 股多因子模型截面定价能力：FF5、动量与 GRS spanning 检验"
paradigm: asset_pricing          # ✅ Lead Author 批准 2026-07-02
engine: python                   # ✅ Lead Author 批准 2026-07-02
contribution_rating: 中          # ✅ 接受整体贡献定位 2026-07-02
run_mode: A
current_module: M2
m2_mode: audit_only
last_updated: 2026-07-15
```

## 模块状态

| 模块 | 状态 | 产出就绪 | 备注 |
|------|------|---------|------|
| M1 选题立项 | done | paper-screen ✅ / paper-brief ✅ / contribution-audit ✅ | 范式 + 贡献审计均已批准 |
| M2 数据接入与样本侦查 | not_started | 输入样本 ⬜ | 前置输入未就绪；尚未到缺失处理卡点 |
| M3 模型实证 | not_started | 结果表图 ⬜ | |
| M4 论文撰写 | not_started | 中/英稿 ⬜ | |
| M5 审稿返修 | not_started | 返修稿 ⬜ | |

> 状态取值：`not_started` / `in_progress` / `blocked_on_human` / `done` / `done(stub)` / `done(external)` / `done(partial)`

## 当前输入请求（非卡点）

```
【M2 前置条件 — 分析样本未就绪】
  当前 `data/final/` 仅有 codebook 模板，尚无 `.parquet` / `.dta` 样本文件。
  请 Lead Author 二选一：
    1) 将已清洗的最终月度面板放入 `data/final/`（推荐文件名：panel_monthly.parquet）
    2) 把 `m2_mode` 改为 `full_pipeline`，将 CSMAR 原始导出放入 `data/raw/`，
       并指令「按 m2-sample-audit 步骤 1-5 清洗+构建，再进入步骤 6」
  样本就绪后，将执行缺失全景扫描 → 汇报 → 等人裁决缺失值处理（M2 核心卡点）。
```

## 当前任务

```
M2 待启动：
  - 待接收：data/final/ 分析样本 或 data/raw/ 原始数据
  - 下一步：样本侦查（只诊断、不自动处理缺失值）
  - 参考：modules/M2-sample-audit/MODULE.md、.cursor/skills/m2-sample-audit/SKILL.md 步骤 6
```
