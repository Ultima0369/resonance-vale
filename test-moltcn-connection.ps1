#!/usr/bin/env pwsh
# Moltcn连接测试脚本

Write-Host "🧪 Moltcn连接测试" -ForegroundColor Cyan
Write-Host "=" * 50

# 检查环境变量
Write-Host "1. 检查环境变量..." -ForegroundColor Yellow

$apiKey = $env:MOLTCN_API_KEY
$agentId = $env:MOLTCN_AGENT_ID

if (-not $apiKey) {
    Write-Host "❌ MOLTCN_API_KEY未设置" -ForegroundColor Red
    Write-Host "   运行 .\configure-moltcn-env.ps1 进行配置" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ MOLTCN_API_KEY: 已设置 (长度: $($apiKey.Length) 字符)" -ForegroundColor Green
}

if (-not $agentId) {
    Write-Host "❌ MOLTCN_AGENT_ID未设置" -ForegroundColor Red
    Write-Host "   运行 .\configure-moltcn-env.ps1 进行配置" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ MOLTCN_AGENT_ID: $agentId" -ForegroundColor Green
}

Write-Host ""
Write-Host "2. 测试网络连接..." -ForegroundColor Yellow

# 测试API服务器连接
$apiHost = "api.moltbook.cn"
try {
    $testResult = Test-NetConnection -ComputerName $apiHost -Port 443 -InformationLevel Detailed -ErrorAction Stop
    
    if ($testResult.TcpTestSucceeded) {
        Write-Host "✅ 可以连接到 $apiHost:443" -ForegroundColor Green
        Write-Host "   延迟: $($testResult.PingReplyDetails.RoundtripTime)ms" -ForegroundColor Gray
    } else {
        Write-Host "❌ 无法连接到 $apiHost:443" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 网络连接测试失败: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "3. 测试API认证..." -ForegroundColor Yellow

# 测试智能体状态API
$apiUrl = "https://api.moltbook.cn/v1/agent/status"
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

try {
    Write-Host "   请求: GET $apiUrl" -ForegroundColor Gray
    
    $response = Invoke-RestMethod -Uri $apiUrl `
        -Method GET `
        -Headers $headers `
        -TimeoutSec 10 `
        -ErrorAction Stop
    
    if ($response.success) {
        Write-Host "✅ API认证成功" -ForegroundColor Green
        Write-Host "   智能体状态: $($response.data.status)" -ForegroundColor Gray
        Write-Host "   智能体名称: $($response.data.name)" -ForegroundColor Gray
        Write-Host "   创建时间: $($response.data.created_at)" -ForegroundColor Gray
        
        if ($response.data.status -eq "pending_claim") {
            Write-Host "⚠️  智能体待认领" -ForegroundColor Yellow
            Write-Host "   认领URL: $($response.data.claim_url)" -ForegroundColor Gray
        }
        
        if ($response.data.email_verified -eq $false) {
            Write-Host "⚠️  邮箱未验证" -ForegroundColor Yellow
            Write-Host "   绑定邮箱: $($response.data.email)" -ForegroundColor Gray
        }
        
    } else {
        Write-Host "❌ API返回错误: $($response.error)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ API请求失败: $_" -ForegroundColor Red
    
    # 尝试获取更多错误信息
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $statusDescription = $_.Exception.Response.StatusDescription
        
        Write-Host "   HTTP状态码: $statusCode ($statusDescription)" -ForegroundColor Gray
        
        if ($statusCode -eq 401) {
            Write-Host "   🔐 认证失败: API Key无效或已过期" -ForegroundColor Red
        } elseif ($statusCode -eq 403) {
            Write-Host "   🚫 权限不足: 智能体ID不匹配或权限不足" -ForegroundColor Red
        } elseif ($statusCode -eq 404) {
            Write-Host "   🔍 资源未找到: 智能体不存在" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "4. 测试心跳功能..." -ForegroundColor Yellow

# 测试心跳API
$heartbeatUrl = "https://api.moltbook.cn/v1/heartbeat"
$heartbeatData = @{
    agent_id = $agentId
    message = "连接测试心跳"
    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
} | ConvertTo-Json

try {
    Write-Host "   请求: POST $heartbeatUrl" -ForegroundColor Gray
    
    $response = Invoke-RestMethod -Uri $heartbeatUrl `
        -Method POST `
        -Headers $headers `
        -Body $heartbeatData `
        -TimeoutSec 10 `
        -ErrorAction Stop
    
    if ($response.success) {
        Write-Host "✅ 心跳功能正常" -ForegroundColor Green
        Write-Host "   消息: $($response.data.message)" -ForegroundColor Gray
        Write-Host "   时间: $($response.data.timestamp)" -ForegroundColor Gray
        Write-Host "   下次心跳: $($response.data.next_heartbeat)" -ForegroundColor Gray
    } else {
        Write-Host "❌ 心跳返回错误: $($response.error)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 心跳请求失败: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "5. 检查本地配置..." -ForegroundColor Yellow

# 检查本地配置文件
$configDir = "$env:USERPROFILE\.moltcn"
$configFile = "$configDir\config.json"

if (Test-Path $configFile) {
    Write-Host "✅ 找到本地配置文件: $configFile" -ForegroundColor Green
    
    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json
        Write-Host "   配置时间: $($config.configured_at)" -ForegroundColor Gray
        Write-Host "   配置用户: $($config.configured_by)" -ForegroundColor Gray
    } catch {
        Write-Host "⚠️  配置文件格式错误" -ForegroundColor Yellow
    }
} else {
    Write-Host "ℹ️  未找到本地配置文件" -ForegroundColor Gray
    Write-Host "   运行 .\configure-moltcn-env.ps1 创建配置文件" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "6. 测试OpenClaw集成..." -ForegroundColor Yellow

# 检查OpenClaw环境
$openclawConfig = "$env:USERPROFILE\.openclaw\config.json"
if (Test-Path $openclawConfig) {
    Write-Host "✅ OpenClaw配置文件存在" -ForegroundColor Green
    
    try {
        $config = Get-Content $openclawConfig -Raw | ConvertFrom-Json
        Write-Host "   OpenClaw版本: $($config.version)" -ForegroundColor Gray
        Write-Host "   工作目录: $($config.workspace)" -ForegroundColor Gray
    } catch {
        Write-Host "⚠️  OpenClaw配置文件格式错误" -ForegroundColor Yellow
    }
} else {
    Write-Host "ℹ️  未找到OpenClaw配置文件" -ForegroundColor Gray
}

# 检查心跳脚本
$heartbeatScript = ".\moltcn-heartbeat.ps1"
if (Test-Path $heartbeatScript) {
    Write-Host "✅ 心跳脚本存在: $heartbeatScript" -ForegroundColor Green
    
    # 测试运行心跳脚本
    Write-Host "   测试运行心跳脚本..." -ForegroundColor Gray
    try {
        & $heartbeatScript -Test -Verbose
        Write-Host "✅ 心跳脚本测试通过" -ForegroundColor Green
    } catch {
        Write-Host "❌ 心跳脚本测试失败: $_" -ForegroundColor Red
    }
} else {
    Write-Host "❌ 心跳脚本不存在" -ForegroundColor Red
    Write-Host "   请确保 moltcn-heartbeat.ps1 在相同目录" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 测试总结" -ForegroundColor Cyan
Write-Host "=" * 50

# 汇总测试结果
$tests = @(
    @{ Name = "环境变量"; Pass = [bool]$apiKey -and [bool]$agentId },
    @{ Name = "网络连接"; Pass = $testResult.TcpTestSucceeded },
    @{ Name = "API认证"; Pass = $response.success -eq $true },
    @{ Name = "心跳功能"; Pass = $heartbeatResponse.success -eq $true },
    @{ Name = "本地配置"; Pass = Test-Path $configFile },
    @{ Name = "心跳脚本"; Pass = Test-Path $heartbeatScript }
)

$passedTests = $tests | Where-Object { $_.Pass } | Measure-Object | Select-Object -ExpandProperty Count
$totalTests = $tests.Count

Write-Host "通过测试: $passedTests/$totalTests" -ForegroundColor $(if ($passedTests -eq $totalTests) { "Green" } else { "Yellow" })

foreach ($test in $tests) {
    $status = if ($test.Pass) { "✅" } else { "❌" }
    Write-Host "   $status $($test.Name)" -ForegroundColor $(if ($test.Pass) { "Green" } else { "Red" })
}

Write-Host ""
if ($passedTests -eq $totalTests) {
    Write-Host "🎉 所有测试通过！Moltcn连接配置完成。" -ForegroundColor Green
    Write-Host "下一步:" -ForegroundColor Cyan
    Write-Host "1. 设置计划任务: .\setup-heartbeat-cron.ps1" -ForegroundColor Yellow
    Write-Host "2. 手动测试: .\moltcn-heartbeat.ps1 -Verbose" -ForegroundColor Yellow
    Write-Host "3. 查看文档: https://www.moltbook.cn/heartbeat-settings.md" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  部分测试失败，需要修复配置" -ForegroundColor Yellow
    Write-Host "建议步骤:" -ForegroundColor Cyan
    Write-Host "1. 运行配置脚本: .\configure-moltcn-env.ps1" -ForegroundColor Yellow
    Write-Host "2. 检查网络连接" -ForegroundColor Yellow
    Write-Host "3. 验证API Key和智能体ID" -ForegroundColor Yellow
    Write-Host "4. 重新运行测试: .\test-moltcn-connection.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "测试完成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "=" * 50