# 程序层说明

## 运行顺序（严格按序执行）

```
code/config/config.do          ← 所有脚本的第一行都 include 此文件
    ↓
code/clean/                    ← 数据清洗：读 data/raw/ → 写 data/processed/
    ↓
code/build/                    ← 样本构建、变量构造：读 processed/ → 写 data/final/
    ↓
code/analysis/{project-slug}/         ← 主回归、识别策略、机制分析：读 data/final/
    ↓
code/output/{project-slug}/           ← 表格/图形生成：读分析结果 → 写 results/
```

调度入口预留为 `scripts/master_build.do` / `scripts/master_build.py`。当前两者尚未接入项目脚本：Python 版只做就绪检查（CI 可用 `--strict`），Stata 版的阶段调用是注释示例，不能视为端到端复现。

> 命名说明：`code/build/` 指数据流水线中的「样本构建」阶段（Gentzkow–Shapiro 惯例）；
> 仓库根目录的 `scripts/` 是流水线入口与辅助服务（MCP 等），两者职责不同。

## 关键约定

1. **路径禁止硬编码**：Stata 通过 `config/config.do` 中的全局变量 `$raw`、`$processed`、`$final`、`$results`、`$code`、`$paperlib` 访问；Python 通过 `config/config.py` 中的 `PATHS` 字典访问。
2. **日志强制开启**：每个 do 文件必须以 `log using "$logs/脚本名.log", replace` 开头。
3. **编号即顺序**：脚本文件名以两位数字开头（如 `01_`、`02_`），数字反映执行顺序。
4. **注释规范**：每个脚本顶部必须有"输入文件 - 输出文件 - 功能说明"三行注释。
5. **工具链**：R / TeX Live / Python 虚拟环境的路径与激活方式见根目录 `ENVIRONMENT.md`；Windows 跑脚本前点调用 `. .\scripts\setup_env.ps1`，macOS/Linux 执行 `source scripts/setup_env.sh`。

## 子目录说明

| 子目录 | 职责 |
|---|---|
| `config/` | 路径配置，不含任何分析逻辑 |
| `clean/` | 数据清洗和标准化 |
| `build/` | 样本筛选、变量构造、数据合并 |
| `analysis/{project-slug}/` | 按论文分包的估计脚本；仓库内的 `_template/` 只是示例槽位 |
| `output/{project-slug}/` | 表格和图形的最终生成脚本；仓库内的 `_template/` 只是示例槽位 |
| `utils/` | 共用宏、自定义函数、ado 文件、知识库索引工具 |
