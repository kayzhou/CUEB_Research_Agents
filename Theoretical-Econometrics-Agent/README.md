# Theoretical-Econometrics-Agent — 理论计量研究智能体框架

> 文档发布版 v2.2（2026-08-05）：支持 Windows/macOS/Linux 原生本地环境，并提供中性 QML 工作流案例
> 面向**理论计量经济学论文生产**的模块化研究工作流，重点覆盖：
> 空间面板（SAR / SDM / SEM / 动态空间面板）、结构断点 / 阈值 / regime change、
> QML 估计、一致性 / 收敛速率 / 渐近分布证明、MATLAB Monte Carlo 模拟、LaTeX 投稿稿。
> 保留三角色内核（Lead Author 人类裁决 + Researcher 执行 + Referee 攻击），
> 把理论研究流程压成 **7 个可独立运行的模块**（M1 模型设定 → M2 文献定位 → M3 QML 估计 →
> M4 渐近理论 → M5 Monte Carlo → M6 论文写作 → M7 审稿返修），
> 并配套 **通用案例（examples）**、**用户资料入口（paper-lib）** 与
> **本机工具链（R / TeX Live / Python / Stata·MATLAB MCP）**。

---

## 一、七个模块

理论计量论文的科研流程与实证论文不同：核心产出是**定理与证明**，模拟只是佐证。
模块划分对应理论论文的自然分工：

| 模块 | 名称 | 核心产出 | 卡点（人裁决） |
|------|------|---------|---------------|
| **M1** | 模型设定与似然函数 | 模型方程、参数空间、QML 对数似然、记号登记表 | 模型设定批准 |
| **M2** | 文献定位与贡献审计 | 文献矩阵、贡献诊断、新颖性风险 | 贡献定位批准 |
| **M3** | QML 估计方法 | 目标函数、集中化或 profile、优化算法、SE 方案 | 估计方案批准 |
| **M4** | 渐近理论与证明 | 假设体系、定理地图、证明蓝图与草稿、proof gap 清单 | 假设体系批准、定理逐条确认 |
| **M5** | Monte Carlo 模拟 | DGP + 估计器、bias/RMSE/CP/失败率表 | 模拟设计批准、结果审视 |
| **M6** | 论文写作 | LaTeX 全稿（正文 + 附录证明） | 章节草稿审阅 |
| **M7** | 审稿与返修 | 五视角评审报告、response 矩阵、终稿一致性检查 | 评审意见裁决、返修稿审定 |

每个模块的完整说明见 `modules/MX-*/MODULE.md`，对应执行细节见 `.cursor/skills/mX-*/SKILL.md`（一一对应，Cursor 自动发现）。

---

## 二、三种运行方式

核心设计目标：**每个模块都能独立运行、可从任一模块切入、也可端到端串联**。

- **方式 A：端到端全流程** —— M1 → M7 顺序执行，适合从一个模型想法开始一篇新论文。
- **方式 B：从某一步切入** —— 例如模型和证明已完成，只跑 M5 模拟 + M6 写作。前置条件按「输入契约」提供。
- **方式 C：单模块独立运行** —— 例如只用 M4 审查你已有的一致性证明并列出 proof gap，或只用 M7 对一篇外部论文做模拟审稿。

---

## 三、模块输入/输出契约（解耦的关键）

每个模块在 `MODULE.md` 顶部声明 **Requires（前置输入）** 和 **Produces（产出）**。
模块之间只通过这些文件交接，不依赖隐藏状态。

```
M1  Requires: 模型想法（口头描述即可）
    Produces: projects/{slug}/config/model_specification.yaml, proofs/notation_registry.md

M2  Requires: 模型设定 + literature/library/ 中的文献（PDF/TXT/BibTeX）
    Produces: literature/literature_matrix.csv, literature/positioning.md

M3  Requires: 模型设定与似然函数
    Produces: estimation/qml_estimation_plan.md（目标函数、算法、SE 方案）

M4  Requires: 模型设定 + 估计方案
    Produces: proofs/assumptions.md, proofs/theorem_map.md, proofs/proof_*.md

M5  Requires: 模型设定 + 估计算法 + config/simulation_design.yaml
    Produces: matlab/ 代码, results/raw|tables/（bias/RMSE/CP 表）

M6  Requires: M1–M5 产出（或你直接提供的等价材料）
    Produces: paper/main.tex + sections/ + appendix/；main.pdf 在本机编译生成，不随发行包分发

M7  Requires: 论文全文（本框架产出或外部论文）
    Produces: reviews/ 评审报告、revision_log.md、终稿一致性检查
```

**从中间切入时**：若上游产出缺失，先用 `templates/paper-project/` 对应模板补一个最小可用版本（stub），
再运行当前模块。缺失什么、补了什么，记录到 `system/metadata.md`。

---

## 四、如何启动

> 完整操作指南见 **`使用手册.md`**。

1. 读 `ORCHESTRATOR.md` → 确认角色架构、不可违反规则、模块路由。
2. 激活本机工具链：Windows 执行 `. .\scripts\setup_env.ps1`，macOS/Linux 执行 `source scripts/setup_env.sh`（详见 `使用手册.md` 第一篇；首次迁到本机见第二篇与 `ENVIRONMENT.md`）。
3. 读 `system/metadata.md` → 确认当前项目 slug、所在模块、产出就绪状态。
4. 新论文先初始化工作区：`python scripts/init_project.py --name {slug} --output projects`。
5. 选运行方式（A/B/C）→ 打开对应模块 `MODULE.md` → 按「执行流程」推进；遇卡点停下等人裁决。

> 启动一句话指令示例：
> - 「跑 M1：请把我的模型想法写成可识别、可估计、可证明的正式设定」
> - 「从 M4 开始：模型与估计量已定，请搭建假设体系和定理地图」
> - 「只用 M7：对这篇理论论文做五视角模拟评审」

---

## 五、目录结构

```
Theoretical-Econometrics-Agent/
├── LICENSE                    # Apache License 2.0（适用边界见第八节）
├── README.md                  # 本文件：模块概览 + 三种运行方式
├── ORCHESTRATOR.md            # 编排器：角色、规则、模块路由、阶段闸门、状态机
├── ENVIRONMENT.md             # 工具链：R/TeX Live/Python 路径、Stata·MATLAB MCP 方案
├── 使用手册.md                 # 研究使用说明（第一篇）+ 本地迁移安装（第二篇）
├── 本地化部署说明.md           # 本地部署：Stata·MATLAB 双模式接入（MCP / 本地直连）
├── requirements.txt           # 直接依赖与兼容范围
├── requirements-lock.txt      # Python 3.10 可复现依赖锁
├── config/
│   ├── README.md               # 本机配置用途与边界
│   ├── local-tools.example.json # 本机工具路径模板
│   └── local-tools.schema.json  # 配置字段约束（local-tools.json 不入库）
├── agents/
│   ├── researcher.md          # 执行者协议（推导、编码、写作）
│   └── referee.md             # 审稿人协议（五视角评审，只攻击不代笔）
├── system/
│   ├── metadata.md            # 状态追踪：当前项目 + 模块状态 + 冻结输入
│   └── integrity-rules.md     # 学术诚信底线（不伪造文献/定理/模拟结果）
├── modules/                   # 七个模块（思维框架 + 卡点 + 模板）
│   ├── M1-model-specification/
│   ├── M2-literature-positioning/
│   ├── M3-qml-estimation/
│   ├── M4-asymptotic-theory/
│   ├── M5-monte-carlo/
│   ├── M6-paper-writing/
│   └── M7-referee-revision/
├── .cursor/
│   ├── rules/                 # 始终生效的路由与研究安全规则
│   └── skills/                # m1–m7 执行框架 Skill（Cursor 自动发现）
├── templates/
│   └── paper-project/         # 论文项目工作区模板（init_project.py 的复制源）
├── projects/                  # 运行时论文工作区；发行包仅保留 .gitkeep，新项目由脚本创建
├── examples/                  # 一个中性 QML 工作流文档案例（只读）
│   └── generic-qml-workflow/  # M1–M7 端到端示例；不含模拟结果或可投稿论文
├── paper-lib/                 # 用户提供的领域资料入口；发行包不内置专用研究材料
└── scripts/                   # 环境激活 + 项目初始化 + 校验工具 + MCP 配置
    ├── setup_env.sh            # macOS/Linux 激活
    ├── setup_env.ps1           # Windows PowerShell 激活
    ├── configure_local.py      # 生成本机路径配置
    ├── check_environment.py    # 跨平台严格环境自检
    ├── init_project.py        # 从模板初始化论文工作区
    ├── build_rag_index.py     # 构建轻量文献索引
    ├── check_latex_notation.py# LaTeX 标签/记号一致性检查
    ├── summarize_reviews.py   # 汇总评审报告
    ├── validate_skills.py     # 校验 .cursor/skills 下所有 SKILL.md
    ├── validate_project.py    # 全框架静态完整性校验
    └── mcp/mcp.json.example   # Stata / MATLAB MCP 客户端配置示例
```

> **模块 vs Skill 的分工**：`modules/MX-*/MODULE.md` 是**思维框架**（产出什么、卡点在哪、协议标准）；
> `.cursor/skills/mX-*/SKILL.md` 是**执行框架**（具体怎么做、装载顺序、常见陷阱）。编号一致，一一对应。
>
> **模板边界**：`templates/paper-project/` 当前以空间面板断点模型为默认骨架。
> 处理其他模型时，必须在 Gate 1 前替换全部不适用的模型、假设、DGP、估计代码与论文占位内容；
> `examples/generic-qml-workflow/` 只展示通用流程，不是可执行模板。

### 论文项目目录命名

`projects/{project-slug}/` 是一篇论文的工作区。项目名不用 `paper01` 这类流水号，
使用小写英文 kebab-case，例如：`linear-qml-study`、`dynamic-panel-model`、`threshold-estimation`。
slug 一旦进入 M3 后不应随意改动；改名须同步更新 `system/metadata.md` 与文档引用。

---

## 六、知识库与工具链

- **通用案例**（`examples/generic-qml-workflow/`）：用线性模型的高斯 QML 展示 M1–M7 契约，
  不提供模拟结果、已核验文献结论或可投稿论文。
- **paper-lib**（`paper-lib/README.md`）：用户提供的领域资料入口；仅保存来源与权限明确的材料，
  引用结论前须回到原文核对。
- **本地迁移**（`使用手册.md` 第二篇）：复制整个项目但不复制服务器 venv/软件；Windows、macOS、Linux 均在本机原生重建环境，不需要 WSL、容器或虚拟机。
- **工具链**（`ENVIRONMENT.md`）：Windows 用 `. .\scripts\setup_env.ps1`，macOS/Linux 用 `source scripts/setup_env.sh`——
  - 项目内 Python 3.10/3.11 `.venv`（日常安装用 `requirements.txt`；可复现安装用 `requirements-lock.txt`）
  - R 4.4+（`spatialreg`/`splm` 等空间计量包按需安装）
  - TeX Live 2026（英文 pdflatex / 中文 xelatex 编译）
  - Stata 经 MCP 接入（推荐开源 [SepineTam/mcp-for-stata](https://github.com/SepineTam/mcp-for-stata) 或 [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp)）
  - MATLAB 经官方开源 MCP 接入（[matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server)）；本机无 MATLAB 时用 Octave / Python(numpy+scipy) 等价实现
  - 本机已安装 Stata/MATLAB 时，也可不配 MCP 走**本地直连**（终端批处理调用），见 `本地化部署说明.md`

---

## 七、不可违反的底线

1. **不伪造**：文献、定理陈述、页码、证明、模拟结果一律不得虚构。
2. **每个符号进记号登记表**；每条假设有明确角色；每个定理绑定其使用的假设编号。
3. **证明缺口显式标注**：`Proof gap` + 缺什么引理/假设；候选结论标 `Candidate`，不冒充已证。
4. 模拟必须记录随机种子、DGP、参数真值、样本规模、重复次数与输出路径；结果表由脚本从原始估计生成，不手工输入。
5. 断点估计量的收敛速率不得套用「通用结论」，必须在当前渐近框架下推导。
6. **审稿只攻击不代笔**：Referee 产出意见，不直接改正文；修改走 M7 返修流程。
7. 人卡点不可跳过：模型设定、贡献定位、估计方案、假设体系、模拟设计、章节草稿、返修审定。
8. 全程中文沟通（英文投稿正文除外）。

---

## 八、许可证与第三方资产边界

本项目中由项目贡献者原创且有权许可的代码、脚本、文档、模板与示例源文件，按根目录
[`LICENSE`](LICENSE) 的 **Apache License 2.0** 授权；文件自身另有声明时，以该声明为准。

Apache License 2.0 **不延伸到**任何第三方资产，包括但不限于：

- 第三方论文、书籍、报告及其 PDF、扫描件或提取文本；
- 第三方数据集、受限数据库内容及其许可控制的派生文件；
- Stata、MATLAB 本体、工具箱、许可证、商标或其他专有组件；
- Python/R 依赖、MCP 服务器及其他外部软件；这些内容分别受其权利人条款约束。

使用者只能在已取得相应权利或适用法允许的范围内，将第三方论文和数据放入自己的
`projects/{slug}/` 运行时工作区；不得据本项目的 Apache License 2.0 重新分发这些资产。
发行树只提供 LaTeX 源文件，不提供 PDF、`.bbl` 或其他编译产物；需要时在本机运行
`latexmk -pdf main.tex` 再生。
