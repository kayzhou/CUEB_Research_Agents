# EconTriad 财经科研智能体

> 版本 **V0.6** · 由首经贸师生团队开发

面向财经论文生产的模块化科研智能体。共享三角色内核——**Lead Author**（人类裁决）· **Researcher**（执行）· **Referee**（只攻击、不代笔）——与本机工具链约定，按研究类型分为两套工作流：

| 目录 | 定位 | 模块 |
|------|------|------|
| [Empirical-Economics-Agent](Empirical-Economics-Agent/) | 实证经济研究：数据 → 估计 → 写作 → 审稿 | M1–M5 |
| [Theoretical-Econometrics-Agent](Theoretical-Econometrics-Agent/) | 理论计量研究：模型 → 证明 → 模拟 → 写作 → 审稿 | M1–M7 |

操作细节、目录约定与底线规则见各目录内的 `README.md`、`ORCHESTRATOR.md` 与 `使用手册.md`。

---

## 共同设计

- **模块化**：每个模块可独立运行、可从中途切入、也可端到端串联；模块间只通过文件契约交接。
- **人卡点不可跳过**：范式/设定、估计或证明方案、结果审视、章节与返修等关键节点由人批准。
- **可复现与诚信**：结果由脚本生成；不伪造文献、数字或证明；引用前核对原文。
- **沟通**：全程中文（英文投稿正文除外）。
- **工具链**：本机 Python / R / TeX Live；Stata、MATLAB 经 MCP 或本地直连接入（见各目录 `ENVIRONMENT.md`、`本地化部署说明.md`）。

---

## 如何选用

- 已有或即将产生**样本与识别/定价策略** → `Empirical-Economics-Agent/`
- 核心是**模型设定、QML、渐近证明与 Monte Carlo** → `Theoretical-Econometrics-Agent/`

进入对应目录后，先读该目录 `README.md`，再按其中「如何启动」打开 `ORCHESTRATOR.md` 与目标模块。

---

## 许可证

各子项目原创代码、文档与模板默认按各自目录下的 [Apache License 2.0](Empirical-Economics-Agent/LICENSE) 授权。第三方论文 PDF、受限数据、Stata/MATLAB 等商业软件及外部依赖不在授权范围内，使用前须自行确认合法权限。
