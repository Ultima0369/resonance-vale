# Simple heartbeat check
$API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"

Write-Host "Moltcn heartbeat check started..."
Write-Host ""

# Set headers
$headers = @{}
$headers.Add("Authorization", "Bearer $API_KEY")
$headers.Add("Content-Type", "application/json")

# 1. Check agent status
Write-Host "Checking agent status..."
try {
    $agentInfo = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agent/info" -Method Get -Headers $headers
    Write-Host "Agent status: OK"
    Write-Host "Name: $($agentInfo.name)"
    Write-Host "Status: $($agentInfo.status)"
    Write-Host "Email: $($agentInfo.email)"
    Write-Host "Email verified: $($agentInfo.email_verified)"
} catch {
    Write-Host "Failed to check agent status: $_"
}

Write-Host ""

# 2. Update state file
Write-Host "Updating state file..."
$statePath = "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json"
$now = Get-Date -Format "yyyy-MM-ddTHH:mm:ss+08:00"

# Read existing state
if (Test-Path $statePath) {
    $state = Get-Content $statePath | ConvertFrom-Json
} else {
    $state = @{
        lastChecks = @{
            moltcn = $null
            email = $null
            calendar = $null
            weather = $null
        }
        moltcn = @{
            agentName = "Xuanji_AI_Assistant"
            apiKey = $API_KEY
            status = "pending_claim"
            email = "3223648367@qq.com"
            emailVerified = $false
            lastCheck = $now
            nextCheck = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss+08:00")
        }
    }
}

# Update check time
$state.lastChecks.moltcn = $now
$state.moltcn.lastCheck = $now
$state.moltcn.nextCheck = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss+08:00")

# Save state
$state | ConvertTo-Json -Depth 10 | Set-Content $statePath -Encoding UTF8
Write-Host "State file updated"

Write-Host ""
Write-Host "Moltcn heartbeat check completed!"
Write-Host "Next check suggested: in 2-3 hours"