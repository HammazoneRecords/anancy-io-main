# Easy build and run script for AnancyIO
param(
    [switch]$Check,
    [switch]$Build,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Logs,
    [switch]$Clean,
    [switch]$Help
)

$ComposeFile = "docker-compose.robust.yml"

function Show-Help {
    Write-Host @"
AnancyIO Docker Helper Script

Usage: .\build.ps1 [options]

Options:
  -Check    Run pre-build validation checks
  -Build    Build the Docker image
  -Start    Start the container (builds if needed)
  -Stop     Stop and remove the container
  -Logs     Show container logs (follow mode)
  -Clean    Clean up Docker resources
  -Help     Show this help message

Examples:
  .\build.ps1 -Check              # Validate before building
  .\build.ps1 -Start              # Build and start
  .\build.ps1 -Logs               # View logs
  .\build.ps1 -Stop               # Stop container
  .\build.ps1 -Clean -Start       # Clean and rebuild

After starting, access at: http://localhost:50080
"@
}

function Invoke-PreCheck {
    Write-Host "`n=== Running Pre-Build Checks ===" -ForegroundColor Cyan
    if (Test-Path "check-docker.ps1") {
        & .\check-docker.ps1
    } else {
        Write-Host "Pre-check script not found, skipping..." -ForegroundColor Yellow
    }
}

function Invoke-Build {
    Write-Host "`n=== Building AnancyIO Docker Image ===" -ForegroundColor Cyan
    Write-Host "This will take 15-25 minutes on first build..." -ForegroundColor Yellow
    Write-Host ""
    docker-compose -f $ComposeFile build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Build completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Build failed!" -ForegroundColor Red
        Write-Host "Check DOCKER_TROUBLESHOOTING.md for solutions" -ForegroundColor Yellow
        exit 1
    }
}

function Invoke-Start {
    Write-Host "`n=== Starting AnancyIO ===" -ForegroundColor Cyan
    docker-compose -f $ComposeFile up -d --build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Container started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Access AnancyIO at: http://localhost:50080" -ForegroundColor Green
        Write-Host ""
        Write-Host "View logs with: .\build.ps1 -Logs" -ForegroundColor Yellow
        Write-Host "Stop with: .\build.ps1 -Stop" -ForegroundColor Yellow
    } else {
        Write-Host "`n✗ Failed to start container!" -ForegroundColor Red
        exit 1
    }
}

function Invoke-Stop {
    Write-Host "`n=== Stopping AnancyIO ===" -ForegroundColor Cyan
    docker-compose -f $ComposeFile down
    Write-Host "✓ Container stopped and removed" -ForegroundColor Green
}

function Invoke-Logs {
    Write-Host "`n=== AnancyIO Logs (Ctrl+C to exit) ===" -ForegroundColor Cyan
    docker-compose -f $ComposeFile logs -f
}

function Invoke-Clean {
    Write-Host "`n=== Cleaning Docker Resources ===" -ForegroundColor Cyan
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker-compose -f $ComposeFile down -v
    
    Write-Host "Removing AnancyIO images..." -ForegroundColor Yellow
    docker images | Select-String "anancy" | ForEach-Object {
        $imageId = ($_ -split '\s+')[2]
        docker rmi $imageId -f 2>$null
    }
    
    Write-Host "Pruning system..." -ForegroundColor Yellow
    docker system prune -f
    
    Write-Host "✓ Cleanup complete!" -ForegroundColor Green
}

# Main execution
if ($Help -or (!$Check -and !$Build -and !$Start -and !$Stop -and !$Logs -and !$Clean)) {
    Show-Help
    exit 0
}

if ($Clean) {
    Invoke-Clean
}

if ($Check) {
    Invoke-PreCheck
}

if ($Build) {
    Invoke-Build
}

if ($Start) {
    Invoke-Start
}

if ($Stop) {
    Invoke-Stop
}

if ($Logs) {
    Invoke-Logs
}
