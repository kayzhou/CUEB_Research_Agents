# M1 — 选题立项与文献调研

> 相对原框架：**全保留**。涵盖论文筛查、范式决策、文献调研、贡献审计、里程碑初始化。

---

## Requires（前置输入）

- 一个研究想法 / 研究问题（一句话即可）
- 目标期刊区间（可选；没有也能跑，后续可补）
- 已有文献线索 / Zotero 库（可选）

## Produces（产出）

- `paper/{project-slug}/paper-screen.md` — 论文筛查
- `paper/{project-slug}/paper-brief.md` — 锁定研究问题、范式、引擎和方法
- `paper/{project-slug}/review/contribution-audit-v1.md` — 贡献审计
- `system/metadata.md` 更新：`project`、`paradigm`、`engine` 已填

## 卡点（人裁决）

1. **范式批准**：因果推断（Stata）vs 资产定价（Python）由 Lead Author 拍板。
2. **贡献审计结论**：评级「中/低」的维度，后续引言不得用强声称。

---

## 执行流程

### 步骤 1：论文筛查

写 `paper-screen.md`，必含：

- 研究问题一句话
- 对标期刊（1-3 本）
- 最接近文献（3-5 篇，含简要对比）
- 推进判断（为什么值得做、与最接近文献的差异）
- 数据可行性初步判断

### 步骤 2：范式决策（卡点）

两层决策树：先判范式，再选引擎。

- **因果推断**：政策/事件/制度冲击的因果效应。方法 DID/IV/RD/Event Study/Synthetic Control。引擎 Stata。核心包 reghdfe、ivreghdfe、csdid、rdrobust、eventdd。
- **资产定价**：预期收益截面差异、因子模型、基金业绩。方法 Portfolio Sort/Fama-MacBeth/GRS/DGTW。引擎 Python。核心包 pandas、linearmodels、statsmodels。

判定后写入 `paper-brief.md` 范式节，更新 `system/metadata.md` 的 `paradigm`/`engine`。**等 Lead Author 批准才进入下一步。**

### 步骤 3：论文简报

写 `paper-brief.md`，必含：

- 研究问题（精确到可检验假设）
- 核心识别/定价逻辑
- 数据来源预期
- 预期贡献方向（数据/识别/机制/市场，至少一项）
- 主要替代解释预判

确保与 `paper-screen.md` 口径一致。

### 步骤 4：文献调研

- **第一站：paper-lib 知识库**——`python code/utils/paperlib_index.py --search <关键词>` 检索目标期刊（《管理世界》2022-2026 全文库）是否已有直接相关研究，命中论文直接读 PDF 原文。
- 再从最接近文献出发：Zotero → 引用扩展 → Google Scholar → 目标期刊近三年目次。
- 一次性原则：新增文献同步更新文献索引。
- 锁定 5-10 篇最接近文献（paper-lib 命中的直接相关论文优先进 Tier 1/2）。

### 步骤 5：贡献审计（卡点）

1. 分层阅读：
   - Tier 1（2-3 篇）深读：识别策略、样本、主要发现、局限。
   - Tier 2（3-4 篇）中读：贡献定位、与本文差异。
   - Tier 3（2-3 篇）轻读：确认不重叠。
2. 构建**比对矩阵**：每篇文献 vs 本文，逐维标注差异化程度。
3. 过**严苛五问**（前两问必须以 paper-lib 检索结果为证据回答）：
   - 这个想法已经被做过了吗？
   - 只是换了市场/样本期吗？
   - 机制是显然的吗？
   - 系数太小没有经济意义吗？
   - 方法没有实质新意吗？
4. 输出贡献评级（数据/识别/机制/市场/整体各一评级）→ 写入 `paper/{project-slug}/review/contribution-audit-v1.md`。

> 贡献审计 → 文献综述 → 引言贡献段是三阶段闭环。评级「中/低」的维度，引言不得使用强声称。

### 步骤 6：里程碑初始化

根据 `paper-brief.md` 调整里程碑标准，确认与 `system/metadata.md` 一致。

---

## Common Pitfalls

1. 范式未定就动数据——范式必须先于任何数据操作。
2. 跳过 paper-brief 直接动笔——没锁定设计后续会漂移。
3. 贡献审计只搜不比对——比对矩阵必须逐文献逐维标注。
4. 在立项阶段定样本范围——样本筛选是后续 + 人裁决职责。

---

## 独立运行说明

M1 是流程起点，无上游依赖，可直接运行。
若你只想做「文献调研 + 贡献审计」而跳过范式决策，可只执行步骤 4-5，并在 `system/metadata.md` 标 M1 为 `done(partial)`。

模板见 `templates/`：`paper-screen-template.md`、`paper-brief-template.md`、`contribution-audit-template.md`。

---

## 细节流程 Skill 与代码/工具

- **执行框架（细节流程）**：`.cursor/skills/m1-project-init/SKILL.md` —— M1 完整工作流、Required Inputs 装载顺序、贡献审计搜索协议、常见陷阱。
- **知识库**：`paper-lib/`（《管理世界》全文库 + `index.csv` 索引，用法见 `paper-lib/README.md`）—— 文献调研第一站、贡献审计的比对证据来源。
- **相关代码/工具**：
  - `code/utils/paperlib_index.py` —— 知识库索引生成与关键词检索。
  - `code/utils/zotero_reader.py` —— 读取 Zotero 库，辅助文献调研与索引。
  - `code/utils/fetch_style_pdf.py` —— 抓取英文期刊范文 PDF，缓存到 `paper-lib/style-references/pdfs/`。
- **引擎决策参考**：`ENVIRONMENT.md` §三（本机可用引擎：Stata 经 MCP / R / Python / MATLAB）。
- **设计理念**：`discussions/`（选题方向、贡献定位的研讨纪要汇总）。
