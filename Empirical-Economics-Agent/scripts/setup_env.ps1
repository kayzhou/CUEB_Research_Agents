# setup_env.ps1 — Windows 原生 PowerShell 环境激活
# 用法（必须点调用以保留环境）：. .\scripts\setup_env.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$ConfigPath = if ($env:EEA_LOCAL_CONFIG) {
    $env:EEA_LOCAL_CONFIG
} else {
    Join-Path $RepoRoot "config\local-tools.json"
}

$env:EEA_REPO_ROOT = $RepoRoot
$env:EEA_LOCAL_CONFIG = $ConfigPath
$env:EEA_TOOLS_ROOT = if ($env:EEA_TOOLS_ROOT) {
    $env:EEA_TOOLS_ROOT
} else {
    Join-Path (Split-Path -Parent $RepoRoot) "tools"
}
$env:PROJECT_SLUG = if ($env:PROJECT_SLUG) {
    $env:PROJECT_SLUG
} else {
    "a-share-multifactor-pricing"
}
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$RepoRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $RepoRoot
}

$Config = [pscustomobject]@{}
if (Test-Path $ConfigPath) {
    $Config = Get-Content -Raw -Encoding UTF8 $ConfigPath | ConvertFrom-Json
    $RequiredKeys = @(
        "python_env",
        "r_bin",
        "texlive_bin",
        "matlab_root",
        "stata_cli"
    )
    $AllowedKeys = $RequiredKeys + @('$schema', '$comment')
    foreach ($Key in $RequiredKeys) {
        if ($Config.PSObject.Properties.Name -notcontains $Key) {
            throw "本机工具配置缺少字段 '$Key'：$ConfigPath"
        }
    }
    foreach ($Key in $Config.PSObject.Properties.Name) {
        if ($AllowedKeys -notcontains $Key) {
            throw "本机工具配置含未知字段 '$Key'：$ConfigPath"
        }
        if ($Config.$Key -isnot [string]) {
            throw "本机工具配置字段 '$Key' 必须是字符串：$ConfigPath"
        }
    }
}

function Get-ConfiguredValue([string]$EnvironmentName, [string]$ConfigName) {
    $FromEnvironment = [Environment]::GetEnvironmentVariable($EnvironmentName)
    if ($FromEnvironment) {
        return [Environment]::ExpandEnvironmentVariables($FromEnvironment)
    }
    if ($Config.PSObject.Properties.Name -contains $ConfigName) {
        $Value = $Config.$ConfigName
        if ($Value) {
            return [Environment]::ExpandEnvironmentVariables($Value)
        }
    }
    return ""
}

# Python：Windows 默认使用项目内 .venv。
$PythonEnv = Get-ConfiguredValue "EEA_PYTHON_ENV" "python_env"
if (-not $PythonEnv) {
    $PythonEnv = Join-Path $RepoRoot ".venv"
}
$ActivateScript = Join-Path $PythonEnv "Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    throw "Python 虚拟环境不存在：$PythonEnv。运行：py -3.10 -m venv .venv；然后安装 requirements.txt。"
}
$env:EEA_PYTHON_ENV = $PythonEnv
. $ActivateScript

# R 与 TeX：显式配置优先；留空时沿用系统 PATH。
$RBin = Get-ConfiguredValue "EEA_R_BIN" "r_bin"
if ($RBin -and (Test-Path $RBin)) {
    $env:PATH = "$RBin;$env:PATH"
}
$Rscript = Get-Command Rscript -ErrorAction SilentlyContinue
if (-not $Rscript) {
    throw "Rscript 未找到；在 config\local-tools.json 填写 r_bin。"
}
if (-not $RBin) {
    $RBin = Split-Path -Parent $Rscript.Source
}
$env:EEA_R_BIN = $RBin

$TexBin = Get-ConfiguredValue "EEA_TEXLIVE_BIN" "texlive_bin"
if ($TexBin -and (Test-Path $TexBin)) {
    $env:PATH = "$TexBin;$env:PATH"
}
$PdfLaTex = Get-Command pdflatex -ErrorAction SilentlyContinue
if (-not $PdfLaTex) {
    throw "pdflatex 未找到；在 config\local-tools.json 填写 texlive_bin。"
}
if (-not $TexBin) {
    $TexBin = Split-Path -Parent $PdfLaTex.Source
}
$env:EEA_TEXLIVE_BIN = $TexBin

# Stata：local-tools 的 stata_cli 统一映射到 EEA_STATA_EXE。
$StataExe = Get-ConfiguredValue "EEA_STATA_EXE" "stata_cli"
if (-not $StataExe) {
    foreach ($Name in @(
        "StataMP-64.exe",
        "StataSE-64.exe",
        "StataBE-64.exe",
        "Stata-64.exe"
    )) {
        $Candidate = Get-Command $Name -ErrorAction SilentlyContinue
        if ($Candidate) {
            $StataExe = $Candidate.Source
            break
        }
    }
}
$env:EEA_STATA_EXE = $StataExe

# MATLAB：配置保存版本根目录，激活时导出可执行文件路径。
$MatlabRoot = Get-ConfiguredValue "EEA_MATLAB_ROOT" "matlab_root"
$MatlabExe = [Environment]::GetEnvironmentVariable("EEA_MATLAB_EXE")
if (-not $MatlabExe -and $MatlabRoot) {
    $Candidate = Join-Path $MatlabRoot "bin\matlab.exe"
    if (Test-Path $Candidate) {
        $MatlabExe = $Candidate
    }
}
if (-not $MatlabExe) {
    $Candidate = Get-Command matlab -ErrorAction SilentlyContinue
    if ($Candidate) {
        $MatlabExe = $Candidate.Source
        if (-not $MatlabRoot) {
            $MatlabRoot = Split-Path -Parent (Split-Path -Parent $MatlabExe)
        }
    }
}
$env:EEA_MATLAB_ROOT = $MatlabRoot
$env:EEA_MATLAB_EXE = $MatlabExe

Write-Host "── Empirical-Economics-Agent 环境 ────────────────"
Write-Host "  Repo    : $RepoRoot"
if (Test-Path $ConfigPath) {
    Write-Host "  Config  : $ConfigPath"
} else {
    Write-Host "  Config  : 未创建（自动探测）"
}
Write-Host "  Python  : $(python --version 2>&1) [$PythonEnv]"
python -c "import numpy, pandas, scipy, statsmodels, linearmodels, sklearn, pyarrow, matplotlib, seaborn, docx, reportlab, lxml, yaml, requests, mcp" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Python 核心依赖不完整：python -m pip install -r requirements.txt"
}
Write-Host "  Py deps : OK"
Write-Host "  R       : $(Rscript --version 2>&1)"
Write-Host "  TeX     : $($PdfLaTex.Source)"
Rscript -e 'p <- c("fixest","did","rdrobust","eventstudyr"); m <- p[!vapply(p, requireNamespace, logical(1), quietly=TRUE)]; cat("  R pkgs  :", if(length(m)) paste("未安装", paste(m, collapse=", ")) else "OK", "\n")'
Write-Host "  Stata   : $(if ($StataExe) { $StataExe } else { '未配置（可使用 R 降级）' })"
Write-Host "  MATLAB  : $(if ($MatlabExe) { $MatlabExe } else { '未配置（可使用 Python 降级）' })"
Write-Host "──────────────────────────────────────────────────"
