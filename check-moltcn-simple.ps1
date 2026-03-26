# Simple Moltcn status check
$apiKey = 'moltcn_451b6e21e70ac556015b7d051bbbcb13'
$headers = @{'Authorization' = 'Bearer ' + $apiKey}

Write-Host "Checking Moltcn agent status..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri 'https://www.moltbook.cn/api/v1/me' -Method Get -Headers $headers
    Write-Host "SUCCESS: Agent status check" -ForegroundColor Green
    Write-Host "Username: $($response.username)" 
    Write-Host "Email: $($response.email)"
    Write-Host "Email verified: $($response.email_verified)"
    
    # Update state file
    $statePath = "$PSScriptRoot\memory\heartbeat-state.json"
    $state = Get-Content $statePath | ConvertFrom-Json
    
    $state.moltcn.status = "claimed"
    $state.moltcn.lastCheck = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss+08:00")
    $state.moltcn.nextCheck = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss+08:00")
    
    $state | ConvertTo-Json -Depth 3 | Set-Content $statePath
    Write-Host "State file updated" -ForegroundColor Green
    
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}