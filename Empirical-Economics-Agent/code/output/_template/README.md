# _template 示例输出脚本骨架

本目录展示 `{project-slug}` 输出子目录应如何组织；`_template` 在模板仓库中只是预留槽位和示例接口，不代表真实项目已启动。

建议命名：
- `01_tables_main.do` / `.py`
- `02_tables_robustness.do` / `.py`
- `03_figures_main.do` / `.py`

要求：
1. 输出文件统一写入对应项目编号的结果目录，例如 `results/tables/{project-slug}/` 和 `results/figures/{project-slug}/`。
2. 结果文件只允许由本目录脚本生成，不允许手工修改。
3. LaTeX 正文通过 `\input{}` 或 `\includegraphics{}` 引用这些生成物。
