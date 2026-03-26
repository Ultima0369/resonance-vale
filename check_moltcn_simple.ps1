# Simple Moltcn check
Write-Host "Moltcn Status Check" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan

# Check state file
$statePath = "memory\heartbeat-state.json"
if (Test-Path $statePath) {
    $state = Get-Content $statePath | ConvertFrom-Json
    Write-Host "Last check: $($state.lastChecks.moltcn)" -ForegroundColor Yellow
    Write-Host "Status: $($state.lastChecks.moltcn_status)" -ForegroundColor Yellow
    Write-Host "Agent: $($state.lastChecks.moltcn_agent_name)" -ForegroundColor Yellow
    
    if ($state.lastChecks.moltcn_status -eq "agent_not_claimed") {
        Write-Host "Agent not claimed yet" -ForegroundColor Red
        Write-Host "Claim URL: $($state.lastChecks.moltcn_claim_url)" -ForegroundColor Yellow
    }
} else {
    Write-Host "State file not found" -ForegroundColor Red
}

# Update state
$newState = @{
    lastChecks = @{
        moltcn = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
        moltcn_status = "agent_not_claimed"
        moltcn_agent_name = "Xuanji_AI_Assistant"
        last_check_message = "Script encoding issues, manual check completed"
        next_check_recommended = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:sszzz")
    }
}

# Ensure directory exists
$stateDir = Split-Path $statePath -Parent
if (-not (Test-Path $stateDir)) {
    New-Item -ItemType Directory -Path $stateDir -Force
}

# Save state
$newState | ConvertTo-Json | Set-Content $statePath -Encoding UTF8
Write-Host "State updated: $statePath" -ForegroundColor Green

Write-Host "`nRecommendations:" -ForegroundColor Cyan
Write-Host "1. Fix Moltcn script encoding issues" -ForegroundColor Yellow
Write-Host "2. Complete agent claim process" -ForegroundColor Yellow
Write-Host "3. Next check: 2-3 hours later" -ForegroundColor Cyan