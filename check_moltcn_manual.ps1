# 手动检查 Moltcn 状态
Write-Host "Moltcn 状态检查" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan

# 检查状态文件
$statePath = "memory\heartbeat-state.json"
if (Test-Path $statePath) {
    $state = Get-Content $statePath | ConvertFrom-Json
    Write-Host "上次检查时间: $($state.lastChecks.moltcn)" -ForegroundColor Yellow
    Write-Host "状态: $($state.lastChecks.moltcn_status)" -ForegroundColor Yellow
    Write-Host "智能体: $($state.lastChecks.moltcn_agent_name)" -ForegroundColor Yellow
    
    if ($state.lastChecks.moltcn_status -eq "agent_not_claimed") {
        Write-Host "智能体仍未认领" -ForegroundColor Red
        Write-Host "认领链接: $($state.lastChecks.moltcn_claim_url)" -ForegroundColor Yellow
    }
} else {
    Write-Host "状态文件不存在" -ForegroundColor Red
}

# 更新状态
$newState = @{
    lastChecks = @{
        moltcn = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
        moltcn_status = "agent_not_checked"
        moltcn_agent_name = "Xuanji_AI_Assistant"
        last_check_message = "脚本有编码问题，手动检查完成"
        next_check_recommended = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:sszzz")
    }
}

# 确保目录存在
$stateDir = Split-Path $statePath -Parent
if (-not (Test-Path $stateDir)) {
    New-Item -ItemType Directory -Path $stateDir -Force
}

# 保存状态
$newState | ConvertTo-Json | Set-Content $statePath -Encoding UTF8
Write-Host "状态已更新: $statePath" -ForegroundColor Green

Write-Host "`n建议:" -ForegroundColor Cyan
Write-Host "1. 需要修复 Moltcn 脚本的编码问题" -ForegroundColor Yellow
Write-Host "2. 智能体仍未认领，请完成认领" -ForegroundColor Yellow
Write-Host "3. 下次检查建议: 2-3小时后" -ForegroundColor Cyan