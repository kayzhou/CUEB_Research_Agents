---
name: m1-project-init
description: "Runs M1 project initiation: paper screening, paradigm and engine selection, literature search, contribution audit, and milestone initialization. Use when starting a new empirical paper, testing a research idea, or auditing novelty."
---

# M1 Project Init — 选题立项与文献调研 Skill

## Use This Skill When

1. 需要从零开始设立一篇新论文（paper screening、范式决策、论文简报）。
2. 需要执行贡献审计——搜索最接近文献、分层阅读、构建比对矩阵、过严苛五问。
3. 需要初始化项目里程碑和元数据。
4. 需要确认研究范式（因果推断 vs 资产定价）和主力引擎（Stata/R vs Python）。
5. 任何 M1 立项阶段的任务。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认三角色架构和不可违反规则。
2. `system/metadata.md`：确认项目当前状态（current_module、paradigm、engine）。
3. `system/milestones.md`：确认当前里程碑状态。
4. `modules/M1-project-init/MODULE.md`：思维框架——执行流程与两个卡点。
5. `modules/M1-project-init/templates/paper-screen-template.md`：论文筛查模板——对标期刊、最接近文献、推进判断。
6. `modules/M1-project-init/templates/paper-brief-template.md`：论文简报模板——研究问题、核心识别/定价逻辑、预期贡献方向。
7. `modules/M1-project-init/templates/contribution-audit-template.md`：贡献审计模板——搜索协议、分层阅读、比对矩阵、严苛五问。
8. `ENVIRONMENT.md` §三：引擎选择决策树（范式 → 引擎的映射）。
9. `paper-lib/index.csv` + `paper-lib/README.md`：知识库检索入口（文献调研第一站）。

## Scope Boundary

1. 本 skill 只处理 M1 立项阶段任务。不可触碰数据层（`data/`）、估计层（`code/analysis/`）、写作层（`paper/{project-slug}/sections/`）。
2. 范式决策完成后，移交 `m2-sample-audit` skill 进入数据阶段。
3. 贡献审计只输出结论和比对矩阵，不直接修改研究设计——修改由 Lead Author 裁决。
4. 本 skill 不决定样本筛选标准、不选择具体估计方法、不草案正文。

## 与其他 skill 的边界判定

| 场景 | 用 m1-project-init | 用其他 skill |
|------|----------------|-------------|
| 论文筛查、范式决策 | ✅ 本 skill | — |
| 贡献审计、文献比对 | ✅ 本 skill | — |
| 里程碑初始化 | ✅ 本 skill | — |
| 数据可行性核验 | — | `m2-sample-audit` |
| 数据清洗、样本构建 | — | `m2-sample-audit` |
| 撰写估计脚本 | — | `m3-estimation` |
| 起草论文正文 | — | `m4-paper-writing` |
| 攻击提案或审查 | — | `m5-referee-review` |

## Workflow（按任务类型）

### 论文筛查任务

1. 读 `modules/M1-project-init/templates/paper-screen-template.md` → 确认筛查框架。
2. **检索知识库**：`python code/utils/paperlib_index.py --search <研究问题关键词>`，确认目标期刊近五年是否已有直接相关研究（先按 `ENVIRONMENT.md` 激活本机环境）。
3. 写 `paper/{project-slug}/paper-screen.md`，必须包含：
   - 研究问题一句话
   - 对标期刊（1-3 本）
   - 最接近文献（3-5 篇，含简要对比；paper-lib 命中的直接相关论文优先列入）
   - 推进判断（为什么值得做、与最接近文献的差异）
   - 数据可行性初步判断

### 范式决策任务

1. 读 `modules/M1-project-init/MODULE.md` 步骤 2 → 两层决策树（先判范式，再选引擎）。
2. 读 `ENVIRONMENT.md` §三 → 本机可用引擎（有 Stata 授权走 Stata MCP；无则因果推断走 R，资产定价走 Python）。
3. 基于 paper-screen 的研究问题，判定范式并给出理由。
4. 写入 `paper/{project-slug}/paper-brief.md` 的范式节。
5. 更新 `system/metadata.md`：`paradigm` 和 `engine` 字段。**等 Lead Author 批准。**

### 论文简报任务

1. 读 `modules/M1-project-init/templates/paper-brief-template.md` → 确认简报结构。
2. 基于 paper-screen 的结论，写 `paper/{project-slug}/paper-brief.md`，必须包含：
   - 研究问题（精确到可检验的假设）
   - 核心识别/定价逻辑（DID/IV/RD 或 Portfolio Sort/FMB 等）
   - 数据来源预期
   - 预期贡献方向（数据/识别/机制/市场，至少一项）
   - 主要替代解释预判
3. 确保 paper-brief 与 paper-screen 口径一致。

### 贡献审计任务

1. 读 `modules/M1-project-init/templates/contribution-audit-template.md` → 载入搜索协议、分层阅读和严苛五问。
2. 执行文献搜索（顺序固定）：
   - **paper-lib 知识库**：`paperlib_index.py --search` 多组关键词检索，锁定直接相关论文
   - Zotero 库（`code/utils/zotero_reader.py`）→ 种子论文引用扩展 → Google Scholar → 目标期刊近三年目次
   - 锁定 5-10 篇最接近文献
3. 分层阅读（paper-lib 命中论文优先进 Tier 1/2，可直接读 PDF 原文）：
   - Tier 1（2-3 篇）：深度阅读——识别策略、样本、主要发现、局限
   - Tier 2（3-4 篇）：中等阅读——贡献定位、与本文差异
   - Tier 3（2-3 篇）：轻量阅读——确认不与本文核心贡献重叠
4. 构建比对矩阵：每篇文献 vs 本文，逐维标注差异化程度。
5. 过严苛五问（以 paper-lib 检索结果为证据回答前两问）：
   - "这个想法已经被做过了吗？"
   - "只是换了市场/样本期吗？"
   - "机制是显然的吗？"
   - "系数太小没有经济意义吗？"
   - "方法没有实质新意吗？"
6. 输出贡献评级（数据/识别/机制/市场/整体各一评级）。
7. 写入 `paper/{project-slug}/review/contribution-audit-[版本].md`。

### 里程碑初始化任务

1. 读 `system/milestones.md` → 确认默认 5 个里程碑。
2. 根据 paper-brief 调整里程碑的具体标准（如适用）。
3. 确保与 `system/metadata.md` 的 current_module 字段一致。

## Output Expectations

一次完整的 M1 任务应产出：

1. `paper/{project-slug}/paper-screen.md`——论文筛查结果（对标期刊、最接近文献、推进判断）。
2. `paper/{project-slug}/paper-brief.md`——论文简报（研究问题、范式、引擎、贡献方向）。
3. `paper/{project-slug}/review/contribution-audit-[版本].md`——贡献审计报告（比对矩阵 + 严苛五问结论）。
4. `system/metadata.md`——更新 current_module → M2、paradigm/engine 字段已填。
5. `system/milestones.md`——5 个里程碑已初始化。

所有产出在进入 M2 前必须经 Lead Author 批准。

## Common Pitfalls

1. **范式未定就写清洗脚本**：范式决策必须先于任何数据操作。M1 确认范式，M2 才开始拿数据。
2. **跳过 paper-brief 直接动笔**：没有 brief 就没有锁定研究设计，后续容易漂移。
3. **贡献审计未完成就写引言**：贡献审计 → 文献综述 → 引言贡献段是三阶段闭环。贡献审计中评级为"中"或"低"的维度，引言中不得使用强声称。
4. **贡献审计只搜索不比对**：比对矩阵必须逐文献逐维标注，不能只列文献摘要。
5. **跳过 paper-lib 直接上 Google Scholar**：知识库是文献搜索第一站——目标期刊已发表的直接相关研究是贡献审计最硬的证据。
6. **在本 skill 中决定样本范围**：样本筛选是 M2 + Lead Author 裁决的职责，立项阶段只做初步可行性判断。
7. **跳过 Lead Author 卡点**：范式决策必须经 Lead Author 批准才能进入 m2-sample-audit。
