$apiKey = "moltcn_451b6e21e70ac556015b7d051bbbcb13"
$headers = @{
    "Authorization" = "Bearer $apiKey"
}

Write-Host "检查智能体状态..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
    Write-Host "智能体状态: $($response.status)" -ForegroundColor Green
    
    if ($response.status -eq "pending_claim") {
        Write-Host "🔗 认领链接: $($response.claim_url)" -ForegroundColor Yellow
        Write-Host "请先认领智能体！" -ForegroundColor Red
    } else {
        Write-Host "✅ 智能体已认领" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ 检查智能体状态失败: $_" -ForegroundColor Yellow
}