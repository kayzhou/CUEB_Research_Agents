# paper/ — 论文项目工作区

`paper/` 按“每篇论文一个项目目录”组织。每个项目目录使用能表达研究主题的 `{project-slug}`，集中保存从立项到返修的全部研究文档；数据、代码和生成结果分别保存在 `data/`、`code/`、`results/`，不混入此处。

## 命名规则

- 使用小写英文 kebab-case：`green-credit-firm-investment`。
- 不使用 `paper01`、`paper02` 等无语义流水号。
- 名称应简短、稳定，并能区分不同论文。
- 项目进入 M2 后不应随意改名。

当前项目：

```text
a-share-multifactor-pricing
```

同一 slug 必须同步用于：

```text
paper/{project-slug}/
code/analysis/{project-slug}/
code/output/{project-slug}/
results/tables/{project-slug}/
results/figures/{project-slug}/
system/metadata.md 的 project 字段
```

## 项目目录职责

推荐结构：

```text
paper/{project-slug}/
├── paper-screen.md              # M1：选题筛查
├── paper-brief.md               # M1：锁定研究设计
├── stylized-facts.md            # M3：典型事实
├── empirical-output-checklist.md# M3：表图与估计清单
├── estimation-risk-memo.md      # M3：估计前风险自检（Researcher）
├── evidence-chain.md            # M4：论文证据链
├── section-briefs/              # M4：章节任务简报
├── sections_cn/                 # M4：中文讨论稿
├── sections/                    # M4：英文投稿稿（LaTeX 真源）
├── discussions/                 # PROPOSAL / ATTACK / RESPONSE / FINAL-VERDICT
├── review/                      # 贡献/样本/逻辑/质量审查、评审与返修
└── style-anatomy/               # M4：目标期刊范文解剖笔记
```

并非所有文件都要在 M1 创建；由各模块按需生成。

## 规范产出路径（单一真源）

| 产出 | 规范路径 |
|------|----------|
| 贡献审计 | `paper/{project-slug}/review/contribution-audit-v1.md` |
| 样本侦查报告 | `paper/{project-slug}/review/sample-audit-report.md` |
| 估计风险备忘 | `paper/{project-slug}/estimation-risk-memo.md` |
| 提案 / 攻击 / 回应 | `paper/{project-slug}/discussions/PROPOSAL-001.md`、`ATTACK-001.md`、`RESPONSE-001.md` |
| 终判 | `paper/{project-slug}/discussions/FINAL-VERDICT-001.md` |
| 7R / 7Q | `paper/{project-slug}/review/logic-review-v1.md`、`quality-assessment-v1.md` |
| Claim 审计 | `paper/{project-slug}/review/claim-audit-v1.md`（Referee 只给建议） |
| 模拟评审 | `paper/{project-slug}/review/simulated-peer-review.md` |
| 真实意见摄入 | `paper/{project-slug}/review/real-expert-intake.md` |
| 回应信 / 修改日志 | `paper/{project-slug}/review/response-letter.md`、`changelog.md` |

版本化报告从 `v1` 开始递增，不覆盖旧版本。

## exports/

`paper/exports/` 是临时 Word/PDF 交换区，用于合作者批注。这里的文件不是论文真源，批注确认后必须同步回对应项目的 `sections/`。
