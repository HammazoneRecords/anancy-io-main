# Pre-build validation script
# Run this before building Docker image

Write-Host "=== AnancyIO Docker Build Pre-Check ===" -ForegroundColor Cyan
Write-Host ""

# Check Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker is running: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running or not installed!" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Check Docker daemon
try {
    docker ps | Out-Null
    Write-Host "✓ Docker daemon is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Cannot connect to Docker daemon!" -ForegroundColor Red
    Write-Host "  Make sure Docker Desktop is fully started." -ForegroundColor Yellow
    exit 1
}

# Check available disk space
Write-Host ""
Write-Host "Checking disk space..." -ForegroundColor Yellow
$drive = (Get-Location).Drive.Name
$disk = Get-PSDrive $drive
$freeSpaceGB = [math]::Round($disk.Free / 1GB, 2)
Write-Host "  Free space on ${drive}: ${freeSpaceGB} GB" -ForegroundColor White

if ($freeSpaceGB -lt 15) {
    Write-Host "✗ Low disk space! Need at least 15GB free." -ForegroundColor Red
    Write-Host "  Current free space: ${freeSpaceGB} GB" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✓ Sufficient disk space available" -ForegroundColor Green
}

# Check available memory
Write-Host ""
Write-Host "Checking available memory..." -ForegroundColor Yellow
$totalRAM = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
Write-Host "  Total RAM: ${totalRAM} GB" -ForegroundColor White

if ($totalRAM -lt 8) {
    Write-Host "⚠ Warning: Less than 8GB RAM detected." -ForegroundColor Yellow
    Write-Host "  Build may be slow. Recommended: 8GB+ RAM" -ForegroundColor Yellow
} else {
    Write-Host "✓ Sufficient memory available" -ForegroundColor Green
}

# Check required files
Write-Host ""
Write-Host "Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "requirements.txt",
    "requirements2.txt",
    "run_ui.py",
    "Dockerfile.robust"
)

$allFilesPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file missing!" -ForegroundColor Red
        $allFilesPresent = $false
    }
}

if (-not $allFilesPresent) {
    Write-Host ""
    Write-Host "✗ Some required files are missing!" -ForegroundColor Red
    exit 1
}

# Check for existing containers
Write-Host ""
Write-Host "Checking for existing containers..." -ForegroundColor Yellow
$existingContainer = docker ps -a --filter "name=anancyio" --format "{{.Names}}"
if ($existingContainer) {
    Write-Host "  ⚠ Found existing container: $existingContainer" -ForegroundColor Yellow
    Write-Host "  Will be stopped and removed during build" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ No conflicting containers" -ForegroundColor Green
}

# Estimated build time
Write-Host ""
Write-Host "=== Pre-check Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Estimated build time: 15-25 minutes (first build)" -ForegroundColor Yellow
Write-Host "Subsequent builds: 2-5 minutes (with cache)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ready to build! Run:" -ForegroundColor Green
Write-Host "  docker-compose -f docker-compose.robust.yml up --build" -ForegroundColor White
Write-Host ""
Write-Host "Or to build in background:" -ForegroundColor Green
Write-Host "  docker-compose -f docker-compose.robust.yml up -d --build" -ForegroundColor White
Write-Host ""
