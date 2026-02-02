# Run AnancyIO (no Docker) using Conda
# Usage: .\run-web.ps1

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$EnvName = "anancyio"

Write-Host "=== AnancyIO (Conda) ===" -ForegroundColor Cyan
Set-Location $ProjectRoot

# Check conda
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Conda not found. Install Miniconda or Anaconda, then run this script again." -ForegroundColor Red
    exit 1
}
Write-Host "Using Conda" -ForegroundColor Green

# Create env if missing (Python 3.12 for compatibility with kokoro etc.)
$envExists = conda env list | Select-String -Pattern "^\s*$EnvName\s" -Quiet
if (-not $envExists) {
    Write-Host "Creating Conda env '$EnvName' with Python 3.12..." -ForegroundColor Yellow
    conda create -n $EnvName python=3.12 -y
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

# Check dependencies and install if needed (conda run avoids activate issues in PowerShell)
Write-Host "Checking dependencies..." -ForegroundColor Yellow
conda run -n $EnvName python -c "import flask" 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies (first time may take several minutes)..." -ForegroundColor Yellow
    conda run -n $EnvName pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "pip install failed. Check errors above." -ForegroundColor Red
        exit 1
    }
}

# Port from .env
$port = 5000
if (Test-Path (Join-Path $ProjectRoot ".env")) {
    $line = Get-Content (Join-Path $ProjectRoot ".env") | Where-Object { $_ -match "^\s*WEB_UI_PORT\s*=\s*(\d+)" } | Select-Object -First 1
    if ($line -match "=\s*(\d+)") { $port = [int]$Matches[1] }
}

Write-Host "Starting at http://localhost:$port ..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor Gray
conda run -n $EnvName --no-capture-output python run_ui.py
