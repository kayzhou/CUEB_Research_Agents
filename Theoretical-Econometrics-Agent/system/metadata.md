# metadata — 状态追踪

> 每次模块收尾时回写本文件。多项目并行时为每个 slug 复制一段。

---

## 当前项目

- **project_slug**: （未设置——运行 `python scripts/init_project.py --name {slug} --output projects` 后填写）
- **模型一句话**: —
- **engine**: （M5 主引擎枚举：`matlab-mcp` / `matlab-local` / `octave` / `python`；见 ENVIRONMENT.md 决策树）
- **stata_engine**: （实证辅助引擎枚举：`stata-mcp` / `stata-local` / `r` / `none`）
- **当前模块**: —
- **运行方式**: （A 端到端 / B 切入 / C 单模块）

## 模块状态

| 模块 | 状态 | Gate | 备注（stub/external/partial 说明） |
|------|------|------|-----------------------------------|
| M1 模型设定 | not_started | Gate 1 未查 | |
| M2 文献定位 | not_started | Gate 2 未查 | |
| M3 QML 估计 | not_started | Gate 3 未查 | |
| M4 渐近理论 | not_started | Gate 4 未查 | |
| M5 Monte Carlo | not_started | Gate 5 未查 | |
| M6 论文写作 | not_started | Gate 6 未查 | |
| M7 审稿返修 | not_started | — | |

状态取值：`not_started` / `in_progress` / `blocked_on_human` / `done` / `done(stub)` / `done(external)` / `done(partial)`

## 冻结输入

| 时间 | 冻结内容 | 文件 | 说明 |
|------|---------|------|------|
| | | | |

## 待人裁决事项

| 时间 | 模块 | 问题 | 状态 |
|------|------|------|------|
| | | | |

## proof gap 总账（跨模块）

| 编号 | 位置 | 缺什么 | 状态 |
|------|------|--------|------|
| | | | |
