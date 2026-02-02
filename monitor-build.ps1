# Monitor Docker build progress
# Usage: .\monitor-build.ps1

Write-Host "=== Docker Build Monitor ===" -ForegroundColor Cyan
Write-Host ""

$containerName = "anancyio-local"

while ($true) {
    Clear-Host
    Write-Host "=== Docker Build Monitor ===" -ForegroundColor Cyan
    Write-Host "Time: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
    Write-Host ""
    
    # Check if building
    $building = docker ps -a --filter "name=buildx" --format "{{.Names}}" 2>$null
    if ($building) {
        Write-Host "⚙️ Building..." -ForegroundColor Yellow
    }
    
    # Check container status
    $container = docker ps -a --filter "name=$containerName" --format "{{.Names}}\t{{.Status}}" 2>$null
    if ($container) {
        $status = $container -split "`t"
        Write-Host "Container: $($status[0])" -ForegroundColor White
        Write-Host "Status: $($status[1])" -ForegroundColor $(if ($status[1] -match "Up") { "Green" } else { "Yellow" })
    } else {
        Write-Host "Container: Not created yet" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "--- Recent Logs ---" -ForegroundColor Cyan
    docker logs $containerName --tail=10 2>&1 | ForEach-Object {
        if ($_ -match "error|Error|ERROR") {
            Write-Host $_ -ForegroundColor Red
        } elseif ($_ -match "warning|Warning") {
            Write-Host $_ -ForegroundColor Yellow
        } else {
            Write-Host $_
        }
    }
    
    Write-Host ""
    Write-Host "Press Ctrl+C to exit | Refreshing every 5 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}
