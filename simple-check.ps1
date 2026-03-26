# 简单的心跳检查
$API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"

Write-Host "Moltcn 心跳检查开始..."
Write-Host ""

# 设置请求头
$headers = @{}
$headers.Add("Authorization", "Bearer $API_KEY")
$headers.Add("Content-Type", "application/json")

# 1. 检查智能体状态
Write-Host "检查智能体状态..."
try {
    $agentInfo = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agent/info" -Method Get -Headers $headers
    Write-Host "智能体状态正常"
    Write-Host "名称: $($agentInfo.name)"
    Write-Host "状态: $($agentInfo.status)"
    Write-Host "邮箱: $($agentInfo.email)"
    Write-Host "邮箱验证: $($agentInfo.email_verified)"
} catch {
    Write-Host "检查智能体状态失败: $_"
}

Write-Host ""

# 2. 更新状态文件
Write-Host "更新状态文件..."
$statePath = "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json"
$now = Get-Date -Format "yyyy-MM-ddTHH:mm:ss+08:00"

# 读取现有状态
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

# 更新检查时间
$state.lastChecks.moltcn = $now
$state.moltcn.lastCheck = $now
$state.moltcn.nextCheck = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss+08:00")

# 保存状态
$state | ConvertTo-Json -Depth 10 | Set-Content $statePath -Encoding UTF8
Write-Host "状态文件已更新"

Write-Host ""
Write-Host "Moltcn 心跳检查完成!"
Write-Host "下次检查建议: 2-3小时后"