# Quick check for Moltcn agent status
Write-Host "🦞 Quick Moltcn Agent Status Check" -ForegroundColor Cyan

# Read credentials
$credPath = "$env:USERPROFILE\.config\moltcn\credentials.json"
if (Test-Path $credPath) {
    $credentials = Get-Content $credPath | ConvertFrom-Json
    Write-Host "Agent: $($credentials.agent_name)" -ForegroundColor Green
    
    $headers = @{
        "Authorization" = "Bearer $($credentials.api_key)"
    }
    
    try {
        $status = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
        Write-Host "Status: $($status.status)" -ForegroundColor Green
        Write-Host "Email verified: $($status.email_verified)" -ForegroundColor Green
        
        # Return status for heartbeat decision
        if ($status.status -eq "active") {
            Write-Host "✅ Agent is active and claimed!" -ForegroundColor Green
            exit 0  # Agent is claimed
        } else {
            Write-Host "❌ Agent is not yet claimed or active" -ForegroundColor Yellow
            exit 1  # Agent not claimed
        }
    } catch {
        Write-Host "Status check failed: $_" -ForegroundColor Red
        exit 1  # Failed to check
    }
} else {
    Write-Host "Credentials file not found" -ForegroundColor Red
    exit 1
}