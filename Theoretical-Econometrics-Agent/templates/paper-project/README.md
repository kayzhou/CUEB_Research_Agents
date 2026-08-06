# 论文工作区 — {project-slug}

> 本目录由 `python scripts/init_project.py --name {slug} --output projects` 从 `templates/paper-project/` 生成。
> 模块流程与卡点见仓库根 `ORCHESTRATOR.md`；当前状态登记在 `system/metadata.md`。
>
> **模板边界**：当前配置、MATLAB 与 LaTeX 骨架以“空间面板 + 单一未知时间断点”为默认起点，
> 不是通用模型生成器。研究其他模型时，必须在 Gate 1 前替换模型方程、参数、假设、DGP、
> 估计代码和论文占位内容；中性流程示例见 `examples/generic-qml-workflow/`。

## 目录约定

```
config/       模型设定 + 模拟设计（M1 / M5 的输入契约）
literature/   library/（原始文献，PDF 配 .txt）+ index/（RAG 索引）+ literature_matrix.csv（M2）
estimation/   QML 估计方案文档（M3）
proofs/       notation_registry.md + assumptions.md + theorem_map.md + proof_*.md（M4）
matlab/       DGP / 估计 / 汇总代码（M5；Octave 兼容）
results/      raw/（每次重复的原始估计）→ tables/ + figures/（脚本生成）
paper/        main.tex + sections/ + appendix/ + refs.bib（M6）
reviews/      评审报告 + revision_log.md（M7）
exports/      docx 导出（给导师/合作者批注）
```

`paper/` 只随模板复制 LaTeX/BibTeX 源文件；PDF、`.bbl`、`.aux`、`.log` 等编译产物
须在本机按需再生，`init_project.py` 会主动忽略这些文件。

## 推荐顺序

1. 填 `config/model_specification.yaml`（M1），冻结模型后再动别的。
2. 核心文献放 `literature/library/`，建索引出文献矩阵（M2）。
3. 写 `estimation/qml_estimation_plan.md`（M3）。
4. 填 `proofs/`：假设 → 定理地图 → 证明蓝图（M4）。
5. 校 `config/simulation_design.yaml`，跑 smoke → 特例 → final（M5）。
6. 组稿编译 `paper/main.tex`（M6）。
7. 五视角评审 + 返修 + 终检（M7），记录进 `reviews/revision_log.md`。
