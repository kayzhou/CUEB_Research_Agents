# ENVIRONMENT — 跨平台工具链与运行环境

> 本文件定义本机路径、激活方式和引擎路由。Windows/macOS 原生迁移流程见 **`使用手册.md` 第 11 章**，不要求 WSL、容器或虚拟机。
> 本机已安装 Stata / MATLAB 时，除 MCP 外还可**本地直连**（终端批处理调用，零 MCP 配置），见根目录 **`本地化部署说明.md`**。

---

## 一、本机配置与一键激活

Windows PowerShell（必须点调用，前面是“点 + 空格”）：

```powershell
. .\scripts\setup_env.ps1
```

macOS/Linux：

```bash
source scripts/setup_env.sh
```

两个脚本都自动推断仓库根目录、激活 Python 环境、加入 R/TeX 路径，并导出 Stata/MATLAB 本地直连变量。首次部署先创建 `.venv` 并安装依赖，再生成本机路径配置：

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python scripts/configure_local.py
```

也可复制 `config/local-tools.example.json` 为 `config/local-tools.json` 后手工填写。该本机文件已被 gitignore，不得提交或跨机器复用。路径解析优先级为：

1. 当前终端的 `EEA_*` 环境变量；
2. `config/local-tools.json`；
3. 项目 `.venv` 与系统 `PATH`；
4. `setup_env.sh` 的既有 Linux 服务器布局兼容回退（仓库同级 `tools/py_env`、`tools/R` 与系统 TeX Live）。

主要变量：

- `EEA_PYTHON_ENV`：Python 虚拟环境根目录；
- `EEA_R_BIN`：包含 `Rscript` 的目录；
- `EEA_TEXLIVE_BIN`：包含 `pdflatex` 的目录；
- `EEA_STATA_EXE`：Stata CLI 可执行文件；
- `EEA_MATLAB_ROOT`：MATLAB 版本根目录（不含 `bin`）；
- `EEA_MATLAB_EXE`：由激活脚本从 `matlab_root` 推导的 MATLAB 可执行文件；
- `PROJECT_SLUG`：默认 `a-share-multifactor-pricing`。

核心 Python、R 或 TeX 路径缺失时激活失败；Stata/MATLAB 是可选商业工具，缺失时按本文决策树降级。

---

## 二、工具清单

### 1. Python（主力引擎：资产定价 / 数据处理 / Word 导出）

```bash
python -m pip install -r requirements.txt
```

- 版本：Python 3.10
- 依赖安装入口：`requirements.txt`。包括 `statsmodels`、`linearmodels`、`pyarrow`、`requests` 和 `mcp`；发布锁文件由发布流程统一生成，不在环境脚本中临时制作。
- 用途路由：
  - 资产定价估计（M3，Portfolio Sort / FMB）→ pandas + scipy/statsmodels
  - 图形生成（M3）→ matplotlib/seaborn，输出到 `results/figures/`
  - LaTeX → docx 导出（M4/M5）→ python-docx，输出到 `paper/exports/`
  - 知识库索引（paper-lib）→ `code/utils/paperlib_index.py`

### 2. R（补充引擎：csdid/rdrobust 等前沿计量包的替代实现）

```bash
Rscript scripts/install_r_packages.R   # 首次使用 R 因果推断分支时运行
```

- 版本：R 4.4.1；调用方式 `R` / `Rscript`。
- 用途路由：Stata 不可用时的因果推断替代引擎——`fixest`（高维固定效应）、`did`（Callaway–Sant'Anna）、`rdrobust`、`eventstudyr`。R 可执行文件已安装不代表这些包已安装；以 `setup_env.sh` 自检结果为准。

### 3. TeX Live（论文编译）

- 版本：TeX Live 2026（pdfTeX 1.40.29）。
- 用途路由：M4/M5 编译 `paper/{project-slug}/sections/` 的英文投稿稿与中文讨论稿（中文用 `xelatex` + ctex）。表格 `.tex` 片段由脚本生成后 `\input{}` 引用，正文不手写数字。

### 4. Stata（因果推断主力，通过 MCP 接入）

本机未安装 Stata 时，因果推断任务降级为 R 引擎（见上）。有 Stata 授权的机器推荐以下**开源、维护活跃**的 MCP 服务器（二选一）：

| 方案 | 仓库 | 适用场景 |
|------|------|---------|
| **MCP-for-Stata**（推荐） | [SepineTam/mcp-for-stata](https://github.com/SepineTam/mcp-for-stata) | Agent 驱动的全自动分析；`uvx stata-mcp install --all` 一键接入 Cursor / Claude Code；注意使用 ≥ v1.17.3（修复命令注入漏洞） |
| **stata-mcp 扩展** | [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) | 在 VS Code / Cursor 内自己写并运行 .do 文件，需要编辑器内实时输出与图形查看 |

仓库还内置一个最小实现 `scripts/mcp/stata_mcp_server.py`（`mcp` 已列入 requirements）。它优先读取兼容文件 `stata_mcp_config_local.py`，否则使用激活脚本导出的 `EEA_STATA_EXE`；服务器会按平台选择 Windows `/e do` 或 Unix `-b do`。

不想配置 MCP 时，也可**本地直连**：从仓库根以批处理方式直接调用本机 Stata（Windows `/e do`、Unix `-b do`），步骤见 `本地化部署说明.md` §3.2。

### 5. MATLAB（结构估计 / 数值方法，通过 MCP 接入）

推荐 MathWorks **官方开源** MCP 服务器：

- 仓库：[matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server)（Go 二进制，跨平台，官方维护）
- 安装：从 Releases 下载对应平台二进制；注册时设置 `--matlab-root=版本根目录` 与 `--initial-working-folder=仓库根目录`。
- 需要本机已有授权且受该服务器当前版本支持的 MATLAB；具体版本以官方 README 为准。
- macOS 先用 `uname -m` 区分 Apple Silicon (`arm64`) 与 Intel (`x86_64`)，下载匹配架构的二进制。执行 `chmod +x`；若 Gatekeeper 隔离下载文件，在确认来源后从“系统设置 → 隐私与安全性”放行，或执行 `xattr -d com.apple.quarantine /path/to/matlab-mcp-server`。
- 不想配置 MCP 时，也可**本地直连**：从仓库根用 `matlab -batch` 运行 .m 脚本（R2019a+），步骤见 `本地化部署说明.md` §4.2。

### 6. MCP 客户端配置

Cursor 在项目根目录的 `.cursor/mcp.json` 中注册 MCP 服务器；该本机配置被 gitignore。优先复制对应平台模板：

- `scripts/mcp/mcp.windows.json.example`
- `scripts/mcp/mcp.macos.json.example`
- `scripts/mcp/mcp.linux.json.example`

通用兼容模板仍保留为 `scripts/mcp/mcp.json.example`。只保留实际使用的服务器并替换全部占位路径。Stata MCP 必须同时设置 `STATA_CLI` 与 `STATA_MCP__CWD`；MATLAB MCP 必须设置初始工作目录。保存后重载 Cursor。

---

## 三、引擎选择决策树（与 M1 范式决策衔接）

```
因果推断（DID/IV/RD/事件研究）
  ├─ 本机有 Stata → Stata（经 MCP 或本地直连）：reghdfe / ivreghdfe / csdid / rdrobust / eventdd
  └─ 无 Stata     → R：fixest / did / rdrobust / eventstudyr
资产定价（Portfolio Sort/FMB/GRS）
  └─ Python：pandas + statsmodels/linearmodels
结构估计 / 数值优化
  └─ MATLAB（经 MCP 或本地直连）或 Python(scipy)
论文编译
  └─ TeX Live：pdflatex（英文）/ xelatex（中文）
```

引擎选定后写入 `system/metadata.md` 的 `engine` 字段；估计脚本头部注明所用引擎与包版本。

---

## 四、迁移与发布环境契约

1. 不提交 `.venv/`、`venv/`、`config/local-tools.json` 或 `.cursor/mcp.json`。
2. 不在共享代码中写本机绝对路径；程序输入输出相对 `REPO_ROOT` 解析。
3. 新机器只迁移仓库与有权使用的研究资产，然后重建 Python、R、TeX 与可选 MCP。
4. `requirements.txt` 始终是依赖安装入口；发布锁文件由维护者的统一发布流程处理。
5. 本机缺少 Stata/MATLAB 不构成框架失败；按决策树降级并在 metadata 中记录。
6. Windows/macOS 的商业软件与 MCP 命令必须在相应真机完成人工验收；当前服务器校验不能替代该步骤。
