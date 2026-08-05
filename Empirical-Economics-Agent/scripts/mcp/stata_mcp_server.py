"""
Stata MCP Server — 通过 MCP 协议在 AI 编码工具（Cursor / Claude Code 等）中运行 Stata 命令。

> 说明：这是仓库内置的最小实现（本机装有 Stata 时可用）。
> 更完整、维护更活跃的开源方案见根目录 ENVIRONMENT.md 的「Stata / MATLAB MCP」一节
> （推荐 SepineTam/mcp-for-stata 或 hanlulong/stata-mcp）。

Stata 可执行文件路径通过级联导入配置：
  1. 每台机器的本地覆盖：scripts/mcp/stata_mcp_config_local.py（gitignored）
  2. setup_env 导出的 EEA_STATA_EXE
  3. config/local-tools.json 的 stata_cli

首次克隆后：
  推荐先运行 scripts/configure_local.py 并激活环境；也可继续复制
  stata_mcp_config.py → stata_mcp_config_local.py 以兼容旧配置方式。

输出路径固定（Agent 无需搜索）：
  - 运行日志 → results/logs/
  - 表格     → results/tables/{project-slug}/
  - 图形     → results/figures/{project-slug}/
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Stata 可执行文件路径必须由本地配置提供；共享文件只是模板。
REPO_ROOT = Path(__file__).resolve().parents[2]
STATA_EXE = ""
try:
    from stata_mcp_config_local import STATA_EXE as _LOCAL_STATA_EXE  # type: ignore[import-not-found]
except ImportError:
    _LOCAL_STATA_EXE = ""
STATA_EXE = _LOCAL_STATA_EXE or os.environ.get("EEA_STATA_EXE", "")
if not STATA_EXE:
    local_tools = REPO_ROOT / "config" / "local-tools.json"
    if local_tools.is_file():
        try:
            configured = json.loads(local_tools.read_text(encoding="utf-8")).get(
                "stata_cli", ""
            )
            if isinstance(configured, str):
                STATA_EXE = os.path.expandvars(os.path.expanduser(configured))
        except (OSError, json.JSONDecodeError):
            STATA_EXE = ""
RESULT_LOGS = REPO_ROOT / "results" / "logs"

mcp = FastMCP("stata", instructions="Execute Stata code and return results.")


def stata_batch_command(do_file: Path) -> list[str]:
    """Return platform-appropriate Stata batch arguments."""
    if sys.platform == "win32":
        return [STATA_EXE, "/e", "do", do_file.as_posix()]
    return [STATA_EXE, "-b", "do", do_file.as_posix()]


def run_stata_code(code: str, title: str = "stata_run") -> str:
    """Run Stata code in batch mode and return the log output."""
    RESULT_LOGS.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="stata_mcp_") as tmp_dir:
        do_file = Path(tmp_dir) / f"{title}.do"
        log_file = RESULT_LOGS / f"{title}_mcp.log"

        do_content = f"""clear all
set more off
capture log close
log using "{log_file.as_posix()}", replace text

{code}

log close
exit, STATA
"""
        do_file.write_text(do_content, encoding="utf-8")

        try:
            result = subprocess.run(
                stata_batch_command(do_file),
                capture_output=True,
                text=True,
                timeout=180,
                cwd=REPO_ROOT,
            )
        except subprocess.TimeoutExpired:
            return "Error: Stata execution timed out (180s)"
        except FileNotFoundError:
            return f"Error: Stata executable not found at {STATA_EXE}"

        if log_file.exists():
            raw = log_file.read_bytes()
            # Stata log uses system locale (GBK on Chinese Windows)
            for enc in ("utf-8", "gbk", "gb18030"):
                try:
                    log_text = raw.decode(enc)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            else:
                log_text = raw.decode("utf-8", errors="replace")
            lines = log_text.splitlines()
            if len(lines) > 500:
                log_text = (
                    "\n".join(lines[:300])
                    + "\n\n... [output truncated at 300 lines] ...\n\n"
                    + "\n".join(lines[-200:])
                )
            return log_text

        # Fallback: return stdout/stderr
        out = result.stdout or ""
        err = result.stderr or ""
        return f"Log not found.\nStdout:\n{out[:3000]}\nStderr:\n{err[:2000]}"


@mcp.tool()
def run_stata(code: str, title: str = "stata_run") -> str:
    """Execute Stata code in batch mode and return the full log output.

    Args:
        code: Stata code to execute (e.g., 'sysuse auto, clear\\ndescribe')
        title: Name prefix for the log file (optional)
    """
    return run_stata_code(code, title)

async def main() -> None:
    if not STATA_EXE:
        print("错误：未配置 Stata 可执行文件路径。", file=sys.stderr)
        print(
            "请运行 scripts/configure_local.py 并 source scripts/setup_env.sh，"
            "或创建 stata_mcp_config_local.py。",
            file=sys.stderr,
        )
        raise SystemExit(1)
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
