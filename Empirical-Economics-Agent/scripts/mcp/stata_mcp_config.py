"""
Stata MCP 配置 —— 兼容共享模板。

首次克隆此工作流后：
1. 推荐使用 config/local-tools.json + scripts/setup_env.* 导出 EEA_STATA_EXE
2. 若沿用旧方式，复制此文件为 stata_mcp_config_local.py（已被 gitignore）
3. 将 STATA_EXE 改为本机 Stata CLI 的完整路径
4. 在 MCP 客户端配置中注册本服务器（示例见 scripts/mcp/mcp.json.example）

示例路径：
  Windows:   "C:/Program Files/Stata19/StataMP-64.exe"
  macOS:     "/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp"（批处理须用小写的命令行程序，非同名 GUI 程序）
  Linux:     "/usr/local/stata19/stata-mp"
"""

STATA_EXE = "C:/Program Files/Stata19/StataMP-64.exe"
