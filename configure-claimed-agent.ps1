# 配置已认领智能体的脚本
param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey,
    
    [string]$AgentName = "已认领智能体"
)

Write-Host "🦞 开始配置已认领的 Moltcn 智能体..." -ForegroundColor Cyan

# 保存凭证到配置文件
$configDir = "$env:USERPROFILE\.config\moltcn"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

$credentials = @{
    api_key = $ApiKey
    agent_name = $AgentName
    claimed = $true
    configured_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
} | ConvertTo-Json

$credentials | Out-File -FilePath "$configDir\credentials.json" -Encoding UTF8
Write-Host "✅ 凭证已保存到: $configDir\credentials.json" -ForegroundColor Green

# 测试 API 连接
Write-Host "`n🔗 测试 API 连接..." -ForegroundColor Cyan
$headers = @{
    "Authorization" = "Bearer $ApiKey"
}

try {
    $status = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
    Write-Host "✅ API 连接成功！" -ForegroundColor Green
    Write-Host "智能体状态: $($status.status)" -ForegroundColor Green
    Write-Host "邮箱绑定: $($status.email_verified)" -ForegroundColor Green
    
    # 更新凭证文件
    $fullCredentials = @{
        api_key = $ApiKey
        agent_name = $AgentName
        claimed = $true
        status = $status.status
        email_verified = $status.email_verified
        configured_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
    } | ConvertTo-Json
    
    $fullCredentials | Out-File -FilePath "$configDir\credentials.json" -Encoding UTF8
    
} catch {
    Write-Host "❌ API 连接失败: $_" -ForegroundColor Red
    Write-Host "请检查 API Key 是否正确" -ForegroundColor Yellow
    exit 1
}

# 设置环境变量
Write-Host "`n⚙️ 设置环境变量..." -ForegroundColor Cyan
[Environment]::SetEnvironmentVariable("MOLTCN_API_KEY", $ApiKey, "User")
[Environment]::SetEnvironmentVariable("MOLTCN_AGENT_NAME", $AgentName, "User")
Write-Host "✅ 环境变量已设置" -ForegroundColor Green
Write-Host "MOLTCN_API_KEY: $($ApiKey.Substring(0, 10))..." -ForegroundColor Gray
Write-Host "MOLTCN_AGENT_NAME: $AgentName" -ForegroundColor Gray

# 测试心跳检查
Write-Host "`n❤️ 测试心跳检查..." -ForegroundColor Cyan
try {
    & "$PSScriptRoot\moltcn-heartbeat-full.ps1" -ApiKey $ApiKey
} catch {
    Write-Host "⚠️ 心跳检查测试失败: $_" -ForegroundColor Yellow
}

Write-Host "`n🎉 智能体配置完成！" -ForegroundColor Green
Write-Host "下一步建议：" -ForegroundColor Cyan
Write-Host "1. 如果邮箱未绑定，运行邮箱绑定脚本" -ForegroundColor Gray
Write-Host "2. 测试在 Moltcn 上发帖" -ForegroundColor Gray
Write-Host "3. 设置定时心跳任务" -ForegroundColor Gray