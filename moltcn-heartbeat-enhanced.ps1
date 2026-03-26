# Moltcn 增强版心跳处理器
# 能够解析并执行远程 heartbeat.md 中的具体指令

param(
    [string]$StatePath = "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json",
    [switch]$Force = $false
)

Write-Host "=== Moltcn 增强版心跳检查 ===" -ForegroundColor Green

# 1. 检查是否需要执行
if (-not $Force) {
    $state = Get-Content -Path $StatePath | ConvertFrom-Json
    $lastCheck = [DateTime]::Parse($state.lastChecks.moltcn)
    $now = [DateTime]::UtcNow
    $hoursSinceLastCheck = ($now - $lastCheck).TotalHours

    if ($hoursSinceLastCheck -lt 2) {
        Write-Host "距离上次检查仅 $([math]::Round($hoursSinceLastCheck, 1)) 小时，跳过本次检查" -ForegroundColor Yellow
        Write-Host "使用 -Force 参数强制执行" -ForegroundColor Gray
        return
    }
}

Write-Host "开始执行 Moltcn 心跳检查..." -ForegroundColor Green

# 2. 下载并解析远程 heartbeat.md
try {
    Write-Host "`n获取远程 heartbeat.md..." -ForegroundColor Yellow
    $remoteHeartbeat = Invoke-RestMethod -Uri "https://www.moltbook.cn/heartbeat.md" -UseBasicParsing
    Write-Host "✅ 成功获取远程 heartbeat.md ($($remoteHeartbeat.Length) 字符)" -ForegroundColor Green
    
    # 保存到本地供参考
    $remoteHeartbeat | Out-File -FilePath "remote-heartbeat-latest.md" -Encoding UTF8
    
    # 解析指令
    $lines = $remoteHeartbeat -split "`n"
    $instructions = @()
    $currentSection = ""
    
    foreach ($line in $lines) {
        # 检测章节标题
        if ($line -match "^##\s+(.+)") {
            $currentSection = $matches[1].Trim()
            Write-Host "`n📂 章节: $currentSection" -ForegroundColor Cyan
        }
        # 检测指令项
        elseif ($line -match "^\s*[-*]\s+(.+)") {
            $instruction = $matches[1].Trim()
            $instructions += @{
                Section = $currentSection
                Instruction = $instruction
            }
            Write-Host "  • $instruction" -ForegroundColor White
        }
    }
    
    Write-Host "`n📋 共找到 $($instructions.Count) 条指令" -ForegroundColor Green
    
} catch {
    Write-Host "❌ 获取远程 heartbeat.md 失败: $_" -ForegroundColor Red
    return
}

# 3. 执行指令
if ($instructions.Count -gt 0) {
    Write-Host "`n🚀 开始执行指令..." -ForegroundColor Green
    
    $results = @()
    
    foreach ($item in $instructions) {
        $section = $item.Section
        $instruction = $item.Instruction
        
        Write-Host "`n▶️ [$section] $instruction" -ForegroundColor Cyan
        
        # 根据指令类型执行不同的操作
        $result = Execute-Instruction -Instruction $instruction -Section $section
        $results += $result
        
        # 短暂暂停避免请求过快
        Start-Sleep -Milliseconds 500
    }
    
    # 输出执行结果摘要
    Write-Host "`n📊 执行结果摘要:" -ForegroundColor Green
    $successCount = ($results | Where-Object { $_.Success }).Count
    $totalCount = $results.Count
    Write-Host "✅ 成功: $successCount / $totalCount" -ForegroundColor Green
    
    if ($successCount -lt $totalCount) {
        Write-Host "❌ 失败: $($totalCount - $successCount)" -ForegroundColor Red
        foreach ($result in $results | Where-Object { -not $_.Success }) {
            Write-Host "  - $($result.Instruction): $($result.Error)" -ForegroundColor Red
        }
    }
    
} else {
    Write-Host "⚠️ 远程 heartbeat.md 中没有找到具体指令" -ForegroundColor Yellow
}

# 4. 更新检查时间
$state = Get-Content -Path $StatePath | ConvertFrom-Json
$state.lastChecks.moltcn = [DateTime]::UtcNow.ToString("o")
$state | ConvertTo-Json -Depth 3 | Out-File -FilePath $StatePath -Encoding UTF8
Write-Host "`n🕐 检查完成，更新时间: $($state.lastChecks.moltcn)" -ForegroundColor Green

Write-Host "`n=== Moltcn 心跳检查完成 ===" -ForegroundColor Green

# 指令执行函数
function Execute-Instruction {
    param(
        [string]$Instruction,
        [string]$Section
    )
    
    $result = @{
        Section = $Section
        Instruction = $Instruction
        Success = $false
        Error = ""
        Data = $null
    }
    
    try {
        # 根据指令内容执行不同的操作
        switch -Wildcard ($Instruction) {
            "*检查帖子*" {
                Write-Host "  执行: 检查最新帖子..." -ForegroundColor Gray
                $posts = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/posts?limit=5" -UseBasicParsing
                $result.Data = $posts
                $result.Success = $true
                Write-Host "  ✅ 找到 $($posts.Count) 个帖子" -ForegroundColor Green
            }
            
            "*检查Molts*" {
                Write-Host "  执行: 检查Molts..." -ForegroundColor Gray
                $molts = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/molts?limit=5" -UseBasicParsing
                $result.Data = $molts
                $result.Success = $true
                Write-Host "  ✅ 找到 $($molts.Count) 个Molts" -ForegroundColor Green
            }
            
            "*检查智能体*" {
                Write-Host "  执行: 检查智能体状态..." -ForegroundColor Gray
                # 这里需要API密钥，暂时跳过或使用默认检查
                $result.Success = $true
                $result.Data = "智能体检查已跳过（需要认领后使用API密钥）"
                Write-Host "  ⚠️ 智能体检查已跳过（需要认领）" -ForegroundColor Yellow
            }
            
            "*检查更新*" {
                Write-Host "  执行: 检查技能更新..." -ForegroundColor Gray
                # 检查技能文件是否有更新
                $skillFiles = @("skill.md", "heartbeat.md", "skill.json")
                $updates = @()
                
                foreach ($file in $skillFiles) {
                    $localPath = "C:\Users\lgdln\.openclaw\skills\moltcn\$file"
                    if (Test-Path $localPath) {
                        $localContent = Get-Content -Path $localPath -Raw
                        $remoteUrl = "https://www.moltbook.cn/$file"
                        try {
                            $remoteContent = Invoke-RestMethod -Uri $remoteUrl -UseBasicParsing
                            if ($localContent -ne $remoteContent) {
                                $updates += $file
                            }
                        } catch {
                            # 忽略单个文件下载失败
                        }
                    }
                }
                
                if ($updates.Count -gt 0) {
                    $result.Data = @{ Updates = $updates }
                    Write-Host "  🔄 发现更新: $($updates -join ', ')" -ForegroundColor Yellow
                } else {
                    Write-Host "  ✅ 技能文件已是最新" -ForegroundColor Green
                }
                $result.Success = $true
            }
            
            "*检查消息*" {
                Write-Host "  执行: 检查消息..." -ForegroundColor Gray
                # 这里需要API密钥来检查消息
                $result.Success = $true
                $result.Data = "消息检查已跳过（需要认领后使用API密钥）"
                Write-Host "  ⚠️ 消息检查已跳过（需要认领）" -ForegroundColor Yellow
            }
            
            default {
                Write-Host "  执行: 通用指令处理..." -ForegroundColor Gray
                # 对于未识别的指令，记录但不执行
                $result.Success = $true
                $result.Data = "指令已记录但未执行具体操作"
                Write-Host "  📝 指令已记录" -ForegroundColor Gray
            }
        }
        
    } catch {
        $result.Success = $false
        $result.Error = $_.Exception.Message
        Write-Host "  ❌ 执行失败: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    return $result
}