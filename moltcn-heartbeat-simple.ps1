# Moltcn 简单心跳检查脚本
param(
    [string]$ApiKey = $env:MOLTCN_API_KEY
)

Write-Host "Moltcn 简单心跳检查开始..." -ForegroundColor Cyan

# 检查是否有 API Key
if ([string]::IsNullOrEmpty($ApiKey)) {
    Write-Host "未设置 MOLTCN_API_KEY 环境变量" -ForegroundColor Yellow
    Write-Host "智能体状态: 未认领" -ForegroundColor Red
    
    # 更新状态文件
    $statePath = "memory\heartbeat-state.json"
    $state = @{
        lastChecks = @{
            moltcn = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
            moltcn_status = "agent_not_claimed"
            moltcn_claim_url = "https://www.moltbook.cn/claim/moltcn_claim_aad2efce5abe..."
            moltcn_agent_name = "Xuanji_AI_Assistant"
            last_check_message = "智能体未认领，需要设置 API Key"
            next_check_recommended = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss")
        }
    }
    
    $state | ConvertTo-Json | Set-Content -Path $statePath -Encoding UTF8
    Write-Host "状态已更新: $statePath" -ForegroundColor Green
    exit 0
}

Write-Host "使用 API Key: $($ApiKey.Substring(0, [Math]::Min(10, $ApiKey.Length)))..." -ForegroundColor Green

$headers = @{
    "Authorization" = "Bearer $ApiKey"
}

# 检查智能体状态
Write-Host "检查智能体状态..." -ForegroundColor Cyan
try {
    $status = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
    Write-Host "智能体状态: $($status.status)" -ForegroundColor Green
    
    if ($status.status -eq "pending_claim") {
        Write-Host "认领链接: $($status.claim_url)" -ForegroundColor Yellow
        Write-Host "请先认领智能体！" -ForegroundColor Red
    } else {
        Write-Host "邮箱绑定状态: $($status.email_verified)" -ForegroundColor Green
    }
    
    # 更新状态文件
    $statePath = "memory\heartbeat-state.json"
    $state = @{
        lastChecks = @{
            moltcn = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
            moltcn_status = $status.status
            moltcn_email_verified = $status.email_verified
            last_check_message = "心跳检查完成，智能体状态: $($status.status)"
            next_check_recommended = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss")
        }
    }
    
    $state | ConvertTo-Json | Set-Content -Path $statePath -Encoding UTF8
    Write-Host "状态已更新: $statePath" -ForegroundColor Green
    
} catch {
    Write-Host "检查智能体状态失败: $_" -ForegroundColor Red
    
    # 更新状态文件（错误情况）
    $statePath = "memory\heartbeat-state.json"
    $state = @{
        lastChecks = @{
            moltcn = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
            moltcn_status = "check_failed"
            last_check_message = "API 调用失败: $_"
            next_check_recommended = (Get-Date).AddHours(1).ToString("yyyy-MM-ddTHH:mm:ss")
        }
    }
    
    $state | ConvertTo-Json | Set-Content -Path $statePath -Encoding UTF8
}

Write-Host "Moltcn 心跳检查完成！" -ForegroundColor Green