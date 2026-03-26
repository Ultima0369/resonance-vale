#!/usr/bin/env pwsh
# Moltcn环境变量配置脚本

Write-Host "🔧 配置Moltcn环境变量" -ForegroundColor Cyan
Write-Host "=" * 50

# 检查当前环境变量
Write-Host "当前环境变量状态:" -ForegroundColor Yellow
$currentApiKey = $env:MOLTCN_API_KEY
$currentAgentId = $env:MOLTCN_AGENT_ID

if ($currentApiKey) {
    Write-Host "✅ MOLTCN_API_KEY: 已设置 (长度: $($currentApiKey.Length) 字符)" -ForegroundColor Green
} else {
    Write-Host "❌ MOLTCN_API_KEY: 未设置" -ForegroundColor Red
}

if ($currentAgentId) {
    Write-Host "✅ MOLTCN_AGENT_ID: 已设置 ($currentAgentId)" -ForegroundColor Green
} else {
    Write-Host "❌ MOLTCN_AGENT_ID: 未设置" -ForegroundColor Red
}

Write-Host ""
Write-Host "📝 请按照以下步骤配置:" -ForegroundColor Cyan
Write-Host "1. 获取你的Moltcn API Key"
Write-Host "2. 获取你的智能体ID"
Write-Host "3. 选择配置方式（临时/永久）"
Write-Host ""

# 获取用户输入
$apiKey = Read-Host "请输入Moltcn API Key"
$agentId = Read-Host "请输入智能体ID"

if (-not $apiKey -or -not $agentId) {
    Write-Host "❌ API Key和智能体ID都不能为空" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "请选择配置方式:" -ForegroundColor Yellow
Write-Host "1. 临时配置（仅当前会话有效）"
Write-Host "2. 永久配置（用户级别）"
Write-Host "3. 永久配置（系统级别）"
Write-Host ""

$choice = Read-Host "请输入选择 (1-3)"

switch ($choice) {
    "1" {
        # 临时配置
        $env:MOLTCN_API_KEY = $apiKey
        $env:MOLTCN_AGENT_ID = $agentId
        
        Write-Host "✅ 临时环境变量已设置" -ForegroundColor Green
        Write-Host "   MOLTCN_API_KEY: $($apiKey.Substring(0, 8))..." -ForegroundColor Gray
        Write-Host "   MOLTCN_AGENT_ID: $agentId" -ForegroundColor Gray
        
        # 测试配置
        Test-MoltcnConfig
    }
    "2" {
        # 用户级别永久配置
        [System.Environment]::SetEnvironmentVariable("MOLTCN_API_KEY", $apiKey, "User")
        [System.Environment]::SetEnvironmentVariable("MOLTCN_AGENT_ID", $agentId, "User")
        
        Write-Host "✅ 用户级别环境变量已设置" -ForegroundColor Green
        Write-Host "   需要重启终端或运行 'refreshenv' 生效" -ForegroundColor Yellow
        
        # 同时设置临时变量以便立即使用
        $env:MOLTCN_API_KEY = $apiKey
        $env:MOLTCN_AGENT_ID = $agentId
        
        Test-MoltcnConfig
    }
    "3" {
        # 系统级别永久配置（需要管理员权限）
        Write-Host "⚠️  系统级别配置需要管理员权限" -ForegroundColor Yellow
        
        $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if ($isAdmin) {
            [System.Environment]::SetEnvironmentVariable("MOLTCN_API_KEY", $apiKey, "Machine")
            [System.Environment]::SetEnvironmentVariable("MOLTCN_AGENT_ID", $agentId, "Machine")
            
            Write-Host "✅ 系统级别环境变量已设置" -ForegroundColor Green
            Write-Host "   需要重启计算机或运行 'refreshenv' 生效" -ForegroundColor Yellow
            
            # 同时设置临时变量
            $env:MOLTCN_API_KEY = $apiKey
            $env:MOLTCN_AGENT_ID = $agentId
            
            Test-MoltcnConfig
        } else {
            Write-Host "❌ 需要以管理员身份运行此脚本" -ForegroundColor Red
            Write-Host "   请右键点击PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
        }
    }
    default {
        Write-Host "❌ 无效的选择" -ForegroundColor Red
    }
}

function Test-MoltcnConfig {
    Write-Host ""
    Write-Host "🧪 测试配置..." -ForegroundColor Cyan
    
    # 测试API Key格式
    if ($env:MOLTCN_API_KEY.Length -lt 20) {
        Write-Host "⚠️  API Key可能过短，请检查" -ForegroundColor Yellow
    } else {
        Write-Host "✅ API Key格式看起来正常" -ForegroundColor Green
    }
    
    # 测试智能体ID格式
    if ($env:MOLTCN_AGENT_ID -match '^[a-zA-Z0-9_-]+$') {
        Write-Host "✅ 智能体ID格式正常" -ForegroundColor Green
    } else {
        Write-Host "⚠️  智能体ID格式可能有问题" -ForegroundColor Yellow
    }
    
    # 创建配置文件
    $configDir = "$env:USERPROFILE\.moltcn"
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    
    $configFile = "$configDir\config.json"
    $config = @{
        api_key = $env:MOLTCN_API_KEY
        agent_id = $env:MOLTCN_AGENT_ID
        configured_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        configured_by = $env:USERNAME
    } | ConvertTo-Json
    
    $config | Out-File -FilePath $configFile -Encoding UTF8
    
    Write-Host "✅ 配置文件已保存: $configFile" -ForegroundColor Green
    
    # 显示下一步指引
    Write-Host ""
    Write-Host "🎉 配置完成！" -ForegroundColor Green
    Write-Host "下一步:" -ForegroundColor Cyan
    Write-Host "1. 运行测试脚本: .\test-moltcn-connection.ps1" -ForegroundColor Yellow
    Write-Host "2. 设置心跳任务: .\setup-heartbeat-cron.ps1" -ForegroundColor Yellow
    Write-Host "3. 查看文档: https://www.moltbook.cn/heartbeat-settings.md" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 配置摘要:" -ForegroundColor Cyan
Write-Host "配置时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "配置用户: $env:USERNAME"
Write-Host "工作目录: $(Get-Location)"
Write-Host "=" * 50