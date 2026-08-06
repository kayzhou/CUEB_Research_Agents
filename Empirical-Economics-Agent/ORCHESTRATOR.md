# ORCHESTRATOR — Empirical-Economics-Agent 编排器

> 本文件是框架的唯一入口骨架。每次启动先读本文件确认角色与当前模块，再按需补读对应 `modules/MX-*/MODULE.md`。

---

## 一、角色架构（三角色）

保留「反对党无处不在」内核，默认由当前主会话同时充当 coordinator：

- **Lead Author（人类）**：研究主题与主要设计不可改。负责全部卡点裁决。
- **Researcher（执行者）** → `agents/researcher.md`：执行 + 拓展思考 + 回应攻击。
- **Referee（审稿人）** → `agents/referee.md`：攻击产出、找漏洞、做模拟专家评审。只攻击不代笔。

简化点：不强制每一步都拆独立 Subagent。轻量任务由主会话直接走「自我攻防」即可；
只有重度子步骤（识别策略、主回归、证据链、正式审稿）才建议启动独立 Referee 会话保证独立性。

---

## 二、启动协议

1. 读本文件 → 确认角色与模块路由。
2. 按平台激活工具链：Windows 点调用 `. .\scripts\setup_env.ps1`；macOS/Linux 执行 `source scripts/setup_env.sh`。本机路径、引擎与 MCP 详情见 `ENVIRONMENT.md`。
3. 读 `system/metadata.md` → 确认项目 slug、当前模块、运行模式和各产出状态。
4. 涉及 M1/M4/M5 文献核对时，运行 `python code/utils/check_paperlib.py`；PDF 不完整则标记知识库阻塞，不得假装已核对原文。
5. 选运行方式（A 端到端 / B 从某步切入 / C 单模块）。
6. 打开目标模块 `MODULE.md` → 检查 Requires 是否齐全；缺则先补 stub。
7. 按模块「执行流程」推进；遇卡点先把状态改为 `blocked_on_human`，再等待裁决。
8. 模块收尾时回写 `system/metadata.md` 的产出状态、冻结输入和下一步。

---

## 三、不可违反规则

1. 原始数据只读；结果只由脚本生成，禁止手工改结果文件。
2. 论文正文数字、表图来自结果文件，不手工输入。
3. **样本侦查先于任何处理**：只诊断缺失、不自动缩尾/插值/删除，等人决策（M2 卡点）。
4. **包优先**：禁止手搓已有成熟包的估计方法；写代码前先搜包，结果写进脚本头注释。
5. **审稿只攻击不建设**：Referee 与模拟专家只产出意见报告，不改代码/正文；修改走 M5 返修流程。
6. **角色不越界**：Researcher 不改研究主题/范式/卡点决策；Referee 不改产出文件。
7. **知识库只读且引用必核对**：`paper-lib/` 不修改不删除；引用其中论文的结论/系数前必须回 PDF 原文核对，只引用直接相关的结果。
8. 人卡点不可跳过：范式决策、贡献审计、缺失值处理、估计计划、典型事实、实证结果、证据链、章节和返修审定。
9. 全程中文沟通（英文投稿正文除外）。

---

## 四、模块路由

每个模块 = 思维框架（MODULE.md）+ 执行框架（对应 Skill，编号一致）+ 相关代码/工具。
先读 MODULE.md 确定模式与卡点，再读 Skill 获取该模式下的完整执行步骤。

| 当前任务 | 模块 | 思维框架 MODULE.md | 执行框架 Skill | 主要代码/工具 |
|---------|------|-------------------|---------------|--------------|
| 立项、筛查、范式、文献、贡献审计 | **M1** | `modules/M1-project-init/MODULE.md` | `.cursor/skills/m1-project-init/SKILL.md` | `code/utils/paperlib_index.py`、`zotero_reader.py`、`fetch_style_pdf.py`、`paper-lib/` |
| 数据接入、清洗构建、缺失值侦查 | **M2** | `modules/M2-sample-audit/MODULE.md` | `.cursor/skills/m2-sample-audit/SKILL.md`（`audit_only` / `full_pipeline`） | `code/utils/validate_schema.py`、`track_n_change.py` |
| 描述统计、主估计、诊断、出表图 | **M3** | `modules/M3-empirical/MODULE.md` | `.cursor/skills/m3-estimation/SKILL.md` | `code/config/`、`code/analysis/`、`code/output/`、`scripts/master_build.*`、Stata/MATLAB MCP（`ENVIRONMENT.md`） |
| 证据链、章节起草、中英转换、润色 | **M4** | `modules/M4-writing/MODULE.md` | `.cursor/skills/m4-paper-writing/SKILL.md` | `paper-lib/`（风格基准）、TeX Live、`paper/exports/`（docx 交换） |
| 内部审查、模拟专家评审、真实意见返修 | **M5** | `modules/M5-review/MODULE.md` | `.cursor/skills/m5-referee-review/SKILL.md` | `code/utils/experiment_summary.py`、`paper-lib/`（7Q 比对）、`paper/exports/` |

### 程序层、流水线与过程记录

- **`code/`**：程序层。运行顺序 `config → clean → build → analysis → output → results`，路径统一走 `code/config/`（Python `PATHS` 字典 / Stata 全局宏），不硬编码。详见 `code/README.md`。
- **`scripts/`**：环境激活、MCP 与流水线入口。当前 `master_build.py` 是**就绪检查骨架**，`master_build.do` 的阶段调用也是示例；只有项目脚本接入后才能称为一键复现。
- **`paper-lib/`**：知识库（目标期刊全文 PDF 库 + `index.csv` 索引，只读）。用法与引用规则见 `paper-lib/README.md`。
- **`discussions/`**：研讨纪要汇总（选题/实证设计/贡献定位，冲突以最新日期为准）+ 设计理念文档（`V3.0-discussion-2-opposition-party.md` 反对党机制、`V3.0-autoscientists-study.md` 自动化科研）。

---

## 五、最小攻防协议（贯穿各模块）

每个重度子步骤遵循：

```
Researcher 写 PROPOSAL（含拓展思考）
  → Referee 写 ATTACK（按决策级别覆盖维度，标 HIGH/MEDIUM/LOW）
  → Researcher 写 RESPONSE（改 / 辩 / 标局限）
  → Lead Author 裁决 → 批准执行
  → Researcher 执行 → 记录 → Referee 审计
```

决策级别（决定攻击覆盖与轮次上限）：

| 级别 | 攻击覆盖 | 轮次上限 | 典型子步骤 |
|------|---------|---------|-----------|
| 重度 | 全维度 | 3 | 识别策略、主回归、证据链、正式审稿 |
| 中度 | 关键维度 + 聚焦 | 2 | 变量构造、诊断解读、章节草稿 |
| 轻度 | 快速扫 | 1 | 表格格式、文件命名、编译修复 |

轻量任务可省略独立会话，由主会话自审；但 HIGH 级问题必须显式记录与回应。

---

## 六、状态机（模块级）

主状态只有四种：

`not_started` → `in_progress` → `blocked_on_human` → `in_progress` → `done`

- `blocked_on_human`：报告和待决问题已落盘，禁止继续执行会受该决定影响的步骤。
- `done`：规范产出齐全、验证完成、冻结输入已记录。

从中间切入时可使用带来源限定的完成态：`done(stub)`、`done(external)`、`done(partial)`；必须在备注中写明缺失项、输入来源和适用边界。
