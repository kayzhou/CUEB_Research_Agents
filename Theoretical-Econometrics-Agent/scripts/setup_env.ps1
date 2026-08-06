# setup_env.ps1 — Windows 原生 PowerShell 环境激活
# 用法（必须点调用以保留环境）：. .\scripts\setup_env.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$ConfigPath = if ($env:TEA_LOCAL_CONFIG) {
    $env:TEA_LOCAL_CONFIG
} else {
    Join-Path $RepoRoot "config\local-tools.json"
}

$env:TEA_REPO_ROOT = $RepoRoot
$env:TEA_LOCAL_CONFIG = $ConfigPath
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$RepoRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $RepoRoot
}

$Config = @{}
if (Test-Path $ConfigPath) {
    $Config = Get-Content -Raw -Encoding UTF8 $ConfigPath | ConvertFrom-Json
}

function Get-ConfiguredValue([string]$EnvironmentName, [string]$ConfigName) {
    $fromEnvironment = [Environment]::GetEnvironmentVariable($EnvironmentName)
    if ($fromEnvironment) { return $fromEnvironment }
    if ($Config.PSObject.Properties.Name -contains $ConfigName) {
        $value = $Config.$ConfigName
        if ($value) { return [Environment]::ExpandEnvironmentVariables($value) }
    }
    return ""
}

$PythonEnv = Get-ConfiguredValue "TEA_PYTHON_ENV" "python_env"
if (-not $PythonEnv) { $PythonEnv = Join-Path $RepoRoot ".venv" }
$ActivateScript = Join-Path $PythonEnv "Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    throw "Python 虚拟环境不存在：$PythonEnv。运行：py -3.10 -m venv .venv；然后安装 requirements.txt。"
}
$env:TEA_PYTHON_ENV = $PythonEnv
. $ActivateScript

$RBin = Get-ConfiguredValue "TEA_R_BIN" "r_bin"
$TexBin = Get-ConfiguredValue "TEA_TEXLIVE_BIN" "texlive_bin"
foreach ($Bin in @($RBin, $TexBin)) {
    if ($Bin -and (Test-Path $Bin)) {
        $env:PATH = "$Bin;$env:PATH"
    }
}
$env:TEA_R_BIN = $RBin
$env:TEA_TEXLIVE_BIN = $TexBin
$env:TEA_MATLAB_ROOT = Get-ConfiguredValue "TEA_MATLAB_ROOT" "matlab_root"
$env:TEA_STATA_CLI = Get-ConfiguredValue "TEA_STATA_CLI" "stata_cli"
$env:TEA_OCTAVE_CLI = Get-ConfiguredValue "TEA_OCTAVE_CLI" "octave_cli"
$env:TEA_PANDOC_CLI = Get-ConfiguredValue "TEA_PANDOC_CLI" "pandoc_cli"

Write-Host "── Theoretical-Econometrics-Agent 环境 ─────────────"
Write-Host "  Repo    : $RepoRoot"
if (Test-Path $ConfigPath) {
    Write-Host "  Config  : $ConfigPath"
} else {
    Write-Host "  Config  : 未创建（PATH 自动探测）"
}
Write-Host "  Python  : $(python --version 2>&1) [$PythonEnv]"
python -c "import numpy, pandas, scipy, statsmodels, linearmodels, matplotlib, seaborn, docx, pypdf, reportlab, yaml, mcp" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Python 依赖不完整：python -m pip install -r requirements.txt"
}
Write-Host "  Py deps : OK"

$Rscript = Get-Command Rscript -ErrorAction SilentlyContinue
if ($Rscript) {
    Write-Host "  R       : $(Rscript --version 2>&1)"
} else {
    Write-Warning "未找到 Rscript；M5 的 R 交叉验证不可用。"
}
$Latexmk = Get-Command latexmk -ErrorAction SilentlyContinue
$PdfLaTex = Get-Command pdflatex -ErrorAction SilentlyContinue
if ($Latexmk -and $PdfLaTex) {
    Write-Host "  TeX     : $($PdfLaTex.Source)"
} else {
    Write-Warning "未找到 latexmk/pdflatex；M6 无法编译论文。"
}
if ((Get-Command matlab -ErrorAction SilentlyContinue) -or $env:TEA_MATLAB_ROOT) {
    Write-Host "  MATLAB  : 已探测（MCP 配置见 ENVIRONMENT.md）"
} elseif ((Get-Command octave -ErrorAction SilentlyContinue) -or $env:TEA_OCTAVE_CLI) {
    Write-Host "  MATLAB  : 未探测；Octave 可作 M5 降级引擎"
} else {
    Write-Host "  MATLAB  : 未探测；M5 可用 Python 降级实现"
}
Write-Host "  Detail  : python scripts\check_environment.py --strict"
Write-Host "──────────────────────────────────────────────────"
