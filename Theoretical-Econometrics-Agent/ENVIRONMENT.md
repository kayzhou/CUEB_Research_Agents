# ENVIRONMENT — 跨平台工具链与运行环境

> 本文件定义项目的环境契约、路径优先级和引擎路由。
> 从服务器迁移到本地的逐步安装说明见 `使用手册.md` 第二篇。
> 本框架直接支持 Windows PowerShell、macOS Terminal 和 Linux shell，不要求 WSL、容器或虚拟机。
> 本机已安装 Stata / MATLAB 时，除 MCP 外还可**本地直连**（终端批处理调用，零 MCP 配置），见根目录 **`本地化部署说明.md`**。

---

## 一、一键激活

Windows PowerShell（点调用，前面是“点 + 空格”）：

```powershell
. .\scripts\setup_env.ps1
```

macOS/Linux：

```bash
source scripts/setup_env.sh
```

两个脚本都自动推断仓库根目录、激活项目内 `.venv`、加入 R/TeX 路径，并检查核心 Python 包。
本机路径配置为 `config/local-tools.json`，从 `config/local-tools.example.json` 复制或由下列命令生成：

```bash
python scripts/configure_local.py
python scripts/check_environment.py --strict
```

路径解析优先级：

1. 当前终端环境变量；
2. `config/local-tools.json`；
3. 系统 `PATH` 与项目内 `.venv`；
4. `setup_env.sh` 仅保留当前服务器旧布局作为兼容回退。

可覆盖变量：

- `TEA_PYTHON_ENV`：虚拟环境根目录；
- `TEA_R_BIN`：包含 `Rscript` 的目录；
- `TEA_TEXLIVE_BIN`：包含 `latexmk/pdflatex` 的目录；
- `TEA_MATLAB_ROOT`：MATLAB 版本根目录（不含 `bin`）；
- `TEA_STATA_CLI`：Stata 可执行文件；
- `TEA_OCTAVE_CLI`、`TEA_PANDOC_CLI`：可选工具。

`config/local-tools.json`、项目 `.venv/` 与 `.cursor/mcp.json` 均在 `.gitignore` 中，不能跨机器复用。

---

## 二、工具清单与用途路由

### 1. Python（核心环境：数值验证 / Word / 框架脚本）

- 版本：Python 3.10 或 3.11；每台机器在项目根重新创建 `.venv`。
- 依赖入口：`requirements.txt`（维护直接依赖与兼容范围）；可复现安装使用 Python 3.10
  生成的 `requirements-lock.txt`（锁定直接及传递依赖）：
  `python -m pip install -r requirements-lock.txt`。更新入口依赖后须重新生成锁文件并在干净环境验证。
- 用途路由：
  - **理论推导的数值反例检查**（M4）→ numpy/scipy：对候选不等式、矩阵界、信息矩阵正定性做小规模数值试探（只做反例排查，不替代证明）。
  - **MATLAB 不可用时的模拟备胎**（M5）→ numpy + scipy.optimize 等价实现 DGP 与 QML。
  - **PDF/TXT 文献预处理**（M2）→ pypdf；扫描 PDF 仍需 OCR。
  - **LaTeX/Markdown → docx 导出**（M6/M7）→ python-docx / Pandoc，输出到 `projects/{slug}/exports/`。
  - **框架脚本**（`scripts/`：RAG 索引、LaTeX 检查、评审汇总、Skill 校验）。

### 2. R（空间计量交叉验证引擎）

- 版本：R 4.4+；调用方式 `R` / `Rscript`（激活脚本加入本机配置路径）。
- 用途路由：**用独立实现交叉验证 MATLAB/Python 的估计结果**——`spatialreg`（SAR/SDM ML 估计）、`splm`（空间面板）、`spdep`（空间权重矩阵）、`strucchange`（断点检验）。小样本下两套实现给出一致估计值，是发现代码 bug 最便宜的方式。
- R 可执行文件已安装不代表这些包已装；首次使用前运行 `Rscript scripts/install_r_packages.R`，以 `setup_env.sh` 自检结果为准。
- Windows/macOS 优先安装 CRAN 二进制包；Linux 源码安装 `sf` 前需系统库 `cmake/libudunits2/GDAL/GEOS/PROJ/SQLite`。完整命令见使用手册。
- R 空间包不可用时，空间估计交叉验证降级为 Python 独立实现；不能假装已完成 R 交叉验证。

### 3. TeX Live（论文编译）

- 版本：TeX Live 2026；macOS 使用同年 MacTeX。要求含 xelatex、latexmk、bibtex。
- 用途路由：M6/M7 编译 `projects/{slug}/paper/main.tex`。英文投稿稿用 `pdflatex`，中文讨论稿用 `xelatex` + ctex。
- 推荐编译命令：`latexmk -pdf main.tex`（自动跑 bibtex 与多轮交叉引用）。
- 编译后运行 `python scripts/check_latex_notation.py --tex projects/{slug}/paper/main.tex` 检查重复标签与未定义引用。

### 4. MATLAB（Monte Carlo 模拟主力，MCP 或本地直连）

理论计量的 Monte Carlo 惯例用 MATLAB。推荐 MathWorks **官方开源** MCP 服务器：

- 仓库：[matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server)（Go 二进制，跨平台，官方维护）
- 安装：从 Releases 下载对应平台二进制；macOS/Linux 执行 `chmod +x`；在 `.cursor/mcp.json` 注册。
- 参数使用 `--matlab-root=/path`，指向版本根目录且不含 `bin`；建议同时设置 `--initial-working-folder=项目根目录`。
- 需要本机已有授权且受该服务器当前版本支持的 MATLAB；具体版本以官方 README 为准。
- 分平台模板：`scripts/mcp/mcp.windows.json.example`、`mcp.macos.json.example`、`mcp.linux.json.example`。
- 不配置 MCP 时，也可**本地直连**：以 `{TEA_MATLAB_ROOT}/bin/matlab -batch` 批处理运行 .m 脚本（R2019a+），步骤见 `本地化部署说明.md` §4.2。

**本机无 MATLAB 时的降级链**（M5 模块自动路由）：

1. **GNU Octave**（开源，语法兼容大部分 MATLAB 代码）：`octave --eval "run('main_run_simulation.m')"`；代码避免用 MATLAB 专有工具箱函数即可两边通用。
2. **Python 等价实现**：numpy + scipy.optimize 重写 DGP 与 QML 目标函数；用 R 或第二套 Python 实现交叉验证。

### 5. Stata（辅助引擎，MCP 或本地直连）

理论计量论文偶尔需要 Stata 做实证应用示例（empirical illustration）或对照已有 xsmle/spxtregress 结果。
有 Stata 授权的机器推荐以下**开源、维护活跃**的 MCP 服务器（二选一）：

| 方案 | 仓库 | 适用场景 |
|------|------|---------|
| **MCP-for-Stata**（推荐） | [SepineTam/mcp-for-stata](https://github.com/SepineTam/mcp-for-stata) | Agent 驱动分析；安装 uv 后执行 `uvx stata-mcp install -c cursor`，再以 `uvx stata-mcp doctor` 验证 |
| **stata-mcp 扩展** | [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) | 在 VS Code / Cursor 内自己写并运行 .do 文件，需要编辑器内实时输出与图形查看 |

本机未安装 Stata 时，实证示例降级为 R（`splm`/`spatialreg`）或 Python。

不配置 MCP 时，也可**本地直连**：以 `TEA_STATA_CLI` 指向的可执行文件批处理运行 do 文件（Windows `/e do`、Unix `-b do`），步骤见 `本地化部署说明.md` §3.2。

### 6. MCP 客户端配置

Cursor 在项目根目录的 `.cursor/mcp.json` 中注册 MCP 服务器；该本机配置已被 gitignore。
复制 `scripts/mcp/` 下与操作系统对应的模板，只保留实际使用的服务器并替换全部占位路径。
修改后执行 `Developer: Reload Window`。Windows JSON 的反斜杠必须写作 `\\`。

---

## 三、引擎选择决策树（与 M5 模拟设计衔接）

```
Monte Carlo 模拟（M5）
  ├─ 本机有 MATLAB 且 MCP 已连接 → matlab-mcp：交互调试
  ├─ 本机有 MATLAB 且路径已登记 → matlab-local：终端 -batch
  ├─ 无 MATLAB 有 Octave → Octave 跑同一套 .m 代码（避免专有工具箱函数）
  └─ 都没有 → Python：numpy + scipy 等价实现
估计结果交叉验证（M5 收尾必做）
  ├─ 首选 R：spatialreg / splm 独立实现，小样本比对估计值
  └─ R 空间包不可用 → Python 第二套独立实现（必须记录降级）
理论推导数值反例检查（M4）
  └─ Python：numpy/scipy 小规模试探
实证应用示例（可选章节）
  ├─ 本机有 Stata 且 MCP 已连接 → stata-mcp：xsmle / spxtregress
  ├─ 本机有 Stata 且路径已登记 → stata-local：终端批处理
  └─ 无 Stata     → R：splm / spatialreg
论文编译（M6/M7）
  └─ TeX Live：latexmk -pdf（英文）/ xelatex（中文）；导出 docx 用 python-docx
```

M5 主引擎写入 `system/metadata.md` 的 `engine` 字段（`matlab-mcp` / `matlab-local` /
`octave` / `python`）；Stata 辅助路线写入 `stata_engine`（`stata-mcp` / `stata-local` /
`r` / `none`）。模拟脚本头部注明所用引擎与版本。

---

## 四、迁移与可复现环境契约

1. 不提交 `.venv/`、`config/local-tools.json`、`.cursor/mcp.json`。
2. 不在可提交代码中写本机绝对路径；程序输入输出相对 `TEA_REPO_ROOT` 或项目根解析。
3. 新机器只复制仓库与研究资产，然后重建 `.venv`、R 包、TeX 与 MCP。
4. 迁移验收命令：

```bash
python scripts/check_environment.py --strict
python scripts/validate_skills.py
```

5. 本机缺少 MATLAB/Stata 不构成框架阻塞；按决策树降级并在 metadata 记录。
6. TeX 版本与包集变化可能改变断行、字体或参考文献结果；迁移后必须重新编译并检查 PDF。
