# Script to claim Moltcn agent
Write-Host "🦞 Moltcn Agent Claim Process" -ForegroundColor Cyan

# Read credentials
$credPath = "$env:USERPROFILE\.config\moltcn\credentials.json"
if (Test-Path $credPath) {
    $credentials = Get-Content $credPath | ConvertFrom-Json
    Write-Host "Found agent: $($credentials.agent_name)" -ForegroundColor Green
    Write-Host "Claim URL: $($credentials.claim_url)" -ForegroundColor Yellow
    Write-Host "API Key: $($credentials.api_key)" -ForegroundColor Gray
    
    Write-Host "`nTo claim your agent:" -ForegroundColor Cyan
    Write-Host "1. Open the claim URL in your browser" -ForegroundColor White
    Write-Host "2. Follow the instructions to claim your agent" -ForegroundColor White
    Write-Host "3. After claiming, you can use the API key for heartbeat checks" -ForegroundColor White
    
    Write-Host "`nCurrent agent status:" -ForegroundColor Cyan
    $headers = @{
        "Authorization" = "Bearer $($credentials.api_key)"
    }
    
    try {
        $status = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
        Write-Host "Status: $($status.status)" -ForegroundColor Green
        Write-Host "Email verified: $($status.email_verified)" -ForegroundColor Green
    } catch {
        Write-Host "Status check failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Credentials file not found" -ForegroundColor Red
}