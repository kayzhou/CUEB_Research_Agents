# Empirical-Economics-Agent — 实证经济研究智能体框架

> 发布版 v1.2（2026-08-05）
> 轻量、模块化的实证研究工作流。
> 保留三角色「反对党」内核（Lead Author 人类裁决 + Researcher 执行 + Referee 攻击），
> 把科研流程压成 **5 个可独立运行的模块**（M1 立项 → M2 数据与样本 → M3 实证 → M4 写作 → M5 审稿返修），
> 并配套 **知识库（paper-lib）** 与 **本机工具链（R / TeX Live / Python / Stata·MATLAB MCP）**。

---

## 一、五个模块

| 模块 | 名称 | 卡点（人裁决） |
|------|------|---------------|
| **M1** | 选题立项与文献调研 | 范式批准、贡献审计结论 |
| **M2** | 数据接入与样本侦查 | `audit_only` 或 `full_pipeline`；缺失值处理决策 |
| **M3** | 模型与实证 | 估计计划批准、典型事实审视、实证结果审视 |
| **M4** | 论文撰写 | 证据链批准、章节草稿审阅 |
| **M5** | 审稿与返修 | 评审意见裁决、返修稿审定、模拟专家评审 + 人工真实意见返修 |

每个模块的完整说明见 `modules/MX-*/MODULE.md`，对应执行细节见 `.cursor/skills/mX-*/SKILL.md`（一一对应，Cursor 可自动发现）。

---

## 二、三种运行方式

核心设计目标：**每个模块都能独立运行、可从任一模块切入、也可端到端串联**。

### 方式 A：端到端全流程

按 M1 → M2 → M3 → M4 → M5 顺序执行。前一模块的产出即后一模块的输入。
适合从零开始一篇新论文。

### 方式 B：从某一步切入

直接运行任意模块。前置条件由你以「输入契约」的形式提供（见下文）。
例如：数据和实证都做完了，只想跑 M4 写作 + M5 审稿。

### 方式 C：单模块独立运行

只跑某一个模块，例如只用 M5 对一篇**外部已有论文**做模拟专家评审 + 返修。
此时 M5 不依赖本框架的前序产出，只需要你提供论文全文。

---

## 三、模块输入/输出契约（解耦的关键）

每个模块在 `MODULE.md` 顶部声明 **Requires（前置输入）** 和 **Produces（产出）**。
模块之间只通过这些文件交接，不依赖隐藏状态。这是「可从任一步切入」的实现基础。

```
M1  Requires: 研究想法 / 目标期刊（可选）
    Produces: paper/{slug}/paper-screen.md, paper-brief.md, review/contribution-audit-v1.md

M2  Requires: m2_mode + 最终样本（audit_only）或原始数据清单（full_pipeline）+ 变量清单/codebook
    Produces: review/sample-audit-report.md, 冻结样本, codebook.md, schema.yaml

M3  Requires: paper-brief.md（识别/定价逻辑）+ 已侦查的干净样本 + codebook
    Produces: analysis/output 脚本, results/ 表图, system/experiments.jsonl, stylized-facts.md

M4  Requires: 实证结果（results/）+ evidence-chain + 目标期刊风格参考（默认 paper-lib）
    Produces: 中文讨论稿 + 英文投稿稿, 表图 note

M5  Requires: 论文全文（本框架产出或外部论文）
    Produces: review/ 下的内部审查、模拟评审、response letter、changelog + 最终稿
```

**从中间切入时**：若上游产出缺失，先用对应模板补一个最小可用版本（stub），再运行当前模块。
缺失什么、补了什么，记录到 `system/metadata.md`。

> 当前仓库提供完整的研究协议、模板、验证工具与就绪检查器，但不内置 CSMAR 数据，也尚未为当前项目实现 clean/build/analysis/output 脚本。`scripts/master_build.py` 只检查就绪状态，不执行研究流水线。

---

## 四、如何启动

> 完整操作指南（含全流程演示、11 个单模块/切入示例、服务器→本地原生迁移、架构对比）见 **`使用手册.md`**；Stata/MATLAB 的 MCP 与本地直连细节见 **`本地化部署说明.md`**。

1. 读 `ORCHESTRATOR.md` → 确认角色架构、不可违反规则、模块路由。
2. 首次部署运行 `python scripts/configure_local.py` 生成本机路径配置；macOS/Linux 执行 `source scripts/setup_env.sh`，Windows PowerShell 点调用 `. .\scripts\setup_env.ps1`（详见 `ENVIRONMENT.md`）。
3. 读 `system/metadata.md` → 确认当前在哪个模块、哪些产出已就绪。
4. 选运行方式（A/B/C）→ 打开对应模块的 `MODULE.md`。
5. 按模块内的「执行流程」推进；遇到卡点停下来等人裁决。

> 启动一句话指令示例：
> - 「跑 M1：我想研究 XX，目标期刊 YY」
> - 「从 M3 开始：数据已就绪，识别策略是 DID」
> - 「只用 M5：对这篇论文做模拟专家评审 + 返修」

---

## 五、目录结构

```
Empirical-Economics-Agent/
├── LICENSE                   # Apache License 2.0（第三方资产不在授权范围）
├── README.md                 # 本文件：模块概览 + 三种运行方式
├── ORCHESTRATOR.md           # 编排器：角色、规则、模块路由、状态机
├── ENVIRONMENT.md            # 工具链：R/TeX Live/Python 路径、Stata·MATLAB MCP 方案
├── 使用手册.md                # 全流程、单模块示例、本地迁移与文件速查
├── 本地化部署说明.md          # 本地部署：Stata·MATLAB 双模式接入（MCP / 本地直连）
├── requirements.txt          # Python 依赖安装入口
├── config/                   # 本机工具路径模板/schema（local-tools.json 不入库）
├── agents/
│   ├── researcher.md          # 执行者协议
│   └── referee.md             # 审稿人协议（含模拟专家评审）
├── system/
│   ├── metadata.md            # 状态追踪：当前模块 + 各产出就绪状态
│   ├── milestones.md          # 里程碑
│   ├── claim-registry.json    # 声明-证据注册表
│   └── experiments.schema.json# 实验记录 schema；experiments.jsonl 首次 M3 运行时创建
├── modules/                  # 五个模块（思维框架 + 卡点 + 模板）
│   ├── M1-project-init/       # 选题立项与文献调研
│   ├── M2-sample-audit/       # 样本侦查
│   ├── M3-empirical/          # 模型与实证
│   ├── M4-writing/            # 论文撰写
│   └── M5-review/             # 审稿 + 模拟专家评审 + 返修
├── .cursor/
│   ├── rules/                # 始终生效的路由与研究安全规则
│   └── skills/               # Cursor 可发现的执行框架 Skill
│       ├── m1-project-init/
│       ├── m2-sample-audit/
│       ├── m3-estimation/
│       ├── m4-paper-writing/
│       └── m5-referee-review/
├── paper-lib/                # 知识库：《管理世界》全文 PDF 库 + index.csv 索引（只读）
├── code/                     # 程序层：config/clean/build/analysis/output/utils
├── data/                     # 三层数据：raw（只读）→ processed → final
├── results/                  # 结果层：tables / figures / logs（只由脚本生成）
├── paper/                    # 论文层：{project-slug}/（sections、review、discussions）+ exports/（docx 交换）
├── scripts/                  # master_build + 分平台环境激活 + 本机配置生成 + mcp/
│   ├── setup_env.sh           # macOS/Linux 激活（兼容既有 Linux 服务器布局）
│   ├── setup_env.ps1          # Windows PowerShell 激活
│   ├── configure_local.py     # 生成 config/local-tools.json
│   └── mcp/                   # 通用及 Windows/macOS/Linux MCP 示例
└── discussions/              # 研讨纪要 + 设计理念（反对党、自动化科研）
```

> **模块 vs Skill 的分工**：`modules/MX-*/MODULE.md` 是**思维框架**（什么模式、什么立场、卡点在哪）；
> `.cursor/skills/mX-*/SKILL.md` 是**执行框架**（具体怎么做、装载顺序、常见陷阱）。编号一致，一一对应，并由 Cursor 自动发现。

### 论文项目目录命名

`paper/{project-slug}/` 是一篇具体论文的工作区，集中保存立项文件、证据链、章节稿、攻防记录和审稿返修材料。项目名不使用 `paper01`、`paper02` 这类无语义流水号，而使用小写英文 kebab-case：

- 当前项目：`a-share-multifactor-pricing`
- 对应目录：`paper/a-share-multifactor-pricing/`
- 同一 slug 同步用于 `code/analysis/`、`code/output/` 和 `results/tables|figures/`。
- 新项目示例：`green-credit-firm-investment`、`digital-transformation-productivity`。

项目 slug 一旦进入 M2 后不应随意改动；如需改名，必须同步更新 `system/metadata.md`、代码目录、结果目录和文档引用。

---

## 六、知识库与工具链

- **paper-lib**（`paper-lib/README.md`）：PDF 不随 Git 分发。先运行 `python code/utils/check_paperlib.py`，通过后再检索与回原文核对。
- **工具链**（`ENVIRONMENT.md`）：Windows 使用 `. .\scripts\setup_env.ps1`，macOS/Linux 使用 `source scripts/setup_env.sh`——
  - 项目内 Python 3.10 `.venv`（依赖安装入口 `requirements.txt`；服务器旧 `tools/py_env` 仅作兼容回退）
  - R 4.4.1（计量包需运行 `Rscript scripts/install_r_packages.R`）
  - TeX Live 2026（英文 pdflatex / 中文 xelatex 编译）
  - Stata 经 MCP 接入（推荐开源 [SepineTam/mcp-for-stata](https://github.com/SepineTam/mcp-for-stata) 或 [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp)；仓库另置最小实现 `scripts/mcp/`）
  - MATLAB 经官方开源 MCP 接入（[matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server)）
  - 本机已装 Stata/MATLAB 时，也可不配 MCP 走**本地直连**（终端批处理调用），见 `本地化部署说明.md`

---

## 七、不可违反的底线

1. 原始数据只读；结果只由脚本生成，不手工改。
2. 论文正文数字来自结果文件，不手工输入。
3. **样本侦查只诊断、不自动处理缺失值**——处理方式由人决策（M2 卡点）。
4. **包优先**：有成熟包就不手搓估计方法。
5. **审稿只攻击不代笔**：Referee/模拟专家产出意见，不直接改正文；修改走返修流程。
6. **角色不越界**：Researcher 不代替人裁决，Referee 不修改研究产出。
7. **知识库只读且引用必核对**：paper-lib 不改不删；引用其结论前回 PDF 原文核对。
8. 人卡点不可跳过：范式、贡献审计、缺失值处理、估计计划、典型事实、实证结果、证据链、章节、返修审定。
9. 全程中文沟通（英文投稿正文除外）。

---

## 八、许可证与第三方资产边界

除各文件另有声明外，本项目原创的源代码、配置、文档与模板按
[Apache License 2.0](LICENSE) 授权。

该许可证**不授予**下列第三方资产的任何权利：

- `paper-lib/` 或其它位置的第三方论文、PDF、书籍与期刊内容；
- `data/` 下由使用者另行取得的数据库、原始数据与衍生数据（包括 CSMAR、Wind 等受限数据）；
- Stata、MATLAB、其工具箱、许可证与可执行文件；本仓库只提供接入配置，不分发这些商业软件；
- 外部 MCP 服务器及其它第三方依赖；它们分别适用各自上游许可证。

使用者须自行确认对论文、数据和商业软件拥有合法访问、复制与运行权限。项目许可证不会覆盖或改变任何第三方条款。
