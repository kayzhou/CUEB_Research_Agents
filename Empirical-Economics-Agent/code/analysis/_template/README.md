# _template 示例分析脚本骨架

本目录展示 `{project-slug}` 分析子目录应如何组织；`_template` 在模板仓库中只是预留槽位和示例接口，不代表真实项目已启动。

建议命名：
- `01_portfolio_sort.py` / `01_baseline_regression.do`
- `02_fmb.py` / `02_event_study.do`
- `03_spanning_test.py` / `03_heterogeneity.do`
- `04_mechanism.py` / `04_mechanism.do`

要求：
1. 第一行加载路径配置：Stata `include ../../config/config.do`；Python `from code.config.config import PATHS`。
2. 顶部写明输入、输出和识别/定价目的。
3. 所有正式结果必须可由 `scripts/master_build.do` 或 `scripts/master_build.py` 统一调度。
