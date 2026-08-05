---
name: m2-sample-audit
description: "Runs M2 sample preparation and audit: optionally builds a reproducible dataset from raw inputs, diagnoses missingness without treatment, records the human decision, and freezes the analysis sample. Use when receiving data, cleaning or merging sources, auditing a final sample, or updating the codebook."
---

# M2 Sample Audit — 数据接入与样本侦查 Skill

本 Skill 有两种显式运行模式：

- `audit_only`（默认）：输入已经清洗、构建完成的最终样本，直接执行步骤 6–7。
- `full_pipeline`（扩展）：输入原始数据，先执行步骤 1–5，再执行步骤 6–7。

启动时必须把所选模式写入 `system/metadata.md` 的 `m2_mode` 字段；不得在未声明模式的情况下从原始数据直接开始。

## Use This Skill When

1. 需要接入新数据源、执行数据可行性核验。
2. 需要编写或修改数据清洗脚本（`code/clean/`）。
3. 需要构建分析样本（`code/build/`，多源合并）。
4. 需要执行样本侦查——缺失值全景扫描、模式诊断、向 Lead Author 汇报。
5. 需要生成或更新 codebook（`data/final/codebook.md`）。
6. 需要执行 Schema 验证（`code/utils/validate_schema.py`）。
7. 任何 M2 数据阶段的任务。

## Required Inputs（优先收集）

1. `ORCHESTRATOR.md`：确认不可违反规则（特别是规则 1：原始数据只读；规则 3：样本侦查先于任何处理）。
2. `system/metadata.md`：确认当前模块和范式（paradigm 字段决定清洗脚本的语言选择）。
3. `modules/M2-sample-audit/MODULE.md`：样本侦查协议——缺失全景扫描、分组对比、MCAR/MAR/MNAR 判断框架。
4. `modules/M2-sample-audit/templates/sample-audit-report-template.md`：侦查汇报模板。
5. `code/README.md`：程序层规范——运行顺序、路径约定、脚本头部注释、编号命名。
6. `ENVIRONMENT.md`：分平台工具链激活（Windows `setup_env.ps1` / macOS/Linux `setup_env.sh`）与引擎路由。
7. `paper/{project-slug}/paper-brief.md`：确认数据需求是否与立项时的预期一致。

## Scope Boundary

1. 本 skill 只处理 M2 数据阶段任务。不执行任何估计或回归分析。
2. `data/raw/` 目录只读，绝不直接修改原始数据文件。
3. **Agent 只诊断和汇报缺失值，不自动处理**——所有缺失值处理决策（缩尾、插值、删除观测）必须由 Lead Author 做出。
4. 三层数据隔离：`raw/` → `processed/` → `final/`，数据流单向。
5. 清洗脚本只做标准化（变量名统一、编码转换、格式统一），不做样本筛选——筛选统一在 `code/build/` 中做。
6. 进入条件：范式已定（`system/metadata.md` 中 paradigm 字段已填），Lead Author 已批准进入数据阶段。

## 与其他 skill 的边界判定

| 场景 | 用 m2-sample-audit | 用其他 skill |
|------|---------------|-------------|
| 数据可行性核验 | ✅ 本 skill | — |
| 逐源清洗脚本 | ✅ 本 skill | — |
| 样本构建（多源合并） | ✅ 本 skill | — |
| 样本侦查（缺失诊断） | ✅ 本 skill | — |
| codebook 生成 | ✅ 本 skill | — |
| Schema 验证 | ✅ 本 skill | — |
| 论文筛查、范式决策 | — | `m1-project-init` |
| 估计脚本、诊断检验 | — | `m3-estimation` |
| 论文写作 | — | `m4-paper-writing` |
| 审查攻击 | — | `m5-referee-review` |

**数据+估计混合任务**：m2-sample-audit 完成 → 移交 `m3-estimation`。两步不同 Agent 会话，不合并。

## Workflow（按步骤顺序）

> `audit_only` 直接从步骤 6 开始；只有 `m2_mode: full_pipeline` 才能执行步骤 1–5。

### 步骤 1：数据可行性核验

1. 对每个计划内数据源，检查：
   - 核心变量是否存在（对照 paper-brief 中的变量需求）
   - 样本期是否覆盖研究需要的区间
   - 关键变量缺失率是否在可控范围内（> 30% 需特别标注）
   - 标识符完整性（Stkcd/PERMNO/GVKEY 等）
2. 输出可行性核验结论：通过 / 有条件通过 / 不通过。
3. **数据可行性不通过 → 立即止损，回报 Lead Author**。不继续投入清洗资源。

### 步骤 2：逐源 intake-report

1. 对每个数据源，生成 intake-report，至少包含：
   - 数据来源、格式、编码
   - 字段清单（变量名、类型、样本期、缺失率初估）
   - 初步质量评估（重复率、异常值标记、编码问题）
2. 优先读 intake-report 和 cleaning-plan，而非原始数据全量；数据预览只读前 N 行（N ≤ 100）。

### 步骤 3：清洗计划

1. 创建或更新 `data/processed/cleaning-plan.md`：
   - 逐源列出清洗步骤
   - 变量映射（原始变量名 → 标准变量名）
   - 合并策略（键变量、合并方式）
   - 预期 N-change（每一步的样本量变化预期）

### 步骤 4：清洗脚本

1. 遵循 `code/README.md` 的程序层规范：
   - 脚本头部：用途说明、输入输出、方法来源、变量定义、关键决策、修改记录
   - 路径通过 `code/config/` 变量引用，禁止硬编码绝对路径
   - Python 用 pathlib（`from code.config import PATHS`），Stata 加载 `code/config/config.do`
   - 一源一脚本：每个数据源一个独立清洗脚本，编号即执行顺序
2. 清洗只做标准化，不做样本筛选：
   - ✅ 统一变量名、统一编码（GBK → UTF-8 等）、标记明显异常值
   - ❌ 删除观测、缩尾、按条件筛选行
3. 运行自动验证：
   - 行数在合理范围内
   - 必填列非空
   - 唯一键无重复
   - 数值范围合理

### 步骤 5：构建脚本

1. 在 `code/build/` 下写构建脚本，链式追加：
   - 从核心表开始（如主回归样本的主体表）
   - 逐步合并其他数据源
   - 在此阶段执行样本筛选（按 paper-brief 定义的样本范围）
2. N-change tracking：每一步筛选后记录样本量变化，输出到日志（`code/utils/track_n_change.py` 可汇总）。

### 步骤 6：样本侦查（卡点，不可跳过）

> ⚠️ **这是 M2 最重要的卡点。样本侦查不完，不进缩尾。**

1. 读 `modules/M2-sample-audit/MODULE.md` → 载入侦查协议（Step 1-3）。
2. 执行全量缺失值全景扫描：
   - 逐变量统计缺失率
   - 按分组（行业/年份/市值分组等）对比缺失率差异
   - 诊断缺失模式：MCAR（完全随机缺失）/ MAR（随机缺失）/ MNAR（非随机缺失）
   - 检查缺失变量之间的相关性
3. **向 Lead Author 汇报缺失全景**，用模板写入 `paper/{project-slug}/review/sample-audit-report.md`，包含：
   - 缺失率汇总表（逐变量）
   - 分组对比结果
   - 缺失模式初步诊断
   - **不做任何处理建议**——只呈现事实
4. 把 `system/metadata.md` 的 M2 状态改为 `blocked_on_human`，并在当前卡点中列出待决定变量。
5. **等 Lead Author 决策**——确认每类缺失值的处理方式后，改回 `in_progress`，才能进入步骤 7。
6. **禁止**：在 Lead Author 决策前执行任何缩尾、插值或删除。

### 步骤 7：缩尾 + codebook

1. 按 Lead Author 批准的决策，执行缩尾（如适用）；处理后样本另存新文件。
2. 生成 `data/final/codebook.md`（"外部读者"标准）：
   - 每个变量：来源、构造公式、处理选择、在回归中的角色
   - 样本筛选步骤和每一步的 N 变化
   - 缺失值处理决策与理由（逐变量）
   - 缩尾处理：变量、阈值、替代方案
3. 双格式导出：`.dta` + `.parquet`。
4. 根据 codebook 创建或更新 `data/final/schema.yaml`。
5. 运行 `python code/utils/validate_schema.py <最终样本路径>` → Schema 验证通过。
6. 将 M2 标为 `done`，记录冻结样本文件名与校验日志，再移交 M3。

## Key Rules

1. **样本侦查先于缩尾**（ORCHESTRATOR 规则 3）：在 Lead Author 批准所有缺失值处理决策之前，不得执行任何缩尾。
2. **Agent 不读原始数据全量**：优先读 cleaning-plan、codebook、intake-report。数据预览只读前 N 行（N ≤ 100）。
3. **路径通过 `code/config/` 管理**：所有脚本中的路径引用必须通过 config 变量，禁止硬编码绝对路径。
4. **三层数据隔离**：`data/raw/` 只读，`data/processed/` 放清洗后中间文件，`data/final/` 放分析就绪样本。数据流单向。
5. **自动处理缺失值是最高级别的违规**：缩尾、插值、删除观测必须由人决策。

## Output Expectations

`audit_only` 必须产出第 5–9 项；`full_pipeline` 必须产出全部：

1. `data/processed/cleaning-plan.md`——清洗计划（逐源步骤、变量映射、合并策略）。
2. 各数据源的 intake-report——数据来源、格式、字段清单、初步质量评估。
3. `code/clean/` 下的清洗脚本——可重跑，一源一脚本，含头部结构化注释。
4. `code/build/` 下的构建脚本——链式追加，含 N-change tracking。
5. `paper/{project-slug}/review/sample-audit-report.md`——缺失全景、模式诊断与人类决策记录。
6. `data/final/` 下的分析样本（`.dta` + `.parquet`）。
7. `data/final/codebook.md`——"外部读者"标准，含变量说明和样本筛选步骤。
8. `data/final/schema.yaml`——最终样本的机器可检验约束。
9. Schema 验证通过（`validate_schema.py <最终样本路径>` 无报错）。

## Common Pitfalls

1. **跳过样本侦查直接缩尾**：这是项目中最严重的流程违规。必须先在缺失全景扫描后等 Lead Author 决策，才能缩尾。
2. **Agent 自动处理缺失值**：Agent 不能自行决定缩尾阈值、插值方法或删除条件。只诊断，不处理。
3. **在 `data/raw/` 中直接修改文件**：所有修改必须通过脚本，输出到 `processed/` 或 `final/`。
4. **编码问题未在清洗阶段处理**：CSMAR 的 GBK、Wind 的 "--" 缺失值标记等必须在清洗脚本中统一处理。
5. **忘记 N-change tracking**：每一步筛选后必须记录样本量变化，这是审稿人常问的问题。
6. **清洗脚本无状态**：每次运行清洗脚本应产生相同输出（设置随机种子如适用）。
7. **codebook 写得太简略**：目标读者是"没看过代码的外部研究者"，每个变量必须说清来源、构造公式、处理选择。
8. **清洗和构建完成后不验证**：必须运行 Schema 验证确认 final 样本的变量存在、类型正确、唯一键无重复。
