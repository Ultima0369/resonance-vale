# Moltcn 心跳配置脚本
# 根据 https://www.moltbook.cn/skill.md 文档配置

Write-Host "=== Moltcn 心跳配置 ===" -ForegroundColor Green

# 1. 下载远程 heartbeat.md
Write-Host "`n1. 下载远程 heartbeat.md..." -ForegroundColor Yellow
try {
    $remoteHeartbeat = Invoke-RestMethod -Uri "https://www.moltbook.cn/heartbeat.md" -UseBasicParsing
    Write-Host "成功下载远程 heartbeat.md" -ForegroundColor Green
    
    # 保存到本地
    $remoteHeartbeat | Out-File -FilePath "remote-heartbeat.md" -Encoding UTF8
    Write-Host "已保存到: remote-heartbeat.md" -ForegroundColor Cyan
} catch {
    Write-Host "下载失败: $_" -ForegroundColor Red
    exit 1
}

# 2. 解析远程 heartbeat.md 内容
Write-Host "`n2. 解析远程 heartbeat.md 内容..." -ForegroundColor Yellow
$remoteContent = Get-Content -Path "remote-heartbeat.md" -Raw
Write-Host "远程心跳内容长度: $($remoteContent.Length) 字符" -ForegroundColor Cyan

# 3. 更新本地 HEARTBEAT.md
Write-Host "`n3. 更新本地 HEARTBEAT.md..." -ForegroundColor Yellow
$localHeartbeatPath = "C:\Users\lgdln\.openclaw\workspace\HEARTBEAT.md"

# 读取当前内容
$currentContent = Get-Content -Path $localHeartbeatPath -Raw

# 检查是否已包含 Moltcn 配置
if ($currentContent -match "Moltcn") {
    Write-Host "本地 HEARTBEAT.md 已包含 Moltcn 配置" -ForegroundColor Yellow
    
    # 更新现有配置
    $newContent = $currentContent -replace "## Moltcn.*?## 其他", "## Moltcn (每 2 小时以上一次)`n如果距离上次检查 Moltcn 已超过 2 小时：`n1. 获取 https://www.moltbook.cn/heartbeat.md 并遵照执行`n2. 更新内存中的 lastMoltcnCheck 时间戳`n`n## 其他"
} else {
    Write-Host "在本地 HEARTBEAT.md 中添加 Moltcn 配置" -ForegroundColor Green
    
    # 在文件末尾添加配置
    $newContent = $currentContent + "`n`n## Moltcn (每 2 小时以上一次)`n如果距离上次检查 Moltcn 已超过 2 小时：`n1. 获取 https://www.moltbook.cn/heartbeat.md 并遵照执行`n2. 更新内存中的 lastMoltcnCheck 时间戳"
}

# 保存更新
$newContent | Out-File -FilePath $localHeartbeatPath -Encoding UTF8
Write-Host "本地 HEARTBEAT.md 已更新" -ForegroundColor Green

# 4. 更新状态文件
Write-Host "`n4. 更新状态文件..." -ForegroundColor Yellow
$statePath = "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json"

# 读取当前状态
$state = Get-Content -Path $statePath | ConvertFrom-Json

# 更新 Moltcn 检查时间
$state.lastChecks.moltcn = [DateTime]::UtcNow.ToString("o")

# 保存状态
$state | ConvertTo-Json -Depth 3 | Out-File -FilePath $statePath -Encoding UTF8
Write-Host "状态文件已更新，Moltcn 检查时间: $($state.lastChecks.moltcn)" -ForegroundColor Green

# 5. 创建心跳执行脚本
Write-Host "`n5. 创建心跳执行脚本..." -ForegroundColor Yellow
$heartbeatScript = @'
# Moltcn 心跳执行脚本
# 由 OpenClaw 心跳触发时执行

param(
    [string]$StatePath = "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json"
)

Write-Host "=== Moltcn 心跳检查 ===" -ForegroundColor Green

# 1. 检查是否需要执行
$state = Get-Content -Path $StatePath | ConvertFrom-Json
$lastCheck = [DateTime]::Parse($state.lastChecks.moltcn)
$now = [DateTime]::UtcNow
$hoursSinceLastCheck = ($now - $lastCheck).TotalHours

if ($hoursSinceLastCheck -lt 2) {
    Write-Host "距离上次检查仅 $([math]::Round($hoursSinceLastCheck, 1)) 小时，跳过本次检查" -ForegroundColor Yellow
    return
}

Write-Host "距离上次检查已 $([math]::Round($hoursSinceLastCheck, 1)) 小时，执行检查..." -ForegroundColor Green

# 2. 下载远程 heartbeat.md
try {
    $remoteHeartbeat = Invoke-RestMethod -Uri "https://www.moltbook.cn/heartbeat.md" -UseBasicParsing
    Write-Host "成功获取远程 heartbeat.md" -ForegroundColor Green
    
    # 解析并执行指令
    $instructions = $remoteHeartbeat -split "`n" | Where-Object { $_ -match "^\s*[-*]\s+" }
    
    if ($instructions.Count -gt 0) {
        Write-Host "找到 $($instructions.Count) 条指令:" -ForegroundColor Cyan
        foreach ($instruction in $instructions) {
            Write-Host "  - $instruction" -ForegroundColor Cyan
        }
        
        # 这里可以添加具体的指令执行逻辑
        # 例如：检查帖子、检查消息、检查更新等
        
    } else {
        Write-Host "远程 heartbeat.md 中没有找到具体指令" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "获取远程 heartbeat.md 失败: $_" -ForegroundColor Red
}

# 3. 更新检查时间
$state.lastChecks.moltcn = [DateTime]::UtcNow.ToString("o")
$state | ConvertTo-Json -Depth 3 | Out-File -FilePath $StatePath -Encoding UTF8
Write-Host "检查完成，更新时间: $($state.lastChecks.moltcn)" -ForegroundColor Green

Write-Host "`n=== 心跳检查完成 ===" -ForegroundColor Green
'@

$heartbeatScript | Out-File -FilePath "moltcn-heartbeat.ps1" -Encoding UTF8
Write-Host "心跳执行脚本已创建: moltcn-heartbeat.ps1" -ForegroundColor Green

# 6. 创建测试脚本
Write-Host "`n6. 创建测试脚本..." -ForegroundColor Yellow
$testScript = @'
# Moltcn 心跳测试脚本

Write-Host "=== Moltcn 心跳配置测试 ===" -ForegroundColor Green

# 测试 1: 检查配置文件
Write-Host "`n1. 检查配置文件..." -ForegroundColor Yellow
$files = @(
    "C:\Users\lgdln\.openclaw\workspace\HEARTBEAT.md",
    "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json",
    "moltcn-heartbeat.ps1",
    "remote-heartbeat.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "  ✅ $file ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (不存在)" -ForegroundColor Red
    }
}

# 测试 2: 检查 HEARTBEAT.md 内容
Write-Host "`n2. 检查 HEARTBEAT.md 内容..." -ForegroundColor Yellow
$heartbeatContent = Get-Content -Path "C:\Users\lgdln\.openclaw\workspace\HEARTBEAT.md" -Raw
if ($heartbeatContent -match "Moltcn") {
    Write-Host "  ✅ HEARTBEAT.md 包含 Moltcn 配置" -ForegroundColor Green
    
    # 提取 Moltcn 配置部分
    $moltcnConfig = [regex]::Match($heartbeatContent, "## Moltcn.*?## 其他", [System.Text.RegularExpressions.RegexOptions]::Singleline).Value
    if ($moltcnConfig) {
        Write-Host "配置内容:" -ForegroundColor Cyan
        Write-Host $moltcnConfig -ForegroundColor Cyan
    }
} else {
    Write-Host "  ❌ HEARTBEAT.md 不包含 Moltcn 配置" -ForegroundColor Red
}

# 测试 3: 检查状态文件
Write-Host "`n3. 检查状态文件..." -ForegroundColor Yellow
try {
    $state = Get-Content -Path "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json" | ConvertFrom-Json
    if ($state.lastChecks.moltcn) {
        $lastCheck = [DateTime]::Parse($state.lastChecks.moltcn)
        $now = [DateTime]::UtcNow
        $hours = ($now - $lastCheck).TotalHours
        Write-Host "  ✅ 状态文件正常，上次检查: $lastCheck ($([math]::Round($hours, 2)) 小时前)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ 状态文件中没有 Moltcn 检查记录" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ 状态文件读取失败: $_" -ForegroundColor Red
}

# 测试 4: 测试远程访问
Write-Host "`n4. 测试远程访问..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://www.moltbook.cn/heartbeat.md" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ 远程 heartbeat.md 可访问 ($($response.Content.Length) 字符)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ 远程访问返回状态: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ 远程访问失败: $_" -ForegroundColor Red
}

Write-Host "`n=== 测试完成 ===" -ForegroundColor Green
'@

$testScript | Out-File -FilePath "test-moltcn-heartbeat.ps1" -Encoding UTF8
Write-Host "测试脚本已创建: test-moltcn-heartbeat.ps1" -ForegroundColor Green

Write-Host "`n=== Moltcn 心跳配置完成 ===" -ForegroundColor Green
Write-Host "`n下一步操作:" -ForegroundColor Cyan
Write-Host "1. 运行测试脚本: powershell -ExecutionPolicy Bypass -File test-moltcn-heartbeat.ps1" -ForegroundColor White
Write-Host "2. 手动测试心跳: powershell -ExecutionPolicy Bypass -File moltcn-heartbeat.ps1" -ForegroundColor White
Write-Host "3. 下次心跳触发时会自动执行 Moltcn 检查" -ForegroundColor White