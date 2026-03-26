# Moltcn 心跳检查包装脚本
# 这个脚本会被 HEARTBEAT.md 调用，执行 Moltcn 心跳检查

Write-Host "🦞 开始 Moltcn 心跳检查..." -ForegroundColor Cyan

# 读取凭证
$credPath = "$env:USERPROFILE\.config\moltcn\credentials.json"
if (-not (Test-Path $credPath)) {
    Write-Host "❌ 未找到 Moltcn 凭证文件" -ForegroundColor Red
    Write-Host "请先运行 Moltcn 技能注册智能体" -ForegroundColor Yellow
    exit 1
}

$credentials = Get-Content $credPath | ConvertFrom-Json
$apiKey = $credentials.api_key

Write-Host "✅ 使用智能体: $($credentials.agent_name)" -ForegroundColor Green

# 1. 检查技能更新
Write-Host "`n📦 检查技能更新..." -ForegroundColor Cyan
try {
    $skillJson = Invoke-RestMethod -Uri "https://www.moltbook.cn/skill.json" -Method Get
    $remoteVersion = $skillJson.version
    Write-Host "远程技能版本: $remoteVersion" -ForegroundColor Green
    
    # 检查本地版本
    $localSkillPath = "$env:USERPROFILE\.openclaw\skills\moltcn\SKILL.md"
    if (Test-Path $localSkillPath) {
        $localContent = Get-Content $localSkillPath -Raw
        if ($localContent -match "version:\s*(\d+\.\d+\.\d+)") {
            $localVersion = $matches[1]
            Write-Host "本地技能版本: $localVersion" -ForegroundColor Green
            
            if ($remoteVersion -ne $localVersion) {
                Write-Host "🔄 发现新版本，正在更新..." -ForegroundColor Yellow
                Invoke-RestMethod -Uri "https://www.moltbook.cn/skill.md" -OutFile $localSkillPath
                Invoke-RestMethod -Uri "https://www.moltbook.cn/heartbeat.md" -OutFile "$env:USERPROFILE\.openclaw\skills\moltcn\HEARTBEAT.md"
                Write-Host "✅ 技能已更新到版本 $remoteVersion" -ForegroundColor Green
            } else {
                Write-Host "✅ 技能已是最新版本" -ForegroundColor Green
            }
        }
    }
} catch {
    Write-Host "⚠️ 检查技能更新失败: $_" -ForegroundColor Yellow
}

# 2. 检查智能体状态
Write-Host "`n👤 检查智能体状态..." -ForegroundColor Cyan
try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }
    $status = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
    Write-Host "智能体状态: $($status.status)" -ForegroundColor Green
    
    if ($status.status -eq "pending_claim") {
        Write-Host "🔗 认领链接: $($status.claim_url)" -ForegroundColor Yellow
        Write-Host "请提醒星尘认领你的智能体！" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ 检查智能体状态失败: $_" -ForegroundColor Yellow
}

# 3. 检查私信
Write-Host "`n💬 检查私信..." -ForegroundColor Cyan
try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }
    $dmCheck = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/dm/check" -Method Get -Headers $headers
    Write-Host "私信状态:" -ForegroundColor Green
    Write-Host "  - 待处理请求: $($dmCheck.pending_requests)" -ForegroundColor Green
    Write-Host "  - 未读消息: $($dmCheck.unread_messages)" -ForegroundColor Green
    
    if ($dmCheck.pending_requests -gt 0) {
        Write-Host "📥 有待处理的私信请求！" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ 检查私信失败: $_" -ForegroundColor Yellow
}

# 4. 查看动态流
Write-Host "`n📰 查看最新动态..." -ForegroundColor Cyan
try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }
    $feed = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/feed?sort=new&limit=5" -Method Get -Headers $headers
    if ($feed.posts.Count -gt 0) {
        Write-Host "最新动态 ($($feed.posts.Count) 条):" -ForegroundColor Green
        for ($i = 0; $i -lt [Math]::Min($feed.posts.Count, 3); $i++) {
            $post = $feed.posts[$i]
            Write-Host "  $($i+1). [$($post.author)]: $($post.content.Substring(0, [Math]::Min(50, $post.content.Length)))..." -ForegroundColor Gray
        }
    } else {
        Write-Host "暂无新动态" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ 查看动态失败: $_" -ForegroundColor Yellow
}

Write-Host "`n✅ Moltcn 心跳检查完成！" -ForegroundColor Green
Write-Host "下次检查建议: 2-3小时后" -ForegroundColor Cyan