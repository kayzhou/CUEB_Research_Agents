---
name: m4-paper-writing
description: "Runs M4 evidence-led paper writing: builds the evidence chain, drafts synchronized Chinese and English sections, aligns prose with verified results and journal exemplars, writes self-contained table notes, and compiles submission files. Use for drafting, translation, polishing, or writing-only revisions that do not change data or methods."
---

# M4 Paper Writing — 论文撰写 Skill

## Use This Skill When

1. 需要起草或修改**不涉及研究设计改动**的实证论文正文，或处理纯写作层的 revision。
2. 需要把中文讨论稿整理成英文学术论文段落，或把英文稿转成中文讨论稿。
3. 需要对现有段落做英文精修、中文润色、去 AI 味或逻辑核对。
4. 需要撰写或修改表格/图形的 caption 与 note。
5. 需要在不改研究设计的前提下，提升论文表述的清晰度、节奏和目标期刊风格一致性。

## Required Inputs

1. `ORCHESTRATOR.md`：确认模块路由、不可违反规则和统一进度。
2. 若当前任务是返修：先按 `modules/M5-review/MODULE.md` 5.4 的 triage 判断它是否只影响证据链或写作层；若已触及研究设计、变量定义或方法选择，切回 `m3-estimation` skill；若触及数据或样本变更，应先行调用 `m2-sample-audit` skill。
3. `paper/{project-slug}/section-briefs/对应章节-brief.md`：确认本轮目标、当前状态和依赖表图。
4. **范文与解剖笔记（写作风格基准）**：
   - 中文稿 → `paper-lib/`（《管理世界》全文库）：用 `paperlib_index.py --search` 选 2–3 篇主题/方法最接近的范文；
   - 英文稿 → `paper-lib/style-references/pdfs/`（`code/utils/fetch_style_pdf.py` 抓取的英文期刊范文）；
   - 对应解剖笔记 `paper/{project-slug}/style-anatomy/*-anatomy.md`：必须读模块B（逐段解剖）、模块C（句式库）、模块D（段落微观结构）。无解剖笔记先补写再动笔。
5. `modules/M4-writing/MODULE.md` 与 `modules/M4-writing/templates/`：证据链、section-brief、表图 note 模板。
6. 相关结果输出：本章需要引用的表格、图形、关键数字或审查报告（`results/` 下，正文数字一律来自结果文件）。
7. `ENVIRONMENT.md`：TeX Live 编译（英文 pdflatex / 中文 xelatex）与 python-docx 导出工具。

## Scope Boundary

1. 本 skill 只处理写作、改写、润色、caption/note 和写作逻辑核对，不负责新增识别策略、估计模型或数据处理决策。
2. 如果修改触及研究设计、变量定义、识别假设或方法选择，应回到 `m3-estimation` skill；若涉及数据层改动则先回 `m2-sample-audit` skill。
3. 共享入口、统一进度与章节状态机制以 `ORCHESTRATOR.md` + `system/metadata.md` 为准；本 skill 不维护平行状态。
4. 当前 skill 是纯写作任务的默认入口；只有当写作同时牵涉方法或结果口径时，才与 `m3-estimation` 联用。
5. 写作层逻辑检查（E 类——措辞/术语/局部一致性）在本 skill 内处理。跨节矛盾或识别链断裂（P1/P2）标记但移交 `m5-referee-review` skill（7R 正式审查）。

## 与其他 skill 的边界判定

| 场景 | 用 m4-paper-writing | 用其他 skill |
|------|--------------------------|-------------|
| 章节起草、中英转换、精修润色 | ✅ 本 skill | — |
| 表图 caption/note 写作 | ✅ 本 skill | — |
| 写作层逻辑核对（措辞/术语/局部） | ✅ 本 skill（E 类） | — |
| 新项目立项、范式决策 | — | `m1-project-init` |
| 数据清洗、样本构建、样本侦查 | — | `m2-sample-audit` |
| 估计脚本、诊断检验、图形生成 | — | `m3-estimation` |
| 7R/7Q 审查、Proposal 攻击 | — | `m5-referee-review` |
| **逻辑检查（P1/P2 跨节/识别链）** | — | `m5-referee-review`（7R 正式审查） |
| **图形任务（生成图）** | — | `m3-estimation` |
| **图形任务（写 note）** | ✅ 本 skill | — |
| **混合返修（写作层）** | ✅ 本 skill | — |
| **混合返修（触及数据/方法）** | — | `m2-sample-audit` 或 `m3-estimation`（先 triage） |

**图形横跨型任务**：分两步——先用 `m3-estimation` 生成图形，再用本 skill 写 note。两步不合并到同一 Agent 会话。

**写作+方法混合任务**：先 `m4-paper-writing` 标记需求 → 移交 `m3-estimation` 出结果 → 再回到本 skill。若涉及数据层变更，则先行 `m2-sample-audit`。

## Workflow

### 阶段 0：写前装载

1. 先读 `ORCHESTRATOR.md` 与 `system/metadata.md`，确认项目整体处于什么阶段。
2. 若当前任务属于返修，先确认 triage 是否已把本轮影响面限定在写作层；若上游数据、样本或识别仍未锁定，暂停写作修改。
3. 读对应 `section-brief`，确认这一轮只解决什么，不解决什么。
4. **装载范文**：
   - 中文讨论稿以 `paper-lib/`《管理世界》范文为基准：检索并锁定 2–3 篇主题/方法最接近的论文，读 PDF 原文；
   - 英文投稿稿以 `paper-lib/style-references/pdfs/` 下目标期刊范文为基准；
   - 读（或先补写）解剖笔记的**模块B（逐段解剖）**、**模块C（句式库）**、**模块D（段落微观结构）**。禁止不读范文就动笔。
5. 对照 `empirical-output-checklist.md` 和结果文件，锁定本章必须引用的表图与关键数字。
6. 动笔前从模块C提取当前章节需要的句式模板（开篇句式→引言、结果报告句式→结果段、贡献声明句式→引言贡献段等），贴到写作区作为脚手架。

### 阶段 1：判断任务类型

1. `章节起草`：从零或半成品推进一整章或一整节。
2. `中转英`：把中文讨论稿改写成英文投稿稿。
3. `中转中`：把零散中文要点整理成可讨论的中文正文。
4. `英文精修/去 AI 味`：在不改研究含义的前提下，让英文稿更自然、简洁、期刊化。
5. `逻辑核对`：只检查逻辑、术语、一致性和表图对应，不做大改。
6. `表图 note/caption`：单独写或改图注、表注、标题。

### 阶段 2：执行原则

1. 高阈值改写：如果原文已经清楚、准确、符合当前章节目标，优先保留原文，只修实质问题。
2. 先抓逻辑主线，再改句子。不要为了语言表面顺滑而打散原有因果链。
3. 除非内容天然并列，否则保持连贯段落，不把连续论证改成机械列表。
4. 英文投稿稿保持 LaTeX 纯净，不额外加入强调格式；中文讨论稿保持普通正文，不堆 Markdown 装饰。
5. 去 AI 味的核心不是"换高级词"，而是去掉空话、机械过渡词、破折号滥用、三点式堆砌和无意义的对称句。
6. 段落论证结构必须与范文模块D的四拍结构一致（判断→数字→经济显著→对比），不能自行发明段落节奏。
7. 句式复用而非抄袭：从模块C选句式模板，填入本论文的具体变量、数据和判断，保留句式骨架但替换全部事实内容。
8. **引用直接相关的结果**：与 paper-lib 文献对话时引用其具体结论与系数量级（"与 XX（2024）发现的 X% 效应相比"），引用前回 PDF 原文核对，不凭记忆转述（规则见 `paper-lib/README.md` §三）。

### 阶段 3：按任务类型输出

#### A. 章节起草

1. 先更新 `section-brief`，写清本轮目标、依赖表图和未决问题。
2. 先产出 `paper/{project-slug}/sections_cn/` 下的中文讨论稿，用于与合作者对齐逻辑。
3. 再同步到 `paper/{project-slug}/sections/` 下的英文投稿稿，确保结构和事实口径一致。

#### B. 中转英

1. 不是逐句直译，而是把中文讨论稿重写成符合 finance/econ 英文论文习惯的段落。
2. 保留全部事实、数字、限定条件和变量定义，不擅自补新结论。
3. 英文稿写完后，检查是否残留中文、未处理的全角标点或不必要的格式命令。

#### C. 中转中

1. 先识别中心判断，再把口语、碎片和跳跃逻辑重组为学术段落。
2. 中文讨论稿服务合作者沟通，允许保留必要的 `[TODO]`、`[CHECK]`，但不允许口径漂移。

#### D. 英文精修 / 去 AI 味

1. 只修逻辑跳跃、术语漂移、机械连接词、空泛夸饰和明显中式英语。
2. 如果原文已经自然、严谨、可投稿，明确给出"保持原文"判断，不做表演式重写。
3. 避免无意义的高级词替换；优先选择朴实、清楚、学界通用的表达。

#### E. 逻辑核对

1. 只报实质问题：逻辑断层、术语混乱、表图与正文不一致、结论超出证据。
2. 语气保持严格、中性、直接；不使用安慰性、鼓励性或谄媚式前置语。
3. 不把可改可不改的风格问题上升成"必须修改"。
4. 若无实质问题，明确给出"检测通过"结论。

#### F. 表图 note / caption

1. 标题要直接命名内容，不用空泛句子或装饰性前缀。
2. note 必须自明：即使不看正文，也能知道样本、变量、估计方法、参数含义、标准误/聚类或置信区间、显著性规则。
3. 中文讨论稿和英文投稿稿都保留完整 note，只做语言切换，不删信息。

### 阶段 4：编译与导出（工具链）

1. **编译**：先按 `ENVIRONMENT.md` 用 Windows `setup_env.ps1` 或 macOS/Linux `setup_env.sh` 载入 TeX Live——英文稿 `pdflatex`，中文稿 `xelatex`（ctex）。编译日志中的 undefined reference / missing figure 必须清零。
2. **docx 导出**（需要 Word 批注的合作者）：用 python-docx（已装于 py_env）把章节导出到 `paper/exports/`；docx 不是论文真源，批注意见须人工同步回 `sections/*.tex`。

## Back-End Self-Check

输出前至少检查以下事项：

1. 术语一致性：同一概念是否在本段、本节与前文中换了名字。
2. 信息完整性：数字、样本期、变量定义、限定条件是否被误删。
3. 表图对应：正文中的每个判断是否有表图支撑；note 是否缺关键口径。
4. 语言纯净度：英文稿是否残留中文、全角标点、无关 LaTeX/Markdown 噪音；中文稿是否仍口语化或翻译腔过重。
5. 修改必要性：是否为了"显得有动作"而改动了本来已经合格的句子；如果是，撤销修改。
6. 范文对齐度：四拍结构是否与范文模块D一致；关键段落句式是否与模块C对应句式在骨架层面吻合。
7. PDF 交叉验证：重要结果段落的论证推进是否与范文 PDF 原文的对应段落节奏一致（非字面对齐，而是一拍一拍的推进方式一致）；引用的文献结论是否已回原文核对。

## Output Expectations

1. `章节起草`：更新的 `section-brief` + 中文讨论稿 + 英文投稿稿。
2. `中转英 / 中转中 / 精修`：正文结果 + 2–3 句中文修改说明；若无需修改，应明确说明保留原文。
3. `逻辑核对`：只输出实质问题列表或"检测通过"。
4. `表图 note / caption`：中文版本与英文版本各一份，且信息完整。
5. 若任务属于写作层返修：同步回写对应 `section-brief`，并在需要时把修改轮次写入 `paper/{project-slug}/review/changelog.md`。

## Common Pitfalls

1. 把"润色"理解成大幅改写，导致原意走样。
2. 把连续论证拆成机械列表，破坏段落推进。
3. 为了去 AI 味而堆更生僻、更华丽的词。
4. 中英文版本不同步，导致两套口径。
5. 表图 note 只写聚类说明，遗漏样本、变量和估计口径。
6. 当修改触及数据/样本/方法时，未先切回对应 skill（`m2-sample-audit` 或 `m3-estimation`），而在写作 skill 中越界处理。
7. 不读 paper-lib 范文、凭"通用学术腔"起草中文稿——《管理世界》有明确的标题、引言与表格惯例，必须先解剖后动笔。
